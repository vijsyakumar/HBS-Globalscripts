#Revised Auth Code
import clr
from System.Net import HttpWebRequest
clr.AddReference("System.Xml")
import sys
from math import ceil
from System.Text import Encoding
Log.Info('22--quote id-->'+str(context.Quote.Id))

#involved party issue #37927 start
import re
#37927 end
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
    #oppurl = "https://it.api-dev.honeywell.com/hbt-sfdc-cpq-partner-functions-api-v1/services/apexrest/partnerfunction/0063J000006lwESQAY"
    #oppurl = "https://{}/hbt-sfdc-cpq-partner-functions-api-v1/services/apexrest/partnerfunction/{}".format(ls_cred.HOST,oppId)
    oppurl = "https://{}/opportunities/api/v1/partner_functions?opportunityId={}".format(ls_cred.HOST,oppId)
    HBS = 'HBT-HBS'
    bearer_token = "Bearer "+bearer_token
    headers = { "Authorization": bearer_token , "HON-Org-Id":HBS}
    response  = RestClient.Get(oppurl,headers)
    get_pf_data(response)

def get_pf_data(response):
    # PFKEY , Busines Partner Name , External ID
    try:
        if response['SoldTo'].Country__c is None or response['SoldTo'].State_Province__c is None:
            Trace.Write("Sold to Party Empty")
        else:
            lv_pfkey = "SP"
            pf = context.Quote.AddInvolvedParty(lv_pfkey, str(response['SoldTo'].Name),str(response['SoldTo'].Source_System_Company_Id__c))
            pf.StreetName = str(response['SoldTo'].Street__c)
            #pf.AddressName = re.sub('[^a-zA-Z0-9 \n\.]', '', str(response['SoldTo'].Street__c))[slice(40)]
            pf.FirstName = re.sub('[^a-zA-Z0-9 \n\.]', '', str(response['SoldTo'].Source_System_Account_Name__c))
            pf.CityName = re.sub('[^a-zA-Z0-9 \n\.]', '', str(response['SoldTo'].City__c))
            pf.PostalCode = str(response['SoldTo'].Postal_Code__c)
            pf.Country = str(response['SoldTo'].Country__c)
            pf.State = str(response['SoldTo'].State_Province__c)
    except Exception as ex:
        Log.Info("Involved Parties Sold to Party Empty")

    try:
        if response['ShipTo'].Country__c is None or response['ShipTo'].State_Province__c is None: 
            Trace.Write("Ship to Party Empty")
        else:
            lv_pfkey = "SH"
            pf = context.Quote.AddInvolvedParty(lv_pfkey, str(response['ShipTo'].Name),str(response['ShipTo'].Source_System_Company_Id__c))
            pf.StreetName = str(response['ShipTo'].Street__c)
            #pf.AddressName =  re.sub('[^a-zA-Z0-9 \n\.]', '',str(response['ShipTo'].Street__c))[slice(40)]
            pf.FirstName = re.sub('[^a-zA-Z0-9 \n\.]', '',str(response['ShipTo'].Source_System_Account_Name__c))
            pf.CityName = re.sub('[^a-zA-Z0-9 \n\.]', '',str(response['ShipTo'].City__c))
            pf.PostalCode = str(response['ShipTo'].Postal_Code__c)
            pf.Country = str(response['ShipTo'].Country__c)
            pf.State = str(response['ShipTo'].State_Province__c)
    except Exception as ex:
        Log.Info("Involved Parties Ship to Party Empty")
    
    try:
        if response['BillTo'].Country__c is None or response['BillTo'].State_Province__c is None:
            Trace.Write("Bill to Party Empty")
        else:
            lv_pfkey = "BP"
            pf = context.Quote.AddInvolvedParty(lv_pfkey, str(response['BillTo'].Name),str(response['BillTo'].Source_System_Company_Id__c))
            pf.StreetName = str(response['BillTo'].Street__c)
            #pf.AddressName = re.sub('[^a-zA-Z0-9 \n\.]', '',str(response['BillTo'].Street__c))[slice(40)]
            pf.FirstName = re.sub('[^a-zA-Z0-9 \n\.]', '', str(response['BillTo'].Source_System_Account_Name__c))
            pf.CityName = re.sub('[^a-zA-Z0-9 \n\.]', '', str(response['BillTo'].City__c))
            pf.PostalCode = str(response['BillTo'].Postal_Code__c)
            pf.Country = str(response['BillTo'].Country__c)
            pf.State = str(response['BillTo'].State_Province__c)

        if response['ShipTo'].Country__c is None or response['ShipTo'].State_Province__c is None:
            Trace.Write("Ship To Party Empty")
        else:
            lv_pfkey = "EN"
            pf = context.Quote.AddInvolvedParty(lv_pfkey, str(response['ShipTo'].Name),str(response['ShipTo'].Source_System_Company_Id__c))
            pf.StreetName = str(response['ShipTo'].Street__c)
            #pf.AddressName = re.sub('[^a-zA-Z0-9 \n\.]', '', str(response['ShipTo'].Street__c))[slice(40)]
            pf.FirstName = re.sub('[^a-zA-Z0-9 \n\.]', '', str(response['ShipTo'].Source_System_Account_Name__c))
            pf.CityName = re.sub('[^a-zA-Z0-9 \n\.]', '', str(response['ShipTo'].City__c))
            pf.PostalCode = str(response['ShipTo'].Postal_Code__c)
            pf.Country = str(response['ShipTo'].Country__c)
            pf.State = str(response['ShipTo'].State_Province__c)
    except Exception as ex:
        Log.Info("Involved Parties Ship To  Party empty")
    try:
        for count, value in enumerate(response['OpportunityTeamMembers']):
            if "Account Manager" in str(response['OpportunityTeamMembers'][count].TeamMemberRole) :
                context.Quote.GetCustomField('CF_Account_Manager').Value = str(response['OpportunityTeamMembers'][count].Name)
            if "Opportunity Owner" in str(response['OpportunityTeamMembers'][count].TeamMemberRole) :
                context.Quote.GetCustomField('CF_Opportunity_Owner').Value = str(response['OpportunityTeamMembers'][count].Name)
            #if "Field Service Leader" in str(response['OpportunityTeamMembers'][count].TeamMemberRole) :
            if "Field Service Supervisor" in str(response['OpportunityTeamMembers'][count].TeamMemberRole):
                #context.Quote.GetCustomField('CF_FSL').Value = str(response['OpportunityTeamMembers'][count].Name)
                #Log.Write('103--Name---->'+str(response['OpportunityTeamMembers'][count].Name))
                lv_name = str(response['OpportunityTeamMembers'][count].Name)
                context.Quote.GetCustomField('CF_FSL').Value = lv_name
                if str(response['OpportunityTeamMembers'][count].User.FederationIdentifier) is not None and str(response['OpportunityTeamMembers'][count].User.FederationIdentifier) != '':
                    lv_id = str(response['OpportunityTeamMembers'][count].User.FederationIdentifier)
                else:
                    lv_id =''
                #lv_id = str(response['OpportunityTeamMembers'][count].User.FederationIdentifier)
                lv_pfkey = "ZL"
                pf = context.Quote.AddInvolvedParty(lv_pfkey, lv_name,lv_id)
    except Exception as ex:
        Log.Info("Involved Parties field service")
    try:
        if not str(response['OpportunityContactRoles']):
            Log.Info("Involved Parties empty contact Person")
        else:
            lv_pfkey = "ZC"
            pf = context.Quote.AddInvolvedParty(lv_pfkey, str(response['OpportunityContactRoles'][0].Contact.Name),str(response['OpportunityContactRoles'][0].Contact.Id))
            if str(response['OpportunityContactRoles'][0].Contact.Email):
                pf.EmailAddress = str(response['OpportunityContactRoles'][0].Contact.Email)
                pf.Phone = str(response['OpportunityContactRoles'][0].Contact.Phone)
            if context.Quote.GetCustomField('CF_Contact_Person').Value == "" :
                context.Quote.GetCustomField('CF_Contact_Person').Value = str(response['OpportunityContactRoles'][0].Contact.Name)
                context.Quote.GetCustomField('CF_Contact_Person_Email').Value = str(response['OpportunityContactRoles'][0].Contact.Email)
                context.Quote.GetCustomField('CF_Contact_Person_Phone').Value = str(response['OpportunityContactRoles'][0].Contact.Phone)
    except Exception as ex:
        Log.Info("Involved Parties empty contact Person---"+str(ex))

