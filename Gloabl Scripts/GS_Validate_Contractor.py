# -----------------------------------------------------------------------------
#			Change History Log
# -----------------------------------------------------------------------------
# Description:
# Script to validate customer type for contractor and check the quote limit for 25k to throw the error message
# -----------------------------------------------------------------------------
# Date			Name				Version		Comments(Changes done)
# -----------------------------------------------------------------------------
# 11/4/2022    sreenivasa mucharla    0          -initial version
# 11/6/2022    Ishika BHattacharya	  3	        -Replaced Hardcodings
#										        -Incorporated Translation
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------

import GM_TRANSLATIONS    # Added by Ishika
from Scripting.Quote import MessageLevel
lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)  # Added by ishika
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '')  # Added by ishika

if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type:  # Added by ishika
    lc_msg = GM_TRANSLATIONS.GetText('000196', lv_LanguageKey, '', '', '', '', '')  # Added by ishika
    lc_contractor = GM_TRANSLATIONS.GetText('000197', lv_LanguageKey, '', '', '', '', '')  # Added by ishika

    def clear_error_message():
        exitmsgs = context.Quote.Messages
        if exitmsgs.Count > 0:
            for msges in exitmsgs:
                #if  "Quote value exceeds 25k for Contractor" in str(msges.Content):  #Commented by ishika
                if lc_msg in str(msges.Content):  #Added by ishika
                    context.Quote.DeleteMessage(msges.Id)

        customer_type = context.Quote.GetCustomField('CF_Customer_Type').Value
        total_sell_price = context.Quote.GetCustomField('CF_Total_Sell_Price').Value
        if total_sell_price:
            total_sell_price = float(total_sell_price)
        else:
            total_sell_price = 0
        #if customer_type == 'contractor' and total_sell_price > 25000.0 : #Commented by ishika
        if customer_type == lc_contractor and total_sell_price > 25000.0:  #Added by ishika
            # Log.Info("==== GS_Validate_Contractor Quote value exceeds 25k for contractor =====")
            # msg = "Quote value exceeds 25k for Contractor"  #Commented by ishika
            msg = lc_msg  #Added by ishika
            #context.Quote.AddMessage(msg,MessageLevel.Error,False)
