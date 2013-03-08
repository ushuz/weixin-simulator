#Weixin-simulator

微信公众平台没有本地调试环境，在进行微信公众平台开发时遇到了很多麻烦。写测试固然是一种方式，但维护一大批测试样例挺费神的。所以希望能有什么东西模拟微信客户端在本地与应用进行交互，求谷歌不得，于是花了几个小时用`tkinter`自己写了个模拟器。


##设置
请根据需要在主文件`gui.py`中修改settings字典，最重要的是修改`url`项的值，将其修改为处理微信消息的相应URL。
```python
settings = {
    # `ToUserName` & `FromUserName` will be placed in the XML data posted to
    # the given URL.
    "ToUserName": "gh_bea8cf2a04fd",
    "FromUserName": "oLXjgjiWeAS1gfe4ECchYewwoyTc",

    # URL of your Wexin handler.
    "url": "http://localhost:8080/weixin",

    # These will be displayed in GUI.
    "mp_display_name": "APP",
    "me_display_name": "ME",

    # The token you submitted to Weixin MP. Used to generate signature.
    "token": ""
}
```

##截图
![Simulator GUI Screenshot](/gui.jpg)
