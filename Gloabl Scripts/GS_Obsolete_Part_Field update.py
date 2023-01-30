#-----------------------------------------------------------------------------
#            Change History Log
#-----------------------------------------------------------------------------
#Description:
#
#-----------------------------------------------------------------------------
# Date            Name                Version        Comments(Changes done)
#-----------------------------------------------------------------------------
# 09/30/2022    H513910                 0             -Initial Version
# 10/14/2022    Mounika Tarigopula      5       -Replaced Hardcodings
#                                                -Incorporated Translation
# 11/03/2022    Srinivasan Dorairaj		9		- Script and SQL Translation changes
#-----------------------------------------------------------------------------
#Begin of change by Mounika
import GM_TRANSLATIONS                   #Inserted by Mounika
lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)    #Inserted by Mounika
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '')   #opportunity type #Added by Srinivasan Dorairaj
lc_flag_T = GM_TRANSLATIONS.GetText('000048', lv_LanguageKey, '', '', '', '', '')    #True
lc_flag_F = GM_TRANSLATIONS.GetText('000068', lv_LanguageKey, '', '', '', '', '')    #False
if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type :           #Added by Srinivasan Dorairaj
	from Scripting.Quote import MessageLevel
	from datetime import date
	curr_date = str(date.today()) #fetching current date
	country = context.Quote.GetCustomField('CF_Country').Value #opportunty country
	for i in context.Quote.GetAllItems():
		part_nbr = i.PartNumber
		p_id = i.Id
		query = SqlHelper.GetFirst("SELECT * FROM CT_PRODUCTS_MASTER WHERE PART_NUMBER = '"+str(part_nbr)+"' and CHANNEL_STATUS = '"+str(country)+"' and LanguageKey = '"+str(lv_LanguageKey)+"'") #fetching details of part (validity status, country, replacement part) #Added by Srinivasan Dorairaj
		if query:
			date = query.CHANNEL_STATUS_VALID_FROM #Validity date
			replacement_part = query.REPLACEMENT_PART #available replacement part number
			if date < curr_date:
				#Trace.Write("Yes")
				#i['QI_isValid'] = "False"                 #commented by Mounika  
				i['QI_isValid'] = lc_flag_F                #Inserted by Mounika
				i['QI_Replacement_Part'] = replacement_part
			else:
				#i['QI_isValid'] = "True"                  #commented by Mounika
				i['QI_isValid'] = lc_flag_T                #Inserted by Mounika