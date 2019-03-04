# 177crawel

简要说明：
========


`1`.该项目通过python3 爬虫技术进行[177漫画](http://www.177pic001.info)下载
      



`2`.使用技术：request进行初始请求,页面分析beautifulsoup获取关键节点，使用aiohhtp异步下载，为保证丢失的图片不至于过多，使用多进程再进行二次下载。使用
tinkter构造用户图形界面，并有各种错误提示，pyinstaller将py文件打包生成windows下exe可执行文件。





`3`.使用方法：直接点开`production`文件夹下的`crawler177.exe`程序即可，先选择本地存储地址（请确保C盘下`User`文件夹有读取权限！！！），再输入漫画的url地址（格式如`http://www.177piczz.info/html/2018/07/2191389.html`，直接复制粘贴浏览器地址栏）即可下载。



`4`.可能会出现如下两个错误：


![……](https://github.com/Areocrystal/177crawel/blob/master/images/error/error1.png)


![……](https://github.com/Areocrystal/177crawel/blob/master/images/error/error2.png)


`5`.现在看该网站要翻墙，所以如果连正常访问都做不了，那肯定也爬不了！

![……](https://github.com/Areocrystal/177crawel/blob/master/images/9150e4e5gy1g08r7hrk3sj206o06mjrf.jpg)