# Logic Execution
QuoteId = context.Quote.Id
QuoteNumber = context.Quote.QuoteNumber
Trace.Write(" QuoteId "+str(QuoteId))
tables = SqlHelper.GetList("select * from  sys_QuoteInvolvedParties where QuoteId = {} ".format(QuoteId))
Trace.Write(" Tables : "+str(tables))
status = context.Quote.StatusName
#sync partner custom action start
try:
    Action = Param.ACTION
except:
    Action = ''
#sync partner custom action end
#Check for Inconsistent Data
flag = False
#if status == 'Preparing' :#commented to avoid multiple execution
    #flag = True
if Action == 'SYNC_PARTNER':
    flag = True
for i in tables:
    if not i.Name:
        flag = True
    break
for i in tables:
    if flag == True:
        context.Quote.DeleteInvolvedParty(i.Id)

#To Check Record Exist or not
if not tables or flag == True:
    Trace.Write("Data")
    system = 'SFDC'
    ls_cred = SqlHelper.GetFirst("SELECT * FROM CT_CREDENTIALS WHERE SYSTEM = '"+str(system)+"' ")
    oppId = context.Quote.OpportunityId
    if oppId is None:
        oppId = context.Quote.GetCustomField('Opportunity_ID').Value
    Log.Info("Parties Involved - Get Opp ID - {} ".format(oppId))
    if oppId:   
        if context.Quote.GetCustomField('CF_Account_Manager'):
            context.Quote.GetCustomField('CF_Account_Manager').Value = ""
        get_opp_data(oppId,ls_cred, getAccessToken(ls_cred))