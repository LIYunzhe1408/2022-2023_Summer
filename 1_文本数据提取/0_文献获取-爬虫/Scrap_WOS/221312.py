import requests
requests.adapters.DEFAULT_RETRIES = 5 # 增加重连次数
s = requests.session()
s = requests.get("https://mail.163.com/")
print(s)
s.keep_alive = False # 关闭多余连接
