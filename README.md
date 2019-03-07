# 177crawel

简要说明：
========


`1`.该项目通过python3.6 爬虫技术对[177漫画](http://www.177pic001.info)上的漫画资源进行下载；
      

`2`.使用方法：直接点开`production`文件夹下的`crawler177.exe`程序即可，先选择本地存储地址（请确保C盘下`User`文件夹有读取权限，会记住初次选择！！！），再输入漫画的url地址即可下载，就这么简单方便。


`3`.使用技术：request进行初始请求,页面分析beautifulsoup获取关键节点，先使用asyncio、aiohttp进行异步下载，为保证丢失的图片不至于过多，使用多进程、retry模块再进行二次下载。使用tinkter构造用户图形界面，并有各种错误提示，pyinstaller将py文件打包生成windows下exe可执行文件。

`4`.注意事项(重要)：

      *使用时请务必关闭xx卫士、xx管家等杀毒软件（尤其360）;
      
      [2].如果正常访问不了那也当然下不了，现在要访问该网站，请用vpn；
      
      [3].保证C盘用户文件夹有读取权限；
      
      [4].不要动里面的图片文件，会造成程序无法运行；
      
      [5].可能会报丢失python36、api等dll文件的错误；
      



`5`.可能会出现如下两个错误：


![……](https://github.com/Areocrystal/177crawel/blob/master/images/error/error1.png)


![……](https://github.com/Areocrystal/177crawel/blob/master/images/error/error2.png)




![……](https://github.com/Areocrystal/177crawel/blob/master/images/9150e4e5gy1g08r7hrk3sj206o06mjrf.jpg)




