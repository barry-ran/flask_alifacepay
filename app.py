from flask import Flask
from flask import render_template, request, Response
from alifacepay import AliFacePay
import threading
from threading import Lock

locks = {}
app = Flask(__name__)

# 基础信息配置
# 只需要三个关键信息 app_id，alipay_public_key，app_private_key
sandbox = True
if sandbox:
    app_id = '2016092900626816'
    alipay_public_key_string = open("G:/python/alipay_key/alipay_public_key_sandbox.txt").read()
else:
    app_id = '2019061665605123'
    alipay_public_key_string = open("G:/python/alipay_key/alipay_public_key.txt").read()

app_private_key_string = open("G:/python/alipay_key/app_private_key.pem").read()

ali_face_pay = AliFacePay(app_id, app_private_key_string, alipay_public_key_string,
                 'http://cfnxpg.natappfree.cc/alipay_nofity', sandbox)


@app.route('/')
def index():
    print('线程标识 ' + str(threading.currentThread().ident))
    return render_template('index.html')


@app.route('/create_trade')
def create_trade():
    out_trade_no = AliFacePay.gen_trade_no('yqhs')
    qr_code = ali_face_pay.precreate(out_trade_no, 1, "测试")

    # 为订单加锁
    l = Lock()
    l.acquire()
    locks[out_trade_no] = l

    return render_template('show_qrcode.html', qrcode_url=qr_code, out_trade_no=out_trade_no)


@app.route('/alipay_nofity', methods=['POST'])
def alipay_nofity():
    data = request.form.to_dict()
    if ali_face_pay.verify_params_sign(data):
        # 通知参数说明 https://docs.open.alipay.com/194/103296#s5
        notify_time = data['notify_time']           # 通知发出的时间
        notify_type = data['notify_type']           # 通知类型
        trade_status = data['trade_status']         # 订单状态
        out_trade_no = data['out_trade_no']         # 订单号
        buyer_logon_id = data['buyer_logon_id']     # 买家支付宝账号
        total_amount = data['total_amount']         # 订单金额
        subject = data['subject']                   # 订单标题

        # 异步通知默认只会收到TRADE_SUCCESS或者TRADE_FINISHED
        # 沙盒下测试居然收到了WAIT_BUYER_PAY，不过实际环境收不到
        if notify_type == 'trade_status_sync':
            print(trade_status)
            pay_success = False
            if trade_status == 'TRADE_SUCCESS' or trade_status == 'TRADE_FINISHED':
                pay_success = True
            if pay_success:
                # 支付成功解锁
                locks[out_trade_no].release()

        return Response('success')

    print('验证签名失败')
    return '404'


@app.route('/wait_pay')
def wait_pay():
    out_trade_no = request.args['out_trade_no']
    # 这里请求在支付成功之前都会阻塞
    locks[out_trade_no].acquire()
    # acquired!
    locks[out_trade_no].release()
    del locks[out_trade_no]
    return Response()


@app.route('/pay_success')
def pay_success():
    return render_template('pay_success.html')


if __name__ == '__main__':
    app.run()
