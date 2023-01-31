import datetime
#CXCPQ-35129 start
from System.Net import WebRequest
from System.Text import Encoding
from System.Net import WebException
from Scripting.Quote import MessageLevel

import GM_TRANSLATIONS																	
lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)									
lc_response = GM_TRANSLATIONS.GetText('000016', lv_LanguageKey, '', '', '', '', '')		
lc_status = GM_TRANSLATIONS.GetText('000043', lv_LanguageKey, '', '', '', '', '')		
lc_200 = GM_TRANSLATIONS.GetText('000051', lv_LanguageKey, '', '', '', '', '')			
lc_msg = GM_TRANSLATIONS.GetText('000097', lv_LanguageKey, '', '', '', '', '')			
lc_m1 = GM_TRANSLATIONS.GetText('000001', lv_LanguageKey, '', '', '', '', '')			
lc_m2 = GM_TRANSLATIONS.GetText('000002', lv_LanguageKey, '', '', '', '', '')

system = 'CPQ'
ls_cred = SqlHelper.GetFirst("SELECT * FROM CT_CREDENTIALS WHERE SYSTEM = '"+str(system)+"' ")	
#CXCPQ-35129 end		
current_time = datetime.datetime.now()
dt_string = current_time.strftime("%d/%m/%Y %H:%M:%S")
user_details = User.Name
q_no = context.Quote.GetCustomField('CF_Quote Number').Value
opp_no = context.Quote.GetCustomField('CF_Opportunity_Number').Value
isPrimary = context.Quote.GetCustomField('CF_Primary_Quote').Value

try:
    primary_onload = Param.primary_onload
except:
    primary_onload = ''
try:    
    getClickVar = Param.getClickVar
except:
    getClickVar =''
#cxcpq-35129 start
def creating_bearer_token():

    data = 'grant_type=password&username='+ls_cred.UserName+'&password='+ls_cred.Password+'&domain='+ls_cred.Domain
    data = Encoding.UTF8.GetBytes(data)
    url = "https://{}/basic/api/token".format(ls_cred.HOST)

    request = WebRequest.Create(url)
    request.Method = "POST"


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
    url = "https://{}/api/v1/quotes/{}/actions/{}/invoke".format(ls_cred.HOST,quote_Id,action_Id)
    encodedKeys = " Bearer "+str(create_jwt_token())
    headers = {"Authorization":encodedKeys}
    data = ""
    result = RestClient.Post(url,data,headers)
    return result
#CXCPQ-35129 end

#CXCPQ-35073 start
QR = SqlHelper.GetFirst("SELECT * FROM CT_PRIMARY_QUOTE where Opportunity_Number = '"+str(opp_no)+"' and Quote_Number='"+str(q_no)+"'")
def primary_check_click(getClickVar):
    get_clicked_value = ''
    Log.Info('getClickVar--->'+str(getClickVar))
    if getClickVar == True:
        Log.Info('getClickVar-81------->')
        context.Quote.GetCustomField('CF_Primary_Quote').Value = 'Yes'
        if QR is None:
            tableInfo = SqlHelper.GetTable('CT_PRIMARY_QUOTE')
            Trace.Write(" Quote Marked as Primary in CT: "+str(q_no))
            tablerow = { "Opportunity_Number" : opp_no, "Quote_Number" : q_no , "Is_Primary_Quote" : 'Yes' }
            tableInfo.AddRow(tablerow)
            SqlHelper.Upsert(tableInfo)
        else:
            newQuoteObj = QuoteHelper.Get(QR.Quote_Number)
            newQuoteObj.Save()
            tableInfo = SqlHelper.GetTable('CT_PRIMARY_QUOTE')
            tablerow = { "CpqTableEntryId" : QR.CpqTableEntryId ,"Opportunity_Number" : opp_no, "Quote_Number" : q_no , "Is_Primary_Quote" : 'Yes' }
            tableInfo.AddRow(tablerow)
            SqlHelper.Upsert(tableInfo)
        #to update other quotes belongs to that opp
        QN_Obj = SqlHelper.GetList("SELECT * FROM CT_PRIMARY_QUOTE where Opportunity_Number = '"+str(opp_no)+"' and Quote_Number not in ('"+str(q_no)+"')")
        for val in QN_Obj:
            tableInfo = SqlHelper.GetTable('CT_PRIMARY_QUOTE')
            tablerow = { "CpqTableEntryId" : val.CpqTableEntryId ,"Opportunity_Number" : opp_no, "Quote_Number" : val.Quote_Number , "Is_Primary_Quote" : '' }
            tableInfo.AddRow(tablerow)
            SqlHelper.Upsert(tableInfo)
        get_clicked_value = 'Yes'
    else:
        context.Quote.GetCustomField('CF_Primary_Quote').Value = ''
        if QR is None:
            tableInfo = SqlHelper.GetTable('CT_PRIMARY_QUOTE')
            Trace.Write(" Quote Marked as Primary in CT: "+str(q_no))
            tablerow = { "Opportunity_Number" : opp_no, "Quote_Number" : q_no , "Is_Primary_Quote" : '' }
            tableInfo.AddRow(tablerow)
            SqlHelper.Upsert(tableInfo)
        else:
            tableInfo = SqlHelper.GetTable('CT_PRIMARY_QUOTE')
            tablerow = { "CpqTableEntryId" : QR.CpqTableEntryId ,"Opportunity_Number" : opp_no, "Quote_Number" : q_no , "Is_Primary_Quote" : '' }
            tableInfo.AddRow(tablerow)
            SqlHelper.Upsert(tableInfo)#CXCPQ-35073 end
        get_clicked_value = ''
    getquote = QuoteHelper.Get(q_no)
    invoke_Action(getquote.Id,2500)
    return get_clicked_value

def get_onload_primary(primary_onload):
    checked_primary_val = ''
    q_no = context.Quote.GetCustomField('CF_Quote Number').Value
    opp_no = context.Quote.GetCustomField('CF_Opportunity_Number').Value
    isPrimary = context.Quote.GetCustomField('CF_Primary_Quote').Value
    QR = SqlHelper.GetFirst("SELECT Is_Primary_Quote FROM CT_PRIMARY_QUOTE where Opportunity_Number = '"+str(opp_no)+"' and Quote_Number='"+str(q_no)+"'")
    if QR is not None and QR.Is_Primary_Quote != '':
        Log.Info('onload cll iinside true--')
        checked_primary_val = 'Yes'
    else:
        Log.Info('onload cll iinside false--')
        checked_primary_val = ''
    Log.Info('onload primary_val--->'+str(checked_primary_val))
    return checked_primary_val

if primary_onload == "ONLOAD":
    ApiResponse = ApiResponseFactory.JsonResponse(get_onload_primary(primary_onload))
else:
    ApiResponse = ApiResponseFactory.JsonResponse(primary_check_click(getClickVar))
    
#if primary_onload != "ONLOAD":
    #getquote = QuoteHelper.Get(q_no)
    #invoke_Action(getquote.Id,2500)#cxcpq-35129 end