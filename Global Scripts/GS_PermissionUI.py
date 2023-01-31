#-----------------------------------------------------------------------------
#            Change History Log
#-----------------------------------------------------------------------------
#Description:
#This script is used for UI Permission for the Standard field, based on 
#the User Type & Status
#-----------------------------------------------------------------------------
# Date            Name                Version        Comments(Changes done)
#-----------------------------------------------------------------------------
# 06/16/2022    Ashutoshkumar Mishra       0             -Initial Version
# 10/18/2022    Ishika Bhattacharya        11            -Incorporated Translation
#03/11/2022     Srijaydhurga               12             -Script translation changes
#-----------------------------------------------------------------------------

from System.Net import WebRequest
from System.Text import Encoding
from System.Net import WebException
import GM_TRANSLATIONS    # Added by Ishika

lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)    # Added by Ishika
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '') # Added by Dhurga
if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type : #Added by Dhurga
    lv_Status = context.Quote.StatusName
    lv_UserType = User.UserType

    class GetPermissionUI():
        def GetPermissionUIsql(self,FieldProperty):
            if FieldProperty:
                lt_field_list = SqlHelper.GetList("Select FieldName from TAB_USERPERMISSIONUI WHERE UserType = '"+str(lv_UserType)+"' AND Status = '"+str(lv_Status)+"' AND Access = '"+str(FieldProperty)+"' and LanguageKey='"+str(lv_LanguageKey)+"'") #Added by Dhurga
                return lt_field_list