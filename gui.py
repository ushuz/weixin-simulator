#  -*-  coding: utf-8  -*-

import time
import random
import urllib2
import hashlib
import xml.etree.cElementTree as ET

import Tkinter as tk
import ScrolledText as st


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


template = '''
<xml>
    <ToUserName><![CDATA[%(to)s]]></ToUserName>
    <FromUserName><![CDATA[%(from)s]]></FromUserName>
    <CreateTime>%(time)d</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[%(content)s]]></Content>
    <MsgId>$(id)s</MsgId>
</xml>
'''


def post(url, data):
    request = urllib2.Request(url, data)
    request.add_header("Content-Type", "text/xml")
    response = urllib2.urlopen(request)
    return response.read()


def send():
    s = e.get().encode('utf-8') #fix chinese commands input
    
    if s:
        t.insert(tk.END, settings["me_display_name"]+"\n", "send_name")
        t.insert(tk.END, s+"\n", "send_content")

        msg = {
            "to": settings["ToUserName"],
            "from": settings["FromUserName"],
            "time": time.time(),
            "content": s,
            "id": str(random.random())[-10:],
        }

        qs = "?signature=%s&timestamp=%s&nonce=%s" % \
            mix(int(msg["time"]), msg["id"])
        receive(msg["time"], post(settings["url"]+qs, template % msg))


def receive(start, response):
    if time.time() - start > 4.95:
        return

    et = ET.fromstring(response)
    print "Received:\n%s\n" % response

    c = unicode(et.find("Content").text)

    t.insert(tk.END, settings["mp_display_name"]+"\n", "receive_name")
    t.insert(tk.END, c+"\n", "receive_content")


def mix(time, salt):
    timestamp = str(time)
    nonce = str(time + int(salt[-6:]))

    l = [timestamp, nonce, settings["token"]]
    l.sort()
    signature = hashlib.sha1("".join(l)).hexdigest()

    return (signature, timestamp, nonce)


def follow():
    msg = {
        "to": settings["ToUserName"],
        "from": settings["FromUserName"],
        "time": time.time(),
        "content": "Hello2BizUser",
        "id": str(random.random())[-10:],
    }
    qs = "?signature=%s&timestamp=%s&nonce=%s" % \
        mix(int(msg["time"]), msg["id"])
    receive(msg["time"], post(settings["url"]+qs, template % msg))


top = tk.Tk()
top.title("微信模拟器")

t = st.ScrolledText(top, width=40)
t.pack()

t.tag_add("send_name", "1.0", "1.end")
t.tag_config("send_name", font=("Arial", "10", "bold"),
            justify=tk.RIGHT, rmargin=6)
t.tag_add("send_content", "2.0", "2.end")
t.tag_config("send_content", spacing3=10, justify=tk.RIGHT, rmargin=6)

t.tag_add("receive_name", "1.0", "1.end")
t.tag_config("receive_name", font=("Arial", "10", "bold"), lmargin1=2)
t.tag_add("receive_content", "2.0", "2.end")
t.tag_config("receive_content", spacing3=10, lmargin1=2)

e = tk.Entry(top)
e.pack(side=tk.LEFT)

b = tk.Button(top, text="发送", command=send)
b.pack(side=tk.LEFT)

a = tk.Button(top, text="关注公众帐号", command=follow)
a.pack(side=tk.RIGHT)

if __name__ == "__main__":
    top.mainloop()
