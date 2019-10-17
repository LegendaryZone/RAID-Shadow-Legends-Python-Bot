# -*- coding: utf-8 -*-
from crypter import SignatureUtils
import requests
import inspect
import random
import time
import simplejson
import re

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
			self.s.headers.update({'locale-name':'en-US','client-type':'Mobile','signin-userId':self.userId,'signin-authKey':self.authKey,'signin-authSeed':self.authSeed,'sign-code':self.crypter.GenerateRequestSignature(postdata,'%s%s%s'%(method,self.userId,self.authKey))})
		if hasattr(self,'r'):
			self.log('old url:%s'%(url))
			segment=re.search('(Segment[0-9]*)',url).group(1)
			url=url.replace(segment,re.search('(Segment[0-9]*)',self.r).group(1))
			self.log('new url:%s'%(url))
		r=self.s.post(url,data=postdata,headers={'client-ver':self.client_ver,'server-method':method})
		self.log('status:%s len:%s'%(r.status_code,len(r.content)))
		if r.content[0]=='e':	return True
		try:
			data= simplejson.loads(r.content.split('!')[0])
		except:
			self.log('no json..')
			return None
		if 'o' in data:
			self.userId=data['o']['s']['sd']['i']
			self.log('hello %s'%(self.userId))
			self.authKey=data['o']['s']['a']
			self.authSeed=data['o']['s']['s']
		if 'l' in data:
			self.r=data['l']['r']
			self.log('found new url.. %s'%(self.r))
		return data

	def AuthenticateExtended(self,data=None):
		if data is not None:	return self.callAPI('https://raid-mauth.x-plarium.com/MobileAuth.ashx',data)
		return self.callAPI('https://raid-mauth.x-plarium.com/MobileAuth.ashx',{"o":{"ld":{"n":1,"c":2000},"d":{"l":[],"g":"cea273cd-c049-4665-9278-993fcaee6cac"},"dd":{"ot":1,"l":"en-GB","ov":self.ov,"d":self.vi,"dn":self.dn,"bn":"com.plarium.raidlegends","nm":1,"ai":self.ai,"vi":self.vi}},"a":27,"c":self.c,"l":"en-US","s":{"u":{}}})

	def SignIn(self):
		return self.callAPI('http://rdint1s09.plrm.zone/Raid/Segment09/segment.ashx',{"s":{"i":self.userId,"l":"en-US","a":0,"f":"","gi":0},"t":3,"c":{"i":2,"v":self.ov,"ct":0,"n":"iPad Air 2","cn":self.dn,"a":"00000000-0000-0000-0000-000000000000","l":"en","f":"en-GB","c":"1.11.3","r":9917,"o":0,"x":2048,"y":1536,"dx":264,"dy":264,"cc":3,"pn":"arm64","gn":"Apple A8X GPU","gm":512,"dm":1988,"am":11258171392,"ab":0,"hde":0,"fps":0,"ui":[{"c":2000,"u":self.userId}],"dui":"0BA85A01-7EA3-4561-B2B4-E7585DDFADE9","wsg":0,"nt":0,"ua":"Mozilla/5.0 (iPad; CPU OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Mobile/14C92","sn":30,"cg":2000},"b":"com.plarium.raidlegends","k":"73c9ec1cbaf89add940ecb3089a6a843","d":self.ov})

	def AutoRefresh(self):
		return self.callAPI('http://rdint1s09.plrm.zone/Raid/Segment09/segment.ashx',{"chat":{"s":0,"i":0,"r":["c.English.1"]},"r":180,"t":1571310796568,"q":[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127],"u":1571310783040,"g":13528,"j":0,"l":{"a":[],"h":[],"i":[],"e":[],"x":[],"t":{},"y":[],"b":[],"f":[],"d":[]},"e":{"t":-62135596800000}})

	def GetUserNotes(self,u):
		return self.callAPI('http://rdint1s09.plrm.zone/Raid/Segment09/segment.ashx',{"u":u})

	def UserAgreement_Accept(self):
		return self.callAPI('http://rdint1s12.plrm.zone/Raid/Segment12/segment.ashx',{"a":[1]})

	def login(self,userId,password):
		self.AuthenticateExtended({"o":{"d":{"l":[{"c":{"i":userId,"a":password}}],"g":"cea273cd-c049-4665-9278-993fcaee6cac"},"dd":{"ot":1,"l":"en-GB","ov":self.ov,"d":self.vi,"dn":self.dn,"bn":"com.plarium.raidlegends","nm":1,"ai":self.ai,"vi":self.vi}},"a":27,"c":self.c,"l":"en-US","s":{"u":{"2000":{"g":{"c":{"i":userId,"a":password}},"h":"534a66ab17182c2fd38947f12359963a","c":{"i":2000,"s":["rdint1s00.plrm.zone/Raid/Segment00","rdint1s01.plrm.zone/Raid/Segment01","rdint1s02.plrm.zone/Raid/Segment02","rdint1s03.plrm.zone/Raid/Segment03","rdint1s04.plrm.zone/Raid/Segment04","rdint1s05.plrm.zone/Raid/Segment05","rdint1s06.plrm.zone/Raid/Segment06","rdint1s07.plrm.zone/Raid/Segment07","rdint1s08.plrm.zone/Raid/Segment08","rdint1s09.plrm.zone/Raid/Segment09","rdint1s10.plrm.zone/Raid/Segment10","rdint1s11.plrm.zone/Raid/Segment11","rdint1s12.plrm.zone/Raid/Segment12","rdint1s13.plrm.zone/Raid/Segment13","rdint1s14.plrm.zone/Raid/Segment14"],"d":{"p":2,"l":"En","n":"Unknown"}}}},"c":2000}})
		self.SignIn()

	def register(self):
		d1= self.AuthenticateExtended()
		self.SignIn()
		return self.UserAgreement_Accept()
		#LogicErrorCode -16
		#ClusterGroup=d1['a'][0]['r']['u']
		#unk1=d1['a'][0]['r']['u']['g']
		#d2= self.AuthenticateExtended({"o":{"d":{"l":[unk1],"g":"cea273cd-c049-4665-9278-993fcaee6cac"},"dd":{"ot":1,"l":"en-GB","ov":self.ov,"d":self.vi,"dn":self.dn,"bn":"com.plarium.raidlegends","nm":1,"ai":self.ai,"vi":self.vi}},"a":27,"c":self.c,"l":"en-US","s":{"u":{"2000":ClusterGroup},"c":2000}})
		#return d2
		
if __name__ == "__main__":
	a=API()
	a.login(24621624,"iocKDnO5jUZbYMl-G4VWDYSTfZk1")