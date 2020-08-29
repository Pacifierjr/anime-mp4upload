from flask import Flask,Response,request,jsonify
from bs4 import BeautifulSoup as bs 
import requests
class mp4(object):
	def __init__(self,url):
		self.url=url.replace("embed-","").replace(".html","")
		html=requests.get(self.url).text
		self.soup=bs(html,'html.parser')
		self.fileName=self.soup.h2.text
		self.fileName=self.fileName.replace('Download File ','')
		self.size="SS"
	def press(self):
		params=dict()
		inputs=self.soup.find_all('input')
		for item in inputs:
			params.update({item['name']:item['value']})
		response=requests.post(self.url,data=params).text
		return response
	def file(self):
		soup=bs(self.press(),'html.parser')
		params=dict()
		inputs=soup.find_all('input')
		for item in inputs:
			params.update({item['name']:item['value']})
		response=requests.post(self.url,data=params,verify=False,allow_redirects=False).headers['Location']
		return {"url":response,"size":self.size,"filename":self.fileName}
app= Flask(__name__)
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
	ep=request.args.get('q')
	html=requests.get('https://vidstreaming.io/videos/'+ep).text
	url="https:"+bs(html,'html.parser').iframe['src']
	print(url)
	html=requests.get(url).text
	soup=bs(html,'html.parser')
	print(soup)
	mp4_embed=soup.find("li",text="Mp4upload")['data-video']
	s2=mp4(mp4_embed).file()['url']
	print (s2)
	return s2
