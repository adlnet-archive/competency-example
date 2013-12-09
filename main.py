import bottle
from bottle import run, request, response, redirect, template
import json
import datetime
import base64
import requests
import urllib
import xml.etree.ElementTree as ET
import os
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

namespaces = {'cf': 'http://ns.medbiq.org/competencyframework/v1/',
			  'lom': 'http://ltsc.ieee.org/xsd/LOM'}

knownframeworkurls = set(['http://adlnet.gov/competency-framework/computer-science/basic-programming'])

@bottle.route('/', method='GET')
@bottle.route('/', method='POST')
def index():
	s = request.environ.get('beaker.session')
	# for uri in knownuris:
	# fwks = []
	form_fwkurl = request.forms.get('frameworkurl', None)
	if form_fwkurl:
		knownframeworkurls.add(form_fwkurl)
	for url in knownframeworkurls:
		getComp(url)

	return template('./templates/index', fwks=getComps(), username=s.get('username', None), error=None)

@bottle.route('/js/<filename:re:.*\.js>')
def send_js(filename):
    return static_file(filename, root='./js', mimetype='text/javascript')

@bottle.route('/me')
def me():
	s = request.environ.get('beaker.session')
	username = s.get('username',None)
	if not username: 
		redirect('/login')
	theid = request.params.get('uri', None)
	if theid:
		c = getComp(theid, user=username)
		return template('./templates/comp', username=username, fwk=c)

	mycomps = getmycomps(username)
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
	
	c = getComp(fwkid, user=username)
	updateCompFwkStatus(username, c, endpoint+"statements", auth)

	c = getComp(fwkid, user=username)

	return template('./templates/comp', username=username, fwk=c)

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
		return template('./templates/login', error="username or password was missing")
	users = db.users
	user = users.find_one({"username":username})
	if user:
		if not check_password_hash(user['pwd'], pwd):
			return template('./templates/login', error="Username exists and password didn't match")
	else:
		email = request.forms.get('email', None)
		name = request.forms.get('name', None)
		if not email or not name:
			return template('./templates/login', error="email or name was missing")
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
	redirect('/login')

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
	# i would expect some sort of recommender to figure out what to deliver
	# for demonstration purposes, we either deliver video or a simple default 'test' page
	if fwkid == 'http://adlnet.gov/competency-framework/scorm/choosing-an-lms':
		user = db.users.find_one({"username":username})
		actor = {'mbox':user['email'], 'name':user['name']}
		user = db.users.find_one({"username":username})
		return template('./templates/demo_video.tpl', compid=theid, fwkid=fwkid, user=username, actor=json.dumps(actor), vidurl=settings.DEMO_VIDEOS[theid], email=user['email'])
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
		
		setAchievement(theid, username)

	return "<p> ok %s</p><p>Your progress has been recorded. <a href='/me'>Back to list</a>" % theid

@bottle.get('/admin/reset')
def reset():
	s = request.environ.get('beaker.session')
	s.invalidate()
	mongo.drop_database(db)

def getmycomps(username):
	# get my comps from db.usercomps
	cursor = db.usercomps.find({"username":username}, {"_id":0})
	return [c for c in cursor]


# same comp could be in more than
# one place in this competency framework

# NOTE!! this system works right now because we only call this 
# after submitting an achieved statement.. if we break up getting 
# achieved statements, we will need to wipe out the statements in 
# the lrs to redemo
def setAchievement(theid, username, single=None):
	if single:
		comps = [single]
	else:
		comps = getUsersComps(username)

	for comp in comps:
		if comp['entry'] == theid:
			comp['met'] = True
			comp['date'] = datetime.datetime.utcnow()
		
		# look through the whole framework for multiple
		# references to the same competency
		if comp.get('competencies', False):
			for c in comp['competencies']:
				setAchievement(theid, username, c)
		
		if rollup(comp):
			comp['met'] = True
			comp['date'] = datetime.datetime.utcnow()
		# only update if this is a root competency framework
		# single means it was called as a competency, not a root framework
		if not single:
			updateComp(comp, username)

