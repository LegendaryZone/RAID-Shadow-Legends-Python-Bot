# -*- coding: utf-8 -*-
from crypter import SignatureUtils
import requests
import json
import inspect
import random
import time
import ast

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class API(object):
	def __init__(self):
		self.s=requests.Session()
		self.s.verify=False
		self.s.headers.update({'Content-Type':'text/html','User-Agent':None})
		self.client_ver='1113'
		self.dn="iPad5,4"
		self.ov="10.2"
		self.ai="00000000-0000-0000-0000-000000000000"
		self.vi=self.rndDeviceId()
		self.c="1.11.3"
		self.s.proxies.update({'http': 'http://127.0.0.1:8888','https': 'https://127.0.0.1:8888',})
		self.crypter=SignatureUtils()

	def log(self,msg):
		print '[%s]%s'%(time.strftime('%H:%M:%S'),msg.encode('utf-8'))

	def rndHex(self,n):
		return ''.join([random.choice('0123456789ABCDEF') for x in range(n)])
	
	def rndDeviceId(self):
		s='%s-%s-%s-%s-%s'%(self.rndHex(8),self.rndHex(4),self.rndHex(4),self.rndHex(4),self.rndHex(12))
		return s

	def callAPI(self,url,data):
		postdata=json.dumps(data,separators=(',', ':')
		if hasattr(self,'userId'):
			self.s.headers.update({'locale-name':'en-US','client-type':'Mobile','signin-userId':self.userId,'signin-authKey':self.authKey,'signin-authSeed':self.authSeed,'sign-code':self.crypter.GenerateRequestSignature(postdata,'%s%s'%(inspect.stack()[1][3],self.authSeed))})
		r=self.s.post(url,data=postdata),headers={'client-ver':self.client_ver,'server-method':inspect.stack()[1][3]})
		data= ast.literal_eval(r.content)
		if 'o' in data:
			self.userId=data['o']['s']['sd']['i']
			self.authKey=data['o']['s']['a']
			self.authSeed=data['o']['s']['s']
		return data
		
	def AuthenticateExtended(self):
		return self.callAPI('https://raid-mauth.x-plarium.com/MobileAuth.ashx',{"o":{"ld":{"n":1,"c":2000},"d":{"l":[],"g":"cea273cd-c049-4665-9278-993fcaee6cac"},"dd":{"ot":1,"l":"en-GB","ov":self.ov,"d":self.vi,"dn":self.dn,"bn":"com.plarium.raidlegends","nm":1,"ai":self.ai,"vi":self.vi}},"a":27,"c":self.c,"l":"en-US","s":{"u":{}}})
		
	def register(self):
		return self.AuthenticateExtended()
		
if __name__ == "__main__":
	a=API()
	print a.register()