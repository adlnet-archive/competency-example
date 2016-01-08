import bottle
from bottle import run, request, response, redirect, template
import json
import base64
import urllib
import requests
import util
from util import settings
from util import performance
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
def index():
	s = request.environ.get('beaker.session')
	username = s.get('username', None)

	return template('./templates/index', username=username, error=None)

@bottle.route('/all_comps', method='POST')
@bottle.get('/all_comps', method='GET')
def all_comps():
	s = request.environ.get('beaker.session')
	username = s.get('username',None)
	if not username:
		redirect('/')

	form_fwkurl = request.forms.get('frameworkurl', None)
	knownframeworkurls = set()

	if form_fwkurl:
		knownframeworkurls.add(form_fwkurl)
	for url in knownframeworkurls:
		util.getComp(url)

	return template('./templates/all_comps.tpl', fwks=util.getAllSystemComps(), username=username)

@bottle.get('/add-framework/<fwk>')
def add_framework(fwk):
	s = request.environ.get('beaker.session')
	username = s.get('username',None)
	if not username:
		redirect('/')

	to_add = fwk
	if to_add == "tetris":
		util.getComp("http://40.129.74.199:8080/competency-framework/xapi/tetris")
	elif to_add == "choosinganlms":
		util.getComp("http://40.129.74.199:8080/competency-framework/scorm/choosing-an-lms")
	elif to_add == "basicprogramming":
		util.getComp("http://40.129.74.199:8080/competency-framework/computer-science/basic-programming")

	return template('./templates/all_comps.tpl', fwks=util.getAllSystemComps(), username=username)

@bottle.get('/badges')
def badges():
	perfwk = db.perfwk.find_one({"entry":"http://40.129.74.199:8080/performance-framework/xapi/tetris"})
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
	my_badges = False

	if theid:
		c = util.getComp(theid, user=username)

		if theid == "http://40.129.74.199:8080/competency-framework/xapi/tetris":
			my_badges = True
		return template('./templates/comp', username=username, fwk=c, my_badges=my_badges)

	mycomps = util.getMyComps(username)
	return template('./templates/me', fwks=mycomps, username=username, error=None)

@bottle.route('/mybadges')
def my_badges():
	s = request.environ.get('beaker.session')
	username = s.get('username',None)
	if not username:
		redirect('/login')

	perfwk = db.perfwk.find_one({"entry":"http://40.129.74.199:8080/performance-framework/xapi/tetris"})
	levels = lines = scores = times = total = 0
	for component in perfwk["components"]:
		if component["id"] == "comp_levels":
			for pl in component["performancelevels"]:
				levels += 1
		elif component["id"] == "comp_lines":
			for pl in component["performancelevels"]:
				lines += 1
		elif component["id"] == "comp_scores":
			for pl in component["performancelevels"]:
				scores += 1
		else:
			for pl in component["performancelevels"]:
				times += 1
	total = levels + lines + scores + times


	performance.updatePerformance(settings.PERFORMANCE_FWKS["tetris"], username)
	comps = util.getComp("http://40.129.74.199:8080/competency-framework/xapi/tetris", username)

	my_levels = my_lines = my_scores = my_times = my_total = 0
	for competency in comps["competencies"]:
		if competency["title"] == "Experience API Tetris Level Competency":
			if 'performances' in competency:
				for perf in competency["performances"]:
					my_levels += 1
		elif competency["title"] == "Experience API Tetris Line Competency":
			if 'performances' in competency:
				for perf in competency["performances"]:
					my_lines += 1
		elif competency["title"] == "Experience API Tetris Score Competency":
			if 'performances' in competency:
				for perf in competency["performances"]:
					my_scores += 1
		else:
			if 'performances' in competency:
				for perf in competency["performances"]:
					my_times += 1
	my_total = my_levels + my_lines + my_scores + my_times

	return template('./templates/mybadges', comps=comps, total=total, my_total=my_total, levels=levels, lines=lines, scores=scores, times=times, my_levels=my_levels, my_lines=my_lines,
		my_scores=my_scores, my_times=my_times)

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

	my_badges = False
	if fwkid == "http://40.129.74.199:8080/competency-framework/xapi/tetris":
		my_badges = True

	return template('./templates/comp', username=username, fwk=c, my_badges=my_badges)

