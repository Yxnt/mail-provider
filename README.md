# mail-provide
阿里云关闭了25和110 相关端口只能使用465访问发信服务器

使用方法
----

1. 克隆代码
```
git clone https://github.com/yxnt/mail-provide
virtualenv venv
venv/bin/pip install -r requirements.txt
```

2. 修改配置文件cfg.json
```
{
    "debug": true,
    "http": {
        "host": "0.0.0.0",
        "port": 4000,
        "token": "63113dd4-3943-4442-a7a2-f33fec994c77"
    },
    "smtp": {
        "addr": "smtp.exmail.qq.com",
        "port": 465,
        "username": "邮箱账号",
        "password": "密码",
        "from": "发信人"
    }
}
```

3. 修改alarm网关地址
```
{
    ...
    "api":{
        ...
        "mail":"http://127.0.0.1:4000/sender/mail/63113dd4-3943-4442-a7a2-f33fec994c77"
    }
    ...
}
```

4. DEBUG运行
```
venv/bin/python mail.py
```

**后台启动可自行使用gunicorn**