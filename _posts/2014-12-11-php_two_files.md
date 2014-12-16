---
layout: post
title: "PHP 两个重要文件(config.php;function.php) "
categories: php
tags: [php]
date: 2014-12-11 01:19:25
---

config.php
 
<pre>
<?php
$mydbhost = 'localhost';//数据库服务器
$mydbuser = 'root';//数据库用户名
$mydbpw = 'admin';//数据库密码
$mydbname = 'myclass';//数据库名
$mydbcharset = 'gbk';//数据库编码,不建议修改.
$Admin_Name = 'admin';//管理员名称
$Admin_Pwd = '21232f297a57a5a743894a0e4a801fc3';//管理员密码
$eachpage = 5;//每页显示留言条数
//分页
 $psql = "select count(*) from message";
 $sum = "<b>";
 $stail = "</b>&nbsp;";
 $link = "<a href="";
 $lmid = "">";
 $ltail = "</a>&nbsp;";
 $curpage = "<a href="";
?>

 
</pre>
function.php
 

<pre>
<?php
class mysql{ 
 function connect($dbhost, $dbuser, $dbpw, $dbname = '',$dbcharset='') { 
     if(!@mysql_connect($dbhost, $dbuser, $dbpw)) {
      $this->show('Can not connect to MySQL server');
  } 
  if($dbname) {
   $this->select_db($dbname);
  }
  if($this->version() > '4.1') {
      if($dbcharset) {   
           $this->query("SET NAMES '".$dbcharset."'"); 
      }
  }
 }
 function select_db($dbname) {
  return mysql_select_db($dbname);
 }
 function fetch_array($query, $result_type = MYSQL_ASSOC) {
  return @mysql_fetch_array($query, $result_type);
 }
 function query($sql, $type = '') {
     if(!($query = mysql_query($sql))) $this->show('MySQL Query Error', $sql);
     return $query;  
 }
 function affected_rows() {
  return mysql_affected_rows();
 }
 function result($query, $row) {
  return mysql_result($query, $row);
 }
 function num_rows($query) {
  return @mysql_num_rows($query);
 }
 function num_fields($query) {
  return mysql_num_fields($query);
 }
 function free_result($query) {
  return mysql_free_result($query);
 }
 function insert_id() {
  return mysql_insert_id();  
 }
 function fetch_row($query) {
  return mysql_fetch_row($query);
 }
 function version() {
  return mysql_get_server_info();
 }
 function close() {
  return mysql_close();
 }
 function show($message = '', $sql = '') {
  if(!$sql) echo $message;
  else echo $message.'<br>'.$sql;
 }
 
// function RSDB($sql = '')
// {
//  return $this -> fetch_array($this -> query($sql));
// }
}
class page extends mysql{
    function pagination($sql,$maxnum,$page,$maxpages,$pagepre,$ext=''){
        global $sum,$stail,$link,$lmid,$ltail,$curpage;//$ext='&class=3'
        $SELF = $_SERVER['PHP_SELF'];
     
     $query = $this->query($sql);
     $rows = $this->fetch_array($query,MYSQL_NUM);
     $totalrows = $rows[0];
 
     $totalpages = ceil($totalrows/$maxnum); 
     $startnum = ($page - 1)*$maxnum; 
     $string = $sum.$totalrows.$stail.$sum.$page."/".$totalpages.$stail;
  
     if($page != 1){
      $string .= $link.$SELF."?page=1".$ext.$lmid."|&lsaquo;".$ltail;
         $string .=  $link.$SELF.'?page='.($page - 1).$ext.$lmid."&lsaquo;&lsaquo;".$ltail;
  }
     if($maxpages>=$totalpages){
      $pgstart = 1;$pgend = $totalpages;
  }
     elseif(($page-$pagepre-1+$maxpages)>$totalpages){
      $pgstart = $totalpages - $maxpages + 1;
   $pgend = $totalpages;
  }
     else{
         $pgstart=(($page<=$pagepre)?1:($page-$pagepre));
         $pgend=(($pgstart==1)?$maxpages:($pgstart+$maxpages-1));
     }
 
     for($pg=$pgstart;$pg<=$pgend;$pg++){
         if($pg == $page){
       $string .=  $curpage.$SELF."?page=".$pg.$ext.$lmid.$pg.$ltail;
   }
         else $string .=  $link.$SELF."?page=".$pg.$ext.$lmid.$pg.$ltail;
     }
  
     if($page != $totalpages){
         $string .=  $link.$SELF.'?page='.($page + 1).$ext.$lmid."&rsaquo;&rsaquo;".$ltail;
         $string .=  $link.$SELF.'?page='.$totalpages.$ext.$lmid."&rsaquo;|".$ltail;
     }
 return $string;
    }
}
function html($str){
    $str = get_magic_quotes_gpc()?$str:addslashes($str);
 return $str;
}
function dehtml($str){
    $str = nl2br(stripslashes($str));
    return $str;
}
function deip($str){
    $arr = explode('.',$str);
 $str = $arr[0].'.'.$arr[1].'.'.$arr[2].'.*';
    return $str;
}
$conn = new mysql();
$conn->connect($mydbhost, $mydbuser, $mydbpw, $mydbname,$mydbcharset);
?>

</pre>
