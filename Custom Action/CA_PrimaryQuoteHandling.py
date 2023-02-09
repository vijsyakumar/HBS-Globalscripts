#-----------------------------------------------------------------------------
#            Change History Log
#-----------------------------------------------------------------------------
#Description:
#This script is used for primary quote handling functionality
#-----------------------------------------------------------------------------
# Date            Name                Version        Comments(Changes done)
#-----------------------------------------------------------------------------
# 10/05/2022    Anil Poply                 0             -Initial Version
# 10/19/2022    Ishika Bhattacharya        1             -Incorporated Translation
# 11/04/2022	Srinivasan Dorairaj		   2			 -Script Translation changes
#-----------------------------------------------------------------------------

import GM_TRANSLATIONS    # Added by Ishika

lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)  # Added by Ishika
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '') #Modified by Srinivasan Dorairaj

primaryquote = int(context.Quote.GetCustomField("CF_Opportunity_PrimaryQuote").Value)

if primaryquote != '' and context.Quote.GetCustomField("CF_PrimaryKey").Value == 'false' or context.Quote.GetCustomField("CF_PrimaryKey").Value == '':
    primaryQuote = QuoteHelper.Get(primaryquote)
    primaryQuote.GetCustomField("CF_PrimaryKey").Value = 'false'
    primaryQuote.Save()