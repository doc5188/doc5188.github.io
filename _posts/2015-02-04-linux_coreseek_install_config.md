---
layout: post
title: "CentOS6.5 安装Sphinx 配置MySQL数据源"
categories: linux
tags: [sphinx, coreseek]
date: 2015-02-04 23:37:38
---


前提安装完mysql，并创建测试表和数据 

<pre>
DROP TABLE IF EXISTS `documents`;
CREATE TABLE IF NOT EXISTS `documents` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `content` text NOT NULL,
  `date_added` datetime NOT NULL,
  `author_id` int(11) NOT NULL,
  `group_id` int(2) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=4 ;

--
-- 转存表中的数据 `documents`
--

INSERT INTO `documents` (`id`, `title`, `content`, `date_added`, `author_id`, `group_id`) VALUES
(1, '愚人节最佳蛊惑爆料 谷歌300亿美元收购百度', '据国外媒体报道，谷歌将巨资收购百度，涉及金额高达300亿美元。谷歌借此重返大陆市场。　　该报道称，目前谷歌与百度已经达成了收购协议，将择机对外公布。百度的管理层将100%保留，但会将项目缩减，包括有啊商城，以及目前实施不力的凤巢计划。正在进行测试阶段的视频网站qiyi.com将输入更多的Youtube资源。(YouTube在大陆区因内容审查暂不能访问)。　　该消息似乎得到了谷歌CEO施密特的确认，在其twitter上用简短而暧昧的文字进行了表述：“ Withdraw from that market? u''ll also see another result, just wait... ” 意思是：从那个市场退出?你还会看到另外一个结果。毫无疑问，那个市场指的就是中国大陆。而另外的结果，对应此媒体报道，就是收购百度，从而曲线返回大陆搜索市场。　　在最近刚刚结束的深圳IT领袖峰会上，李彦宏曾言，“谷歌没有退出中国，因为还在香港”。也似乎在验证被收购的这一事实。　　截止发稿，百度的股价为597美元，市值为207亿美元。谷歌以高达300亿美元的价格，实际溢价高达50%。而谷歌市值高达1796亿美元，而且手握大量现金，作这样的决策也在情理之中。    近日，很多媒体都在报道百度创始人、CEO李彦宏的两次拒购：一次是百度上市前夕，李彦宏拒绝谷歌的并购，这个细节在2月28日央视虎年首期对话节目中得到首次披露﹔一次是在百度国际化战略中，拒绝采用海外并购的方式，而是采取了从日本市场开始的海外自主发展之路。这也让笔者由此开始思考民族品牌的发展之路。 　　收购是打压中国品牌的惯用伎俩　　2010年2月28日，央视经济频道《对话》节目昨晚推出虎年首期节目，百度董事长兼CEO李彦宏作为嘉宾做客节目。李彦宏首度谈及2005年百度上市前夕，谷歌CEO施密特曾秘密造访百度时秘密谈话的内容，主要是劝阻百度上市，李彦宏断然拒绝了施密特的“好意”。今天看来，施密特当日也许已有不祥的预感，这个几百人的小公司终有一日会成为他们的大麻烦。　　本期《对话》一经播出，便引发了业界讨论。　　外资品牌通过收购打压中国品牌的案例不胜枚举。从以往跨国企业并购的中国品牌来看，真正让其活下来的品牌并不多，要么被雪藏，要么被低端化。　　因此，2005年百度没有接受Google的收购邀请，坚持自主发展，这对于保护中国品牌，维护中国网民信息安全有着至关重要的作用。当前百度市场份额高达76%，并持续增长，这也充分验证了李彦宏拒绝收购决策的正确性。　　今天看来，“百度一下”已经成为3亿多中国网民的网络生存法则，而直到今天环视全球，真正能像中国一样，拥有自己独立搜索引擎的只有4个国家！我们也许应该庆幸当时李彦宏的选择。这个故事也告诉我们，中国企业做品牌还要靠自己！　　收购也可能是中国企业走出去的陷阱　　同样在2月28日，亚布力第十届年会上，李彦宏在论坛上指出：“我们和很多其它公司的国际化路子是很不一样的，我们不是去买一个国外的公司，”，李彦宏解释了百度率先选择日本作为走出去的对象的原因，因为日本和中国一衣带水的近邻优势，日本的市场规模，在日本也没有一家独大的搜索引擎。　　中国企业收购这些外资品牌目的是“借船出海”。外资品牌进入中国是收购中国优质品牌，而中国企业进入国外市场的收购策略恰恰相反，这也是中国企业借船出海屡屡失败的原因所在。　　笔者认为，中国互联网公司走出去要依靠自身发展，并不能单纯依靠收购。李彦宏在百度成立伊始就抱定了国际化决心，使百度真正在面对国际化机遇时，更加冷静和具有前瞻力。李彦宏也承认当前百度在日本还处于初级发展阶段，但他也预言“2012年，百度与Google划洋而治”，对此我们拭目以待！', '2010-04-01 22:20:07', 1, 2),
(2, 'Twitter主页改版 推普通用户消息增加趋势话题', '4月1日消息，据国外媒体报道，Twitter本周二推出新版主页，目的很简单：帮助新用户了解Twitter和增加用户黏稠度。　　新版Twittter入口处的内容眼花缭乱，在头部下方有滚动的热门趋势话题，左边列出了普通用户账户和他们最新的消息。　　另一个显著的部分是“Top Tweets”，它采用了新算法推选出最热门的话题，每个几秒刷新一次。Twitter首席科学家Abdur Chowdhury表示，这种算法选出了所有用户的信息，而不是拥有大量追随者所发的信息。　　首页对于首次访问网站的用户非常重要，因为这决定了用户的第一印象。研究发现，多达60%的Twittter用户在注册后的一个月内不再访问网站。Twittter希望能更好地展现网站的面貌，帮助游客找到感兴趣的东西。', '2010-04-01 23:25:48', 1, 3),
(3, '死都要上！Opera Mini 体验版抢先试用', 'Opera一直都被认为是浏览速度飞快，同时在移动平台上更是占有不少的份额。不久前，Opera正式向苹果提交了针对iPhone设计的Opera Mini。日前，台湾IT网站放出了Opera Mini和Safari的评测文章，下面让我们看看Opera和Safari到底谁更好用更快吧。　　Opera Mini VS Safari，显示方式很不相同和Safari不同的是，Opera Mini会针对手机对网页进行一些调整　　Opera Mini与Safari的运作原理不大相同。网页会通过Opera的服务器完整压缩后再发送到手机上，不像Safari可通过Multi-Touch和点击的方式自由缩放，Opera Mini会预先将文字照iPhone的宽度做好调整，点击区域后自动放大。如果习惯了Safari的浏览方式，会感觉不大顺手，不过对许多宽度太宽，缩放后文字仍然显示很小的网页来说，Opera Mini的显示方式比较有优势。　　打开测试网站首页所花费的流量，Safari和Opera Mini的差距明显可见。这个在国内移动资费超高的局面来说，Opera Mini估计会比较受欢迎和省钱。Opera Mini的流量少得惊人，仅是Safari的十分之一　　兼容性相比，Safari完胜打开Google首页，Safari上是iPhone专用界面，Opera则是一般移动版本　　Opera Mini的速度和省流量还是无法取代Safari成为iPhone上的主要浏览器。毕竟iPhone的高占有率让许多网站，线上服务都为Safari设计了专用页面。光Google的首页为例子就看出了明显的差别。另外，像Google Buzz这样线上应用，就会出现显示错误。Google Buzz上，Opera无法输入内容　　Opera Mini其他专属功能页面内搜索和关键字直接搜索相当人性化　　除了Opera独创的Speed Dial九宫格快速启动页面外，和Opera Link和电脑上的Opera直接同步书签、Speed Dial设定外。Opera Mini还能够直接搜索页面中的文字，查找资料时相当方便。另外也能选取文字另开新分页搜索，比起Safari还要复制、开新页、粘贴简单许多。同时还能将整个页面打包存储，方便离线浏览。　　现在Opera Mini想要打败Safari还剩下一个很严重的问题-苹果何时会或者会不会通过Opera Mini的审核。', '2010-04-01 12:01:00', 2, 3);
</pre>


