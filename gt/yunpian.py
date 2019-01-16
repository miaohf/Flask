from yunpian_python_sdk.model import constant as YC
from yunpian_python_sdk.ypclient import YunpianClient
# 初始化client,apikey作为所有请求的默认值
clnt = YunpianClient('9930e55281443d213f58729a32db572a')
param = {YC.MOBILE:'13819063105',YC.TEXT:'【拓展时代】尊敬的承租户许跃伟，您所承租的（车站南路888号）房屋，根据合同约定应于2019年2月28日前支付租金23600元，请及时缴纳。详情咨询84111813。'}
r = clnt.sms().single_send(param)
# 获取返回结果, 返回码:r.code(),返回码描述:r.msg(),API结果:r.data(),其他说明:r.detail(),调用异常:r.exception()
# 短信:clnt.sms() 账户:clnt.user() 签名:clnt.sign() 模版:clnt.tpl() 语音:clnt.voice() 流量:clnt.flow()


