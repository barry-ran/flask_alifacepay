# flask_alifacepay
支付宝当面付集成到flask中的简单demo

[支付宝当面付](https://blog.csdn.net/rankun1/article/details/92401295)支持个人申请，无需企业认证，可以参见[我的博客](https://blog.csdn.net/rankun1/article/details/92401295)有详细教程。

# 描述
基于[之前封装的支付宝当面付sdk](https://github.com/barry-ran/alifacepay)集成到flask中，这是一个简单的demo。

# 使用步骤
- 克隆项目到本地
- 安装requirements.txt所需依赖库
- 使用pycharm打开源码目录
- 配置app.py中app_id，alipay_public_key，app_private_key，ontify_url为你自己的
- 运行app.py即可

注意：ontify_url需要你有公网ip，没有的话可以使用[netapp](http://natappfree.cc/)实现内网穿透
# 效果图

![主页](https://raw.githubusercontent.com/barry-ran/flask_alifacepay/master/screenshots/主页.png)

![付款页面](https://raw.githubusercontent.com/barry-ran/flask_alifacepay/master/screenshots/付款页面.png)

![支付成功](https://raw.githubusercontent.com/barry-ran/flask_alifacepay/master/screenshots/支付成功.png)