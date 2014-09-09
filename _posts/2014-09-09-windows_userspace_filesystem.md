---
layout: post
title: "Windows用户态的文件系统驱动 dokan"
date: 2014-09-09 13:03;02
categories: 文件系统
tags: [windows, 文件系统, fuse, dokan]
---

dokan是用户态的文件系统驱动，可以称之为fuse for windows。可以用来开发虚拟磁盘，即在“我的电脑”中虚拟出一个硬盘来，可以是硬盘，也可以是可移动磁盘或者网络硬盘。

<img src="/upload/images/09191524_V67t.png">

CreateFile、FindFiles、GetFileInformation需要最优先实现，有了这两个接口，就可以浏览目录了。

进入CreateFile，需要判断请求的虚拟文件是目录还是文件，如果是目录，则需要设置 DokanFileInfo->IsDirectory为True，并直接返回成功。虚拟文件的打开可以根据 CreationDisposition、AccessMode、ShareMode三者组合。最简单的做法是在最开始处对做判断，因为它只有五种可能 性，把文件不存在，但却需要以只读打开的都排除，然后就可以放心地应用：读使用”rb+”, 写使用”wb+”。

Create中返回的文件描述符或者类似的数据可以保存DokanFileInfo->context中，这个值可以在以后的其它函数调用中 访问到：比如CloseFile, CleanUp, DeleteFile, ReadFile, WriteFile等等。

CreateDirectory和实际的文件操作一致。
OpenDirectory一般直接返回成功，除非目录无访问权限，可以人为地返回-1。
CloseFile用处不大，因为在CloseFile之前，有一道CleanUp调用，已经清除了打开的文件。
CleanUp和CloseFile好像会被一前一后地调用，在CleanUp中需要做的事情是根据DokanFileInfo->context 保存的值关闭虚拟文件。并且DokanFileInfo->DeleteOnClose如果为True，则需要把当前请求的文件或者目录删除。文件 删除的动作实际是在Cleanup中实现的。

DeleteDirectory和DeleteFile两个接口实现中，不能够真正去删除文件，而是在文件或者目录需要删除时，返回0即可，系统会继续调用上面说的cleanup来处理删除事件。

在文件的删除时，有可能操作系统传递过来的请求文件并未被关闭，但好在同时DokanFileInfo->context也会被一同传递来，所以可以先强行关闭打开的文件，然后做删除操作。

操作系统的应用程序每次读写文件都是通过ReadFile、WriteFile接口完成的，一般情况下一次求请的大小比较小，比如 65535Bytes等，但也有例外，比如使用FastCopy等多线程文件快速复制工具时，它会直接向ReadFile请求32MB的大小。

ReadFile WriteFile一般情况下都会有DokanFileInfo->context参数传进来，就像平常我们写文件读写的代码一样，总是先 fopen个FILE*出来，然后再读写。 但是也有例外，比如记事本在读文件的时候，就只是给个路径+文件名。 这个时候，需要在ReadFile WriteFile临时专门为这一次请求打开文件，在退出函数时，一定要关闭它。

FlushFileBuffers是个没用的东西，可以不实现。

GetFileInformation非常重要，资源管理器每次打开目录时，会查询当前目录每个文件的信息。如果给出的信息不恰当，比如文件时间如 果是个变化的值（比如图省事，将所以文件的时间设置为当前时间），这样会导致系统不断地查询，非常的恐怖。 在返回的dwFileAttributes中，需要小心地设置文件类型，文件和目录千万要区别正确。 试过FILE_ATTRIBUTE_NORMAL+FILE_ATTRIBUTE_ARCHIVE-FILE_ATTRIBUTE_ENCRYPTED以 及FILE_ATTRIBUTE_DIRECTORY就基本正常工作了，FILE_ATTRIBUTE_ENCRYPTED一定要去掉，不然系统会认为你 虚拟出来的盘符是加密的，往其它盘复制文件时会提示不能处理加密文件而直接失败。

FindFiles函数中，我们需要用传递进来的函数指针FillFindData将我们需要显示的目录和文件填充到系统为我们准备好的地方。只要 文件的属性dwFileAttributes像样，可以构造虚拟文件和目录（比如可以将数据库里的用户和组记录读出来，表示成一层层的目录）。

MoveFile就是移动文件及改名，没什么特殊的地方。

SetEndOfFile一般情况下使用不到，但是如果有软件调用了这个API则还是有用的，比如像fastCopy，为了尽可能地加快复制速度， 它每次从内存将固定大小的数据保存到硬盘，比如大小为31MB的文件，实际上它写了32MB（文件尾部的数据其实是多余的），这是用readFile WriteFile实现的。但它最后会根据原文件的真实大小来做一次setEndOfFile将其裁剪到正确的大小。如果不实现 setEndOfFile，fastcopy就没用了。

SetFileAttributes和SetFileTime如果不想实现，就让它返回0，最好不要为了禁用这两个api.因为像Word之类的软 件，它很在意这两个函数，在保存文件时候不厌其烦地调用，所以为了让Word在虚拟盘上工作正常，必须忽悠它，否则不能保存做过编辑的文档。

GetDiskFreeSpace是返回驱动器的容量信息的，比如虚拟盘可以做容量限制。
GetVolumeInformation返回驱动器的卷标和文件系统类型，可以随便设置，文件类型可以随便取名，比如“XX文件系统”，和NTFS/FAT32是同等地位的。

GetFileInformation 有时候传递过来的DokanFileInfo->context不是空的，所以一定要使用它来查询文件大小。 假设DokanFileInfo->context保存的是fopen打开的fd, 如果使用传递过来的文件名去GetFileAttribute或者Stat()真实文件，有可能会因为缓存的缘故查询到的文件大小不是实时的。这一点在对 文件大小变化敏感的软件上特别重要，比较变态的Word，在保存的时候，它会先保存到临时文件，保存过程中，写一点数据，马上查询文件大小是否有变化是否 和写的数据大小一致。如果这时GetFIleInformation马马虎虎地返回个大小，Word就罢工了，它会以为当前磁盘是不稳定的，或者容量比较 用光，而拒绝保存。
