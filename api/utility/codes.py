def decode(stream: bytes) -> str:
    codes = ('utf8', 'cp936', 'gbk', 'gb2312')
    for code in codes:
        try:
            ret = stream.decode(code)
            return ret
        except Exception as e:
            _ = e
