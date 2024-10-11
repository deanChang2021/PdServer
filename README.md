# pdServer 
Author by dean @portunid Team, wx:cdszsz。
- 1、我们的脚手架项目可以：
- 2、fastApi实现一个服务器；
- 3、PyQt5实现了GUI开发；
- 4、简单的SQL访问（未实现ORM）；
- 5、JWT实现的token鉴权；
- 6、logger日志组件；
- 7、ini系统配置持久化；
- 8、多线程(GUI/SERVER)与业务任务队列多协程实现并发；


# 基本介绍
pdServer是我们实践过程中的产物，当我们在开发各类python应用时，经常需要一个server来提供服务。
于是我们使用fastApi来提实现，并在这个过程中不断的完善。

## 联系我们

你可以通过微信： cdszsz 联系我们，为你提供一些支持。
公众号： AIGC中文站

## 简介
首先运行
```commandline
pip install -r requirements.txt
```
完成依赖包的安装。

开发参考：
https://mp.weixin.qq.com/s/2JsfcQDAEnhtB_tzHnEITQ

serverMain.py是启动入口，完成初始化
```
 """初始化redis"""
    initRedis()
    logging.info("完成Redis加载")

    """初始化窗口"""
    setupWindow()
    logging.info("完成界面加载")

```
