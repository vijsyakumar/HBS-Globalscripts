#-----------------------------------------------------------------------------
#			Change History Log
#-----------------------------------------------------------------------------
#Description:
#Script removes Old Error Message Created during ECC Order Integration
#-----------------------------------------------------------------------------
# Date			Name				Version		Comments(Changes done)
#-----------------------------------------------------------------------------
# 10/08/2022	Shweta Kandwal		0			Initial Creation
# 10/14/2022	MarripudiKrishna	7			-Replaced Hardcodings
#				Chaitanya						-Incorporated Translation
# 11/3/2022     Srijaydhurga        8           Script changes translations
#-----------------------------------------------------------------------------

#This function returns text/messages to CPI
import GM_TRANSLATIONS
lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)
lc_response = GM_TRANSLATIONS.GetText('000016', lv_LanguageKey, '', '', '', '', '')
lc_status = GM_TRANSLATIONS.GetText('000043', lv_LanguageKey, '', '', '', '', '')
lc_200 = GM_TRANSLATIONS.GetText('000051', lv_LanguageKey, '', '', '', '', '')
lc_msg = GM_TRANSLATIONS.GetText('000097', lv_LanguageKey, '', '', '', '', '')
lc_m1 = GM_TRANSLATIONS.GetText('000098', lv_LanguageKey, '', '', '', '', '')
lc_m2 = GM_TRANSLATIONS.GetText('000099', lv_LanguageKey, '', '', '', '', '')
lc_m3 = GM_TRANSLATIONS.GetText('000002', lv_LanguageKey, '', '', '', '', '')
#lc_op_type = GM_TRANSLATIONS.GetText('000024', lv_LanguageKey, '', '', '', '', '')
#if (context.Quote.GetCustomField('CF_Opportunity_Type').Value) == lc_op_type :
def data_update(Param):
    if Param.QuoteNumber:
        qt_err      = SqlHelper.GetTable('CT_ORDER_BOOKING_ERROR_LOGS')
        qt_err_list = SqlHelper.GetList(" SELECT * FROM CT_ORDER_BOOKING_ERROR_LOGS WHERE QUOTE_ID = '"+str(Param.QuoteNumber)+"' and LanguageKey='"+str(lv_LanguageKey)+"'")#Added By Srijaydhurga
        #Log.Info("=== Remove Error Log qt number ==="+str(Param.QuoteNumber))
        
        
        
        for row in qt_err_list:
           
            qt_err.AddRow(row)
            if qt_err:
                SqlHelper.Delete(qt_err)
                #return {"Response":[{"Status":"200","Message":"Old Messages removed from Error Log"}]}
                return {lc_response:[{lc_status:lc_200,lc_msg:lc_m1}]}
            else:
                #return {"Response":[{"Status":"200",""m:"No Old Records in Error Table"}]}
                return {lc_response:[{lc_status:lc_200,lc_msg:lc_m2}]}
    else:
        return lc_m3

    if Param is not None:
        data = data_update(Param)
        ApiResponse = ApiResponseFactory.JsonResponse(data)
