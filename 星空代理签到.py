"""
星空代理 V1.00
注册地址：http://www.xkdaili.com/?ic=7d6acs0s
签到送IP

Author：Unknown
Updated: By Huansheng
const $ = new Env("星空代理签到");
cron: 10 00 * * *
"""
# 变量 export xingkong="账户1:密码&账户2:密码"
import os
import re
from notify import send

import requests

try:
    xingkong = os.environ["xingkong"]
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        # Requests sorts cookies= alphabetically
        # 'Cookie': 'ASP.NET_SessionId=23dfn2mafqhzkuuzosirclt1; Hm_lvt_d76458121a7604d3e55d998f66ef0be6=1659492634; dt_cookie_user_name_remember=DTcms=18729469208; Hm_lpvt_d76458121a7604d3e55d998f66ef0be6=1659493214',
        "DNT": "1",
        "Origin": "http://www.xkdaili.com",
        "Referer": "http://www.xkdaili.com/main/usercenter.aspx",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 Edg/103.0.1264.77",
        "X-Requested-With": "XMLHttpRequest",
    }
    # 用于拼接
    st = ""
    params = {
        "action": "user_receive_point",
    }
    # 按照空格分隔多个账户
    accounts = xingkong.split("&")
    for i in accounts:
        up = i.split(":")
        if len(up) == 2:
            data = {"username": up[0], "password": up[1], "remember": 1, "code": 0}
        else:
            print(f"{i} 配置有误，请检查")
            continue
        try:
            aa = requests.post(
                "http://www.xkdaili.com/tools/submit_ajax.ashx?action=user_login&site_id=1",
                headers=headers,
                data=data,
            )
            ck = aa.cookies
            asp = re.findall(r"ASP\.NET_SessionId=(\w+)", str(ck))
            dt = re.findall(r"dt_cookie_user_name_remember=(\w+=\w+)", str(ck))
            if len(dt) == 0:
                print("\n登录失败，请检查账号或密码，手动登录测试 或 不知何原因需要验证码导致无法登录，暂时无解")
                continue
            cookies = {
                "ASP.NET_SessionId": asp[0],
                # "dt_cookie_user_name_remember": dt[0],
                "dt_cookie_user_name_remember": "DTcms=" + up[0],
                "dt_cookie_user_pwd_remember": "DTcms=" + up[1],
            }

            data = {
                "type": "login",
            }

            response = requests.post(
                "http://www.xkdaili.com/tools/submit_ajax.ashx",
                params=params,
                headers=headers,
                data=data,
                verify=False,
                cookies=cookies,
            )
            txt = response.json()
            print("\n星空签到 ", txt["msg"])
            st += f"\n账户 {up[0]} 星空签到 {txt['msg']}"
        except Exception as e:
            print(f"\n账户 {up[0]} 星空签到异常 {str(e)}")
            st += f"\n账户 {up[0]} 星空签到异常 {str(e)}"
    # 执行完毕发送通知
    send("\n星空签到 ", f"{st}")
except Exception as e:
    print("\n星空签到失败,失败原因 ", str(e))
    if str(e) == "list index out of range":
        send("\n星空代理签到失败,失败原因 ", f"{str(e)}")
