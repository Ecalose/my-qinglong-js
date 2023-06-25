"""

time: 2023.6.25
cron: 2 8 * * *
new Env('望潮');
地址：https://tzapp.taizhou.com.cn/webChannels/invite?inviteCode=BYFKC9&tenantId=64&accountId=6492edb1bf15a44961ee74b3
进入app-首页-阅读有礼，先点击右下角抽奖，绑定zfb号
！！！！！一定要先去绑定zfb号！！！！！
抓包域名: xmt.taizhou.com.cn/prod-api/user-read/app/login
抓包域名后面的: id和sessionId的值
环境变量名称：bd_wc = id=后面的值#sessionId=后面的值
注：用'#'号分开两个参数，顺序不要乱，先是id的值然后sessionId的值
多账号新建变量或者用 & 分开

"""

import lzma, base64import hashlib
import random
import string
import time
import requests
from os import environ,path
from functools import partial
from datetime import datetime
def load_send():
 global send
 cur_path=path.abspath(path.dirname(__file__))
 if path.exists(cur_path+"/SendNotify.py"):
  try:
   from SendNotify import send
   print("加载通知服务成功！")
  except Exception as e:
   send=False
   print(e)
   print('''加载通知服务失败~\n优惠流量卡：https://s.yam.com/6GOox''')
 else:
  send=False
  print('''加载通知服务失败~\n优惠流量卡：https://s.yam.com/6GOox''')
load_send()
def get_environ(key,default="",output=True):
 def no_read():
  if output:
   print(f"未填写环境变量 {key} 请添加")
  return default
 return environ.get(key)if environ.get(key)else no_read()
def generate_random_string(length):
 letters_and_digits=string.ascii_lowercase+string.digits
 return ''.join(random.choice(letters_and_digits)for i in range(length))
