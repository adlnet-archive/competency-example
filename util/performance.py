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

def updateLevels(levelsarray,fwkuri, username):
    comp = getComponent(fwkuri, 'comp_levels')
    lvlmax = max(levelsarray)
    met = []
    for plvl in comp["performancelevels"]:
        if lvlmax > plvl["score"]["singlevalue"]:
            met.append(plvl["id"])

def updateLines(linesarray, fwkuri, username):
    comp = getComponent(fwkuri, 'comp_lines')
    lvlmax = max(linesarray)
    met = []
    for plvl in comp['performancelevels']:
        if lvlmax > plvl['score']['singlevalue']:
            met.append(plvl['id'])

def updateTimes(timesarray, fwkuri, username):
    comp = getComponent(fwkuri, 'comp_times')
    lvlmax = max(linesarray)
    met = []
    for plvl in comp['performancelevels']:
        if lvlmax > plvl['score']['singlevalue']:
            met.append(plvl['id'])

def updateScores(scorearray, fwkuri, username):
    comp = getComponent(fwkuri, 'comp_scores')
    lvlmax = max(linesarray)
    met = []
    for plvl in comp['performancelevels']:
        if lvlmax > plvl['score']['singlevalue']:
            met.append(plvl['id'])

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
    
    updateLines(lines, perfwkuri, username)
    updateLevels(levels, perfwkuri, username)
    updateScores(scores, perfwkuri, username)
    updateTimes(times, perfwkuri, username)

    updateLevels(levels, perfwkuri, username)
    updateLines(lines, perfwkuri, username)
    updateScores(scores, perfwkuri, username)
    updateTimes(times, perfwkuri, username)

def getComponent(perfwkuri, compid):
    perfwk = db.perfwk.find_one({"entry":perfwkuri})
    for com in perfwk['components']:
        if com['id'] == compid:
            return com
    return None

def updateLevels(levelsarray, fwkuri, username):
    comp = getComponent(fwkuri, 'comp_levels')
    lvlmax = max(levelsarray)
    compuri = getCompURIFromPFWK(comp)
    perfs = getUserTetrisCompPerformances(compuri, username)
    existing = [p['levelid'] for p in perfs]
    for plvl in comp['performancelevels']:
        if plvl['id'] in existing:
            continue
        if lvlmax >= int(plvl['score']['singlevalue']):
            ## do more, build performance object... reference in comment below
            ## then add it
            p = {}
            p['entry'] = fwkuri
            p['levelid'] = plvl['id']
            p['leveldescription'] = plvl['description']
            p['levelscore'] = plvl['score']['singlevalue']
            p['score'] =  lvlmax
            perfs.append(p)
    saveUserTetrisCompPerformances(compuri, username, perfs)

def updateLines(linesarray, fwkuri, username):
    comp = getComponent(fwkuri, 'comp_lines')
    lvlmax = max(linesarray)
    compuri = getCompURIFromPFWK(comp)
    perfs = getUserTetrisCompPerformances(compuri, username)
    existing = [p['levelid'] for p in perfs]
    for plvl in comp['performancelevels']:
        if plvl['id'] in existing:
            continue
        if lvlmax >= int(plvl['score']['singlevalue']):
            ## do more, build performance object... reference in comment below
            ## then add it
            p = {}
            p['entry'] = fwkuri
            p['levelid'] = plvl['id']
            p['leveldescription'] = plvl['description']
            p['levelscore'] = plvl['score']['singlevalue']
            p['score'] =  lvlmax
            perfs.append(p)
    saveUserTetrisCompPerformances(compuri, username, perfs)

def updateScores(scoresarray, fwkuri, username):
    comp = getComponent(fwkuri, 'comp_scores')
    lvlmax = max(scoresarray)
    compuri = getCompURIFromPFWK(comp)
    perfs = getUserTetrisCompPerformances(compuri, username)
    existing = [p['levelid'] for p in perfs]
    for plvl in comp['performancelevels']:
        if plvl['id'] in existing:
            continue
        if lvlmax >= int(plvl['score']['singlevalue']):
            ## do more, build performance object... reference in comment below
            ## then add it
            p = {}
            p['entry'] = fwkuri
            p['levelid'] = plvl['id']
            p['leveldescription'] = plvl['description']
            p['levelscore'] = plvl['score']['singlevalue']
            p['score'] =  lvlmax
            perfs.append(p)
    saveUserTetrisCompPerformances(compuri, username, perfs)

def updateTimes(timesarray, fwkuri, username):
    comp = getComponent(fwkuri, 'comp_times')
    lvlmax = max(timesarray)
    compuri = getCompURIFromPFWK(comp)
    perfs = getUserTetrisCompPerformances(compuri, username)
    existing = [p['levelid'] for p in perfs]
    for plvl in comp['performancelevels']:
        if plvl['id'] in existing:
            continue
        if lvlmax >= int(plvl['score']['singlevalue']):
            ## do more, build performance object... reference in comment below
            ## then add it
            p = {}
            p['entry'] = fwkuri
            p['levelid'] = plvl['id']
            p['leveldescription'] = plvl['description']
            p['levelscore'] = plvl['score']['singlevalue']
            p['score'] =  lvlmax
            perfs.append(p)
    saveUserTetrisCompPerformances(compuri, username, perfs)

def getCompURIFromPFWK(comp):
    for c in comp['competencies']:
        if c.get('type', "") == "http://ns.medbiq.org/competencyobject/v1/":
            return c['entry']

def getUserTetrisCompPerformances(compuri, username):
    cf = db.usercomps.find_one({"username":username, "entry":"http://12.109.40.34/competency-framework/xapi/tetris"})
    for c in cf['competencies']:
        if c['entry'] == compuri:
            return c.get('performances', [])

def saveUserTetrisCompPerformances(compuri, username, perfs):
    cf = db.usercomps.find_one({"username":username, "entry":"http://12.109.40.34/competency-framework/xapi/tetris"})
    for c in cf['competencies']:
        if c['entry'] == compuri:
            c['performances'] = perfs
    db.usercomps.update({"username":username, "entry":"http://12.109.40.34/competency-framework/xapi/tetris"}, cf)