def setAchievements(fwkcomp, ids, username, subfwk=False):
	for comp in fwkcomp['competencies']:
		if comp['entry'] in ids:
			comp['met'] = True
			comp['date'] = datetime.datetime.utcnow()

		if comp.get('competencies', False):
			for c in comp['competencies']:
				setAchievements(comp, ids, username, True)

		if rollup(comp):
			comp['met'] = True
			comp['date'] = datetime.datetime.utcnow()

	if not subfwk:
		if rollup(fwkcomp):
			fwkcomp['met'] = True
			fwkcomp['date'] = datetime.datetime.utcnow()
		updateComp(fwkcomp, username)

def rollup(comp):
	res = True
	if comp.get('competencies', False):
		for c in comp['competencies']:
			res = res & rollup(c)
	else:
		res = comp.get('met', False)
	return res

def getUserCompsById(theid, username):
	mapfunc = """
	function(){
	  function dfs(node){
		  //emit(node.url, node.my_id)
		  if (node.entry === "%s") {
			return true;
		  }
		  else {
			for(var i in node.competencies) {
			  if (dfs(node.competencies[i])) {
				return true;
			  }
			}
		  }
		  return false;
	  }
	  if (this.username === "%s" && dfs(this)) {
		emit(this._id, this)
	  }
	}
	""" % (theid, username)
	#function(key, values){return JSON.stringify(values);}
	reducefunc = """
	function(key, values){return values;}
	"""

	result = db.usercomps.map_reduce(mapfunc, reducefunc, "myresults")
	return [d['value'] for d in result.find()]

def getComps():
	return db.compfwk.find(fields={'_id': False})

#workin on it
def updateCompFwkStatus(username, fwk, endpoint, auth):
	headers = {        
	            'Authorization': auth,
	            'content-type': 'application/json',        
	            'X-Experience-API-Version': '1.0.0'
	    		}

	# if framework comp ['met'] is true: return... everything is already met
	if fwk.get('met', False):
		return
	# request achieved with fwk uri and related activities
	mbox = db.users.find_one({"username":username})['email']
	actor = urllib.quote_plus(json.dumps({'mbox':mbox}))
	query_string = '?agent={0}&verb={1}&activity={2}&related_activities={3}'
	achievedverb = 'http://adlnet.gov/expapi/verbs/achieved'
	fwkentry = fwk['encodedentry']
	achievedquery = query_string.format(actor,achievedverb, fwkentry, 'true')

	get_resp = requests.get(endpoint + achievedquery , headers=headers, verify=False)
	if get_resp.status_code != 200:
		return
	achieved_ids = [s['object']['id'] for s in json.loads(get_resp.content)['statements']]
	# for each competency see if there is an id in the achieved array of statements that matches
	setAchievements(fwk, achieved_ids, username)

	updateCompetency(fwk, username, actor, headers, endpoint)

# now we wanna find 'passed' statements for each competency
def updateCompetency(fwkcomp, username, actor, headers, endpoint, subfwk=False):
	query_string = '?agent={0}&verb={1}&activity={2}&related_activities={3}'
	passedverb = 'http://adlnet.gov/expapi/verbs/passed'

	for comp in fwkcomp['competencies']:
		if comp.get('met', False):
			continue

		if comp.get('competencies', False):
			updateCompetency(comp, username, actor, headers, endpoint, True)
			if rollup(comp):
				comp['met'] = True
				comp['date'] = datetime.datetime.utcnow()	

		compentry = comp['encodedentry']
		passedquery = query_string.format(actor,passedverb, compentry, 'true')

		get_resp = requests.get(endpoint + passedquery , headers=headers, verify=False)
		if get_resp.status_code != 200:
			return

		if json.loads(get_resp.content).get('statements', False):
			comp['met'] = True
			comp['date'] = datetime.datetime.utcnow()

	# after all of that, do rollup.. see if all competencies in a framework are met, if so set fwk met
	if not subfwk:
		if rollup(fwkcomp):
			fwkcomp['met'] = True
			fwkcomp['date'] = datetime.datetime.utcnow()
		updateComp(fwkcomp, username)

