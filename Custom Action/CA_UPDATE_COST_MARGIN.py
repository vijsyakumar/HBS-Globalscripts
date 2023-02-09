# -----------------------------------------------------------------------------
#			Change History Log
# -----------------------------------------------------------------------------
# Description:
# GS API to post data from CPQ to NEX
# -----------------------------------------------------------------------------
# Date			Name				Version		Comments(Changes done)
# -----------------------------------------------------------------------------
# 17/01/2023   Priyanka Thakur	    0          -initial version
# -----------------------------------------------------------------------------
#Revised Auth Code
import clr
from System.Net.Http import HttpClient
from System.Net import HttpWebRequest
clr.AddReference("System.Xml")
import sys
from math import ceil
from System.Text import Encoding
#Log.Info('22--quote id-->'+str(context.Quote.Id))
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
    #Trace.Write(atoken)
    return "{} ".format(atoken)

def post_opp_data(quoteId, ls_cred, bearer_token):
    grossMargin = context.Quote.GetCustomField('CF_Gross_Margin').Value
    marginAmount = context.Quote.GetCustomField('CF_Margin_Amount').Value
    cost=  context.Quote.QuoteTables["Quote_Details"].Rows[0].GetColumnValue('QT_Total_Cost')
    #Trace.Write(grossMargin)
    #Trace.Write(marginAmount)
    #Trace.Write(cost)
    oppurl = "https://{}/cpq/quote/api/v1/quote".format(ls_cred.HOST)
    HBS = 'HBT-HBS'
    bearer_token = "Bearer "+bearer_token
    payload = '{"Gross_Margin__c": '+str(grossMargin)+',"Cost__c": '+str(cost)+',"Margin_Amount__c": '+str(marginAmount)+'}'
    headers = { "Authorization": bearer_token , "HON-Org-Id":HBS,'quoteId': str(quoteId)}
    response  = RestClient.Patch(oppurl,payload,headers)

# Logic Execution
quoteId = context.Quote.Id
#Trace.Write(" quoteId "+str(quoteId))

system = 'SFDC'
ls_cred = SqlHelper.GetFirst("SELECT * FROM CT_CREDENTIALS WHERE SYSTEM = '"+str(system)+"' ")


#Log.Info("Parties Involved - Get Opp ID - {} ".format(oppId))
if quoteId:
    post_opp_data(str(quoteId),ls_cred, getAccessToken(ls_cred))