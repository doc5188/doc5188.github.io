---
layout: post
title: "PHP网站地图生成类(一)"
categories: php
tags: [网站地图生成]
date: 2014-10-20 10:13:07
---

做网站的朋友们都有过这样的经历，在一个新站刚刚开始运营时，最希望的就是百度、google这样的搜索引擎来索引自己的页面，恨不得让蜘蛛不停地爬，赶快把自己新添加的页面索引进去。

加速搜索引擎的收录方法有很多，比如在一些人气较高的地方，找与自己网站相关的板块，发一些推广文章；或者与其他站长交换一下连接，增加页面的外部链接；最基本的也是每个站长都要做的事情就是生成自己的Sitemap，提交给各大搜索引擎。

今天就和大家分享一个php网站地图生成类，希望对大家的互联网生活有所帮助。

<pre>
/**
* @category   class
* @package    SitemapGenerator
* @author     Pawe? Antczak <pawel@antczak.org>
* @translate 10V | www.smartwei.com
* @copyright 2009 Pawe? Antczak
* @license    http://www.gnu.org/licenses/gpl.html GPL V 2.0
* @version    1.2.0
* @see        http://www.sitemaps.org/protocol.php
* @see        http://en.wikipedia.org/wiki/Sitemaps
* @see        http://en.wikipedia.org/wiki/Sitemap_index
*/
class SitemapGenerator {
    /**
     * sitemap的名字
     * @var string
     * @access public
     */
    public $sitemapFileName = "sitemap.xml";
    /**
     * sitemap索引的名字
     * @var string
     * @access public
     */

    public $sitemapIndexFileName = "sitemap-index.xml";
    /**
     * robots文件的名字
     * @var string
     * @access public
     */
    public $robotsFileName = "robots.txt";
    /**
     * 每一个sitemap文件包含的连接数
     * 每个sitemap文件包含连接数最好不要 50,000.
     * sitemap文件的大小最好不要超过10MB,如果网站的链接很长的话，请减少页面包含链接数
     * @var int
     * @access public
     */
    public $maxURLsPerSitemap = 50000;
    /**
     * 如果该变量设置为true, 会生成两个sitemap文件，后缀名分别是.xml和.xml.gz 而且会被添加到robots.txt文件中.
     * 同时.gz文件会被提交给搜索引擎。
     * 如果每页包含的连接数大于50,000，则这个字段将被忽略，除了sitemap索引文件之外，其他sitemap文件都会被压缩
     * @var bool
     * @access public
     */
    public $createGZipFile = false;
    /**
     * 网站的url
     * 脚本向搜索引擎提交sitemap时会用到这个变量
     * @var string
     * @access private
     */
    private $baseURL;
    /**
     * 相关脚本的路径
     * 当你想把sitemap和robots文件放在不同的路径时，设置这个变量。
     * @var string
     * @access private
     */
    private $basePath;
    /**
     * 这个类的版本号
     * @var string
     * @access private
     */
    private $classVersion = "1.2.0";
    /**
     * 搜索引擎的URL
     * @var array of strings
     * @access private
     */
    private $searchEngines = array(
        array("http://search.yahooapis.com/SiteExplorerService/V1/updateNotification?appid=USERID&url=",
        "http://search.yahooapis.com/SiteExplorerService/V1/ping?sitemap="),
        "http://www.google.com/webmasters/tools/ping?sitemap=",
        "http://submissions.ask.com/ping?sitemap=",
        "http://www.bing.com/webmaster/ping.aspx?siteMap="
    );
    /**
     * url数组
     * @var array of strings
     * @access private
     */
    private $urls;
    /**
     * sitemap的数组
     * @var array of strings
     * @access private
     */

    private $sitemaps;
    /**
     * sitemap索引的数组
     * @var array of strings
     * @access private
     */

    private $sitemapIndex;
     /**
     * 当前sitemap的全路径
     * @var string
     * @access private
     */
    private $sitemapFullURL;

