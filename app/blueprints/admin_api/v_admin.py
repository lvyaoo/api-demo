from flask import g

from . import bp_admin_api
from ...api_utils import *
from ...models import Admin


@bp_admin_api.route('/admin/login/', methods=['PUT'])
def login():
    """管理员登录"""
    username, password = map(g.json.get, ['username', 'password'])
    claim_args(1203, username, password)
    claim_args_str(1204, username, password)
    admin = Admin.get_by_username(username)
    claim_args_true(1301, admin)
    claim_args_true(1302, admin.check_password(password))

    admin.login(g.ip)
    data = {
        'token': admin.gen_token(),
        'admin': admin.to_dict()
    }
    return api_success_response(data)


@bp_admin_api.route('/current_admin/', methods=['GET'])
def get_current_admin():
    """获取当前管理员详情"""
    data = {
        'admin': g.admin.to_dict()
    }
    return api_success_response(data)


@bp_admin_api.route('/current_admin/password/', methods=['PUT'])
def update_current_admin_password():
    """修改当前管理员密码"""
    password = g.json.get('password')
    claim_args(1203, password)
    claim_args_str(1204, password)
    claim_args_true(1303, len(password) >= Admin.MIN_PW_LEN)

    g.admin.set_password(password)
    return api_success_response({})
