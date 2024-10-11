### author by dean, 202409 , portunid team。
### 本工具这里实现了aes的加解密。
###
from Crypto.Cipher import AES
import base64

# 补位
pad = lambda s: s + chr(16 - len(s) % 16) * (16 - len(s) % 16)
# 除去补16字节的多余字符
unpad = lambda s: s[:-s[-1]]

defaultKey = 'dean@portunid123'  # 秘钥

# 加密函数
def aesECBEncrypt(data, key=defaultKey):   # ECB模式的加密函数，data为明文，key为16字节密钥
    key = key.encode('utf-8')
    data = pad(data)             # 补位
    data = data.encode('utf-8')
    aes = AES.new(key=key, mode=AES.MODE_ECB)  # 创建加密对象
    # encrypt AES加密  B64encode为base64转二进制编码
    result = base64.b64encode(aes.encrypt(data))
    return str(result, 'utf-8')        # 以字符串的形式返回


# 解密函数
def aesECBDecrypt(data, key=defaultKey):  # ECB模式的解密函数，data为密文，key为16字节密钥
    key = key.encode('utf-8')
    aes = AES.new(key=key, mode=AES.MODE_ECB)  # 创建解密对象

    # decrypt AES解密  B64decode为base64 转码
    result = aes.decrypt(base64.b64decode(data))
    result = unpad(result)  # 除去补16字节的多余字符
    return str(result, 'utf-8')  # 以字符串的形式返回


