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


TPL_TEXT = '''
<xml>
    <ToUserName><![CDATA[%(to)s]]></ToUserName>
    <FromUserName><![CDATA[%(from)s]]></FromUserName>
    <CreateTime>%(time)d</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[%(content)s]]></Content>
    <MsgId>$(id)s</MsgId>
</xml>
'''

TPL_EVENT = '''
<xml>
    <ToUserName><![CDATA[%(to)s]]></ToUserName>
    <FromUserName><![CDATA[%(from)s]]></FromUserName>
    <CreateTime>%(time)d</CreateTime>
    <MsgType><![CDATA[event]]></MsgType>
    <Event><![CDATA[%(event)s]]></Event>
    <EventKey><![CDATA[%(key)s]]></EventKey>
</xml>'''


def post(qs, data):
    # Concatenate URL with query string
    url = settings["url"] + qs
    request = urllib2.Request(url, data)
    request.add_header("Content-Type", "text/xml")
    response = urllib2.urlopen(request)
    return response.read()


def send():
    s = e.get().encode('utf-8')     # Fix Chinese input.

    if not s:
        return

    # Simulation for clicking the menu.
    # Usage: EVENT_TYPE@EVENT_KEY
    #        'c@KEY_FIND'   - 'CLICK' event with 'KEY_FIND' as event key
    #        'v@www.qq.com' - 'VIEW' event with 'www.qq.com' as event key
    if s.startswith("c@") or s.startswith("v@"):
        event, key = s.split("@")
        msg = {
            "to": settings["ToUserName"],
            "from": settings["FromUserName"],
            "time": time.time(),
            "event": "CLICK" if event == "c" else "VIEW",
            "key": key
        }
        qs = "?signature=%s&timestamp=%s&nonce=%s" % \
            mix(int(msg["time"]))
        receive(msg["time"], post(qs, TPL_EVENT % msg))
    # Simulation for sending a message.
    else:
        t.insert(tk.END, settings["me_display_name"]+"\n", "send_name")
        t.insert(tk.END, s+"\n", "send_content")

        msg = {
            "to": settings["ToUserName"],
            "from": settings["FromUserName"],
            "time": time.time(),
            "content": s,
            "id": str(random.random())[-10:]
        }

        qs = "?signature=%s&timestamp=%s&nonce=%s" % \
            mix(int(msg["time"]))
        receive(msg["time"], post(qs, TPL_TEXT % msg))


def receive(start, response):
    if time.time() - start > 4.95:
        return

    if not response:
        print "No response."
        return

    print "Received:\n%s\n" % response.decode("utf-8")
    et = ET.fromstring(response)

    to = et.find("ToUserName").text.decode("utf-8")
    fr = et.find("FromUserName").text.decode("utf-8")

    type = et.find("MsgType").text.decode("utf-8")
    if type == u"text":
        c = unicode(et.find("Content").text)
    elif type == u"news":
        l = []
        for i in et.find("Articles").findall("item"):
            l.append(unicode(i.find("Title").text))
            l.append(unicode(i.find("Description").text))
            l.append(unicode(i.find("PicUrl").text))
            l.append(unicode(i.find("Url").text))
            l.append("---")
        c = u"\n".join(l)
    else:
        print "Unknown response."
        return

    t.insert(tk.END, settings["mp_display_name"]+"\n", "receive_name")
    t.insert(tk.END, c+"\n", "receive_content")
    t.yview_moveto(1.0)


def mix(time):
    timestamp = str(time)

    # I don't know how Weixin generate the 9-digit nonce, so I turn to random.
    nonce = str(int(random.random()))[-9:]

    l = [timestamp, nonce, settings["token"]]
    l.sort()
    signature = hashlib.sha1("".join(l)).hexdigest()

    return signature, timestamp, nonce


def follow():
    msg = {
        "to": settings["ToUserName"],
        "from": settings["FromUserName"],
        "time": time.time(),
        "event": "subscribe",
        "key": ""
    }
    qs = "?signature=%s&timestamp=%s&nonce=%s" % \
        mix(int(msg["time"]))
    receive(msg["time"], post(qs, TPL_EVENT % msg))


def unfollow():
    msg = {
        "to": settings["ToUserName"],
        "from": settings["FromUserName"],
        "time": time.time(),
        "event": "unsubscribe",
        "key": ""       # `EventKey` in `unsubscribe` event is empty.
    }
    qs = "?signature=%s&timestamp=%s&nonce=%s" % \
        mix(int(msg["time"]))
    receive(msg["time"], post(qs, TPL_EVENT % msg))


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

a = tk.Button(top, text="取消关注", command=unfollow)
a.pack(side=tk.RIGHT)

if __name__ == "__main__":
    top.mainloop()
