import random
import string
from typing import Optional, Union


def to_bytes(bytes_or_str: Union[bytes, str]) -> bytes:
    """将字符串转换为bytes"""
    if isinstance(bytes_or_str, str):
        value = bytes_or_str.encode()
    else:
        value = bytes_or_str
    return value


def to_str(bytes_or_str: Union[bytes, str]) -> str:
    """将字符串转换为str"""
    if isinstance(bytes_or_str, bytes):
        value = bytes_or_str.decode()
    else:
        value = bytes_or_str
    return value


def nullable_strip(s: Optional[str]) -> Optional[str]:
    """移除字符串首尾的空格并返回，若结果为空字符串则返回None"""
    if s:
        value = s.strip() or None
    else:
        value = None
    return value


def gen_random_str(length: int, chars: str='uld', *, prefix: str='', suffix: str='') -> str:
    """生成随机字符串

    Args:
        length: 字符串总长度
        chars: 使用的字符种类：'u' - 大写字母，'l' - 小写字母，'d' - 数字
        prefix: 字符串前缀
        suffix: 字符串后缀
    """
    random_part_len = length - len(prefix + suffix)
    if random_part_len < 0:
        raise ValueError('Invalid length')
    population = ''
    if 'u' in chars:
        population += string.ascii_uppercase
    if 'l' in chars:
        population += string.ascii_lowercase
    if 'd' in chars:
        population += string.digits
    elements = random.choices(population, k=random_part_len)
    return prefix + ''.join(elements) + suffix
