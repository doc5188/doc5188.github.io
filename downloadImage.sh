#!/bin/bash
#########################################################################
# File Name: downloadImage.sh
# Author: Gavin Tao
# mail: gavin.tao17@gmail.com
# Created Time: Fri 26 Sep 2014 04:09:11 PM CST
#########################################################################

file_path=${1:-""}

url_pre=${2:-""}
domain_url=""
parent_url=""

if [ ! -z $url_pre ];then
		#http://www.grabsun.com/article/2012/95263.html
		#http://www.grabsun.com
		#www.grabsun.com
	echo $url_pre |grep -E "^http://" || url_pre=http://${url_pre}
	parent_url=`dirname $url_pre`
	domain_url=`echo $url_pre|awk -F'/' '{print $1"//"$3}'`

fi

if [ -z $file_path ];then
		echo "$0 <file_path>"
		exit 1
fi

output_txt=""

for fn in `grep -oE "<img[^>]*?src=['\"]([^\"]*?)['\"]" $file_path |awk -F"src=" '{print $2}' | sed "s/'//g" | sed 's/"//g'`
do
	echo $fn |grep -E "^http://"
	ret=$?
	if [ "$ret" != "0" ];then
		echo "add url pre"
		echo $fn | grep -E "^/" && fn=$domain_url$fn
		echo $fn | grep -E "^/" && fn=$parent_url$fn
	else
		echo "$fn"
	fi
	#echo $fn |grep -E "^http://" || fn=${url_pre}$fn
	echo $fn |grep -E "^http://" || continue

	if [ ! -f `basename $fn` ];then
		wget $fn
	fi
	output_txt=$output_txt'\n<img src="/upload/images/'$(basename $fn)'" />'

done

echo $output_txt
