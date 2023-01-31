# -----------------------------------------------------------------------------
#			Change History Log
# -----------------------------------------------------------------------------
# Description:
# This script assigns non removale writeins to quote table QT_Quote_Summary
# -----------------------------------------------------------------------------
# Date			Name				Version		Comments(Changes done)
# -----------------------------------------------------------------------------
# 10/18/2022    AshutoshKumar Mishra  0         -initial version
# 11/5/2022  	Ishika BHattacharya	  6	        -Replaced Hardcodings
#										        -Incorporated Translation
# 12/04/2023 	Ashutosh Mishra					-Changes done for Roll Up & Event add
# 01/30/2023     Sumandrita						- Introduced 'QI_Category' to incorporated changes for CXCPQ-38244
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
from Scripting.Quote import MessageLevel
import GM_TRANSLATIONS  # Added by ishika

lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)  # Added by ishika
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '')  # Added by ishika

lv_transtype = context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value



lc_lang_des = GM_TRANSLATIONS.GetText('000064', lv_LanguageKey, '', '', '', '', '')
quote_status_ID = context.Quote.StatusId #Added by Aditi 14th Jan

try:
	_LanguageDescription = context.Quote.GetCustomField("CF_Language").AttributeValue
except:
    _LanguageDescription = lc_lang_des



if _LanguageDescription == "":
    _LanguageDescription = lc_lang_des

    
_LanguageKey = SqlHelper.GetFirst("SELECT * FROM CT_MASTER_LANGUAGES WHERE LanguageDescription = '{}'".format(_LanguageDescription))
if _LanguageKey:
    _OpportunityType = context.Quote.GetCustomField("CF_Opportunity_Type").Value
    _TransactionType = SqlHelper.GetFirst("SELECT * FROM CT_TRANSACTION_TYPE WHERE LanguageKey = '{0}' and OpportunityType = '{1}' ".format(_LanguageKey.LanguageKey, _OpportunityType))
    if _TransactionType:
        context.Quote.GetCustomField("CF_TRANSACTION_TYPE").Value = _TransactionType.TransactionType


