#coding=utf-8
from SDK.CCPRestSDK import REST
import ConfigParser

accountSid = '8a216da85d158d1b015d3cf8221a1143'#'您的主账号'
# 说明：主账号，登陆云通讯网站后，可在控制台首页中看到开发者主账号ACCOUNT SID。

accountToken = '6400b3f90a914ecf8dcc533591507137' #'您的主账号Token'
# 说明：主账号Token，登陆云通讯网站后，可在控制台首页中看到开发者主账号AUTH TOKEN。

appId = '8a216da85d158d1b015d3cf823fb1149'#'您的应用ID'
# 请使用管理控制台中已创建应用的APPID。

serverIP = 'app.cloopen.com'
# 说明：请求地址，生产环境配置成app.cloopen.com。

serverPort = '8883'
# 说明：请求端口 ，生产环境为8883.

softVersion = '2013-12-26'  # 说明：REST API版本号保持不变。


# 发送模板短信
# @param to  必选参数     短信接收彿手机号码集合,用英文逗号分开
# @param datas 可选参数    内容数据
# @param tempId 必选参数    模板Id

def sendTemplateSMS(to, datas, tempId):
    # 初始化REST SDK
    rest = REST(serverIP, serverPort, softVersion)
    rest.setAccount(accountSid, accountToken)
    rest.setAppId(appId)

    result = rest.sendTemplateSMS(to, datas, tempId)
    for k, v in result.iteritems():
        if k == 'templateSMS':
            for k, s in v.iteritems():
                print '%s:%s' % (k, s)
        else:
            print '%s:%s' % (k, v)

#sendTemplateSMS(mobile, [mobile_code, 30], 1)