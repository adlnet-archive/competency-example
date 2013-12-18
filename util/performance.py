import requests
import json
import urllib
from pymongo import MongoClient
from util import settings

mongo = MongoClient()
db = mongo.compapp

def updatePerformance(perfwkuri, username):
    # need to check competencies type
    objid = getObjId(perfwkuri)
    if not objid:
        return
    stms = getStatements(objid, username)

    # no generalized way to figure out performance values in statement, yet
    # for now... we hard coded what to look for if the statements are about tetris
    if perfwkuri == settings.PERFORMANCE_FWKS['tetris']:
        evaluateTetrisStatements(stms, perfwkuri, username)
    else:
        print "unknown performance uri: %s" % perfwkuri

def getObjId(perfwkuri):
    pf = db.perfwk.find_one({"entry":perfwkuri})
    for ref in pf['references']:
        if not ref.get('type', False):
            return ref.get('objecturi', None)

def getStatements(objuri, username):
    mbox = db.users.find_one({"username":username})['email']
    actor = urllib.quote_plus(json.dumps({'mbox':mbox}))
    query_string = '?agent={0}&verb={1}&activity={2}&related_activities={3}'
    # tetris doesn't use expapi
    finishedverb = 'http://adlnet.gov/xapi/verbs/completed'
    finishedquery = query_string.format(actor, finishedverb, objuri, 'true')

    endpoint = settings.LRS_STATEMENT_ENDPOINT

    url = endpoint + finishedquery
    print url
    get_resp = requests.get(url, headers=settings.HEADERS, verify=False)
    
    if get_resp.status_code != 200:
        print "got an error from performance.getStatements: %s" % get_resp.content
        return []

    return json.loads(get_resp.content)['statements']
    
def evaluateTetrisStatements(stmts, perfwkuri, username):
    levels = []
    lines = []
    scores = []
    times = []
    for s in stmts:
        levels.append(s['result']['extensions']['ext:level'])
        lines.append(s['result']['extensions']['ext:lines'])
        scores.append(s['result']['score']['raw'])
        times.append(s['result']['extensions']['ext:time'])

    print "%s\n%s\n%s\n%s" % (levels, lines, scores, times)