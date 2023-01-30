#-----------------------------------------------------------------------------
#            Change History Log
#-----------------------------------------------------------------------------
#Description:
#This script is used for selecting all uploaded valid parts
#-----------------------------------------------------------------------------
# Date            Name                Version        Comments(Changes done)
#-----------------------------------------------------------------------------
# 08/06/2022    AshutoshKumar Mishra       0             -Initial Version
# 10/18/2022    Ishika Bhattacharya        3             -Incorporated Translation
# 11/04/2022	Dhruv				   	   4		     -Transacrtion type
#												          check implemented
#-----------------------------------------------------------------------------

import GM_TRANSLATIONS    # Added by Ishika

lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)  # Added by Ishika
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '') #Modified by Dhruv
if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type:  #Modified by Dhruv
    validPartsCon = Product.GetContainerByName("AR_Product_Upload_Valid")

    if validPartsCon:
        if Product.Attr('AR_SelectValidParts').SelectedValue:
            validPartsCon.MakeAllRowsSelected()
        else:
            for row in validPartsCon.Rows:
                row.IsSelected = False
        validPartsCon.Calculate()
