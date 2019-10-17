# -*- coding: utf-8 -*-
from hashlib import md5

class SignatureUtils(object):
	def __init__(self):
		self.RequestSignaturePreSeed = "7ECC680B8F3942689BF505F04D339C4C"
		self.ResponseSignaturePreSeed = "CFED0D9E5D3248878D0FCD877B5A6CF0"

	def GenerateRequestSignature(self,data,seed):
		return md5(self.RequestSignaturePreSeed+data+seed).hexdigest()

	def md5(self,data):
		return md5(data).hexdigest()