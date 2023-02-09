#-----------------------------------------------------------------------------
#            Change History Log
#-----------------------------------------------------------------------------
#Description:
#This action is for sending the proposal to current user' 
#-----------------------------------------------------------------------------
# Date            Name                Version        Comments(Changes done)
#-----------------------------------------------------------------------------
# 10/26/2022    Dhruv Bhatnagar           0             -Initial Version
# 11/05/2022	Dhruv Bhatnagar			  7			   -Tranlation corrections
# 12/22/2022    Payal Gupta               8            - Changes as per enhancement
#-----------------------------------------------------------------------------

import clr

clr.AddReference('System.Xml')

from System.Xml import XmlDocument

from System import DateTime, Random

import re

import clr

clr.AddReference("System.Net")

from System.Net import Mail,NetworkCredential

from System.Net.Mail import SmtpClient, Attachment, MailMessage, MailAddress

import GM_TRANSLATIONS    # Added by Ishika

lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)  
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '') #Modified by Dhruv

if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type : #Modified by Dhruv


    fromStr = User.Email

    fromUsername = User.Name
    ProposalName = str(context.Quote.GetCustomField('CF_ProposalName').AttributeValue) #Modified by Payal

    toStr = fromStr

    toUsername = fromStr

    subjectStr = ProposalName 

    bodyStr =  ProposalName

    context.Quote.GenerateDocument(ProposalName, GenDocFormat.PDF)
    fileContent = context.Quote.GetLatestGeneratedDocumentStream()
    fileName =    context.Quote.GetLatestGeneratedDocumentFileName()
    document = Attachment(fileContent, fileName)
    #att = Attachment(FileHelper.GetStreamFromPath('images/ajax.gif'), 'image.gif')

    if fromStr != "" and toStr != "":
        mailAddrFrom = MailAddress(fromStr,fromUsername)
        mailAddrTo = MailAddress(toStr,toUsername)
        mailObj = MailMessage( mailAddrFrom, mailAddrTo)
        mailObj.IsBodyHtml = True;
        mailObj.Subject = subjectStr
        mailObj.Body = bodyStr
        smtpServer = SmtpClient("10.150.65.7")
        #mailObj.Attachments.Add(att)
        mailObj.Attachments.Add(document)
        smtpServer.Send(mailObj)