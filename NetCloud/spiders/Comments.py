# -*- coding: utf-8 -*-

import scrapy
import json
import os
import base64
from Crypto.Cipher import AES



class CommentsSpider(scrapy.Spider):
    name = 'Comments'
    allowed_domains = ['music.163.com']
    start_urls = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_7535?csrf_token='
    # 头部信息
    headers = {
        'Host': "music.163.com",
        'Accept-Language': "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        'Accept-Encoding': "gzip, deflate",
        'Content-Type': "application/x-www-form-urlencoded",
        'Connection': "keep-alive",
        'Referer': 'http://music.163.com/'
    }

    def __init__(self):
        pass

    def start_requests(self):
        self.get_song_comment()
        pass

    def parse(self, response):

        print(response)

        pass

    def createSecretKey(self, n):
        return (''.join(map(lambda xx:(hex(ord(xx))[2:]),os.urandom(n))))[0:16]

    def AES_encrypt(self, text, secKey):
        '''进行AES加密
        '''
        pad = 16 - len(text) % 16
        text = text + pad * chr(pad)
        encryptor = AES.new(secKey, 2, '0102030405060708')
        encrypt_text = encryptor.encrypt(text.encode())
        encrypt_text = base64.b64encode(encrypt_text)
        return encrypt_text

    def rsaEncrypt(self, text, pubKey, modulus):
        '''进行RSA加密
        '''
        text = text[::-1]
        rs = int(text.encode('hex'), 16) ** int(pubKey, 16) % int(modulus, 16)
        return format(rs, 'x').zfill(256)

    def encrypted_request(self, text):
        '''将明文text进行两次AES加密获得密文encText,
        因为secKey是在客户端上生成的，所以还需要对其进行RSA加密再传给服务端。
        '''
        pubKey = '010001'
        modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        nonce = '0CoJUm6Qyw8W8jud'

        text = json.dumps(text)
        secKey = self.createSecretKey(16)
        encText = self.AES_encrypt(self.AES_encrypt(text, nonce), secKey)
        encSecKey = self.rsaEncrypt(secKey, pubKey, modulus)
        data = {
            'params': encText,
            'encSecKey': encSecKey
        }
        return data

    def AES_encrypt(self, text, secKey):
        '''进行AES加密
        '''
        pad = 16 - len(text) % 16
        text = text + pad * chr(pad)
        encryptor = AES.new(secKey, 2, '0102030405060708')
        encrypt_text = encryptor.encrypt(text.encode())
        encrypt_text = base64.b64encode(encrypt_text)
        return encrypt_text

    def get_offset(self, offset=0):
        '''偏移量
        '''
        if offset == 0:
            text = {'rid': '', 'offset': '0', 'total': 'true', 'limit': '20', 'csrf_token': ''}
        else:
            text = {'rid': '', 'offset': '%s' % offset, 'total': 'false', 'limit': '20', 'csrf_token': ''}
        return text

    def get_json_data(self, url, offset):
        '''json 格式的评论
        '''
        text = self.get_offset(offset)
        data = self.encrypted_request(text)

        scrapy.Request(url=url, data=data, method='POST', callback=self.parse)
        pass

    def get_song_comment(self):
        self.get_json_data(self.start_urls, offset=0)
