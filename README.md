API Mock工具
============
API Mock工具是用python编写的一个轻量级web程序（全部代码100+行），提供给客户端开发和QA的一个数据接口，通过它，你可以创建任意服务端还未实现的接口，或者对已有接口返回数据进行任意修改，以达到模拟不同数据返回客户端的开发和测试。

如何使用
-------
1.通过浏览器访问http://“服务部署的ip地址”:8080/<br>
2.通过如下图在左边‘‘接口编辑区’’进行模拟数据的编辑，并点击下方“Submit”按钮提交保存<br>
![readme](https://raw.github.com/donotwarry/Simple-Mock-Server/master/readme.png)<br>
3.通过访问http://“服务部署的ip地址”:8080/mock?url=“待模拟的请求地址”进行数据读取，如果命中规则中的mock请求，则直接返回mock接口，否则返回“待模拟的请求地址”的数据response<br>

构建自己的API模拟环境
-------
1.安装python环境，详见：http://www.python.org/<br>
2.安装web.py模块，详见：http://webpy.org/<br>
3.下载工具包源码解压，执行其中的mockserver文件（python mockserver.py）<br>
4.打开浏览器输入http://localhost:8080/访问<br>
