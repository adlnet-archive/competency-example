import util
from util import performance, settings
from pymongo import MongoClient
from werkzeug.security import generate_password_hash

mongo = MongoClient()
db = mongo.compapp

def createuser(username="tom", pwd="1234", email="mailto:tomcreighton@example.com", name="tom creighton"):
	if db.users.find_one({"username":username}):
		print "user already existed... didn't make another one"
		return

	db.users.insert({"username":username, "pwd": generate_password_hash(pwd), "email":email, "name":name})

def main():
	util.parsePerformanceFwk()
	objuri = performance.getObjId(settings.PERFORMANCE_FWKS['tetris'])
	print "object uri from performance fwk: %s" % objuri
	createuser()
	import json

	performance.evaluateTetrisStatements(performance.getStatements(objuri, "tom"), settings.PERFORMANCE_FWKS['tetris'], "tom")

if __name__ == '__main__':
	main()