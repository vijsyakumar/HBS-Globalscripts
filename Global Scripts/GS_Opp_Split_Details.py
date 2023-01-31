import clr 
from System.Net import HttpWebRequest
clr.AddReference("System.Xml")
import sys
from math import ceil
from System.Text import Encoding

def clear_error_message():
    exitmsgs = context.Quote.Messages
    if exitmsgs.Count > 0:
        for msges in exitmsgs:
            if  "Booking percent is greater than 100 percent please check" in str(msges.Content):
                context.Quote.DeleteMessage(msges.Id)

def getAccessToken(ls_cred):
#Get credentails
    url = "https://{}/v2/oauth/accesstoken".format(ls_cred.HOST)
    clr.AddReference("Newtonsoft.Json")
    from Newtonsoft.Json import JsonConvert
    from Newtonsoft.Json.Linq import JObject

    clr.AddReference('System.Net.Http')
    from System.Net.Http import HttpClient
    with HttpClient() as api:
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = AuthorizedRestClient.GetClientCredentialsGrantOAuthToken('BPOAuth', url)
        atoken = response["access_token"]
    return "{} ".format(atoken)

def get_opp_data(oppId, ls_cred, bearer_token):
    try:
        Log.Info("====GS_Opp_Split_Details get_opp_data is called ====")
        #param_value = "SELECT+Id,OpportunityId,Split,SplitNote,Split_Owner_Name__c,SplitAmount,SplitPercentage+FROM+OpportunitySplit+WHERE+OpportunityId='"+oppId+"'+LIMIT+100"
        body = {"query":"SELECT+Id,OpportunityId,Split,SplitNote,Split_Owner_Name__c,SplitAmount,SplitPercentage,Split_Owner_EID__c+FROM+OpportunitySplit+WHERE+OpportunityId='"+oppId+"'+LIMIT+100"}
        
        oppurl = "https://{}/opportunities/api/v1/split".format(ls_cred.HOST)
        Log.Info("====GS_Opp_Split_Details get_opp_data  oppurl ===="+oppurl)
        HBS = 'HBT-HBS'
        bearer_token = "Bearer "+bearer_token
        headers = { "Authorization": bearer_token , "HON-Org-Id":HBS}
        
        response  = RestClient.Post(oppurl,RestClient.SerializeToJson(body),headers)
        #RestClient.Post(Final_Url , RestClient.SerializeToJson(final_request_body), header)
        Trace.Write("====GS_Opp_Split_Details get_opp_data  response===="+str(response))
        get_opp_split_data(response)
    except Exception as ex:
        Trace.Write("=== GS_Opp_Split_Details ex==="+str(ex))

def get_opp_split_data(response):
    Log.Info("====GS_Opp_Split_Details get_opp_split_data response : ====",str(response))
    split_list = response.records
    #Log.Info("====GS_Opp_Split_Details get_opp_split_data split_list : ====",str(split_list))
    split_range = 0
    if len(split_list) > 5:
        split_range = 5
    else:
        split_range = len(split_list)
    #Log.Info("===GS_Opp_Split_Details split_range ===",str(split_range))
    getcount =0#CXCPQ-34734 start
    for i in range(0,split_range):#CXCPQ-34734 start
        if split_list[i]['SplitPercentage'] > 0:

            context.Quote.GetCustomField('CF_EID_'+str(i+1)+'_Rate').Value = split_list[i]['SplitPercentage']
            context.Quote.GetCustomField('CF_EID_'+str(i+1)).Value =split_list[i]['Split_Owner_EID__c']
            context.Quote.GetCustomField('CF_EID_NAME_'+str(i+1)).Value = split_list[i]['Split_Owner_Name__c']
            getcount = getcount+1
    if context.Quote.GetCustomField('CF_EID_NAME_1').Value == "" or context.Quote.GetCustomField('CF_EID_NAME_1').Value is None:
        context.Quote.GetCustomField('CF_EID_1_Rate').Value = context.Quote.GetCustomField('CF_EID_' + str(getcount + 1) + '_Rate').Value
        context.Quote.GetCustomField('CF_EID_NAME_1').Value = context.Quote.GetCustomField('CF_EID_NAME_' + str(getcount + 1)).Value
        context.Quote.GetCustomField('CF_EID_1').Value = context.Quote.GetCustomField('CF_EID_' + str(getcount + 1)).Value
        context.Quote.GetCustomField('CF_EID_' + str(getcount + 1) + '_Rate').Value =''
        context.Quote.GetCustomField('CF_EID_NAME_' + str(getcount + 1)).Value = ''
        context.Quote.GetCustomField('CF_EID_' + str(getcount + 1)).Value =''
    if context.Quote.GetCustomField('CF_EID_NAME_2').Value == "" or context.Quote.GetCustomField('CF_EID_NAME_2').Value is None:
        #Log.Info('getcount=='+str(getcount))
        context.Quote.GetCustomField('CF_EID_2_Rate').Value = context.Quote.GetCustomField('CF_EID_' + str(getcount + 1) + '_Rate').Value
        context.Quote.GetCustomField('CF_EID_NAME_2').Value = context.Quote.GetCustomField('CF_EID_NAME_' + str(getcount + 1)).Value
        context.Quote.GetCustomField('CF_EID_2').Value = context.Quote.GetCustomField('CF_EID_' + str(getcount + 1)).Value
        context.Quote.GetCustomField('CF_EID_' + str(getcount + 1) + '_Rate').Value =''
        context.Quote.GetCustomField('CF_EID_NAME_' + str(getcount + 1)).Value = ''
        context.Quote.GetCustomField('CF_EID_' + str(getcount + 1)).Value =''
    if context.Quote.GetCustomField('CF_EID_NAME_3').Value == "" or context.Quote.GetCustomField('CF_EID_NAME_3').Value is None:
        #Log.Info('getcount=='+str(getcount))
        context.Quote.GetCustomField('CF_EID_3_Rate').Value = context.Quote.GetCustomField('CF_EID_' + str(getcount + 1) + '_Rate').Value
        context.Quote.GetCustomField('CF_EID_NAME_3').Value = context.Quote.GetCustomField('CF_EID_NAME_' + str(getcount + 1)).Value
        context.Quote.GetCustomField('CF_EID_3').Value = context.Quote.GetCustomField('CF_EID_' + str(getcount + 1)).Value
        context.Quote.GetCustomField('CF_EID_' + str(getcount + 1) + '_Rate').Value =''
        context.Quote.GetCustomField('CF_EID_NAME_' + str(getcount + 1)).Value = ''
        context.Quote.GetCustomField('CF_EID_' + str(getcount + 1)).Value =''
    if context.Quote.GetCustomField('CF_EID_NAME_4').Value == "" or context.Quote.GetCustomField('CF_EID_NAME_4').Value is None:
        #Log.Info('getcount=='+str(getcount))
        context.Quote.GetCustomField('CF_EID_4_Rate').Value = context.Quote.GetCustomField('CF_EID_' + str(getcount + 1) + '_Rate').Value
        context.Quote.GetCustomField('CF_EID_NAME_4').Value = context.Quote.GetCustomField('CF_EID_NAME_' + str(getcount + 1)).Value
        context.Quote.GetCustomField('CF_EID_4').Value = context.Quote.GetCustomField('CF_EID_' + str(getcount + 1)).Value
        context.Quote.GetCustomField('CF_EID_' + str(getcount + 1) + '_Rate').Value =''
        context.Quote.GetCustomField('CF_EID_NAME_' + str(getcount + 1)).Value = ''
        context.Quote.GetCustomField('CF_EID_' + str(getcount + 1)).Value =''
    
        
