import json
import os
import base64

def handler(event, context):
    print(f"Received event: {json.dumps(event)}")
    print(f"Received context: {context}")
    try:
        authorization_header = event.get('authorizationToken', '')
        method = event.get('methodArn', '')
        if not authorization_header:
            return {
                "statusCode" : 401,
                "headers" : {
                    "Access-Control-Allow-Origin" : "*",
                    "Access-Control-Allow-Methods" : "GET",
                    "Access-Control-Allow-Headers": "Content-Type",
                    "content-type" : "application/json"
                },
                "body": json.dumps("'message':'Unauthorized'")
            }
        
        #used Vml0YWxpU2F2ZWx5ZXY9UEFTU1dPUkQ=

        try:
            encoded_credentials = authorization_header.split(' ')[1]
            decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
            userName, password = decoded_credentials.split('=')
        except Exception:
            return _generatePolicy('UnknownUser', method, 'Deny')

        storedPassword = os.getenv(userName)

        password = password.strip()

        if storedPassword and storedPassword == password:
            policy = _generatePolicy(userName, method, 'Allow')
            print(f"Policy: {policy}")
            return policy
        
        return _generatePolicy(userName, method, 'Deny')
    except Exception as e:
        return {
            "statusCode" : 500,
            "body": json.dumps({'error': str(e)})
        }
    
def _generatePolicy(principalId, resource, effect):
    authResponse = {
        'principalId': principalId
    }
    if resource:
        policy_document = {
            'Version': '2012-10-17',
            'Statement': [{
                'Action': 'execute-api:Invoke',
                'Effect': effect,
                'Resource': resource
            }]
        }
        authResponse['policyDocument'] = policy_document

    print(f"auth_response: {authResponse}")
    return authResponse
