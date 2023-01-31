#-----------------------------------------------------------------------------
#            Change History Log
#-----------------------------------------------------------------------------
#Description:
#Order Failed count
#-----------------------------------------------------------------------------
# Date            Name                Version        Comments(Changes done)
#-----------------------------------------------------------------------------
# 09/12/2022   Sreenivas Mucharla       0             -Initial Version
# 10/14/2022   Mounika Tarigopula       6             -Replaced Hardcodings
#                                                     -Incorporated Translation
# 11/03/2022   Srinivasan Dorairaj		8			  -Script Translation changes
#-----------------------------------------------------------------------------
#Begin of change by Mounika
import GM_TRANSLATIONS
lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '')      #Added by Srinivasan Dorairaj
if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type :          #Added by Srinivasan Dorairaj
    lc_log1 = GM_TRANSLATIONS.GetText('000076', lv_LanguageKey, '', '', '', '', '')
    lc_log2 = GM_TRANSLATIONS.GetText('000078', lv_LanguageKey, '', '', '', '', '')
    lc_log3 = GM_TRANSLATIONS.GetText('000081', lv_LanguageKey, '', '', '', '', '')
    lc_log4 = GM_TRANSLATIONS.GetText('000083', lv_LanguageKey, '', '', '', '', '')
    lc_log5 = GM_TRANSLATIONS.GetText('000084', lv_LanguageKey, '', '', '', '', '')
    lc_ord_confirm = GM_TRANSLATIONS.GetText('000079', lv_LanguageKey, '', '', '', '', '')
    lc_ord_placed = GM_TRANSLATIONS.GetText('000080', lv_LanguageKey, '', '', '', '', '')
    lc_booked = GM_TRANSLATIONS.GetText('000082', lv_LanguageKey, '', '', '', '', '')
	
    order_failed_str = context.Quote.GetCustomField('CF_ORD_FAILED_COUNT').Value
    #Log.Info("=== CA_ORD_FALED_COUNT Action Start===== ["+str(order_failed_str)+"]")
    order_failed_str = context.Quote.GetCustomField('CF_ORD_FAILED_COUNT').Value
    #Trace.Write("=== CA_Place_Order Action Start===== ")    #commented By Mounika
    Trace.Write(lc_log1)                                     #Inserted by Mounika
    order_failed_count= 0
    if(order_failed_str is None or len(order_failed_str) ==0 ):
		order_failed_count= 0
		context.Quote.GetCustomField('CF_ORD_FAILED_COUNT').Value = str(order_failed_count)
		#Trace.Write("=== CA_ORD_FALED_COUNT Action order_failed_count ===== "+order_failed_count) #commented By Mounika
		Trace.Write(lc_log2+order_failed_count)             #Inserted by Mounika
		#Log.Info("=== CA_ORD_FALED_COUNT Action order_failed_count ===== "+order_failed_count)
	#if context.Quote.StatusName == ("Order Confirmation Pending") or context.Quote.StatusName == ("Order Placed"):  #commented By Mounika
    if context.Quote.StatusName == (lc_ord_confirm) or context.Quote.StatusName == (lc_ord_placed):#Inserted by Mounika
        order_failed_count+= 1
        context.Quote.GetCustomField('CF_ORD_FAILED_COUNT').Value = str(order_failed_count)
        #Trace.Write("===CA_ORD_FALED_COUNT Action Order Confirmation Pending ===== "+str(context.Quote.GetCustomField('CF_ORD_FAILED_COUNT').Value))  #commented By Mounika
        Trace.Write(lc_log3+str(context.Quote.GetCustomField('CF_ORD_FAILED_COUNT').Value))   #Inserted by Mounika
        #Log.Info("=== Order Confirmation Pending ===== "+str(context.Quote.GetCustomField('CF_ORD_FAILED_COUNT').Value))
	#elif context.Quote.StatusName == ("Booked"):       #commented By Mounika
    elif context.Quote.StatusName == (lc_booked):       #Inserted by Mounika
        #Trace.Write("=== CA_ORD_FALED_COUNT Action Booked status ===== "+str(context.Quote.GetCustomField('CF_ORD_FAILED_COUNT').Value))           #commented By Mounika
        Trace.Write(lc_log4+str(context.Quote.GetCustomField('CF_ORD_FAILED_COUNT').Value))              #Inserted by Mounika
	#Trace.Write("=== CA_ORD_FALED_COUNT Action End===== ")                 #commented By Mounika
	Trace.Write(lc_log5)                       #Inserted by Mounika
	#Log.Info("=== CA_ORD_FALED_COUNT Action End===== ")