# 177crawel

简要说明：
========


`1`.该项目通过python3.6 爬虫技术对177漫画网上的本子资源进行下载:smiley:（*一定要VPN）；
      

`2`.__使用方法__：-_直接点开**production**文件夹下的**crawler177.exe**即可，先选择本地存储地址（请确保C盘下`User`文件夹有读取权限，会记住初次选择！！！），再粘贴漫画单本url即可下载_。


`3`.__使用技术__：fake_useragent伪造ua信息，request进行初始请求,页面分析beautifulsoup获取关键节点，使用多进程下载，异步aiohttp、asyncio
会被拦截已放弃。tkinter构造用户图形交互界面，并涵盖各种错误提示，pyInstaller将.py文件打包生成windows下exe可执行文件,解决pyinstaller打包多进程文件执行时无响应还会大量占用cpu和内存资源造成系统卡死的问题，通过访问windows剪切板实现智能粘贴。

`4`.*__注意事项__：

     [1].使用时请务必关闭xx卫士、xx管家等杀毒软件（尤其360）;
      
     [2].如果正常访问不了那也当然下不了，一定要用vpn；
      
     [3].保证C盘用户文件夹有读取权限；
      
     [4].不要移动其中的图片文件，会造成程序无法运行；
      
     [5].可能会报丢失python36、api等dll文件的错误；
      



`5`.可能会出现如下两个错误：


![……](https://github.com/Areocrystal/177crawel/blob/master/images/error/error1.png)


![……](https://github.com/Areocrystal/177crawel/blob/master/images/error/error2.png)



`6`.开源，请勿用于商业用途。



![……](https://github.com/Areocrystal/177crawel/blob/master/images/9150e4e5gy1g08r7hrk3sj206o06mjrf.jpg)




