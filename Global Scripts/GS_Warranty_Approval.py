#-----------------------------------------------------------------------------
#			Change History Log
#-----------------------------------------------------------------------------
#Description:
#checking warranty approval
#-----------------------------------------------------------------------------
# Date			Name				Version		Comments(Changes done)
#-----------------------------------------------------------------------------
# 08/08/2022    Karthikraj			   0		-Initial Version
# 				Thiruvenkatasamy
#
# 10/14/2022	Abhilash		       21		 -Replaced Hardcodings
#												 -Incorporated Translation
#
# 11/04/2022	Dhruv				   30		 -SQL translation,Transacrtion type
#												  check implemented
# 12/15/2022    Dhruv				   40		 -CXCPQ-35214: Passing value as 'None'
#												  for warranty Approval custom field
#											      mapped with CRM when returning to default
#												  Warranty approval Value on Quote
#-----------------------------------------------------------------------------

from Scripting.Quote import MessageLevel
import GM_TRANSLATIONS
lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '') #Modified by Dhruv
if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type:  #Modified by Dhruv
    lc_message = GM_TRANSLATIONS.GetText('000041', lv_LanguageKey, '', '', '', '', '')
    lc_message2 = GM_TRANSLATIONS.GetText('000013', lv_LanguageKey, '', '', '', '', '')
    opp_country = context.Quote.GetCustomField('CF_Country').Value #fetching opporutunity country
    rgm = GM_TRANSLATIONS.GetText('000163', lv_LanguageKey, '', '', '', '', '')
    hbs_President = GM_TRANSLATIONS.GetText('000164', lv_LanguageKey, '', '', '', '', '')
    warranty_type = context.Quote.GetCustomField('Warranty Duration(in months)').Value #fetching warranty value
    #checking default warranty of that country
    #if warranty value is > default and <48 months showing message with the required approver name
    #if warranty value >48 months showing message with the required approver name
    #Storing the approval level value to send SFDC
    #if opp_country is not None:  #Commented by Ishika
    if opp_country:  #Added by Ishika
        query = SqlHelper.GetFirst("SELECT * FROM CT_WARRANTY_DURATION WHERE Country = '"+str(opp_country)+"'")
        #if query.Warranty_Duration is not None:  #Commented by Ishika
        if query.Warranty_Duration:  #Added by Ishika
            default_warranty = str(query.Warranty_Duration)
            if int(warranty_type) == int(default_warranty):
                context.Quote.GetCustomField('CF_WarrantyApproval').Value = 'NONE' #Insert By Dhruv:CXCPQ-35214
                Trace.Write("True")
                #Log.Write(value+ str(CF_WarrantyApproval))
                #message = "Warranty Approval requested from DGM in NEX"
                message = lc_message
                #message2 = "Warranty Approval requested from HBS President in NEX"
                message2 = lc_message2
                exitmsg = context.Quote.Messages
                if exitmsg.Count > 0:
                    for msge in exitmsg:
                        if message in str(msge.Content):
                             context.Quote.DeleteMessage(msge.Id)
                        if message2 in str(msge.Content):
                             context.Quote.DeleteMessage(msge.Id)
            elif int(warranty_type) > int(default_warranty) and int(warranty_type) <= 48:
                #Trace.Write("Yes")
                context.Quote.GetCustomField('CF_WarrantyApproval').Value = rgm
                #message = "Warranty Approval requested from DGM in NEX"
                message = lc_message
                #message2 = "Warranty Approval requested from HBS President in NEX"
                message2 = lc_message2
                exitmsg = context.Quote.Messages
                if exitmsg.Count > 0:
                    for msge in exitmsg:
                        if message in str(msge.Content):
                             context.Quote.DeleteMessage(msge.Id)
                        if message2 in str(msge.Content):
                             context.Quote.DeleteMessage(msge.Id)
                context.Quote.AddMessage(message,MessageLevel.Warning,False)
            elif int(warranty_type)> 48 :
                context.Quote.GetCustomField('CF_WarrantyApproval').Value = hbs_President
                #message = "Warranty Approval requested from HBS President in NEX"
                message = lc_message
                #message2 = "Warranty Approval requested from DGM in NEX"
                message2 = lc_message2
                exitmsg = context.Quote.Messages
                if exitmsg.Count > 0:
                    for msge in exitmsg:
                        if message in str(msge.Content):
                             context.Quote.DeleteMessage(msge.Id)
                        if message2 in str(msge.Content):
                             context.Quote.DeleteMessage(msge.Id)
                context.Quote.AddMessage(message2,MessageLevel.Warning,False)