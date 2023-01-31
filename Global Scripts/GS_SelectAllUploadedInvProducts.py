#-----------------------------------------------------------------------------
#            Change History Log
#-----------------------------------------------------------------------------
#Description:
#This script is used for selecting all uploaded invalid parts
#-----------------------------------------------------------------------------
# Date            Name                Version        Comments(Changes done)
#-----------------------------------------------------------------------------
# 07/25/2022    AshutoshKumar Mishra       0             -Initial Version
# 10/18/2022    Ishika Bhattacharya        2             -Incorporated Translation
# 11/04/2022	Dhruv				   	   3			 -Transacrtion type
#												 		  check implemented
#-----------------------------------------------------------------------------


import GM_TRANSLATIONS    # Added by Ishika

lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)  # Added by Ishika
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '') #Modified by Dhruv
if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type:  #Modified by Dhruv
    InvalidPartsCon = Product.GetContainerByName("AR_Product_Upload_Invalid")


    if InvalidPartsCon:
        if Product.Attr('AR_SelectInValidParts').SelectedValue:
            InvalidPartsCon.MakeAllRowsSelected()
        else:
            for row in InvalidPartsCon.Rows:
                row.IsSelected = False
        InvalidPartsCon.Calculate()
