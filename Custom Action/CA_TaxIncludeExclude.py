#-----------------------------------------------------------------------------
#			Change History Log
#-----------------------------------------------------------------------------
#Description:
#Tax value computed only for testing purpose - it will be fetched from ECC
#-----------------------------------------------------------------------------
# Date			Name				Version		Comments(Changes done)
#-----------------------------------------------------------------------------
# 01/04/2023     Aditi                  0         -initial version
# 02/01/2023     Aditi                            -removed all rounding
#-----------------------------------------------------------------------------

#**********Tax value computed only for testing purpose - it will be fetched from ECC************
#context.Quote.GetCustomField('CF_TotalTax').Value = float(context.Quote.Totals.Amount)*0.07
#***********************************************************************************************
import GM_TRANSLATIONS

#Get user launguage from dictionary
lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '') #Modified by Dhruv


if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type:  #Modified by Dhruv
    lc_inc_tax = GM_TRANSLATIONS.GetText('000113', lv_LanguageKey, '', '', '', '', '')
    lc_exc_tax = GM_TRANSLATIONS.GetText('000114', lv_LanguageKey, '', '', '', '', '')
    #context.Quote.GetCustomField('CF_TaxIncludedAmount').Value = round(float(context.Quote.GetCustomField('CF_Total_Sell_Price').Value),2) #Commented by Payal
    taxInfo = context.Quote.GetCustomField('Tax').Value
    sellPrice = context.Quote.GetCustomField('CF_Total_Sell_Price').Value
    totalTax = context.Quote.GetCustomField('CF_TotalTax').Value


    if taxInfo:
        #if taxInfo == "Include Tax" and totalTax:
        if taxInfo == lc_inc_tax and totalTax!='': #Edited by Payal
            #total_value = round(float(sellPrice) + float(totalTax),2) #Added by Payal #Commented by Aditi 1stFeb2023 to remove rounding
            total_value = float(sellPrice) + float(totalTax)
            context.Quote.GetCustomField('CF_TaxIncludedAmount').Value = "%.2f" % total_value #Edited by Payal
        elif taxInfo == lc_inc_tax and totalTax == '':
            #context.Quote.GetCustomField('CF_TaxIncludedAmount').Value =  "%.2f" %(round(float(sellPrice),2)) #Edited by Payal #Commented by Aditi 1stFeb2023 to remove rounding
            context.Quote.GetCustomField('CF_TaxIncludedAmount').Value =  "%.2f" %(float(sellPrice))
        #elif taxInfo == "Exclude Tax":
        elif taxInfo == lc_exc_tax :
            #context.Quote.GetCustomField('CF_TaxIncludedAmount').Value = "%.2f" %(round(float(sellPrice),2)) #Edited by Payal #Commented by Aditi 1stFeb2023 to remove rounding
            context.Quote.GetCustomField('CF_TaxIncludedAmount').Value = "%.2f" %(float(sellPrice))
    else:
        #context.Quote.GetCustomField('CF_TaxIncludedAmount').Value = "%.2f" %(round(float(sellPrice),2)) #Edited by Payal #Commented by Aditi 1stFeb2023 to remove rounding
        context.Quote.GetCustomField('CF_TaxIncludedAmount').Value = "%.2f" %(float(sellPrice))


    #Trace.Write(str(context.Quote.Totals.Amount)+str(type(context.Quote.GetCustomField('CF_TaxIncludedAmount').Value))+str(context.Quote.GetCustomField('CF_TaxIncludedAmount').Value))