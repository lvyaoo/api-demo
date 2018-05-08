from os import getenv
from typing import Iterable

from qiniu import Auth
import requests


class YPService:
    """云片"""
    def __init__(self, api_key: str):
        self.api_key = api_key

    def single_send(self, mobile: str, text: str) -> dict:
        """单条发送

        Args:
            mobile: 手机号码
            text: 短信内容
        """
        data = {
            'apikey': self.api_key,
            'mobile': mobile,
            'text': text
        }
        resp = requests.post('https://sms.yunpian.com/v2/sms/single_send.json', data=data)
        return resp.json()

    def batch_send(self, mobiles: Iterable[str], text: str) -> dict:
        """批量发送

        Args:
            mobiles: 手机号码列表
            text: 短信内容
        """
        data = {
            'apikey': self.api_key,
            'mobile': ','.join(mobiles),
            'text': text
        }
        resp = requests.post('https://sms.yunpian.com/v2/sms/batch_send.json', data=data)
        return resp.json()


class QNService:
    """七牛"""
    def __init__(self, access_key: str, secret_key: str, bucket: str, domain: str):
        self.auth = Auth(access_key, secret_key)
        self.bucket = bucket
        self.domain = domain

    def gen_upload_token(self, key: str=None, expires: int=3600) -> str:
        """生成上传凭证

        Args:
            key: 上传的文件名
            expires: 上传凭证的过期时间（秒）
        """
        return self.auth.upload_token(self.bucket, key=key, expires=expires)


yp_service = YPService(getenv('YP_API_KEY'))
qn_service = QNService(getenv('QN_ACCESS_KEY'), getenv('QN_SECRET_KEY'), getenv('QN_BUCKET'), getenv('QN_DOMAIN'))
