# 177crawel

简要说明：
========


`1`.该项目通过python3 爬虫技术进行[177漫画](http://www.177pic.info)下载
      



`2`.使用技术：request进行初始请求,页面分析beautifulsoup获取关键节点，使用aiohhtp异步下载，为保证丢失的图片不至于过多，使用多进程再进行二次下载。使用

tinkter构造用户图形界面，并有各种错误提示，pyinstaller将整个py文件打包成windows下exe可执行文件。





`3`.使用方法：直接点开`dist`文件夹下的exe文件，先选择本地存储地址（请确保C盘下User文件夹有读取权限！！！），再输入漫画的url地址即可下载。





`4`.现在看该网站要翻墙，所以如果连正常访问都做不了，那肯定也爬不了！

