import base64

LRS_STATEMENT_ENDPOINT = 'http://localhost:8000/xapi/statements'

ENDPOINT_AUTH_USERNAME = 'tom'

ENDPOINT_AUTH_PASSWORD = '1234'

AUTHORIZATION = "Basic %s" % base64.b64encode("%s:%s" % (ENDPOINT_AUTH_USERNAME, ENDPOINT_AUTH_PASSWORD))

HEADERS = {        
                'Authorization': AUTHORIZATION,
                'content-type': 'application/json',        
                'X-Experience-API-Version': '1.0.0'
        }
DEMO_VIDEOS = {
	"http://adlnet.gov/competency/scorm/choosing-an-lms/part1":"http://www.youtube.com/watch?v=MPNXsR4Ne5I",
	"http://adlnet.gov/competency/scorm/choosing-an-lms/part2":"http://www.youtube.com/watch?v=4I7_oNiHw6U",
	"http://adlnet.gov/competency/scorm/choosing-an-lms/part3":"http://www.youtube.com/watch?v=VH1_78Gjk1o",
	"http://adlnet.gov/competency/scorm/choosing-an-lms/part4":"http://www.youtube.com/watch?v=fCaHP8LZAIo",
	"http://adlnet.gov/competency/scorm/choosing-an-lms/part5":"http://www.youtube.com/watch?v=tlBbt5niQto"
}
