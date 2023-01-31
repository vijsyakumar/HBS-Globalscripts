############## change history ###########################
# 01/14/2023   Aditi Sharma                       -Added condition check for Preparing status and transaction type
#---------------------------------------------------------------------------------------------
import GM_TRANSLATIONS

lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User) #Added by Aditi 14th Jan
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '') #Added by Aditi 14th Jan
quote_status_ID = context.Quote.StatusId #Added by Aditi 14th Jan

if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type and quote_status_ID==32: #Added by Aditi 14th Jan
	for i in context.Quote.GetAllItems():
		if i['QI_Product_Type'] == "Honeywell Labor":
			Log.Info("i.Quantity---->"+str(i.Quantity))
			i['QI_hours'] = i.Quantity
			Log.Info("i.QI_hours--1111-->"+str(i['QI_hours']))

			
	FP_Type = {'Honeywell Hardware', 'Honeywell Software'}
	for i in context.Quote.GetAllItems():
		if i['QI_Product_Type'] in FP_Type:
			lv_price = SqlHelper.GetFirst(" SELECT DISTINCT CUSTOMS FROM CT_PRODUCTS_MASTER WHERE PART_NUMBER = '{0}' and CUSTOMS <> 0 ".format(i.PartNumber))
			if lv_price is not None:
				i['QI_CUSTOMS_PERCENT'] = lv_price.CUSTOMS
				if i['QI_CUSTOMS_PERCENT'] is not None and i['QI_Total_Cost'] > 0:
					i['QI_CUSTOMS_AMOUNT'] = float(i['QI_CUSTOMS_PERCENT'])/100 * float(i['QI_Total_Cost'])
				
			elif i['QI_Product_Type'] != 'Honeywell Labor':
				if  len(set(context.Quote.GetInvolvedParties())) > 0:
					for bp in context.Quote.GetInvolvedParties():
						if bp.PartnerFunctionKey == "SP":
							bp_country  = bp.Country
							
							if bp_country:
								lv_price1 = SqlHelper.GetFirst(" SELECT DISTINCT * FROM CT_FACTORS WHERE COUNTRY = '{0}' and CUSTOMS_PERC <> 0 ".format(bp_country))
								if lv_price1:
									i['QI_CUSTOMS_PERCENT'] = float(lv_price1.CUSTOMS_PERC)
									
								else:
									i['QI_CUSTOMS_PERCENT'] = float(1.86)
									
								if i['QI_CUSTOMS_PERCENT'] > 0 and i['QI_Total_Cost'] > 0:
									i['QI_CUSTOMS_AMOUNT'] = float(i['QI_CUSTOMS_PERCENT'])/100 * float(i['QI_Total_Cost'])
		if i['QI_Product_Type'] == 'Honeywell Labor':
			i['QI_hours'] = i.Quantity
			Log.Info("i.QI_hours--2222-->"+str(i['QI_hours']))
			