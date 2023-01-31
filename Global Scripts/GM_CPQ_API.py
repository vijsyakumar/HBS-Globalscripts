from System.Net import WebRequest
from System.Text import Encoding
from System.Net import WebException

system = 'CPQ'
ls_cred = SqlHelper.GetFirst("SELECT * FROM CT_CREDENTIALS WHERE SYSTEM = '"+str(system)+"' ")

def creating_bearer_token():

    data = 'grant_type=password&username='+ls_cred.UserName+'&password='+ls_cred.Password+'&domain='+ls_cred.Domain
    data = Encoding.UTF8.GetBytes(data)
    url = "https://{}/basic/api/token".format(ls_cred.HOST)
    #url = "https://sandbox.webcomcpq.com/basic/api/token"
    request = WebRequest.Create(url)
    request.Method = "POST"

    # Set the ContentType property of the WebRequest.
    request.ContentType = "application/x-www-form-urlencoded"
    request.Accept = 'application/json'
    request.ContentLength = data.Length
    request.GetRequestStream().Write(data, 0, data.Length)

    response = request.GetResponse()
    stream = RestClient.DeserializeJson(StreamReader(response.GetResponseStream()).ReadToEnd())
    bearer_token = stream.access_token
    Trace.Write("token created {}".format(bearer_token))
    return bearer_token

def create_jwt_token():
    url = "https://sandbox.webcomcpq.com/api/rd/v1/core/GenerateJWT"
    url = "https://{}/api/rd/v1/core/GenerateJWT".format(ls_cred.HOST)
    encodedKeys = "Bearer "+str(creating_bearer_token())
    headers = {"Authorization":encodedKeys}
    data = ""
    jwt_resp_token = RestClient.Post(url,data,headers)
    return jwt_resp_token.token

def invoke_Action(quote_Id,action_Id):
    #url = "https://sandbox.webcomcpq.com/api/v1/quotes/6221/actions/2500/invoke"
    url = "https://{}/api/v1/quotes/{}/actions/{}/invoke".format(ls_cred.HOST,quote_Id,action_Id)
    encodedKeys = " Bearer "+str(create_jwt_token())
    headers = {"Authorization":encodedKeys}
    data = ""
    result = RestClient.Post(url,data,headers)
    return result