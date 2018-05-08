# api-demo

## Environment Variables

    FLASK_ENV [development|production] (default: production)
    FLASK_CONFIG [development|testing|production] (default: development)
    SERVER_NAME
    MYSQL_USER
    MYSQL_PASSWORD
    MYSQL_HOST (default: 127.0.0.1)
    MYSQL_PORT (default: 3306)
    MYSQL_DB
    CELERY_BROKER_USER
    CELERY_BROKER_PASSWORD
    CELERY_BROKER_HOST (default: 127.0.0.1)
    CELERY_BROKER_PORT (default: 5672)
    CELERY_BROKER_VHOST
    REDIS_HOST (default: 127.0.0.1)
    REDIS_PORT (default: 6379)
    REDIS_DB (default: 0)
    AES_KEY_SEED
    YP_API_KEY
    QN_ACCESS_KEY
    QN_SECRET_KEY
    QN_BUCKET
    QN_DOMAIN

## API Overview

**All data is sent and received as JSON.**

**success response**

    {
        code: 0
        message: 'Success'
        data: {
            <响应数据>
        }
    }

**error response**

    {
        code: <错误码>
        message: <错误信息>
        data: {}
    }

**错误码 & 错误信息**

    1000: 'Internal Server Error'  <- 服务端错误
    1100: 'Bad Request'  <- POST/PUT方法发送非JSON数据
    1101: 'Unauthorized'  <- login_required访问拦截
    1102: 'Unauthorized'
    1103: 'Forbidden'
    1104: 'Not Found'
    1201: 'url参数不完整'
    1202: 'url参数值错误'
    1203: 'json数据不完整'
    1204: 'json数据类型错误'
    1205: 'json数据值错误'
    1301: '用户名错误'
    1302: '密码错误'
    1303: '密码长度至少6位'

## Admin API References

### | 管理员相关

**管理员登录**

    PUT  /api/admin/login/

    必填JSON数据：
        username [string]: 用户名
        password [string]: 密码

    响应数据：
        token [string]: 身份令牌
        admin [object]: 管理员对象

    错误码：
        1203: 'json数据不完整'
        1204: 'json数据类型错误'
        1301: '用户名错误'
        1302: '密码错误'

**获取当前管理员详情**
_(login_required)_

    GET  /api/current_admin/

    响应数据：
        admin [object]: 管理员对象

**修改当前管理员密码**
_(login_required)_

    PUT  /api/current_admin/password/

    必填JSON数据：
        password [string]: 密码

    错误码：
        1203: 'json数据不完整'
        1204: 'json数据类型错误'
        1303: '密码长度至少6位'

## Admin Extensions

**获取七牛上传凭证**

    GET  /ext/qn/upload_token/

## Model References

**Admin 管理员**

    id [int]: 主键
    uuid [string]: UUID
    create_time [string]: 创建时间
    update_time [string]: 更新时间
    username [string]: 用户名
    mobile [string(null)]: 手机号码
    last_login_time [string(null)]: 最近登录时间
    last_login_ip [string(null)]: 最近登录IP
    auth [int]: 权限

## Model Dependencies

_- : null=False_

_* : null=True_

**Admin**
