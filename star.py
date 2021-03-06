#encoding:utf-8
import urllib2,cookielib,urllib,json,sys,time,re,threading,random
from  opener import getOpener


def queryUrl(url):
        opener=getOpener()
        cnt=0
        while True:
		cnt+=1
                try:
                        request=opener.open(url,timeout=2)
                        break
                except:
			if cnt>10:
				cnt=0
				opener=getOpener()
	print '\rdone in '+str(cnt)+' request(s)'
        html=request.read()
        html=html.replace('\n',' ')
	return html


class timer(threading.Thread):
	url=""
	res=[]
	def __init__(self,url,res):
		threading.Thread.__init__(self)
		self.url=url
		self.res=res
	
	def run(self):	
		html=queryUrl(self.url)
		data=json.loads(html)
		for j in xrange(10):
			try:
				user=data['cards'][0]['card_group'][j]
				uid=user['user']['id']
				self.res.append(uid)
			except:
				pass

def getFollowers(containerId):
	user_url="http://m.weibo.cn/page/json?containerid="+containerId+"_-_FOLLOWERS"
	html=queryUrl(user_url)
	data=json.loads(html)
	formated=json.dumps(data,indent=4)
	count=data['count']
	page_count=(count-1)/10+1
	timers=[]
	res=[]
	for i in xrange(page_count):
		timers.append(timer(user_url+'&page='+str(i+1),res))
	for i in xrange(page_count):
		timers[i].setDaemon(True)
		timers[i].start()
	for i in xrange(page_count):
		timers[i].join()
	return res


def getUser(uid):
	user_url="http://m.weibo.cn/u/"+str(uid)
	html=queryUrl(user_url)
	config=re.findall(r'window.\$config=(.*?);',html)[0]
	render=re.findall(r'window.\$render_data =(.*?);',html)[0]
	config=config.replace(' ','')
	config=config.replace('\'','\"')
	render=render.replace(' ','')
	render=render.replace('\'','\"')
	config_decoded=json.loads(config)
	render_decoded=json.loads(render)
	containerId= render_decoded['common']['containerid']
	Id=render_decoded['stage']['page'][1]['id']
	description=render_decoded['stage']['page'][1]['description']
	nativePlace=render_decoded['stage']['page'][1]['nativePlace']
	name=render_decoded['stage']['page'][1]['name']
	gender=render_decoded['stage']['page'][1]['ta']
	dicts={}
	dicts['uid']=Id
	dicts['containerId']=containerId
	dicts['description']=description
	dicts['nativePlace']=nativePlace
	dicts['name']=name
	dicts['gender']=gender
	return dicts
	
if __name__=='__main__':
	uid='1660141095'
	containerId='1005051660141095'
	dicts=getUser(uid)
	res=getFollowers(dicts['containerId'])
	print res
	print len(res)



