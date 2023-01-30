#-----------------------------------------------------------------------------
#			Change History Log
#-----------------------------------------------------------------------------
#Description:
#updates quote information in CPQ
#-----------------------------------------------------------------------------
# Date			Name				Version		Comments(Changes done)
#-----------------------------------------------------------------------------
# 10/08/2022	Shweta Kandwal		0			Initial Creation
# 10/18/2022	Dhruv Bhatnagar		95			-Replaced Hardcodings
#												-Incorporated Translation
#-----------------------------------------------------------------------------
from System.Net import WebRequest
from System.Text import Encoding
from System.Net import WebException
from Scripting.Quote import MessageLevel

import GM_TRANSLATIONS																	#Inserted by Dhruv
lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)									#Inserted by Dhruv
lc_response = GM_TRANSLATIONS.GetText('000016', lv_LanguageKey, '', '', '', '', '')		#Inserted by Dhruv
lc_status = GM_TRANSLATIONS.GetText('000043', lv_LanguageKey, '', '', '', '', '')		#Inserted by Dhruv
lc_200 = GM_TRANSLATIONS.GetText('000051', lv_LanguageKey, '', '', '', '', '')			#Inserted by Dhruv
lc_msg = GM_TRANSLATIONS.GetText('000097', lv_LanguageKey, '', '', '', '', '')			#Inserted by Dhruv
lc_m1 = GM_TRANSLATIONS.GetText('000001', lv_LanguageKey, '', '', '', '', '')			#Inserted by Dhruv
lc_m2 = GM_TRANSLATIONS.GetText('000002', lv_LanguageKey, '', '', '', '', '')			#Inserted by Dhruv

system = 'CPQ'
ls_cred = SqlHelper.GetFirst("SELECT * FROM CT_CREDENTIALS WHERE SYSTEM = '"+str(system)+"' ")


#CXCPQ-33538  start
lc_quotetax = GM_TRANSLATIONS.GetText('000218', lv_LanguageKey, '', '', '', '', '')



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

def data_update(Param):
    
    if Param.QuoteNumber:
        so_num = None
        getquote = QuoteHelper.Get(str(Param.QuoteNumber))
        Log.Info("=== GS_API_ECC_UPDATE_SO Quote Number ===",str(Param.QuoteNumber))
        if Param.SO_Number:
            so_num = str(Param.SO_Number)
            srv_num = str(Param.SRVO_Number)
            #Log.Info("=== GS_API_ECC_UPDATE_SO SO Number {} ===".format(str(Param.SO_Number)))
            Log.Info("=== GS_API_ECC_UPDATE_SO SO Number {} ===")
            #QuoteHelper.Get(str(Param.QuoteNumber)).GetCustomField('CF_SO_Number').Value = str(Param.SO_Number)
            getquote.GetCustomField('CF_SO_Number').Value = str(so_num.lstrip("0"))
            getquote.GetCustomField('CF_Sales_Order').Value = str(so_num).lstrip("0")
            getquote.GetCustomField('CF_Service_Order').Value = str(srv_num).lstrip("0")
            QuoteHelper.Get(str(Param.QuoteNumber)).GetCustomField('Project Name').Value = str(Param.SO_Number)
            getquote.GetCustomField('CF_Booked_Date').Value = getquote.DateModified
            getquote.ChangeStatus('Booked')
            getquote.Save()
            try:
                invoke_Action(getquote.Id,2500)
            except Exception as ex:
                Log.Info("Exception Raised for Invoke Action")
            #return {"Response":[{"Status":"200","Message":"Successfully update in CPQ"}]}	#Commented by Dhruv
            return {lc_response:[{lc_status:lc_200,lc_msg:lc_m1}]}					#Inserted by Dhruv
        else:
            getquote.GetCustomField('CF_TotalTax').Value = str(Param.TotalTax)
            Log.Info("=== GS_API_ECC_UPDATE_SO Total Tax Update===",str(getquote.GetCustomField('CF_TotalTax').Value))

        getquote.GetCustomField('CF_SFDC_Total_Amount').Value = str(getquote.Totals.Amount) + " " + getquote.GetCustomField('CF_Quote_Currency').Value

        #Log.Info("=== GS_API_ECC_UPDATE_SO CF_SFDC_Total_Amount ===",str(getquote.GetCustomField('CF_SFDC_Total_Amount').Value))
        Log.Info("=== GS_API_ECC_UPDATE_SO ==CALAVULATE TAX=")
        ##CXCPQ-33538  start
        totalTax = getquote.GetCustomField('CF_TotalTax').Value
        if totalTax is None or totalTax == '':
            context.Quote.AddMessage(lc_quotetax,MessageLevel.Warning,False)
        else:
            Log.Write('121-clear messgae-')#CXCPQ-33538  end
        #getquote.Save()
    else:
        #return "Please provide valid QuoteNumber"	#Commented by Dhruv
        return str(lc_m2)							#Inserted by Dhruv

#Log.Info("=== GS_API_ECC_UPDATE_SO CI_Booked_Date ===")
if Param is not None:
    #Log.Info("=== GS_API_ECC_UPDATE_SO CI_Booked_Date ===",str(Param))
    data = data_update(Param)
    #Log.Info("=== GS_API_ECC_UPDATE_SO CI_Booked_Date ===",str(data))
    ApiResponse = ApiResponseFactory.JsonResponse(data)