    /**
     * 构造函数
     * @param string $baseURL 你网站的URL, 以 / 结尾.
     * @param string|null $basePath sitemap和robots文件存储的相对路径.
     */
    public function __construct($baseURL, $basePath = "") {
        $this->baseURL = $baseURL;
        $this->basePath = $basePath;
    }
    /**
     * 使用这个方法可以同时添加多个url
     * 每个链接有4个参数可以设置
     * @param array of arrays of strings $urlsArray
     */
    public function addUrls($urlsArray) {
        if (!is_array($urlsArray))
            throw new InvalidArgumentException('参数$aURLs需要时数组');
        foreach ($urlsArray as $url) {
            $this->addUrl(isset ($url[0]) ? $url[0] : null,
                isset ($url[1]) ? $url[1] : null,
                isset ($url[2]) ? $url[2] : null,
                isset ($url[3]) ? $url[3] : null);
        }
    }
    /**
     * 使用这个方法每次添加一个连接到sitemap中
     * @param string $url URL
     * @param string $lastModified 当被修改时，使用ISO 8601
     * @param string $changeFrequency 搜索引擎抓取信息的频率
     * @param string $priority 你网站中连接的权重
     * @see http://en.wikipedia.org/wiki/ISO_8601
     * @see http://php.net/manual/en/function.date.php
     */
    public function addUrl($url, $lastModified = null, $changeFrequency = null, $priority = null) {
        if ($url == null)
            throw new InvalidArgumentException("URL 是必填项.");
        $urlLenght = extension_loaded('mbstring') ? mb_strlen($url) : strlen($url);
        if ($urlLenght > 2048)
            throw new InvalidArgumentException("URL的长度不能超过2048。
                                                请注意，见此url长度需要使用mb_string扩展.
                                                请确定你的服务器已经打开了这个模块");
        $tmp = array();
        $tmp['loc'] = $url;
        if (isset($lastModified)) $tmp['lastmod'] = $lastModified;
        if (isset($changeFrequency)) $tmp['changefreq'] = $changeFrequency;
        if (isset($priority)) $tmp['priority'] = $priority;
        $this->urls[] = $tmp;
    }
    /**
     * 在内存中创建sitemap.
     */
    public function createSitemap() {
        if (!isset($this->urls))
            throw new BadMethodCallException("请先加载addUrl或者addUrls方法.");
        if ($this->maxURLsPerSitemap > 50000)
            throw new InvalidArgumentException("每个sitemap中的链接不能超过50,000个");

        $generatorInfo = '<!-- generator="SimpleSitemapGenerator/'.$this->classVersion.'" -->
                          <!-- sitemap-generator-url="http://www.antczak.org"
                          sitemap-generator-version="'.$this->classVersion.'" -->
                          <!-- generated-on="'.date('c').'" -->';
        $sitemapHeader = '<?xml version="1.0" encoding="UTF-8"?>'.$generatorInfo.'
                            <urlset
                                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                                xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9
                                http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd"
                                xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
                         </urlset>';
        $sitemapIndexHeader = '<?xml version="1.0" encoding="UTF-8"?>'.$generatorInfo.'
                                <sitemapindex
                                    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                                    xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9
                                    http://www.sitemaps.org/schemas/sitemap/0.9/siteindex.xsd"
                                    xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
                              </sitemapindex>';
        foreach(array_chunk($this->urls,$this->maxURLsPerSitemap) as $sitemap) {
            $xml = new SimpleXMLElement($sitemapHeader);
            foreach($sitemap as $url) {
                $row = $xml->addChild('url');
                $row->addChild('loc',htmlspecialchars($url['loc'],ENT_QUOTES,'UTF-8'));
                if (isset($url['lastmod'])) $row->addChild('lastmod', $url['lastmod']);
                if (isset($url['changefreq'])) $row->addChild('changefreq',$url['changefreq']);
                if (isset($url['priority'])) $row->addChild('priority',$url['priority']);
            }
            if (strlen($xml->asXML()) > 10485760)
                throw new LengthException("sitemap文件的大小不能超过10MB (10,485,760),
                    please decrease maxURLsPerSitemap variable.");
            $this->sitemaps[] = $xml->asXML();

        }
        if (sizeof($this->sitemaps) > 1000)
            throw new LengthException("sitemap索引文件最多可以包含1000条索引.");
        if (sizeof($this->sitemaps) > 1) {
            for($i=0; $i<sizeof($this->sitemaps); $i++) {
                $this->sitemaps[$i] = array(
                    str_replace(".xml", ($i+1).".xml.gz", $this->sitemapFileName),
                    $this->sitemaps[$i]
                );
            }
            $xml = new SimpleXMLElement($sitemapIndexHeader);
            foreach($this->sitemaps as $sitemap) {
                $row = $xml->addChild('sitemap');
                $row->addChild('loc',$this->baseURL.htmlentities($sitemap[0]));
                $row->addChild('lastmod', date('c'));
            }
            $this->sitemapFullURL = $this->baseURL.$this->sitemapIndexFileName;
            $this->sitemapIndex = array(
                $this->sitemapIndexFileName,
                $xml->asXML());
        }
        else {
            if ($this->createGZipFile)
                $this->sitemapFullURL = $this->baseURL.$this->sitemapFileName.".gz";
            else
                $this->sitemapFullURL = $this->baseURL.$this->sitemapFileName;
            $this->sitemaps[0] = array(
                $this->sitemapFileName,
                $this->sitemaps[0]);
        }
    }
    /**
     * 如果你不想生成sitemap文件，指向用其中的内容，这个返回的数组就包含了对应的信息.
     * @return 字符串数组
     * @access public
     */
    public function toArray() {
        if (isset($this->sitemapIndex))
            return array_merge(array($this->sitemapIndex),$this->sitemaps);
        else
            return $this->sitemaps;
    }
    /**
     * 写sitemap文件
     * @access public
     */
    public function writeSitemap() {
        if (!isset($this->sitemaps))
            throw new BadMethodCallException("请先加载createSitemap方法.");
        if (isset($this->sitemapIndex)) {
            $this->_writeFile($this->sitemapIndex[1], $this->basePath, $this->sitemapIndex[0]);
            foreach($this->sitemaps as $sitemap) {
                $this->_writeGZipFile($sitemap[1], $this->basePath, $sitemap[0]);
            }
        }
        else {
            $this->_writeFile($this->sitemaps[0][1], $this->basePath, $this->sitemaps[0][0]);
            if ($this->createGZipFile)
                $this->_writeGZipFile($this->sitemaps[0][1], $this->basePath, $this->sitemaps[0][0].".gz");
        }
    }
    /**
     * 如果robots.txt文件存在，更新该文件，将新添加的信息写入其中
     * 如果robots.txt文件不存在，则创建该文件，写入刚添加的信息
     * @access public
     */
    public function updateRobots() {
        if (!isset($this->sitemaps))
            throw new BadMethodCallException("请先加载createSitemap方法");
        $sampleRobotsFile = "User-agent: *\nAllow: /";
        if (file_exists($this->basePath.$this->robotsFileName)) {
            $robotsFile = explode("\n", file_get_contents($this->basePath.$this->robotsFileName));
            $robotsFileContent = "";
            foreach($robotsFile as $key=>$value) {
                if(substr($value, 0, <IMG alt=8) src="http://www.smartwei.com/wp-includes/images/smilies/icon_cool.gif"> == 'Sitemap:') unset($robotsFile[$key]);
                else $robotsFileContent .= $value."\n";
            }
            $robotsFileContent .= "Sitemap: $this->sitemapFullURL";
            if ($this->createGZipFile && !isset($this->sitemapIndex))
                $robotsFileContent .= "\nSitemap: ".$this->sitemapFullURL.".gz";
            file_put_contents($this->basePath.$this->robotsFileName,$robotsFileContent);
        }
        else {
            $sampleRobotsFile = $sampleRobotsFile."\n\nSitemap: ".$this->sitemapFullURL;
            if ($this->createGZipFile && !isset($this->sitemapIndex))
                $sampleRobotsFile .= "\nSitemap: ".$this->sitemapFullURL.".gz";
            file_put_contents($this->basePath.$this->robotsFileName, $sampleRobotsFile);
        }
    }
    /**
     * 将新生成的sitemap提交给搜索引擎，包括：Google, Ask, Bing and Yahoo。
     * 如果你没有填写yahooid,yahoo也会被通知。
     * 但是每天最多提交一次，重复提交yahoo会拒绝接受信息
     * @param string $yahooAppId 你网站的Yahoo Id
     * @return 以数组形式返回每个搜索引擎的消息
     * @access public
     */
    public function submitSitemap($yahooAppId = null) {
        if (!isset($this->sitemaps))
            throw new BadMethodCallException("To submit sitemap, call createSitemap function first.");
        if (!extension_loaded('curl'))
            throw new BadMethodCallException("cURL library is needed to do submission.");
        $searchEngines = $this->searchEngines;
        $searchEngines[0] = isset($yahooAppId) ? str_replace("USERID", $yahooAppId, $searchEngines[0][0]) : $searchEngines[0][1];
        $result = array();
        for($i=0;$i<sizeof($searchEngines);$i++) {
            $submitSite = curl_init($searchEngines[$i].htmlspecialchars($this->sitemapFullURL,ENT_QUOTES,'UTF-8'));
            curl_setopt($submitSite, CURLOPT_RETURNTRANSFER, true);
            $responseContent = curl_exec($submitSite);
            $response = curl_getinfo($submitSite);
            $submitSiteShort = array_reverse(explode(".",parse_url($searchEngines[$i], PHP_URL_HOST)));
            $result[] = array("site"=>$submitSiteShort[1].".".$submitSiteShort[0],
                "fullsite"=>$searchEngines[$i].htmlspecialchars($this->sitemapFullURL, ENT_QUOTES,'UTF-8'),
                "http_code"=>$response['http_code'],
                "message"=>str_replace("\n", " ", strip_tags($responseContent)));
        }
        return $result;
    }
    /**
     * 保存文件
     * @param string $content
     * @param string $filePath
     * @param string $fileName
     * @return bool
     * @access private
     */
    private function _writeFile($content, $filePath, $fileName) {
        $file = fopen($filePath.$fileName, 'w');
        fwrite($file, $content);
        return fclose($file);
    }
    /**
     * 保存 GZipped文件.
     * @param string $content
     * @param string $filePath
     * @param string $fileName
     * @return bool
     * @access private
     */
    private function _writeGZipFile($content, $filePath, $fileName) {
        $file = gzopen($filePath.$fileName, 'w');
        gzwrite($file, $content);
        return gzclose($file);
    }
}
</pre>

转自：http://www.smartwei.com/php-sitemap-generator-class.html