class Ghdy:
 def __init__(self,ck):
  self.account=ck[0]
  self.session=ck[1]
  self.id_dict={}
  self.JSESSIONID=''
  self.s_JSESSIONID=''
  self.msg=''
 def login(self):
  try:
   time.sleep(0.5)
   url="https://xmt.taizhou.com.cn/prod-api/user-read/app/login"
   headers={'Host':'xmt.taizhou.com.cn','Connection':'keep-alive','Pragma':'no-cache','Cache-Control':'no-cache','User-Agent':'Mozilla/5.0 (Linux; Android 11; Redmi Note 8 Pro Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.141 Mobile Safari/537.36;xsb_wangchao;xsb_wangchao;5.3.1;native_app','Accept':'*/*','X-Requested-With':'com.shangc.tiennews.taizhou','Sec-Fetch-Site':'same-origin','Sec-Fetch-Mode':'cors','Sec-Fetch-Dest':'empty','Referer':'https://xmt.taizhou.com.cn/readingAward/','Accept-Language':'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'}
   params={'id':self.account,'sessionId':self.session}
   r=requests.get(url,params=params,headers=headers)
   if '成功' in r.json()['msg']:
    xx=f'🚀登录成功：{r.json()["data"]["nickName"]}'
    self.msg+=xx+'\n'
    print(xx)
    jsessionid=r.cookies
    cookies_dict=jsessionid.get_dict()
    for k,y in cookies_dict.items():
     self.JSESSIONID=f'{k}={y}'
   elif '失败' in r.json()['msg']:
    xx=f'⛔️{r.json()["msg"]}'
    self.msg+=xx+'\n'
    print(xx)
  except Exception as e:
   print(e)
 def get_id(self):
  try:
   today=datetime.today().strftime('%Y%m%d')
   url=f'https://xmt.taizhou.com.cn/prod-api/user-read/list/{today}'
   headers={'Host':'xmt.taizhou.com.cn','Connection':'keep-alive','Pragma':'no-cache','Cache-Control':'no-cache','User-Agent':'Mozilla/5.0 (Linux; Android 11; Redmi Note 8 Pro Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.141 Mobile Safari/537.36;xsb_wangchao;xsb_wangchao;5.3.1;native_app','Accept':'*/*','X-Requested-With':'com.shangc.tiennews.taizhou','Sec-Fetch-Site':'same-origin','Sec-Fetch-Mode':'cors','Sec-Fetch-Dest':'empty','Referer':'https://xmt.taizhou.com.cn/readingAward/','Accept-Language':'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7','Cookie':self.JSESSIONID}
   r=requests.get(url,headers=headers)
   if '成功' in r.json()['msg']:
    r_list=r.json()['data']['articleIsReadList']
    id_dict={}
    for i in r_list:
     id_dict[i['id']]=i['newsId']
    self.id_dict=id_dict
    if self.id_dict:
     xx="✅文章加载成功"
     self.msg+=xx+'\n'
     print(xx)
   elif '重新' in r.json()['msg']:
    xx=f'⛔️文章加载失败：{r.json()["msg"]}'
    print(xx)
    self.msg+=xx+'\n'
   else:
    xx=f'⛔️请求异常：{r.json()["msg"]}'
    print(xx)
    self.msg+=xx+'\n'
  except Exception as e:
   print(e)
 def look(self):
  try:
   for idd,new_id in self.id_dict.items():
    a8=generate_random_string(8)
    b4=generate_random_string(4)
    c4=generate_random_string(4)
    d4=generate_random_string(4)
    e12=generate_random_string(12)
    request=f'{a8}-{b4}-{c4}-{d4}-{e12}'
    current_timestamp=int(time.time()*1000)
    sha=f'/api/article/detail&&{self.session}&&{request}&&{current_timestamp}&&FR*r!isE5W&&64'
    sha256=hashlib.sha256()
    sha256.update(sha.encode('utf-8'))
    signature=sha256.hexdigest()
    url='https://vapp.taizhou.com.cn/api/article/detail'
    headers={'X-SESSION-ID':self.session,'X-REQUEST-ID':f'{request}','X-TIMESTAMP':f'{current_timestamp}','X-SIGNATURE':f'{signature}','X-TENANT-ID':'64','User-Agent':'5.3.1;00000000-699e-0680-ffff-ffffc24c26a8;Xiaomi Redmi Note 8 Pro;Android;11;tencent','X-ACCOUNT-ID':self.session,'Cache-Control':'no-cache','Host':'vapp.taizhou.com.cn','Connection':'Keep-Alive','Accept-Encoding':'gzip'}
    params={'id':new_id}
    r=requests.get(url,params=params,headers=headers)
    if r.json()['message']=='success':
     xx=f'✅开始浏览《{r.json()["data"]["article"]["list_title"]}》'
     print(xx)
     self.msg+=xx+'\n'
     time.sleep(3)
     current_timestamp=int(time.time()*1000)
     sha=f'&&{idd}&&TlGFQAOlCIVxnKopQnW&&{current_timestamp}'
     md5=hashlib.md5()
     md5.update(sha.encode('utf-8'))
     signature=md5.hexdigest()
     headers={'Host':'xmt.taizhou.com.cn','Connection':'keep-alive','Pragma':'no-cache','Cache-Control':'no-cache','User-Agent':'Mozilla/5.0 (Linux; Android 11; Redmi Note 8 Pro Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.141 Mobile Safari/537.36;xsb_wangchao;xsb_wangchao;5.3.1;native_app','Accept':'*/*','X-Requested-With':'com.shangc.tiennews.taizhou','Sec-Fetch-Site':'same-origin','Sec-Fetch-Mode':'cors','Sec-Fetch-Dest':'empty','Referer':'https://xmt.taizhou.com.cn/readingAward/','Accept-Encoding':'gzip, deflate','Accept-Language':'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7','Cookie':self.JSESSIONID}
     params={'articid':idd,'timestamp':current_timestamp,'signature':signature}
     r=requests.get('https://xmt.taizhou.com.cn/prod-api/already-read/article',params=params,headers=headers)
     if '成功' in r.json()['msg']:
      xx=f'✅浏览完成'
      print(xx)
      self.msg+=xx+'\n'
     elif '重新' in r.json()['msg']:
      xx=f'⛔️浏览失败：{r.json()["msg"]}'
      print(xx)
      self.msg+=xx+'\n'
     else:
      xx=f'⛔️浏览异常：{r.json()["msg"]}'
      print(xx)
      self.msg+=xx+'\n'
    elif '不存在' in r.json()['msg']:
     xx=f'⛔️浏览失败：{r.json()["msg"]}'
     print(xx)
     self.msg+=xx+'\n'
    else:
     xx=f'⛔️浏览异常：{r.json()["msg"]}'
     print(xx)
     self.msg+=xx+'\n'
   c_headers={'Host':'xmt.taizhou.com.cn','Connection':'keep-alive','Pragma':'no-cache','Cache-Control':'no-cache','User-Agent':'Mozilla/5.0 (Linux; Android 11; Redmi Note 8 Pro Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.141 Mobile Safari/537.36;xsb_wangchao;xsb_wangchao;5.3.1;native_app','Accept':'*/*','X-Requested-With':'com.shangc.tiennews.taizhou','Sec-Fetch-Site':'same-origin','Sec-Fetch-Mode':'cors','Sec-Fetch-Dest':'empty','Referer':'https://xmt.taizhou.com.cn/readingAward/','Accept-Encoding':'gzip, deflate','Accept-Language':'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7','Cookie':self.JSESSIONID}
   today=datetime.today().strftime('%Y%m%d')
   c_r=requests.get(f'https://xmt.taizhou.com.cn/prod-api/user-read-count/count/{today}',headers=c_headers)
   if '成功' in c_r.json()['msg']:
    xx=f'✅全部浏览完成，准备开始抽红包吧！'
    print(xx)
    self.msg+=xx+'\n'
   else:
    xx=c_r.json()['msg']
    print(xx)
    self.msg+=xx+'\n'
  except Exception as e:
   print(e)
 def chou(self):
  try:
   c_headers={'Host':'srv-app.taizhou.com.cn','Connection':'keep-alive','Pragma':'no-cache','Cache-Control':'no-cache','User-Agent':'Mozilla/5.0 (Linux; Android 11; Redmi Note 8 Pro Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.141 Mobile Safari/537.36;xsb_wangchao;xsb_wangchao;5.3.1;native_app','Accept':'*/*','X-Requested-With':'com.shangc.tiennews.taizhou','Sec-Fetch-Site':'same-origin','Sec-Fetch-Mode':'cors','Sec-Fetch-Dest':'empty','Referer':'https://srv-app.taizhou.com.cn/luckdraw/','Accept-Encoding':'gzip, deflate','Accept-Language':'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7','Cookie':''}
   c_params={'accountId':self.account,'sessionId':self.session}
   c_r=requests.get('https://srv-app.taizhou.com.cn/tzrb/user/loginWC',params=c_params,headers=c_headers)
   jsessionid=c_r.cookies
   cookies_dict=jsessionid.get_dict()
   for k,y in cookies_dict.items():
    JSESSIONID=f'{k}={y}'
    self.s_JSESSIONID=JSESSIONID
   url='https://srv-app.taizhou.com.cn/tzrb/userAwardRecordUpgrade/save'
   headers={'Host':'srv-app.taizhou.com.cn','Connection':'keep-alive','Content-Length':'13','Pragma':'no-cache','Cache-Control':'no-cache','User-Agent':'Mozilla/5.0 (Linux; Android 11; Redmi Note 8 Pro Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.141 Mobile Safari/537.36;xsb_wangchao;xsb_wangchao;5.3.1;native_app','Content-type':'application/x-www-form-urlencoded','Accept':'*/*','Origin':'https://srv-app.taizhou.com.cn','X-Requested-With':'com.shangc.tiennews.taizhou','Sec-Fetch-Site':'same-origin','Sec-Fetch-Mode':'cors','Sec-Fetch-Dest':'empty','Referer':'https://srv-app.taizhou.com.cn/luckdraw/','Accept-Encoding':'gzip, deflate','Accept-Language':'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7','Cookie':self.s_JSESSIONID}
   data={'activityId':'67'}
   r=requests.post(url,headers=headers,data=data)
   if '成功' in r.json()['message']:
    xx=f'✅抽奖成功'
    print(xx)
    self.msg+=xx+'\n'
   elif '明天' in r.json()['message']:
    xx=f'❌{r.json()["message"]}'
    print(xx)
    self.msg+=xx+'\n'
   else:
    xx=f'⛔️{r.json()["message"]}'
    print(xx)
    self.msg+=xx+'\n'
   jl_headers={'Host':'srv-app.taizhou.com.cn','Connection':'keep-alive','Pragma':'no-cache','Cache-Control':'no-cache','User-Agent':'Mozilla/5.0 (Linux; Android 11; Redmi Note 8 Pro Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.141 Mobile Safari/537.36;xsb_wangchao;xsb_wangchao;5.3.1;native_app','Accept':'*/*','X-Requested-With':'com.shangc.tiennews.taizhou','Sec-Fetch-Site':'same-origin','Sec-Fetch-Mode':'cors','Sec-Fetch-Dest':'empty','Referer':'https://srv-app.taizhou.com.cn/luckdraw/','Accept-Encoding':'gzip, deflate','Accept-Language':'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7','Cookie':self.s_JSESSIONID}
   jl_params={'pageSize':'10','pageNum':'1','activityId':'67'}
   jl_r=requests.get('https://srv-app.taizhou.com.cn/tzrb/userAwardRecordUpgrade/pageList',params=jl_params,headers=jl_headers)
   if '成功' in jl_r.json()['message']:
    jl_list=jl_r.json()['data']['records']
    xx='🎁抽奖记录🎁'
    print(xx)
    self.msg+=xx+'\n'
    for i in jl_list:
     xx=f'⏰{i["createTime"]}: {i["awardName"]}'
     print(xx)
     self.msg+=xx+'\n'
    send("🔔望潮通知",self.msg)
   else:
    send("🔔望潮通知",self.msg)
  except Exception as e:
   print(e)
if __name__=='__main__':
 print=partial(print,flush=True)
 token=get_environ("bd_wc")
 cks=token.split("&")
 print("🔔检测到{}个ck记录\n🔔开始望潮任务".format(len(cks)))
 for ck_all in cks:
  ck=ck_all.split("#")
  run=Ghdy(ck)
  print()
  run.login()
  run.get_id()
  run.look()
  run.chou()