lv_Remvbl = ""
#Log.Info("=== CF_Country ==="+str(context.Quote.GetCustomField('CF_Country').Value))
#Log.Info("=== CF_TRANSACTION_TYPE ==="+str(context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value))
if ((context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value == lc_trans_type) or (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value == "")) and quote_status_ID==32:  # Added by Ishika
    Log.Write("=======RQ--True=======")

    lc_Consumables = GM_TRANSLATIONS.GetText('000177', lv_LanguageKey, '', '', '', '', '') # Added by Ishika
    lc_Travel = GM_TRANSLATIONS.GetText('000178', lv_LanguageKey, '', '', '', '', '')   # Added by Ishika
    lc_Travel_exp = GM_TRANSLATIONS.GetText('000225', lv_LanguageKey, '', '', '', '', '')   # Added by Ishika
    lc_Environmental = GM_TRANSLATIONS.GetText('000179', lv_LanguageKey, '', '', '', '', '')   # Added by Ishika
    lc_Administartion_Fee = GM_TRANSLATIONS.GetText('000180', lv_LanguageKey, '', '', '', '', '')   # Added by Ishika
    lc_None = GM_TRANSLATIONS.GetText('000108', lv_LanguageKey, '', '', '', '', '')   # Added by Ishika
    lc_False = GM_TRANSLATIONS.GetText('000068', lv_LanguageKey, '', '', '', '', '')   # Added by Ishika
    lc_Others = GM_TRANSLATIONS.GetText('000215', lv_LanguageKey, '', '', '', '', '')
    lc_extra = GM_TRANSLATIONS.GetText('000121', lv_LanguageKey, '', '', '', '', '')
    lc_mand = GM_TRANSLATIONS.GetText('000213', lv_LanguageKey, '', '', '', '', '')
    lc_travel_typ = GM_TRANSLATIONS.GetText('000085', lv_LanguageKey, '', '', '', '', '')
    lc_man_item = GM_TRANSLATIONS.GetText('000227', lv_LanguageKey, '', '', '', '', '')

    # lv_consumable = "Consumables"  # Commented by Ishika
    lv_consumable = lc_Consumables   # Added by Ishika
    #lv_Travel = "Travel"            # Commented by Ishika
    lv_Travel = lc_Travel            # Added by Ishika
    #lv_env = "Environmental"        #Commeneted by Ishika
    lv_env = lc_Environmental        # Added by Ishika
    #lv_admin = "Administartion Fee" #Commented by Ishika
    lv_admin = lc_Administartion_Fee # Added by Ishika

    # lv_type = {"Consumables", "Travel", "Environmental", "Administartion Fee"}       #Commented by Ishika
    lv_type = {lc_Consumables, lc_Travel, lc_Environmental, lc_Administartion_Fee}     # Added by Ishika

    # lv_add = None    #Commented by Ishika
    lv_add = lc_None   # Added by Ishika

    lv_country = context.Quote.GetCustomField('CF_Country').Value
    """check_MANDCHARGES = False
    for qi in context.Quote.GetAllItems():
        if qi.ProductSystemId in ['RQ_Mandatory_Charges_cpq']:
            check_MANDCHARGES = True
    if not check_MANDCHARGES:
        context.Quote.GetCustomField('CF_NonRemovable').Value = ""
    else:
        context.Quote.GetCustomField('CF_NonRemovable').Value = "Done"
    lv_Remvbl = context.Quote.GetCustomField('CF_NonRemovable').Value
    quote_currency = context.Quote.GetCustomField('CF_Quote_Currency').Value
    Log.Info("=== CF_Country ==="+str(lv_country))"""
    
    lv_Remvbl = context.Quote.GetCustomField('CF_NonRemovable').Value
    quote_currency = context.Quote.GetCustomField('CF_Quote_Currency').Value

    if lv_country and context.Quote.GetAllItems().Count == 0:
        Log.Write("=======lv_Remvbl--True=======")
        NonRem = context.Quote.AddItem(int(lc_man_item),int(1))
        NonRem['QI_PROD_CATEGORY'] = lc_mand
        Log.Write("=======lv_Remvbl--ADDED=======")
        context.Quote.GetCustomField('CF_NonRemovable').Value = "Done"
        for child_item in context.Quote.GetItemByItemId(NonRem.Id).AsMainItem.GetChildItems():
            
                        
            if child_item.RolledUpQuoteItem == "1.1":
                sellPrice = 0
                ls_cons_nonremoval = SqlHelper.GetFirst("Select * from CT_NONREMOVAL_WRITEIN WHERE COUNTRY = '{}' and WRITEIN_TYPE = '{}' and LanguageKey = '{}'".format(lv_country, lv_consumable, lv_LanguageKey))
                
                child_item['QI_Product_Type'] = lc_extra #str(ls_cons_nonremoval.WRITEIN_TYPE)
                child_item['QI_PROD_CATEGORY']  = lc_Others
                child_item['QI_Category']  = lc_Others
                child_item.PartNumber = str(ls_cons_nonremoval.WRITEIN_TYPE)
                child_item.Description = str(ls_cons_nonremoval.WRITEIN_TYPE)
                child_item['QI_Description'] = str(ls_cons_nonremoval.WRITEIN_TYPE)
                child_item.NetPrice = float(ls_cons_nonremoval.PRICE) #* float(child_item['QI_Exchange_Rate'])
                child_item['QI_Final_Sell_Price'] = float(ls_cons_nonremoval.PRICE) #* float(child_item['QI_Exchange_Rate'])
                child_item['QI_List_Price'] = float(0) #float(ls_cons_nonremoval.PRICE)
                child_item.DiscountPercent = float(0)
                child_item.DiscountAmount = float(0)
                child_item['QI_Cost_Currency'] = str(quote_currency)
                #child_item['QI_Exchange_Rate'] = float(0)
                child_item['QI_WTW_COST'] = float(0)
                child_item['QI_UNIT_WTW_COST'] = float(0)
                child_item['QI_WTW_Margin'] = float(0)
                child_item['QI_MARGIN_AMOUNT'] = float(ls_cons_nonremoval.PRICE)
                child_item['QI_MARGIN_PERCENTAGE'] = float(100)
                #NonRem['QI_MARGIN_PERCENTAGE'] = float(100)
                sellPrice += child_item.NetPrice
                NonRem.NetPrice  += child_item.NetPrice
                NonRem['QI_Final_Sell_Price']  += child_item.NetPrice
                
            
            elif child_item.RolledUpQuoteItem == "1.2":        
                ls_travel_nonremoval = SqlHelper.GetFirst("Select * from CT_NONREMOVAL_WRITEIN WHERE COUNTRY = '{}' and WRITEIN_TYPE = '{}' and LanguageKey = '{}'".format(lv_country, lv_Travel, lv_LanguageKey))
                
                child_item['QI_Product_Type'] = lc_travel_typ #str(ls_travel_nonremoval.WRITEIN_TYPE)
                child_item['QI_PROD_CATEGORY']  = lc_Travel_exp
                child_item['QI_Category']  = lc_Travel_exp
                child_item.PartNumber = str(ls_travel_nonremoval.WRITEIN_TYPE)
                child_item.Description = str(ls_travel_nonremoval.WRITEIN_TYPE)
                child_item['QI_Description'] = str(ls_travel_nonremoval.WRITEIN_TYPE)
                child_item.NetPrice = float(ls_travel_nonremoval.PRICE) #* float(child_item['QI_Exchange_Rate'])
                child_item['QI_Final_Sell_Price'] = float(ls_travel_nonremoval.PRICE) #* float(child_item['QI_Exchange_Rate'])
                child_item['QI_List_Price'] = float(0) #float(ls_cons_nonremoval.PRICE)
                child_item.DiscountPercent = float(0)
                child_item.DiscountAmount = float(0)
                child_item['QI_Cost_Currency'] = str(quote_currency)
                #child_item['QI_Exchange_Rate'] = float(0)
                child_item['QI_WTW_COST'] = float(0)
                child_item['QI_UNIT_WTW_COST'] = float(0)
                child_item['QI_WTW_Margin'] = float(0)
                child_item['QI_MARGIN_AMOUNT'] = float(ls_travel_nonremoval.PRICE)
                child_item['QI_MARGIN_PERCENTAGE'] = float(100)
                sellPrice += child_item.NetPrice
                NonRem.NetPrice  += child_item.NetPrice
                NonRem['QI_Final_Sell_Price']  += child_item.NetPrice
                
            elif child_item.RolledUpQuoteItem == "1.3":
                ls_env_nonremoval = SqlHelper.GetFirst("Select * from CT_NONREMOVAL_WRITEIN WHERE COUNTRY = '{}' and WRITEIN_TYPE = '{}' and LanguageKey = '{}'".format(lv_country, lv_env, lv_LanguageKey))
                
                child_item['QI_Product_Type'] = lc_extra #str(ls_env_nonremoval.WRITEIN_TYPE)
                child_item['QI_PROD_CATEGORY']  = lc_Others
                child_item['QI_Category']  = lc_Others
                child_item.PartNumber = str(ls_env_nonremoval.WRITEIN_TYPE)
                child_item.Description = str(ls_env_nonremoval.WRITEIN_TYPE)
                child_item['QI_Description'] = str(ls_env_nonremoval.WRITEIN_TYPE)
                child_item.NetPrice = float(ls_env_nonremoval.PRICE) #* float(child_item['QI_Exchange_Rate'])
                child_item['QI_Final_Sell_Price'] = float(ls_env_nonremoval.PRICE) #* float(child_item['QI_Exchange_Rate'])
                child_item['QI_List_Price'] = float(0) #float(ls_cons_nonremoval.PRICE)
                child_item.DiscountPercent = float(0)
                child_item.DiscountAmount = float(0)
                child_item['QI_Cost_Currency'] = str(quote_currency)
                #child_item['QI_Exchange_Rate'] = float(0)
                child_item['QI_WTW_COST'] = float(0)
                child_item['QI_UNIT_WTW_COST'] = float(0)
                child_item['QI_WTW_Margin'] = float(0)
                child_item['QI_MARGIN_AMOUNT'] = float(ls_env_nonremoval.PRICE)
                child_item['QI_MARGIN_PERCENTAGE'] = float(100)
                sellPrice += child_item.NetPrice
                NonRem.NetPrice  += child_item.NetPrice
                NonRem['QI_Final_Sell_Price']  += child_item.NetPrice
                
            elif child_item.RolledUpQuoteItem == "1.4":
                ls_adm_nonremoval = SqlHelper.GetFirst("Select * from CT_NONREMOVAL_WRITEIN WHERE COUNTRY = '{}' and WRITEIN_TYPE = '{}' and LanguageKey = '{}'".format(lv_country,lv_admin, lv_LanguageKey))
                
                child_item['QI_Product_Type'] = lc_extra #str(ls_adm_nonremoval.WRITEIN_TYPE)
                child_item['QI_PROD_CATEGORY']  = lc_Others
                child_item['QI_Category']  = lc_Others
                child_item.PartNumber = str(ls_adm_nonremoval.WRITEIN_TYPE)
                child_item.Description = str(ls_adm_nonremoval.WRITEIN_TYPE)
                child_item['QI_Description'] = str(ls_adm_nonremoval.WRITEIN_TYPE)
                child_item.NetPrice = float(ls_adm_nonremoval.PRICE) #* float(child_item['QI_Exchange_Rate'])
                child_item['QI_Final_Sell_Price'] = float(ls_adm_nonremoval.PRICE) #* float(child_item['QI_Exchange_Rate'])
                child_item['QI_List_Price'] = float(0) #float(ls_cons_nonremoval.PRICE)
                child_item.DiscountPercent = float(0)
                child_item.DiscountAmount = float(0)
                child_item['QI_Cost_Currency'] = str(quote_currency)
                #child_item['QI_Exchange_Rate'] = float(0)
                child_item['QI_WTW_COST'] = float(0)
                child_item['QI_UNIT_WTW_COST'] = float(0)
                child_item['QI_WTW_Margin'] = float(0)
                child_item['QI_MARGIN_AMOUNT'] = float(ls_adm_nonremoval.PRICE)
                child_item['QI_MARGIN_PERCENTAGE'] = float(100)
                NonRem['QI_MARGIN_PERCENTAGE'] = float(100)
                sellPrice += child_item.NetPrice
                NonRem['QI_Cost_Currency'] = str(quote_currency)
                NonRem['QI_WTW_Margin'] = float(0)
                NonRem.NetPrice  += child_item.NetPrice
                NonRem['QI_Final_Sell_Price']  += child_item.NetPrice
                NonRem['QI_MARGIN_AMOUNT'] = float(NonRem['QI_Final_Sell_Price'])
                
                abc = sellPrice
                context.Quote.GetCustomField("CF_Total_Sell_Price").Value = sellPrice
                
                
    elif lv_country and lv_Remvbl == "Done":
        for i in context.Quote.GetAllItems():
            if i.ProductSystemId == "RQ_Mandatory_Charges_cpq":
                sellPrice = 0
                lv_net_price = 0
                lv_final_price = 0
                #i.NetPrice = float(0)
                #i['QI_Final_Sell_Price'] = float(0)
                
                for child_item in context.Quote.GetItemByItemId(i.Id).AsMainItem.GetChildItems():
                    
                    child_item['QI_WTW_Margin'] = float(0)
                    i['QI_WTW_Margin'] = float(0)
                    #child_item['QI_MARGIN_AMOUNT'] = float(0)
                    #child_item['QI_MARGIN_PERCENTAGE'] = float(0)
                    
                    
                    if child_item.RolledUpQuoteItem == "1.1":
                        
                        child_item['QI_PROD_CATEGORY']  = lc_Others
                        child_item['QI_Category']  = lc_Others
                        child_item['QI_Product_Type'] = lc_extra
                        
                        
                        ls_cons_nonremoval = SqlHelper.GetFirst("Select * from CT_NONREMOVAL_WRITEIN WHERE COUNTRY = '{}' and WRITEIN_TYPE = '{}' and LanguageKey = '{}'".format(lv_country, lv_consumable, lv_LanguageKey))
                        
                        child_item.NetPrice = float(ls_cons_nonremoval.PRICE) * float(child_item['QI_Exchange_Rate'])
                        child_item['QI_Final_Sell_Price'] = float(ls_cons_nonremoval.PRICE) * float(child_item['QI_Exchange_Rate'])
                        child_item['QI_MARGIN_AMOUNT'] = float(child_item.NetPrice)
                        child_item['QI_MARGIN_PERCENTAGE'] = float(100)
                        child_item['QI_Mand_Charges_Validation'] = "True" #added by Sumandrita
                        sellPrice += child_item.NetPrice
                        lv_net_price  += child_item.NetPrice
                        lv_final_price  += child_item['QI_Final_Sell_Price']
                        
                    elif child_item.RolledUpQuoteItem == "1.2": 
                        child_item['QI_PROD_CATEGORY']  = lc_Travel_exp
                        child_item['QI_Category']  = lc_Travel_exp
                        child_item['QI_Product_Type'] = lc_travel_typ
                        
                        ls_cons_nonremoval = SqlHelper.GetFirst("Select * from CT_NONREMOVAL_WRITEIN WHERE COUNTRY = '{}' and WRITEIN_TYPE = '{}' and LanguageKey = '{}'".format(lv_country, lv_Travel, lv_LanguageKey))
                        
                        child_item.NetPrice = float(ls_cons_nonremoval.PRICE) * float(child_item['QI_Exchange_Rate'])
                        child_item['QI_Final_Sell_Price'] = float(ls_cons_nonremoval.PRICE) * float(child_item['QI_Exchange_Rate'])
                        child_item['QI_MARGIN_AMOUNT'] = float(child_item.NetPrice)
                        child_item['QI_MARGIN_PERCENTAGE'] = float(100)
                        child_item['QI_Mand_Charges_Validation'] = "True" #added by Sumandrita
                        sellPrice += child_item.NetPrice
                        lv_net_price  += child_item.NetPrice
                        lv_final_price  += child_item['QI_Final_Sell_Price']
                            
                    elif child_item.RolledUpQuoteItem == "1.3":
                        
                        child_item['QI_PROD_CATEGORY']  = lc_Others
                        child_item['QI_Category']  = lc_Others
                        child_item['QI_Product_Type'] = lc_extra
                        
                        ls_cons_nonremoval = SqlHelper.GetFirst("Select * from CT_NONREMOVAL_WRITEIN WHERE COUNTRY = '{}' and WRITEIN_TYPE = '{}' and LanguageKey = '{}'".format(lv_country, lv_env, lv_LanguageKey))
                        
                        child_item.NetPrice = float(ls_cons_nonremoval.PRICE) * float(child_item['QI_Exchange_Rate'])
                        child_item['QI_Final_Sell_Price'] = float(ls_cons_nonremoval.PRICE) * float(child_item['QI_Exchange_Rate'])
                        child_item['QI_MARGIN_AMOUNT'] = float(child_item.NetPrice)
                        child_item['QI_MARGIN_PERCENTAGE'] = float(100)
                        child_item['QI_Mand_Charges_Validation'] = "True" #added by Sumandrita
                        sellPrice += child_item.NetPrice
                        lv_net_price  += child_item.NetPrice
                        lv_final_price  += child_item['QI_Final_Sell_Price']
                            
                    elif child_item.RolledUpQuoteItem == "1.4":
                        
                        child_item['QI_PROD_CATEGORY']  = lc_Others
                        child_item['QI_Category']  = lc_Others
                        child_item['QI_Product_Type'] = lc_extra
                        
                        ls_cons_nonremoval = SqlHelper.GetFirst("Select * from CT_NONREMOVAL_WRITEIN WHERE COUNTRY = '{}' and WRITEIN_TYPE = '{}' and LanguageKey = '{}'".format(lv_country, lv_admin, lv_LanguageKey))
                        
                        child_item.NetPrice = float(ls_cons_nonremoval.PRICE) * float(child_item['QI_Exchange_Rate'])
                        child_item['QI_Final_Sell_Price'] = float(ls_cons_nonremoval.PRICE) * float(child_item['QI_Exchange_Rate'])
                        child_item['QI_MARGIN_AMOUNT'] = float(child_item.NetPrice)
                        child_item['QI_MARGIN_PERCENTAGE'] = float(100)
                        child_item['QI_Mand_Charges_Validation'] = "True" #added by Sumandrita
                        sellPrice += child_item.NetPrice
                        lv_net_price  += child_item.NetPrice
                        lv_final_price  += child_item['QI_Final_Sell_Price']
                
                i.NetPrice = float(lv_net_price)
                i['QI_MARGIN_AMOUNT'] = float(i.NetPrice)
                i['QI_MARGIN_PERCENTAGE'] = float(100)
                i['QI_Final_Sell_Price'] = float(lv_final_price)