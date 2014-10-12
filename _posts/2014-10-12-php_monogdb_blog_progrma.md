---
layout: post
title: "使用PHP和MongoDB创建简单的博客程序"
categories: php
tags: [php, mongodb]
date: 2014-10-12 20:39:54
---

       本教程中，UncleToo将和大家一起学习如何使用PHP和MongoDB创建一个简单的博客程序。之所以选择博客，是因为它是一个基本的CRUD应用程序，非常适合PHP和MongoDB开发。对于MongoDB，本人也是初学，如果大家有更好的建议或方法，可以留言互相讨论。

       关于MongoDB的基础知识和安装，本文不再详述，请大家参开本站NoSQL频道的相关文章。在这篇文章中，我们将主要学习下面几点内容：

连接到MongoDB数据库

将文档保存在一个集合

集合中的文档查询

执行范围查询

排序文件，更新文件，删除一个集合中的一个或多个文档



安装MongoDB驱动

       在开发之前，我们需要确定PHP中是否安装了MongoDB驱动，如果还没有，请按以下步骤安装：

如果是Linux系统，执行下面命令：

{% highlight bash %}
# pecl install mongo
{% endhighlight %}

在PHP.INI文件中添加extension=mongo.so
<pre>
sudo -i

echo 'extension=mongo.so' >> /etc/php5/apache2/php.ini
</pre>

重启服务并验证驱动是否安装成功：

<pre>
php -i |grep "mongo"

php --re mongo
</pre>


如果是Windows系统，你需要做以下几件事：

<pre>
1、下载的ZIP压缩包https://github.com/mongodb/mongo-php-driver/downloads并解压缩

2、将解压缩文件夹下的php_mongo.dll文件拷贝到PHP扩展目录

3、打开PHP.INI文件，并添加: extension=php_mongo.dll

4、重启服务并使用phpinfo()验证是否安装成

</pre>

链接/选择MongoDB数据库

PHP链接MongoDB的方式和其他数据库类似，默认主机是localhost，默认端口为27017。

{% highlight php %}
$connection = new Mongo();
{% endhighlight %}
连接到远程主机可选自定义端口和身份验证：

{% highlight php %}
$connecting_string = sprintf('mongodb://%s:%d/%s', $hosts, $port,$database), $connection= new Mongo($connecting_string,array('username'=>$username,'password'=>$password));
{% endhighlight %}


数据库链接成功后，我们就可以访问数据库了。

{% highlight php %}
$dbname = $connection->selectDB('dbname');
{% endhighlight %}


数据库链接准备就绪了，下面我们就可以操作数据库了。MongoDB为我们提供了用于读取和操作数据丰富的语义。CRUD操作也就是创建，读取，更新和删除，这些是数据库最基础的操作。



创建/选择一个集合

创建/选择集合与创建链接是类似的，如果集合不存在，则创建它。

{% highlight php %}
$collection = $dbname->collection;
{% endhighlight%}
或者

{% highlight php %}
$collection = $dbname->selectCollection('collection');
{% endhighlight %}
如，下面的语句是在博客中将创建“posts”集合：

{% highlight php %}
$posts = $dbname->posts
{% endhighlight %}


创建文档

在MongoDB中创建一个文件很简单。创建一个数组，使用insert()方法将其插入到集合对象中：

{% highlight php %}
$post = array(
        'title'     => 'MongoDB文档',
        'content'   => 'MongoDB 是一种文档型数据库...',
        'saved_at'  => new MongoDate()
    );
    $posts->insert($post);
{% endhighlight %}
数组$post会自动接收一个_id字段，最为文档的唯一主键。我们也可以使用save()方法可以更新现有记录，如果记录不存在则创建新的记录。



查询文档

为了得到一个集合的数据，我们用find()方法，该方法获取一个集合中的所有数据。 findOne()返回满足指定查询条件的一个文件。 下面的例子可以查询一个或多个记录。

{% highlight bash %}
// 所有记录
$result = $posts::find();
// 一条记录
$id = '52d68c93cf5dc944128b4567';
$results = $posts::findOne(array('_id' => new MongoId($id)));
{% endhighlight %}


更新文档

修改一个现有的文档或文档集合。默认情况下, update()方法更新一个文档。如果多选项设置为true,该方法更新与查询条件相匹配的所有文档。

