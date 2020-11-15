import os

BASE_DIRS = os.path.dirname(__file__)

# 参数
options = {
    'port': 8000,
}

# 配置
settings = {
    "static_path": os.path.join(BASE_DIRS, 'static'),
    "template_path": os.path.join(BASE_DIRS, 'templates'),
    # 安全cookie的秘钥,uuid base64加密获得  base64.b64encode(uuid.uuid4().bytes + uuid.uuid4.bytes)
    "cookie_secret": '2LBKQd6iTOWKBlPiyvXG+1aTW0PdDEHsmkb4s+Nzfcs=',
    "xsrf_cookies": False,  # True为开启同源保护
    "debug": True,
}
