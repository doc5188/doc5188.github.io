---
layout: post
title: "virtio驱动如何同设备交互"
date: 2014-09-02 13:20:38
categories: 虚拟化
tags: [qemu, kvm, virtio, 虚拟化]
---

virtio设备是作为pci设备被使用的，因此具有pci设备的所有属性：

virtio header占用pci设备的24字节的配置空间：32 * (0 - 5)

virtio header后面跟随一个device specific的config结构

virtio header包括：
<pre>
/* A 32-bit r/o bitmask of the features supported by the host */
#define VIRTIO_PCI_HOST_FEATURES 0

/* A 32-bit r/w bitmask of features activated by the guest */
#define VIRTIO_PCI_GUEST_FEATURES 4

/* A 32-bit r/w PFN for the currently selected queue */
#define VIRTIO_PCI_QUEUE_PFN  8

/* A 16-bit r/o queue size for the currently selected queue */
#define VIRTIO_PCI_QUEUE_NUM  12

/* A 16-bit r/w queue selector */
#define VIRTIO_PCI_QUEUE_SEL  14

/* A 16-bit r/w queue notifier */
#define VIRTIO_PCI_QUEUE_NOTIFY  16

/* An 8-bit device status register.  */
#define VIRTIO_PCI_STATUS  18

/* An 8-bit r/o interrupt status register.  Reading the value will

return the
 * current contents of the ISR and will also clear it.  This is

effectively
 * a read-and-acknowledge. */
#define VIRTIO_PCI_ISR   19

/* The bit of the ISR which indicates a device configuration change. */
#define VIRTIO_PCI_ISR_CONFIG  0x2

/* MSI-X registers: only enabled if MSI-X is enabled. */
/* A 16-bit vector for configuration changes. */
#define VIRTIO_MSI_CONFIG_VECTOR        20
/* A 16-bit vector for selected queue notifications. */
#define VIRTIO_MSI_QUEUE_VECTOR         22
/* Vector value used to disable MSI for queue */
#define VIRTIO_MSI_NO_VECTOR            0xffff
</pre>

每个特定设备还有自己的配置结构体，以上是通用部分

guest读写方式：
{% highlight c %}
/* Select the queue we're interested in */
iowrite16(index, vp_dev->ioaddr + VIRTIO_PCI_QUEUE_SEL);

/* Check if queue is either not available or already active. */
num = ioread16(vp_dev->ioaddr + VIRTIO_PCI_QUEUE_NUM);
{% endhighlight %}


virtio驱动通过读取和写入这些配置空间实现通用的guest特性，队列，中断等等

方面同qemu-kvm交互的功能

qemu-kvm提供了下面这个函数结构体来响应guest的不同读写请求。

{% highlight c %}
static const MemoryRegionPortio virtio_portio[] = {
    { 0, 0x10000, 1, .write = virtio_pci_config_writeb, },
    { 0, 0x10000, 2, .write = virtio_pci_config_writew, },
    { 0, 0x10000, 4, .write = virtio_pci_config_writel, },
    { 0, 0x10000, 1, .read = virtio_pci_config_readb, },
    { 0, 0x10000, 2, .read = virtio_pci_config_readw, },
    { 0, 0x10000, 4, .read = virtio_pci_config_readl, },
    PORTIO_END_OF_LIST()
};

static const MemoryRegionOps virtio_pci_config_ops = {
    .old_portio = virtio_portio,
    .endianness = DEVICE_LITTLE_ENDIAN,
};
{% endhighlight %}

virtio设备作为pci设备被guest识别，guest通过读写pci设备配置空间的信息来

同qemu-kvm交互。

所以实际上是guest为queue分配vring表的空间，然后通过上面这种交互方式将地

址传递给qemu-kvm，qemu-kvm把地址复制给guest选定的queue，这样guest和

qemu-kvm就共用这一片vring表的空间。

guest通过queue发送消息，实际上就是向这一片共享的vring表空间写入信息并标

识为等待qemu-kvm读取，qemu-kvm读取并处理后又将结果写进去（guest写的信息

里面预留空间给qemu-kvm来写了）再标识为已处理，同时发一个中断，guest接到

中断就去读取处理结果。