{% highlight bash %}
$id ='52d68c93cf5dc944128b4567';
    $posts->update(
        array('_id'=>newMongoId($id)),
    array('$set'=> array(title'   => 'Whatis phalcon'))
    );
{% endhighlight %}
update()方法接受两个参数。第一个是要更新的对象，第二个是与更新对象匹配的记录。还有第三个可选参数,用来传递一个选项数组。



上面是所有在本次项目中要用到的数据库操作的基本方法，下面我们就开始创建博客，整个博客项目我们将建立如下层次结构的文件：

<pre>
   |-------admin
           |------index.php                  
           |------auth.php
   |-------view
           |------admin
                   |-------create.view.php    
                   |-------dashbroad.view.php
           |------index.view.php              
           |------layout.php      
           |------single.view.php            
   |-------config.php                          
   |-------app.php                            
   |-------db.php                        
   |-------index.php
   |-------single.php
   |-------static                              
               |-----css
               |-----js
   |-------vendor
               |----markdown        
</pre>



下面我们分别编写每个文件。

<a href="http://www.uncletoo.com/example/php-mongodb-master.rar" >【点击下载完整源码】</a>



config.php

这是配置文件,它告诉应用程序如何连接到数据库。在这里,我们可以定义数据库名称，用户访问数据库的用户名和密码

{% highlight php %}
<?php
        define('URL','http://www.uncletoo.com/MDB/blog-mongodb');
        define('UserAuth','uncletoo');
        define('PasswordAuth','123');
        $config = array('username'=>'uncletoo','password'=>'123','dbname'=>'blog','connection_string'=> sprintf('mongodb://%s:%d/%s','127.0.0.1','27017','blog'));
?>
{% endhighlight %}
这里我们定义UserAuth和PasswordAuth参数通过HTTP身份验证保护管理文件夹。为简单起见我们这里使用HTTP身份验证。



app.php

这个文件主要是将多个PHP文件包含在一起

{% highlight php %}
<?php
    include 'config.php';
    include 'layout.php';
    include 'db.php';
    use Blog\DB,
        Blog\Layout;
    // Constructor to the db
    $db = new DB\DB($config);
    // Constructor to layout view
    $layout = new Layout\Layout();
?>
{% endhighlight %}


admin

这个文件夹包含CRUD代码。

{% highlight php %}
<?php
require_once 'auth.php';
require_once '../app.php';
require_once '../vendor/markdown/Markdown.inc.php';
use \Michelf\MarkdownExtra,
    \Michelf\Markdown;
if ((is_array($_SESSION) && $_SESSION['username'] == UserAuth)) {
    $data = array();
    $status = (empty($_GET['status'])) ? 'dashboard' : $_GET['status'];
    switch ($status) {
        //create post
        case 'create':
            break;
        //edit post
        case 'edit':
            break;
        //delete post
        case 'delete':
            //display all post in dashboard
        default:
            $currentPage = (isset($_GET['page'])) ? (int)$_GET['page'] : 1;
            $data = $db->get($currentPage, 'posts');
            $layout->view('admin/dashboard', array(
                'currentPage' => $data[0],
                'totalPages' => $data[1],
                'cursor' => $data[2]
            ));
            break;
    }
}
?>
{% endhighlight %}
下面，我们在layout.php类文件中创建view方法，来自动加载dashboard.view.php。

{% highlight bash %}
<?php namespace Blog\Layout;
Class Layout
{
    /**
     * @var array
     */
    public $data;
    public function view($path, $data)
    {
        if (isset($data)) {
            extract($data);
        }
        $path .= '.view.php';
        include "views/layout.php";
    }
}
?>
{% endhighlight %}
GET参数status对应于一个CRUD操作，如当status为create时：

{% highlight php %}
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $article = array();
    $article['title'] = $_POST['title'];
    $article['content'] = Markdown::defaultTransform($_POST['content']);
    $article['saved_at'] = new MongoDate();
    if (empty($article['title']) || empty($article['content'])) {
        $data['status'] = 'Please fill out both inputs.';
    } else {
// then create a new row in the collection posts
        $db->create('posts', $article);
        $data['status'] = 'Row has successfully been inserted.';
    }
}
{% endhighlight %}

{% highlight php %}
$layout->view('admin/create', $data);
{% endhighlight %}
函数view('admin/create', $data)显示了一个HTML表单，用户可以写一个新博客的标题/内容，并将用户提交的数据保存到MongoDB中。 默认情况下，脚本将显示下面的HTML表单：

{% highlight html %}
<form action="" method="post">
    <div><label for="Title">Title</label>
        <input type="text" name="title" id="title" required="required"/>
    </div>
    <label for="content">Content</label>
    <p><textarea name="content" id="content" cols="40" rows="8" class="span10"></textarea></p>
    <div class="submit"><input type="submit" name="btn_submit" value="Save"/></div>
</form>
{% endhighlight %}
显示如下：

<img src="/upload/images/2014031139517237.gif" />

使用PHP和MongoDB创建简单的博客程序



下面我们看看db.php文件，这个文件包含了博客程序中对数据库的所有操作。

{% highlight php %}
<?php
namespace Blog\DB;
class DB
{
    /**
     * Return db
     * @var object
     */
    private $db;
    /**
     * Results limit.
     * @var integer
     */
    public $limit = 5;
    public function __construct($config)
    {
        $this->connect($config);
    }
    //connecting mongodb
    private function connect($config)
    {
    }
    //get all data
    public function get($page, $collection)
    {
    }
    //get one data by id
    public function getById($id, $collection)
    {
    }
    //create article
    public function create($collection, $article)
    {
    }
    //delete article by id
    public function delete($id, $collection)
    {
    }
    //update article
    public function update($id, $collection, $acticle)
    {
    }
    //create and update comment
    public function commentId($id, $collection, $comment)
    {
    }
}
?>

{% endhighlight %}
MongoDB游标功能可以帮助我们很容易的实现分页。

{% highlight php %}
public function get($page,$collection){
        $currentPage = $page;
        $articlesPerPage = $this->limit;
        //number of article to skip from beginning
        $skip = ($currentPage - 1) * $articlesPerPage;
        $table = $this->db->selectCollection($collection);
    $cursor = $table->find();
        //total number of articles in database
        $totalArticles = $cursor->count();
        //total number of pages to display
        $totalPages = (int) ceil($totalArticles / $articlesPerPage);
        $cursor->sort(array('saved_at' => -1))->skip($skip)->limit($articlesPerPage);
        $data=array($currentPage,$totalPages,$cursor);
    return $data;
}
{% endhighlight %}

index.php

view文件夹内存放的是模板文件,例如index.view.php。下面是index.php文件代码：

{% highlight php %}
<?php
require 'app.php';
try {
    $currentPage = (isset($_GET['page'])) ? (int)$_GET['page'] : 1; //current page number
    $data = $db->get($currentPage, 'posts');
    $layout->view('index', array(
        'currentPage' => $data[0],
        'totalPages' => $data[1],
        'cursor' => $data[2],
        'name' => 'Duy Thien'
    ));
} catch (Exception $e) {
    echo 'Caught exception: ', $e->getMessage(), "\n";
}
?>
{% endhighlight %}


single.php

当你浏览一个帖子页面(点击阅读更多的文章),你看的就是view文件夹中的single.view.php文件。下面是single.php文件代码：

{% highlight bash %}
<?php
require 'app.php';
// Fetch the entire post
$post = $db->getById($_GET['id'], 'posts');
if ($post) {
    $layout->view('single', array(
        'article' => $post
    ));
}
?>
{% endhighlight %}
这个文件接收_id作为一个HTTP GET参数。我们articles记录集中调用findOne()方法将_id值作为参数传递。findOne()方法用于检索单个文档。getById()函数是在db.php文件中。

<img src="/upload/images/2014031139661117.gif" />

使用PHP和MongoDB创建简单的博客程序

在输入框中任意输入一些信息。然后点击保存按钮,页面会重新加载刚刚发布的评论。这就是comment.php需要实现的功能:

{% highlight php %}
<?php
require 'app.php';
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $id = $_POST['article_id'];
    $comment = array(
        'name' => $_POST['fName'],
        'email' => $_POST['fEmail'],
        'comment' => $_POST['fComment'],
        'posted_at' => new MongoDate()
    );
    $status = $db->commentId($id, 'posts', $comment);
    if ($status == TRUE) {
        header('Location: single.php?id=' . $id);
    }
}
?>

{% endhighlight %}

<a href="http://www.uncletoo.com/example/php-mongodb-master.rar" >【点击下载完整源码】</a>



到此为止，一个简单的博客程序创建完成。如果你有更好的想法可以与UncleToo联系，或者在下面发表评论互相学习。

<pre>
referer: http://www.uncletoo.com/html/application/843.html
</pre>
