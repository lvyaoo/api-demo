from os import getenv
from typing import BinaryIO, Iterable, Optional, Union

import requests
from qiniu import Auth, put_data, put_file


class YPService:
    """云片"""
    def __init__(self, api_key: str):
        self.api_key = api_key

    def single_send(self, mobile: str, text: str) -> dict:
        """单条发送，返回云片响应数据

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
        """批量发送，返回云片响应数据

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

    def upload_data(self, key: str, data: Union[bytes, BinaryIO]) -> Optional[str]:
        """上传二进制流，上传成功则返回URL

        Args:
            key: 上传的文件名
            data: 上传的二进制流
        """
        up_token = self.gen_upload_token(key)
        ret, _ = put_data(up_token, key, data)
        if ret and ret.get('key') == key:
            url = 'http://{0}/{1}'.format(self.domain, key)
            return url

    def upload_file(self, key: str, file_path: str) -> Optional[str]:
        """上传文件，上传成功则返回URL

        Args:
            key: 上传的文件名
            file_path: 上传文件的路径
        """
        up_token = self.gen_upload_token(key)
        ret, _ = put_file(up_token, key, file_path)
        if ret and ret.get('key') == key:
            url = 'http://{0}/{1}'.format(self.domain, key)
            return url


yp_service = YPService(getenv('YP_API_KEY'))
qn_service = QNService(getenv('QN_ACCESS_KEY'), getenv('QN_SECRET_KEY'), getenv('QN_BUCKET'), getenv('QN_DOMAIN'))
