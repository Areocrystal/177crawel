# 177crawel

简要说明：
========


`1`.该项目通过python3.6 爬虫技术对177漫画网上的本子资源进行下载:smiley:；
      

`2`.__使用方法__：-_直接点开**production**文件夹下的**crawler177.exe**即可，先选择本地存储地址（请确保C盘下`User`文件夹有读取权限，会记住初次选择！！！），再粘贴漫画单本url即可下载_。


`3`.__使用技术__：fake_useragent伪造ua信息，request进行初始请求,页面分析beautifulsoup获取关键节点，先使用asyncio、aiohttp进行异步下载，为保证丢失的图片不至于过多，使用多进程、retry再进行二次下载。tkinter构造用户图形交互界面，并涵盖各种错误提示，PyInstaller将.py文件打包生成windows下exe可执行文件。

`4`.*__注意事项__：

     [1].使用时请务必关闭xx卫士、xx管家等杀毒软件（尤其360）;
      
     [2].如果正常访问不了那也当然下不了，现在要访问该网站，请用vpn；
      
     [3].保证C盘用户文件夹有读取权限；
      
     [4].不要移动其中的图片文件，会造成程序无法运行；
      
     [5].可能会报丢失python36、api等dll文件的错误；
      



`5`.可能会出现如下两个错误：


![……](https://github.com/Areocrystal/177crawel/blob/master/images/error/error1.png)


![……](https://github.com/Areocrystal/177crawel/blob/master/images/error/error2.png)





![……](https://github.com/Areocrystal/177crawel/blob/master/images/9150e4e5gy1g08r7hrk3sj206o06mjrf.jpg)