{% highlight c %}
/*
函数功能：为目标设备获取一个queue
vdev：目标设备
index：给目标设备使用的queue的编号
callback：queue的回调函数
name：queue的名字
msix_vec：给queue使用的msix vector的编号
*/
static struct virtqueue *setup_vq(struct virtio_device *vdev, 
 unsigned index, void (*callback)(struct virtqueue *vq),
     const char *name, u16 msix_vec)
{
 struct virtio_pci_device *vp_dev = to_vp_device(vdev);
 struct virtio_pci_vq_info *info;
 struct virtqueue *vq;
 unsigned long flags, size;
 u16 num;
 int err;

 /* 通知guest我们想要使用的queue的号码 */
/* Select the queue we're interested in */
 iowrite16(index, vp_dev->ioaddr + VIRTIO_PCI_QUEUE_SEL);

 /* 返回刚刚选中的queue的可用列表数，从而判断该queue是否可用 */
/* Check if queue is either not available or already active. */
 num = ioread16(vp_dev->ioaddr + VIRTIO_PCI_QUEUE_NUM);
        /* 如果num为0，则该queue不可用，因为没空闲列表了。
    返回刚刚选中的queue的地址，如果该queue的地址非空，则它已经
    在被使用了，该queue不可用。
  */
 if (!num || ioread32(vp_dev->ioaddr + VIRTIO_PCI_QUEUE_PFN))
  return ERR_PTR(-ENOENT);

 /* allocate and fill out our structure the represents an active
  * queue */
 info = kmalloc(sizeof(struct virtio_pci_vq_info), GFP_KERNEL);
 if (!info)
  return ERR_PTR(-ENOMEM);

 info->num = num;
 info->msix_vector = msix_vec;

 size = PAGE_ALIGN(vring_size(num, VIRTIO_PCI_VRING_ALIGN));
 /* 为vring表分配空间 */
 info->queue = alloc_pages_exact(size, GFP_KERNEL|__GFP_ZERO);
 if (info->queue == NULL) {
  err = -ENOMEM;
  goto out_info;
 }

 /* activate the queue */
 /* 将vring表的地址传递给qemu-kvm，guest将和qemu-kvm通过共享
    这一共同的vring表来完成信息交互：
    1.guest通过queue发信息就是向vring表写入信息并标识为等待
      qemu-kvm端virtio驱动读取，同时通过notify设备通知qemu-kvm
      端virtio驱动。
    2.qemu-kvm端virtio驱动处理后将结果也写入vring表（guest发的
      信息预留了返回结果的空间）并标识为已处理，同时发送中断通  

             知guest。
    3.guest中断处理函数判明中断类型，读取返回结果。
  */
 iowrite32(virt_to_phys(info->queue) >>

VIRTIO_PCI_QUEUE_ADDR_SHIFT, vp_dev->ioaddr + VIRTIO_PCI_QUEUE_PFN);

 /* create the vring */
 /* 创建vring_virtqueue结构体，作为queue和vring协同工作的桥梁，
    queue和vring都嵌入在vring_virtqueue结构体之中，返回给驱动的

queue实际就是vring_virtqueue的成员，queue是vring_virtqueue结构体提供给

上层驱动的接口，vring结构体则负责管理vring表，是操作vring表的接口。
 */
 vq = vring_new_virtqueue(index, info->num, 

VIRTIO_PCI_VRING_ALIGN, vdev,true, info->queue, vp_notify, callback,

name);
 if (!vq) {
  err = -ENOMEM;
  goto out_activate_queue;
 }

 vq->priv = info;
 info->vq = vq;
 /* 如果使用msix vector，则将msix vector编号写入到设备的配置空间 

   去，再读取的目的就是判断qemu-kvm端是否能够支持。
  */
 if (msix_vec != VIRTIO_MSI_NO_VECTOR) {
  iowrite16(msix_vec, vp_dev->ioaddr +

VIRTIO_MSI_QUEUE_VECTOR);
  msix_vec = ioread16(vp_dev->ioaddr +

VIRTIO_MSI_QUEUE_VECTOR);
  if (msix_vec == VIRTIO_MSI_NO_VECTOR) {
   err = -EBUSY;
   goto out_assign;
  }
 }

 if (callback) {
  spin_lock_irqsave(&vp_dev->lock, flags);
  list_add(&info->node, &vp_dev->virtqueues);
  spin_unlock_irqrestore(&vp_dev->lock, flags);
 } else {
  INIT_LIST_HEAD(&info->node);
 }

 return vq;

out_assign:
 vring_del_virtqueue(vq);
out_activate_queue:
 iowrite32(0, vp_dev->ioaddr + VIRTIO_PCI_QUEUE_PFN);
 free_pages_exact(info->queue, size);
out_info:
 kfree(info);
 return ERR_PTR(err);
}
 
{% endhighlight %}
