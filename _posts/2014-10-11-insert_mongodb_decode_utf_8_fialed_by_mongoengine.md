---
layout: post
title: "Importing file with unknown encoding from Python into MongoDB"
categories: 数据库 
tags: [mongodb, mongoengine, pymongo]
date: 2014-10-11 17:52:54
---

Working on importing a tab-delimited file over HTTP in Python.

Before inserting a row's data into MongoDB, I'm removing slashes, ticks and quotes from the string.

Whatever the encoding of the data is, MongoDB is throwing me the exception:

bson.errors.InvalidStringData: strings in documents must be valid UTF-8

So in an endeavour to solve this problem, from the reading I've done I want to as quickly as I can, convert the row's data to Unicode using the unicode() function. In addition, I have tried calling the decode() function passing "unicode" as the first parameter but receive the error:

LookupError: unknown encoding: unicode

From there, I can make my string manipulations such as replacing the slashes, ticks, and quotes. Then before inserting the data into MongoDB, convert it to UTF-8 using the str.encode('utf-8') function.

Problem: When converting to Unicode, I am receiving the error

UnicodeDecodeError: 'ascii' codec can't decode byte 0x93 in position 1258: ordinal not in range(128)

With this error, I'm not exactly sure where to continue.

My question is this: How do I successfully import the data from a file without knowing its encoding and successfully insert it into MongoDB, which requires UTF-8?

Thanks Much!


==================================


Try these in order:

(0) Check that your removal of the slashes/ticks/etc is not butchering the data. What's a tick? Please show your code. Please show a sample of the raw data ... use print repr(sample_raw data) and copy/paste the output into an edit of your question.

(1) There's an old maxim: "If the encoding of a file is unknown, or stated to be ISO-8859-1, it is cp1252" ... where are you getting it from? If it's coming from Western Europe, the Americas, or any English/French/Spanish-speaking country/territory elsewhere, and it's not valid UTF-8, then it's likely to be cp1252

[Edit 2] Your error byte 0x93 decodes to U+201C LEFT DOUBLE QUOTATION MARK for all encodings cp1250 to cp1258 inclusive ... what language is the text written in? [/Edit 2]

(2) Save the file (before tick removal), then open the file in your browser: Does it look sensible? What do you see when you click on View / Character Encoding?

(3) Try chardet

Edit with some more advice:

Once you know what the encoding is (let's assume it's cp1252):

(1) convert your input data to unicode: uc = raw_data.decode('cp1252')

(2) process the data (remove slashes/ticks/etc) as unicode: clean_uc = manipulate(uc)

(3) you need to output your data encoded as utf8: to_mongo = clean_uc.encode('utf8')

Note 1: Your error message says "can't decode byte 0x93 in position 1258" ... 1258 bytes is a rather long chunk of text; is this reasonable? Have you had a look at the data that it is complaining about? How? what did you see?
