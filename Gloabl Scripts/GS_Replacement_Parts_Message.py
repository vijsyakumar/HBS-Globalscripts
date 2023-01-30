#-----------------------------------------------------------------------------
#			Change History Log
#-----------------------------------------------------------------------------
#Description:
#This script remove the Product Upload container from quote cart items
#-----------------------------------------------------------------------------
# Date			Name				Version		Comments(Changes done)
#-----------------------------------------------------------------------------
# 7/4/2022      Ayush                  0         -initial version
#
# 10/14/2022	Abhilash		       1		 -Replaced Hardcodings
#												 -Incorporated Translation
# 11/04/2022	Dhruv				   7   		 -SQL translation,Transacrtion type
#												  check implemented
#-----------------------------------------------------------------------------

from Scripting.Quote import MessageLevel
import GM_TRANSLATIONS
lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '') #Modified by Dhruv
if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type:  #Modified by Dhruv
    curr_date = DateTime.Now
    str_date = str(curr_date)
    expectedcurrent_date = str_date.split()
    current_date = expectedcurrent_date[0]

    query = SqlHelper.GetList("SELECT * FROM CT_REPLACEMENT_PARTS WHERE LanguageKey='{}'".format(lv_LanguageKey)) #Modified by Dhruv
    #if query:
    for inn in query:
        org_nbr = inn.Original_Part_Number


        for i in context.Quote.GetAllItems():
            part_nbr = i.PartNumber


            if i.PartNumber == inn.Original_Part_Number:


                replace_date = str(inn.Date_Of_Replacement)
                splitreplace_date = replace_date.split()
                replacement_date = splitreplace_date[0]

                #msg = 'This product has been expired, there is a replacement part available"'+str(inn.Replacement_Part_Number)+'" '
                msg = GM_TRANSLATIONS.GetText('000012', lv_LanguageKey, str(inn.Replacement_Part_Number), '', '', '', '')
                if current_date >= replacement_date:

                    context.Quote.AddMessage(msg,MessageLevel.Warning,False)