def getUsersComps(username):
	return db.usercomps.find({"username":username})	

def getComp(compuri, user=None):
	if user:
		mycomp = db.usercomps.find_one({"username":user, "entry":compuri}, {"_id":0})
		if mycomp:
			return mycomp
		else:
			comp = getComp(compuri)
			saveComp(comp, user)
			return comp
	
	fixed = compuri if not compuri.endswith('.xml') else compuri[:-4]
	comp = db.compfwk.find_one({"entry":compuri}, {"_id":0})
	if comp:
		return comp

	comp = parsecompetencies(compuri)

	saveComp(comp)
	return comp

def saveComp(comp, user=None):
	if user:
		comp['username'] = user
		db.usercomps.insert(comp)
	else:
		db.compfwk.insert(comp)

def updateComp(comp, username=None):
	if username:
		db.usercomps.update({"username":comp['username'], "entry":comp['entry']}, comp)
	else:
		db.compfwk.update({"entry":comp['entry']}, comp)

def parsecompetencies(uri):
	# cuz our xml is hosted with .xml right now
	uri = tempfix(uri)
	competencies = []
	res = requests.get(uri).text
	fmwkxml = ET.fromstring(res)

	competencies = parse(fmwkxml)
	return competencies

def parse(xmlbit):
	obj = {}
	obj['type'] = 'framework' if 'CompetencyFramework' in xmlbit.tag else 'competency'
	obj['catalog'] = getcatalog(xmlbit)
	obj['entry'] = getentry(xmlbit)
	obj['encodedentry'] = urllib.quote_plus(getentry(xmlbit))
	obj['title'] = gettitle(xmlbit)
	obj['description'] = getdescription(xmlbit)
	obj['date'] = datetime.datetime.utcnow()
	for include in xmlbit.findall('cf:Includes', namespaces=namespaces):
		if not obj.get('competencies', False):
			obj['competencies'] = []
		url = tempfix(include.find('cf:Entry', namespaces=namespaces).text)
		nxt = ET.fromstring(requests.get(url).text)
		c = parse(nxt)
		obj['competencies'].append(c)
	return structure(xmlbit, obj)

def structure(fmwk, root):
	if not root.get('competencies', False):
		return root
	# keys = root['competencies'].keys()
	# if no relations, return comps
	for relation in fmwk.findall('cf:Relation', namespaces=namespaces):
	# else look at fmwk relations
	# for each Relation
	#     get Reference1 object from comps, set Relationship attr to Reference2 entry
		ref1 = relation.find('cf:Reference1/cf:Entry', namespaces=namespaces).text
		rel = relation.find('cf:Relationship', namespaces=namespaces).text
		rel = rel[rel.rfind('#') + 1:]
		ref2 = relation.find('cf:Reference2/cf:Entry', namespaces=namespaces).text
		# if i'm referencing the framework as a relation... i can't do it here
		if ref1 == root['entry']:
			if not root.get(rel, False):
				root[rel] = []
			root[rel].append(ref2)
		else:
			for comp in root['competencies']:
				if ref1 == comp['entry']:
					if not comp.get(rel, False):
						comp[rel] = []
					comp[rel].append(ref2)
	return root

def tempfix(url):
	if url.endswith('.xml'):
		return url
	return url + ".xml"

def getcatalog(xml):
	return xml.find('lom:lom/lom:general/lom:identifier/lom:catalog', namespaces=namespaces).text

def getentry(xml):
	return xml.find('lom:lom/lom:general/lom:identifier/lom:entry', namespaces=namespaces).text

def gettitle(xml):
	return xml.find('lom:lom/lom:general/lom:title/lom:string[@language="en"]', namespaces=namespaces).text

def getdescription(xml):
	return xml.find('lom:lom/lom:general/lom:description/lom:string[@language="en"]', namespaces=namespaces).text

run(app, host='localhost', port=8888, reloader=True)