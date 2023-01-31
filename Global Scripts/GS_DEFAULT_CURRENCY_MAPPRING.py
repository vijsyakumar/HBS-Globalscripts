Log.Info('cuurrency fetch')
quote = context.Quote
get_salesorg = quote.GetCustomField('CF_Sales_Org').Value
CF_Country = quote.GetCustomField('CF_Country').Value
get_default_curr = SqlHelper.GetFirst("SELECT DEF_CURRENCY from CT_DF_PRICING_SAL where COUNTRY='{0}' and SALES_ORG='{1}'".format(CF_Country,get_salesorg))
if get_default_curr:
	context.Quote.GetCustomField('CF_DEFAULT_CURR').Value = get_default_curr.DEF_CURRENCY