@bottle.get('/test')
def gettest():
	s = request.environ.get('beaker.session')
	username = s.get('username',None)
	if not username:
		redirect('/login')

	fwkid = request.params.get('fwkid', None)
	theid = request.params.get('compid', None)
	print theid
	print fwkid
	if not theid and not fwkid:
		redirect('/')

	# because this is a demo, we pick with framework we can
	# do a LR lookup on
	if fwkid == 'http://40.129.74.199:8080/competency-framework/scorm/choosing-an-lms':
		user = db.users.find_one({"username":username})
		actor = {'mbox':user['email'], 'name':user['name']}
		urls = util.getContentURLsFromLR(theid)
		#endpoint = settings.LRS_STATEMENT_ENDPOINT
		#auth = settings.AUTHORIZATION
		if urls:
			return template('./templates/videolist.tpl', user=username, compid=theid, actor=json.dumps(actor), urls=urls)

	if theid == 'http://40.129.74.199:8080/competency/computer-science/understanding-variables':
		return template('./templates/understanding-variables.tpl', compid=theid, fwkid=fwkid, user=username)
	elif theid == 'http://40.129.74.199:8080/competency/computer-science/case-statements':
		return template('./templates/case-statements.tpl', compid=theid, fwkid=fwkid, user=username)
	elif theid == 'http://40.129.74.199:8080/competency/computer-science/if-else':
		return template('./templates/if-else.tpl', compid=theid, fwkid=fwkid, user=username)
	elif theid == 'http://40.129.74.199:8080/competency/computer-science/for-loop':
		return template('./templates/for-loop.tpl', compid=theid, fwkid=fwkid, user=username)
	elif theid == 'http://40.129.74.199:8080/competency/computer-science/while-loop':
		return template('./templates/while-loop.tpl', compid=theid, fwkid=fwkid, user=username)
	elif theid == 'http://40.129.74.199:8080/competency/computer-science/understanding-functions':
		return template('./templates/understanding-functions.tpl', compid=theid, fwkid=fwkid, user=username)

	return template('./templates/test.tpl', compid=theid, fwkid=fwkid, user=username)

@bottle.post('/test')
def posttest():
	fwkid = request.forms.get('fwkid')
	theid = request.forms.get('compid')
	testname = request.params.get('testname')
	s = request.environ.get('beaker.session')
	username = s.get('username',None)
	if not username:
		redirect('/login')

	user = db.users.find_one({"username":username})
	if not user:
		redirect('/login')


	actor = {'mbox':user['email'], 'name':user['name']}
	questions = []
	answers = []
	types = []
	responses = []

	for x in range(1,6):
		questions.append(request.forms.get('questionasked' + str(x)))
		answers.append(request.forms.get('answer' + str(x)))
		types.append(request.forms.get('type' + str(x)))
		responses.append(request.forms.get('question' + str(x)))

	test_name = 'activity:%s_quiz' % testname
	display_name = urllib.unquote_plus(testname) + ' quiz'

	wrong, data = util.get_result_statements(responses, answers, types, questions, actor, test_name, display_name, fwkid, theid)
	post_resp = requests.post(settings.LRS_STATEMENT_ENDPOINT, data=json.dumps(data), headers=settings.HEADERS, verify=False)
	status = post_resp.status_code
	content = post_resp.content

   	stmt_results = util.retrieve_statements(status, content, theid, actor)

	achieved = False
	latest_attempt = stmt_results[0]

	if latest_attempt["verb"]["id"] == "http://adlnet.gov/expapi/verbs/passed":
		achieved = True

	if achieved:
		util.setAchievement(theid, username)

	return template('./templates/results', theid=theid, passed=achieved)

@bottle.get('/admin/reset')
def reset():
	s = request.environ.get('beaker.session')
	s.invalidate()
	mongo.drop_database(db)
	util.parsePerformanceFwk()
	redirect('/')

@bottle.get('/admin')
def reset():
	return template('./templates/admin.tpl')


if __name__ == '__main__':
	util.parsePerformanceFwk()
	run(app, host='0.0.0.0', port=8888, server='gunicorn')
