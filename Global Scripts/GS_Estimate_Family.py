#-----------------------------------------------------------------------------
#            Change History Log
#-----------------------------------------------------------------------------
#Description:
#calculate and show the cost or price   details for the entire contract duration.
#-----------------------------------------------------------------------------
# Date            Name                Version        Comments(Changes done)
#-----------------------------------------------------------------------------
# 09/08/2022    Ishika Bhattacharya    0          -Initial Version
# 10/18/2022    Dhruv Bhatnagar        7         -Replaced Hardcodings
#                                                 -Incorporated Translation
# 11/04/2022	Srinivasan Dorairaj	   8		 -Script and SQL Translation changes
#-----------------------------------------------------------------------------

import GM_TRANSLATIONS                   #Inserted by Dhruv
lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)    #Inserted by Dhruv
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '') #Modified by Srinivasan Dorairaj
if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type : #Modified by Srinivasan Dorairaj
    lc_hvac = GM_TRANSLATIONS.GetText('000049', lv_LanguageKey, '', '', '', '', '') #Inserted by Dhruv
    lc_Total = GM_TRANSLATIONS.GetText('000052', lv_LanguageKey, '', '', '', '', '') #Inserted by Dhruv
    def info():
        sale_price = 0
        hours = 0
        marginprcnt = 0
        marginAmt = 0
        cost = 0
        sell_price = 0
        discprcnt = 0
        discamt = 0
        for product in context.Quote.GetAllItems():
            if len(product.RolledUpQuoteItem) == 1:
                #Trace.Write('prod id:{}'.format(product.Id))	#Commented by Dhruv
                # SolFam_Sale, SolFam_Hour, SolFam_Cost, SolFam_MarginAmt, SolFam_Labor = 0, 0, 0, 0, 0

                for sol_family in context.Quote.GetItemByItemId(product.Id).AsMainItem.GetChildItems():

                    m = len(sol_family.RolledUpQuoteItem.split('.'))
                    # Trace.Write('m:{}'.format(m))

                    #Begin of change by Dhruv
                    #if m == 2 and sol_family.Description == 'HVAC Controls (BMS)':
                        #Trace.Write('sol_family.Desc:{}'.format(sol_family.Description))
                        #Trace.Write('HVAC:{}'.format(sol_family['QI_Yearly_Sell_Price']))
                    if m == 2 and sol_family.Description == lc_hvac:
                        #End of change by Dhruv
                        sale_price += sol_family['QI_Yearly_Sell_Price']
                        hours += sol_family['QI_hours']
                        cost += sol_family['QI_Total_Cost']
                        sell_price += sol_family['QI_Sell_Price']
                        marginprcnt += sol_family['QI_MARGIN_PERCENTAGE']
                        marginAmt += sol_family['QI_MARGIN_AMOUNT']
                        #discprcnt += sol_family['Discount Percent']
                        #discamt += sol_family['Discount Amount']

        #Trace.Write('HVAC FINAL SUM:{}'.format(sale_price))	#Commented by Dhruv
        #Trace.Write('HVAC HOURS:{}'.format(hours))				#Commented by Dhruv
        return {'salePrice':sale_price, 'Hours':hours, 'Cost' :cost, 'SellPrice' :sell_price, 'Marginprcnt' :marginprcnt, 'Marginamt' :marginAmt, 'Discprcnt' :discprcnt, 'Discamt' : discamt}

    info()

    def sql_helper(escalation_method):
        from datetime import datetime
        arr = []
        query = SqlHelper.GetList("SELECT * FROM CT_ESCALATIONS WHERE ESCALATION_METHOD = '"+str(escalation_method)+"' AND LanguageKey='"+lv_LanguageKey+"' ") #Modified by Srinivasan Dorairaj
        for i in query:
            query_inf = {}
            query_inf['date'] = i.DATE_FROM
            query_inf['percentage'] = i.EXCALATION_PERCENTAGE
            arr.append(query_inf)
        arr.sort(key = lambda x: datetime.strptime(str(x['date'])[0:str(x['date']).index('AM')], '%m/%d/%Y %H:%M:%S'))
        return arr[-1]['percentage']


    def add_row(quote_table, percentage, idx):
        y = int(quote_table.Rows[idx - 1]['Contract_Year'].split()[1])
        year = ' '.join(['Year', str(int(y) + 1)])
        newRow = quote_table.AddNewRow()
        newRow['Sr_No'] = quote_table.Rows[idx - 1]['Sr_No'] + 1
        newRow['Contract_Year'] = year
        newRow['HVAC_Controls_BMS_'] = quote_table.Rows[idx - 1]['HVAC_Controls_BMS_'] * percentage
        newRow['Fire'] = quote_table.Rows[idx - 1]['Fire'] * percentage
        newRow['Security'] = quote_table.Rows[idx - 1]['Security'] * percentage
        newRow['Energy_and_Sustainability'] = quote_table.Rows[idx - 1]['Energy_and_Sustainability'] * percentage
        newRow['ICT_and_Cyber_Security_'] = quote_table.Rows[idx - 1]['ICT_and_Cyber_Security_'] * percentage
        newRow['Emergency_Service'] = quote_table.Rows[idx - 1]['Emergency_Service'] * percentage
        newRow['Training'] = quote_table.Rows[idx - 1]['Training'] * percentage
        newRow['Total_Sell_Price'] = (quote_table.Rows[idx - 1]['Total_Sell_Price'] * percentage) + quote_table.Rows[idx - 1]['Total_Sell_Price']
        newRow['YoY_Escalation_'] = percentage * 100
        newRow['YoY_Escalation_Amount'] = quote_table.Rows[idx - 1]['Total_Sell_Price'] * percentage   

    def solution_family(escalation_method, user_val=None):
        percentage = sql_helper(escalation_method)/100
        #Trace.Write('percentage:{}'.format(percentage))					#Commented by Dhruv
        quote_table=context.Quote.QuoteTables['Estimate_Solution_Family']
        saleprice = info()
        sp = saleprice['salePrice']
        #Trace.Write('sp:{}'.format(sp))								    #Commented by Dhruv
        newRow = quote_table.AddNewRow()
        newRow['Sr_No'] = 1
        newRow['Contract_Year'] = 'Year 1'
        newRow['HVAC_Controls_BMS_'] = int(sp)
        newRow['Fire'] = 560
        newRow['Security'] = 678
        newRow['Energy_and_Sustainability'] = 900
        newRow['ICT_and_Cyber_Security_'] = 789
        newRow['Emergency_Service'] = 345
        newRow['Training'] = 888
        newRow['Total_Sell_Price'] = 26987
        newRow['YoY_Escalation_'] = 0
        newRow['YoY_Escalation_Amount'] = 0
        # Trace.Write('table:{}, {}'.format(quote_table.Rows[0]['Contract_Year'], float(3)//100))
        for idx in range(1, 9):
            if user_val:
                add_row(quote_table, user_val, idx)
                user_val = None
            else:
                add_row(quote_table, percentage, idx) 
    solution_family('B1')

    def add_last_row():
        HVAC_Controls_BMS_sum, Fire_sum, Security_sum, Energy_and_Sustainability_sum, ICT_and_Cyber_Security_sum,Emergency_Service_sum, Training_sum, Total_Sell_Price_sum = 0, 0, 0, 0, 0, 0, 0, 0
        quote_table=context.Quote.QuoteTables['Estimate_Solution_Family']
        for i in quote_table.Rows:
            # Trace.Write('val:{}'.format(i['HVAC_Controls_BMS_']))
            HVAC_Controls_BMS_sum += i['HVAC_Controls_BMS_']
            Fire_sum += i['Fire']
            Security_sum += i['Security']
            Energy_and_Sustainability_sum += i['Energy_and_Sustainability']
            ICT_and_Cyber_Security_sum += i['ICT_and_Cyber_Security_']
            Emergency_Service_sum += i['Emergency_Service']
            Training_sum += i['Training']
            Total_Sell_Price_sum += i['Total_Sell_Price']
        # Trace.Write('1:{}, 2:{}'.format(HVAC_Controls_BMS_sum, Fire_sum,Security_sum))
        lastRow = quote_table.AddNewRow()
        #lastRow['Contract_Year'] = 'Total'		#Commented by Dhruv
        lastRow['Contract_Year'] = lc_Total		#Inserted by Dhruv
        lastRow['HVAC_Controls_BMS_'] = HVAC_Controls_BMS_sum
        lastRow['Fire'] = Fire_sum
        lastRow['Security'] = Security_sum
        lastRow['Energy_and_Sustainability'] = Energy_and_Sustainability_sum
        lastRow['ICT_and_Cyber_Security_'] = ICT_and_Cyber_Security_sum
        lastRow['Emergency_Service'] = Emergency_Service_sum
        lastRow['Training'] = Training_sum
        lastRow['Total_Sell_Price'] = Total_Sell_Price_sum
        lastRow['YoY_Escalation_'] = Total_Sell_Price_sum
        lastRow['YoY_Escalation_Amount'] = Total_Sell_Price_sum
    add_last_row()