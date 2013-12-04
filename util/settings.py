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