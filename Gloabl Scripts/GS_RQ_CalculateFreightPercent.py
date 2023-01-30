#-----------------------------------------------------------------------------
#			Change History Log
#-----------------------------------------------------------------------------
#Description:
#Based on the conditions we are enabling the Request For Approval action button
#-----------------------------------------------------------------------------
# Date			Name				Version		Comments(Changes done)
#-----------------------------------------------------------------------------
# 9/25/2022     Aditi                  0         -initial version
#
# 10/17/2022	Abhilash		       19		 -Replaced Hardcodings
#												 -Incorporated Translation
#
# 10/27/2022    Aditi                  20        -Replaced table CT_Country_FreightDetails
# 11/04/2022	Dhruv				   21		 -SQL translation,Transacrtion type
#												  check implemented
# 01/14/2023   Aditi Sharma                       -Added condition check for Preparing status
#-----------------------------------------------------------------------------
import GM_TRANSLATIONS

#Get user launguage from dictionary
lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '') #Modified by Dhruv
quote_status_ID = context.Quote.StatusId #Added by Aditi 14th Jan

if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type and quote_status_ID==32:  #Modified by Dhruv #Modified by Aditi 14th Jan
    lc_fst_party = GM_TRANSLATIONS.GetText('000020', lv_LanguageKey, '', '', '', '', '')
    lc_hh = GM_TRANSLATIONS.GetText('000027', lv_LanguageKey, '', '', '', '', '')
    lc_third_pty = GM_TRANSLATIONS.GetText('000065', lv_LanguageKey, '', '', '', '', '')
    lc_adhoc = GM_TRANSLATIONS.GetText('000111', lv_LanguageKey, '', '', '', '', '')
    
    #context.Quote.GetCustomField("CF_Country").Value = 'US'
    #context.Quote.GetCustomField("CF_Opportunity_Type").Value = 'Reactive Quoted (230)'
    oppType = context.Quote.GetCustomField('CF_Opportunity_Type').Value
    allowedOppTypes = ['Airport Reactive Quoted (235)','Reactive Quoted (230)','Energy Reactive Quoted (230/252)']
    if oppType in allowedOppTypes:
        for qitem in context.Quote.GetAllItems():
            prodType = qitem.ProductTypeName
            oppCountry = context.Quote.GetCustomField('CF_Country').Value
            quoteMarketCurr = context.Quote.SelectedMarket.CurrencyCode
            #Trace.Write(oppCountry)
            #Trace.Write(prodType)
            if not qitem['QI_FREIGHT_PERCENT']:
                #Aditi: 6th Oct: Product type will be Honeywell Hardware instead of First party material, so modified the condition
                #if prodType == 'First Party Material' or prodType == 'Honeywell Hardware':
                if prodType == lc_fst_party or prodType == lc_hh:
                    firstPquery = SqlHelper.GetFirst("SELECT * FROM CT_SKU_FreightDetails WHERE S_PartNumber = '{}' AND S_CountryCode = '{}' AND S_SupplierCurrency = '{}' AND LanguageKey='{}'".format(qitem.PartNumber,oppCountry,quoteMarketCurr,lv_LanguageKey))	#Modified by Dhruv
                    #Trace.Write("----->"+str(firstPquery.S_FreightPercent))
                    #### if freight percent is present for first party in SKU table
                    if firstPquery:
                        if firstPquery.S_FreightPercent and firstPquery.S_FreightPercent>0:
                            #Trace.Write(firstPquery.S_FreightPercent)
                            qitem['QI_FREIGHT_PERCENT'] = firstPquery.S_FreightPercent

                    #### if freight percent is not present for first party in SKU table
                    else:
                        #Trace.Write(qitem.PartNumber)
                        #altPquery = SqlHelper.GetFirst("SELECT * FROM CT_Country_FreightDetails WHERE C_CountryCode = '{}'".format(oppCountry)) #commented by Aditi 27th Oct
                        altPquery = SqlHelper.GetFirst("SELECT * FROM CT_FACTORS WHERE COUNTRY = '{}' AND LanguageKey='{}'".format(oppCountry,lv_LanguageKey)) #Modified by Dhruv
                        #Trace.Write(altPquery.FREIGHT_PERC)
                        if altPquery:
                            if altPquery.FREIGHT_PERC and altPquery.FREIGHT_PERC>0: #replaced as FREIGHT_PERC by Aditi 27th Oct
                                qitem['QI_FREIGHT_PERCENT'] = altPquery.FREIGHT_PERC

                #### if product is of third party or adhoc
                #elif prodType == 'Third Party' or prodType == 'Adhoc':
                elif prodType == lc_third_pty or prodType == lc_adhoc:
                    #otherPquery = SqlHelper.GetFirst("SELECT * FROM CT_Country_FreightDetails WHERE C_CountryCode = '{}'".format(oppCountry)) #commented by Aditi 27th Oct
                    otherPquery = SqlHelper.GetFirst("SELECT * FROM CT_FACTORS WHERE COUNTRY = '{}' AND LanguageKey='{}'".format(oppCountry,lv_LanguageKey)) #Modified by Dhruv
                    #Trace.Write(otherPquery.FREIGHT_PERC)
                    if otherPquery:
                        if otherPquery.FREIGHT_PERC and otherPquery.FREIGHT_PERC>0: #replaced as FREIGHT_PERC by Aditi 27th Oct
                            qitem['QI_FREIGHT_PERCENT'] = otherPquery.FREIGHT_PERC