1、下载Sphinx
<pre>
cd /usr/software
wget http://sphinxsearch.com/files/sphinx-2.1.5-release.tar.gz
</pre>
或者直接去Sphinx官网去下载最新版本

2、安装依赖包

<pre>
yum install make gcc g++ gcc-c++ libtool autoconf automake imake mysql-devel libxml2-devel expat-devel
</pre>

3、安装Sphinx 

<pre>
tar zxvf sphinx-2.1.5-release.tar.gz

cd sphinx-2.1.5-release

./configure --prefix=/usr/local/sphinx

make

make install

vi /etc/ld.so.conf 

/usr/local/mysql/lib #增加这一行保存 

/sbin/ldconfig -v
</pre>


 4、配置Sphinx

<pre>
cd /usr/local/sphinx/etc
cp sphinx-min.conf.dist csft.conf
</pre>

vi csft.conf


<pre>
source mysql
{
  type              = mysql
  sql_host          = 10.10.3.203
  sql_user          = root
  sql_pass          = dsideal
  sql_db            = test
  sql_port          = 3306
  sql_sock          = /usr/local/mysql/mysql.sock
  sql_query_pre     = SET NAMES utf8
  sql_query         = SELECT id, group_id, UNIX_TIMESTAMP(date_added) AS date_added, title, content FROM documents
  sql_attr_uint     = group_id
  #sql_attr_timestamp= date_added
  #sql_query_info_pre= SET NAMES utf8
  #sql_query_info    = SELECT * FROM aaa WHERE id=$id
}
index index_mysql
{
  source        = mysql
  path          = /usr/local/sphinx/var/data
  docinfo       = extern
  mlock         = 0
  min_word_len  = 1
  charset_type  = utf-8
  charset_table = U+FF10..U+FF19->0..9, 0..9, U+FF41..U+FF5A->a..z, U+FF21..U+FF3A->a..z,A..Z->a..z, a..z, U+0149, U+017F, U+0138, U+00DF, U+00FF, U+00C0..U+00D6->U+00E0..U+00F6,U+00E0..U+00F6, U+00D8..U+00DE->U+00F8..U+00FE, U+00F8..U+00FE, U+0100->U+0101, U+0101,U+0102->U+0103, U+0103, U+0104->U+0105, U+0105, U+0106->U+0107, U+0107, U+0108->U+0109,U+0109, U+010A->U+010B, U+010B, U+010C->U+010D, U+010D, U+010E->U+010F, U+010F,U+0110->U+0111, U+0111, U+0112->U+0113, U+0113, U+0114->U+0115, U+0115, U+0116->U+0117,U+0117, U+0118->U+0119, U+0119, U+011A->U+011B, U+011B, U+011C->U+011D,U+011D,U+011E->U+011F, U+011F, U+0130->U+0131, U+0131, U+0132->U+0133, U+0133, U+0134->U+0135,U+0135, U+0136->U+0137, U+0137, U+0139->U+013A, U+013A, U+013B->U+013C, U+013C,U+013D->U+013E, U+013E, U+013F->U+0140, U+0140, U+0141->U+0142, U+0142, U+0143->U+0144,U+0144, U+0145->U+0146, U+0146, U+0147->U+0148, U+0148, U+014A->U+014B, U+014B,U+014C->U+014D, U+014D, U+014E->U+014F, U+014F, U+0150->U+0151, U+0151, U+0152->U+0153,U+0153, U+0154->U+0155, U+0155, U+0156->U+0157, U+0157, U+0158->U+0159,U+0159,U+015A->U+015B, U+015B, U+015C->U+015D, U+015D, U+015E->U+015F, U+015F, U+0160->U+0161,U+0161, U+0162->U+0163, U+0163, U+0164->U+0165, U+0165, U+0166->U+0167, U+0167,U+0168->U+0169, U+0169, U+016A->U+016B, U+016B, U+016C->U+016D, U+016D, U+016E->U+016F,U+016F, U+0170->U+0171, U+0171, U+0172->U+0173, U+0173, U+0174->U+0175,U+0175,U+0176->U+0177, U+0177, U+0178->U+00FF, U+00FF, U+0179->U+017A, U+017A, U+017B->U+017C,U+017C, U+017D->U+017E, U+017E, U+0410..U+042F->U+0430..U+044F, U+0430..U+044F,U+05D0..U+05EA, U+0531..U+0556->U+0561..U+0586, U+0561..U+0587, U+0621..U+063A, U+01B9,U+01BF, U+0640..U+064A, U+0660..U+0669, U+066E, U+066F, U+0671..U+06D3, U+06F0..U+06FF,U+0904..U+0939, U+0958..U+095F, U+0960..U+0963, U+0966..U+096F, U+097B..U+097F,U+0985..U+09B9, U+09CE, U+09DC..U+09E3, U+09E6..U+09EF, U+0A05..U+0A39, U+0A59..U+0A5E,U+0A66..U+0A6F, U+0A85..U+0AB9, U+0AE0..U+0AE3, U+0AE6..U+0AEF, U+0B05..U+0B39,U+0B5C..U+0B61, U+0B66..U+0B6F, U+0B71, U+0B85..U+0BB9, U+0BE6..U+0BF2, U+0C05..U+0C39,U+0C66..U+0C6F, U+0C85..U+0CB9, U+0CDE..U+0CE3, U+0CE6..U+0CEF, U+0D05..U+0D39, U+0D60,U+0D61, U+0D66..U+0D6F, U+0D85..U+0DC6, U+1900..U+1938, U+1946..U+194F, U+A800..U+A805,U+A807..U+A822, U+0386->U+03B1, U+03AC->U+03B1, U+0388->U+03B5, U+03AD->U+03B5,U+0389->U+03B7, U+03AE->U+03B7, U+038A->U+03B9, U+0390->U+03B9, U+03AA->U+03B9,U+03AF->U+03B9, U+03CA->U+03B9, U+038C->U+03BF, U+03CC->U+03BF, U+038E->U+03C5,U+03AB->U+03C5, U+03B0->U+03C5, U+03CB->U+03C5, U+03CD->U+03C5, U+038F->U+03C9,U+03CE->U+03C9, U+03C2->U+03C3, U+0391..U+03A1->U+03B1..U+03C1,U+03A3..U+03A9->U+03C3..U+03C9, U+03B1..U+03C1, U+03C3..U+03C9, U+0E01..U+0E2E,U+0E30..U+0E3A, U+0E40..U+0E45, U+0E47, U+0E50..U+0E59, U+A000..U+A48F, U+4E00..U+9FBF,U+3400..U+4DBF, U+20000..U+2A6DF, U+F900..U+FAFF, U+2F800..U+2FA1F, U+2E80..U+2EFF,U+2F00..U+2FDF, U+3100..U+312F, U+31A0..U+31BF, U+3040..U+309F, U+30A0..U+30FF,U+31F0..U+31FF, U+AC00..U+D7AF, U+1100..U+11FF, U+3130..U+318F, U+A000..U+A48F,U+A490..U+A4CF
  min_prefix_len = 0
  min_infix_len = 1
  ngram_len     = 1

}
indexer
{
  mem_limit    = 256M
}
searchd
{
  listen            = 3312
  listen            = 3313:mysql41
  log               = /usr/local/sphinx/var/log/searchd.log
  query_log         = /usr/local/sphinx/var/log/query.log
  read_timeout      = 5
  client_timeout    = 300
  max_children      = 30
  pid_file          = /usr/local/sphinx/var/log/searchd.pid
  max_matches       = 1000
  seamless_rotate   = 1
  preopen_indexes   = 1
  unlink_old        = 1
}
</pre>


5、启动Sphinx、创建索引

<pre>
#启动
/usr/local/sphinx/bin/searchd -c /usr/local/sphinx/etc/csft.conf
#创建索引
/usr/local/sphinx/bin/indexer -c /usr/local/sphinx/etc/csft.conf --rotate --all
#停止
/usr/local/sphinx/bin/searchd -c /usr/local/sphinx/etc/csft.conf --stop
</pre>

6、

<pre>
CREATE TABLE `documents_sphinxse` (
  `id` bigint(20) unsigned NOT NULL,
  `weight` int(11) DEFAULT '1',
  `query` varchar(3072) NOT NULL,
  `author_id` int(10) unsigned DEFAULT '0',
  `group_id` int(10) unsigned DEFAULT '0',
  KEY `query` (`query`(1024))
) ENGINE=SPHINX DEFAULT CHARSET=utf8 CONNECTION='sphinx://10.10.3.203:3312';
</pre>


7、

<pre>
Select id from     documents_sphinxse where query="增加用户"; 
</pre>

 
 那么，写在配置文件中的group_id是什么意思呢？
