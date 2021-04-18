#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
@File : telebot.py
@Time : 2020/6/19
@Author : hackhub
@Version : 0.0.1
@Contact : hackhub.me@gmail.com
@License : (C)Copyright 2020, HACKHUB-ME
@Desc : None
'''

import requests
from pyrogram import Client, Filters
import json


button = False
api_id = ""
api_hash = ""
account_id = #

if (api_id == "" or api_hash == ""):
    api_id = int(input("api_id: "))
    api_hash = input("api_hash: ")


# app = Client("my_account", api_id, api_hash, proxy={"hostname":"127.0.0.1","port":1080})
app = Client("my_account", api_id, api_hash)
@app.on_message(Filters.reply | Filters.me)
def my_handler(client, message):
    message_dict = json.loads(str(message))
    global button
    flag = False
    need_reply = False
    try:
        is_bot = message_dict["from_user"]["is_bot"]
        if not is_bot:
            if "reply_to_message" in message_dict:
                reply_user_id = message_dict["reply_to_message"]["from_user"]["id"]
                if int(reply_user_id) == account_id:
                    flag = True
                    need_reply = True
            elif int(message_dict["from_user"]["id"]) == account_id:
                flag = True
                need_reply = False
            if flag:
                chat_id = message_dict["chat"]["id"]
                if "text" in message_dict:
                    message_text = message_dict["text"]
                    if "开启祖安语录" in message_dict["text"]:
                        button = True
                        app.send_message(chat_id, "祖安语录已经开启")
                        print("祖安语录开启")
                    elif "关闭祖安语录" in message_dict["text"]:
                        button = False
                        print("祖安语录关闭")
                        app.send_message(chat_id, "祖安语录已经关闭")
                    elif "帮助" in message_dict["text"]:
                        app.send_message(chat_id, "支持命令'开启祖安语录'和'关闭祖安语录'，当前状态：{}".format(button))
                    zuan = "祖安语录"
                    if button:
                        if zuan not in message_text:
                            zuan_content = reply()
                            print(zuan_content)
                            reply_msg = "祖安语录：{}".format(zuan_content)
                            if need_reply:
                                app.send_message(chat_id, reply_msg, reply_to_message_id=message.message_id)
                            else:
                                app.send_message(chat_id, reply_msg)
    except Exception as msg:
        print(msg)


def reply(api_url="https://nmsl.shadiao.app/api.php?level=min&lang=zh_cn", timeout=3, my_proxies=None, reconnect_times=3):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"}
    try:
        response = requests.get(url=api_url, headers=headers, proxies=my_proxies, timeout=timeout)
        connected = True
    except ConnectionError:
        connected = False
    for reconnect_time in range(reconnect_times):
        if not connected:
            try:
                response = requests.get(url=api_url, headers=headers, proxies=my_proxies, timeout=timeout)
            except ConnectionError:
                pass
        else:
            break
    if connected:
        try:
            return response.text
        except Exception:
            print(response)
    else:
        raise ConnectionError


if __name__ == "__main__":
    print("开始监听")
    app.start()
    print("结束监听")
