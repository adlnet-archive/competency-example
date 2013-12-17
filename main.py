import bottle
from bottle import run, request, response, redirect, template
import json
import base64
import requests
import util
from util import settings
from pymongo import MongoClient
from beaker.middleware import SessionMiddleware
from werkzeug.security import generate_password_hash, check_password_hash
from bottle import static_file

session_opts = {
	'session.type': 'memory',
	'session.auto': True
}

app = SessionMiddleware(bottle.app(), session_opts)
 
mongo = MongoClient()
db = mongo.compapp

@bottle.route('/js/<filename:re:.*\.js>')
def send_js(filename):
    return static_file(filename, root='./js', mimetype='text/javascript')

@bottle.route('/static/badges/<filename>')
def server_static(filename):
    return static_file(filename, root='./static/badges')

@bottle.route('/', method='GET')
@bottle.route('/', method='POST')
def index():
	s = request.environ.get('beaker.session')
	form_fwkurl = request.forms.get('frameworkurl', None)
	
	if form_fwkurl:
		util.getComp(form_fwkurl)

	username = s.get('username', None)
	num_user_comps = len(util.getMyComps(username))
	return template('./templates/index', fwks=util.getAllSystemComps(), username=username, comps=num_user_comps, error=None)

@bottle.get('/badges')
def badges():
	perfwk = db.perfwk.find_one({"entry":"http://12.109.40.34/performance-framework/xapi/tetris"})
	if not perfwk:
		return template('./templates/badges', fwk={}, error="Tetris badges not found")

	return template('./templates/badges.tpl', fwk=perfwk, error="")

@bottle.get('/login')
def getlogin():
	s = request.environ.get('beaker.session')
	username = s.get('username',None)
	if username:
		redirect('/')
	return template('./templates/login', error=None)

@bottle.post('/login')
def postlogin():
	s = request.environ.get('beaker.session')
	username = request.forms.get('username', None)
	pwd = request.forms.get('password', None)
	
	if not username or not pwd:
		return template('./templates/login', error="Username or password was missing")
	
	users = db.users
	user = users.find_one({"username":username})
	
	if user:
		if not check_password_hash(user['pwd'], pwd):
			return template('./templates/login', error="Username exists and password didn't match")
	else:
		email = request.forms.get('email', None)
		name = request.forms.get('name', None)
		
		if not email or not name:
			return template('./templates/login', error="Email or name was missing")
		
		if not email.startswith("mailto:"):
			email = "mailto:%s" % email
		users.insert({"username":username, "pwd": generate_password_hash(pwd), 
					  "email":email, "name":name})
	s['username'] = username
	s.save()
	redirect('/')

@bottle.get('/logout')
def getlogout():
	s = request.environ.get('beaker.session')
	username = s.get('username',None)
	if username:
		s.invalidate()
	redirect('/')

@bottle.route('/me')
def me():
	s = request.environ.get('beaker.session')
	username = s.get('username',None)
	if not username: 
		redirect('/login')
	theid = request.params.get('uri', None)
	if theid:
		c = util.getComp(theid, user=username)
		return template('./templates/comp', username=username, fwk=c)

	mycomps = util.getMyComps(username)
	return template('./templates/me', fwks=mycomps, username=username, error=None)

@bottle.post('/update')
def updatecomp():
	s = request.environ.get('beaker.session')
	username = s.get('username',None)
	if not username: 
		redirect('/login')
	endpoint = request.forms.get('endpoint', None)
	auth = "Basic %s" % base64.b64encode("%s:%s" % (request.forms.get('name', None), request.forms.get('password', None)))
	fwkid = request.forms.get('fwkid', None)
	
	c = util.getComp(fwkid, user=username)
	util.updateCompFwkStatus(username, c, endpoint+"statements", auth)
	return template('./templates/comp', username=username, fwk=c)

@bottle.get('/test')
def gettest():
	s = request.environ.get('beaker.session')
	username = s.get('username',None)
	if not username:
		redirect('/login')
	fwkid = request.params.get('fwkid', None)
	theid = request.params.get('compid', None)
	if not theid and not fwkid:
		redirect('/')
	
	# because this is a demo, we pick with framework we can 
	# do a LR lookup on
	if fwkid == 'http://adlnet.gov/competency-framework/scorm/choosing-an-lms':
		user = db.users.find_one({"username":username})
		actor = {'mbox':user['email'], 'name':user['name']}
		urls = util.getContentURLsFromLR(theid)
		if urls:
			return template('./templates/videolist.tpl', user=username, compid=theid, actor=json.dumps(actor), urls=urls)
	return template('./templates/test.tpl', compid=theid, fwkid=fwkid, user=username)

@bottle.post('/test')
def posttest():
	fwkid = request.forms.get('fwkid')
	theid = request.forms.get('compid')
	s = request.environ.get('beaker.session')
	username = s.get('username',None)
	if not username:
		redirect('/login')

	user = db.users.find_one({"username":username})
	if not user:
		redirect('/login')

	actor = {'mbox':user['email'], 'name':user['name']}

	# here would be some sort of evaluation
	evaluated = request.forms.get('evaluated', False)
	
	if not evaluated:
		data = {
			'actor': actor,
			'verb': {'id': 'http://adlnet.gov/expapi/verbs/passed', 'display':{'en-US': 'passed'}},
			'object':{'id': 'some:activity_id_foo'},
			'context':{'contextActivities':{'other':[{'id':theid}]}}
			}
		post_resp = requests.post(settings.LRS_STATEMENT_ENDPOINT, data=json.dumps(data), headers=settings.HEADERS, verify=False)

	query_string = '?verb={0}&activity={1}&related_activities={2}'.format('http://adlnet.gov/expapi/verbs/passed', theid, 'true')
	get_resp = requests.get(settings.LRS_STATEMENT_ENDPOINT + query_string , headers=settings.HEADERS, verify=False)
	
	results = json.loads(get_resp.content)
	stmt_results = results['statements']

	achieved = False
	for stmt in stmt_results:
		if 'context' in stmt:
			if 'contextActivities' in stmt['context']:
				if 'other' in stmt['context']['contextActivities']:
					for acts in stmt['context']['contextActivities']['other']:
						if theid in acts['id']:
							achieved = True
							break

	if achieved:
		achieved_data = {
			'actor': {'mbox':user['email'], 'name':user['name']},
			'verb': {'id': 'http://adlnet.gov/expapi/verbs/achieved', 'display':{'en-US': 'achieved'}},
			'object':{'id': theid},
			'context':{'contextActivities':{'parent':[{'id':fwkid}]}}
			}	
		post_resp = requests.post(settings.LRS_STATEMENT_ENDPOINT, data=json.dumps(achieved_data), headers=settings.HEADERS, verify=False)
		util.setAchievement(theid, username)
	return "<p> ok %s</p><p>Your progress has been recorded. <a href='/me'>Back to list</a>" % theid

@bottle.get('/admin/reset')
def reset():
	s = request.environ.get('beaker.session')
	s.invalidate()
	mongo.drop_database(db)
	redirect('/')

if __name__ == '__main__':
	util.parsePerformanceFwk()
	util.getComp("http://12.109.40.34/competency-framework/xapi/tetris")
	run(app, host='localhost', port=8888, reloader=True)
