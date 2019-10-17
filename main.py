# -*- coding: utf-8 -*-
from crypter import SignatureUtils
import requests
import inspect
import random
import time
import simplejson

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
		postdata=simplejson.dumps(data,separators=(',', ':'))
		method=inspect.stack()[1][3].replace('_','.')
		if hasattr(self,'userId'):
			self.s.headers.update({'locale-name':'en-US','client-type':'Mobile','signin-userId':self.userId,'signin-authKey':self.authKey,'signin-authSeed':self.authSeed,'sign-code':self.crypter.GenerateRequestSignature(postdata,'%s%s'%(method,self.authSeed))})
		r=self.s.post(url,data=postdata,headers={'client-ver':self.client_ver,'server-method':method})
		if r.content[0]=='e':	return True
		try:
			data= simplejson.loads(r.content)
		except:
			self.log('no json..')
			return None
		if 'o' in data:
			self.userId=data['o']['s']['sd']['i']
			self.authKey=data['o']['s']['a']
			self.authSeed=data['o']['s']['s']
		return data

	def AuthenticateExtended(self,data=None):
		if data is not None:	return self.callAPI('https://raid-mauth.x-plarium.com/MobileAuth.ashx',data)
		return self.callAPI('https://raid-mauth.x-plarium.com/MobileAuth.ashx',{"o":{"ld":{"n":1,"c":2000},"d":{"l":[],"g":"cea273cd-c049-4665-9278-993fcaee6cac"},"dd":{"ot":1,"l":"en-GB","ov":self.ov,"d":self.vi,"dn":self.dn,"bn":"com.plarium.raidlegends","nm":1,"ai":self.ai,"vi":self.vi}},"a":27,"c":self.c,"l":"en-US","s":{"u":{}}})

	def SignIn(self):
		return self.callAPI('http://rdint1s12.plrm.zone/Raid/Segment12/segment.ashx',{"s":{"i":self.userId,"l":"en-US","a":0,"f":"","gi":0},"t":3,"c":{"i":2,"v":"10.2","ct":0,"n":"iPad Air 2","cn":"iPad5,4","a":"00000000-0000-0000-0000-000000000000","l":"en","f":"en-GB","c":"1.11.3","r":9917,"o":0,"x":2048,"y":1536,"dx":264,"dy":264,"cc":3,"pn":"arm64","gn":"Apple A8X GPU","gm":512,"dm":1988,"am":12677853184,"ab":0,"hde":0,"fps":0,"ui":[{"c":2000,"u":self.userId}],"dui":self.vi,"wsg":0,"nt":0,"ua":"Mozilla/5.0 (iPad; CPU OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Mobile/14C92","sn":30,"cg":2000},"b":"com.plarium.raidlegends","d":"10.2"})

	def UserAgreement_Accept(self):
		return self.callAPI('http://rdint1s12.plrm.zone/Raid/Segment12/segment.ashx',{"a":[1]})

	def register(self):
		d1= self.AuthenticateExtended()
		self.SignIn()
		return self.UserAgreement_Accept()
		#LogicErrorCode -16
		#ClusterGroup=d1['a'][0]['r']['u']
		#unk1=d1['a'][0]['r']['u']['g']
		#d2= self.AuthenticateExtended({"o":{"d":{"l":[unk1],"g":"cea273cd-c049-4665-9278-993fcaee6cac"},"dd":{"ot":1,"l":"en-GB","ov":"10.2","d":self.vi,"dn":"iPad5,4","bn":"com.plarium.raidlegends","nm":1,"ai":self.ai,"vi":self.vi}},"a":27,"c":self.c,"l":"en-US","s":{"u":{"2000":ClusterGroup},"c":2000}})
		#return d2
		
if __name__ == "__main__":
	a=API()
	print a.register()