# Logic Execution
Log.Info("====GS_Opp_Split_Details is called ====")
context.Quote.GetCustomField('CF_EID_1').Value = ""
context.Quote.GetCustomField('CF_EID_2').Value = ""
context.Quote.GetCustomField('CF_EID_3').Value = ""
context.Quote.GetCustomField('CF_EID_4').Value = ""
context.Quote.GetCustomField('CF_EID_5').Value = ""
context.Quote.GetCustomField('CF_EID_NAME_1').Value = ""
context.Quote.GetCustomField('CF_EID_NAME_2').Value = ""
context.Quote.GetCustomField('CF_EID_NAME_3').Value = ""
context.Quote.GetCustomField('CF_EID_NAME_4').Value = ""
context.Quote.GetCustomField('CF_EID_NAME_5').Value = ""
context.Quote.GetCustomField('CF_EID_1_Rate').Value = ""
context.Quote.GetCustomField('CF_EID_2_Rate').Value = ""
context.Quote.GetCustomField('CF_EID_3_Rate').Value = ""
context.Quote.GetCustomField('CF_EID_4_Rate').Value = ""
context.Quote.GetCustomField('CF_EID_5_Rate').Value = ""

records = context.Quote.Id
system = 'SFDC'
ls_cred = SqlHelper.GetFirst("SELECT * FROM CT_CREDENTIALS WHERE SYSTEM = '"+str(system)+"' ")
oppId = context.Quote.OpportunityId
if oppId :
    get_opp_data(oppId,ls_cred, getAccessToken(ls_cred))
else:
    oppId = context.Quote.GetCustomField('Opportunity_ID').Value
    get_opp_data(oppId,ls_cred, getAccessToken(ls_cred))

try:
    Log.Info("===GS_Opp_Split_Details triggered for Booking Calculation=====")
    Booking1= context.Quote.GetCustomField('CF_EID_1_Rate').Value
    Booking2= context.Quote.GetCustomField('CF_EID_2_Rate').Value
    Booking3= context.Quote.GetCustomField('CF_EID_3_Rate').Value
    Booking4= context.Quote.GetCustomField('CF_EID_4_Rate').Value
    Booking5= context.Quote.GetCustomField('CF_EID_5_Rate').Value
    if Booking1 is None or Booking1=="":
        Booking1 = 0.0
    if Booking2 is None or Booking2=="":
        Booking2 = "0.0"
    if Booking3 is None or Booking3=="":
        Booking3 = "0.0"
    if Booking4 is None or Booking4=="":
        Booking4 = "0.0"
    if Booking5 is None or Booking5=="":
        Booking5 = "0.0"
    finalbooking = float(Booking1)+float(Booking2)+float(Booking3)+float(Booking4)+float(Booking5)
    #Log.Info("====GS_Opp_Split_Details final booking value=====",str(finalbooking)) 
    context.Quote.GetCustomField('CF_EID_Total_Rate').Value = str(finalbooking)
    #Log.Info("*** GS_Opp_Split_Details Total Booking value****",context.Quote.GetCustomField('CF_EID_Total_Rate').Value)
    if finalbooking > 100:
        msg = "Booking percent is greater than 100 percent please check"
        clear_error_message()
        #context.Quote.AddMessage(msg,MessageLevel.Error,False)
    else:
        clear_error_message()
except Exception as ex:
    Log.Info("=== GS_Book exceptionoccured ===",str(ex))