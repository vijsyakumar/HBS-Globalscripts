#-----------------------------------------------------------------------------
#Description:
#   This script is used for Submit for BSC Process
#-----------------------------------------------------------------------------
# Date            Name                Version        Comments(Changes done)
#-----------------------------------------------------------------------------
# 11/13/2022    Shweta Kandwal             0             -Initial Version
#12/20/2022     Srijaydhurga                             -CXCPQ-35141
#01/19/2023     Sanket Mhapsekar                         -CXCPQ-33607
#-----------------------------------------------------------------------------

##Added by Aditi for maximum approval level
import datetime
from Scripting.Quote import MessageLevel
import GM_TRANSLATIONS    # Added by Ishika
lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)  # Added by Ishika
#lc_op_type = GM_TRANSLATIONS.GetText('000024', lv_LanguageKey, '', '', '', '', '') #commented by Aditi 1st Nov 2022
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '') #added by Aditi 1st Nov 2022
lc_partsOnly = GM_TRANSLATIONS.GetText('000019', lv_LanguageKey, '', '', '', '', '') #added by Aditi 17 Jan 2023

#if (context.Quote.GetCustomField('CF_Opportunity_Type').Value) == lc_op_type:  # Added by Ishika #commented by Aditi 1st Nov 2022
if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type : #added by Aditi 1st Nov 2022
    lc_Auto = GM_TRANSLATIONS.GetText('000158', lv_LanguageKey, '', '', '', '', '') # Added by Ishika
    lc_approved = GM_TRANSLATIONS.GetText('000071', lv_LanguageKey, '', '', '', '', '') # Added by Ishika
    lc_true = GM_TRANSLATIONS.GetText('000159', lv_LanguageKey, '', '', '', '', '') # Added by Ishika
    lc_False = GM_TRANSLATIONS.GetText('000068', lv_LanguageKey, '', '', '', '', '') # Added by Ishika
    lc_functional_approval_InProgress = GM_TRANSLATIONS.GetText('000160', lv_LanguageKey, '', '', '', '', '') # Added by Ishika
    lc_Y = GM_TRANSLATIONS.GetText('000189', lv_LanguageKey, '', '', '', '', '')
    lc_status_ready_for_approval = GM_TRANSLATIONS.GetText('000044', lv_LanguageKey, '', '', '', '', '') # Added by Ishika

    ###########Added by Sreenivas###########################################
    def clear_func_approval_message():
        exitmsgs = context.Quote.Messages
        if exitmsgs.Count > 0:
            for msges in exitmsgs:
                #if  "Functional Approval is in Progress" in str(msges.Content):  #Commented by Ishika
                if lc_functional_approval_InProgress in str(msges.Content):  #Added by Ishika
                    context.Quote.DeleteMessage(msges.Id)

    quoteid = context.Quote.Id
    #Trace.Write("=== Request for Approval quoteid===="+str(quoteid))
    approvalStatusFlag = True
    funcApprovalRecords = SqlHelper.GetList("SELECT * FROM CT_QUOTE_FUNC_APPROVAL where QuoteId ={0}".format(quoteid))#Corrected by Dhruv
    if funcApprovalRecords:
        for record in funcApprovalRecords:
            if (record.Required.lower() == lc_true and record.Approval_Status != lc_approved):#Added by Ishika below 5 lines added by sanket for ignore CXCPQ-33607
                approvalStatusFlag = lc_False
                break
    if approvalStatusFlag == lc_False:
        #throw error message
        msg = lc_functional_approval_InProgress   #Added by Ishika
        clear_func_approval_message()
        context.Quote.AddMessage(msg,MessageLevel.Error,lc_False)
    else:
        #Log.Info("=== Request for Approval else logic start====")
        clear_func_approval_message()
        #####################################################################
        lc_msg3 = GM_TRANSLATIONS.GetText('000206', lv_LanguageKey, '', '', '', '', '')
        #CXCPQ-35141 start
        lc_msg17 = GM_TRANSLATIONS.GetText('000217', lv_LanguageKey, '', '', '', '', '')

        def clearmsg():
            exitmsgs = context.Quote.Messages
            if exitmsgs.Count > 0:
                for msges in exitmsgs:
                    if  str(msges.Content):
                        context.Quote.DeleteMessage(msges.Id)


        if (context.Quote.GetCustomField('CF_Original_RQ_Sales_Order').Value is  None or context.Quote.GetCustomField('CF_Original_RQ_Sales_Order').Value =='') and context.Quote.GetCustomField('CF_Opportunity_Sub-type').Value in ('Variation Add','Variation Deduct'):
            context.Quote.AddMessage(lc_msg3,MessageLevel.Warning,False)#RQ sales order#CXCPQ-37836 start

        now = datetime.datetime.now()    
        if (context.Quote.GetCustomField('CF_Opportunity_Sub-type').Value and context.Quote.GetCustomField('CF_Customer_PO_Number').Value and context.Quote.GetCustomField('CF_PO_Date').Value and  context.Quote.GetCustomField('CF_Honeywell_Signed_Date').Value and context.Quote.GetCustomField('CF_Customer_Signed_Date').Value and context.Quote.GetCustomField('CF_Order_Reason_Booking').Value and context.Quote.GetCustomField('CF_Required_Delivery_Date').Value):
            if context.Quote.GetCustomField('CF_Opportunity_Sub-type').Value in ('Variation Add','Variation Deduct') and context.Quote.GetCustomField('CF_Original_RQ_Sales_Order').Value:
                clearmsg()
                context.Quote.AddMessage(lc_msg17,MessageLevel.Warning,False)
                context.Quote.GetCustomField("CF_BSC_Timestamp").Value = now.strftime("%Y/%m/%dT%H:%M:%S 000+0000")
                
            elif context.Quote.GetCustomField('CF_Opportunity_Sub-type').Value == 'New' and context.Quote.GetCustomField('CF_Opportunity_Sub-type').Value not in ('Variation Add','Variation Deduct'):
                clearmsg()
                context.Quote.AddMessage(lc_msg17,MessageLevel.Warning,False)
                context.Quote.GetCustomField("CF_BSC_Timestamp").Value = now.strftime("%Y/%m/%dT%H:%M:%S 000+0000")
            else:
                context.Quote.GetCustomField("CF_BSC_Timestamp").Value = ''
        else:
            context.Quote.GetCustomField("CF_BSC_Timestamp").Value = ""
            Log.Info('Booking request Failure---')#CXCPQ-35141 end   