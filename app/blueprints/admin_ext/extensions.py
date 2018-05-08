from flask import jsonify

from . import bp_admin_ext
from ...models import Admin
from utils.service_util import qn_service


@bp_admin_ext.route('/data/init/', methods=['GET'])
def data_init():
    """数据初始化"""
    if Admin.select().count() == 0:
        Admin.new('admin', 'interval')
    return 'Success'


@bp_admin_ext.route('/qn/upload_token/', methods=['GET'])
def get_qn_upload_token():
    """获取七牛上传凭证"""
    data = {
        'uptoken': qn_service.gen_upload_token()
    }
    return jsonify(data)
