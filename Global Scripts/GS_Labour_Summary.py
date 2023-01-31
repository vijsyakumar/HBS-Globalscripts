'''def add_row1():
    try:
        quote_table=context.Quote.QuoteTables['LABOR_SUMMARY']
        row_values = [{'Sr_no':1, 'Solution_Family':'HVAC Controls(BMS)','Hours':47.64, 'Rate':97.03, 'Total_Labor':4622.51},
                      {'Sr_no':2, 'Solution_Family':'Fire','Hours':0, 'Rate':150, 'Total_Labor':0.00},
                      {'Sr_no':3, 'Solution_Family':'Security','Hours':2.19, 'Rate':97.03, 'Total_Labor':212.49},
                      {'Sr_no':4, 'Solution_Family':'Energy & Sustainability','Hours':8.21, 'Rate':97.03, 'Total_Labor':796.62},
                      {'Sr_no':5, 'Solution_Family':'ICT and Cyber Security','Hours':0, 'Rate':97.03, 'Total_Labor':0.00},
                      {'Sr_no':6, 'Solution_Family':'Emergency Service','Hours':14.56, 'Rate':97.03, 'Total_Labor':1412.76},
                      {'Sr_no':7, 'Solution_Family':'Comprehensive Supervisor','Hours':0, 'Rate':97.03, 'Total_Labor':0.00}]
        for value in range(len(row_values)):
            newRow = quote_table.AddNewRow()
            newRow['Sr_No_'] = row_values[value]['Sr_no']
            newRow['Solution_Family'] = row_values[value]['Solution_Family']
            newRow['Hours'] = row_values[value]['Hours']
            newRow['Rate'] = row_values[value]['Rate']
            newRow['Total_Labor'] = row_values[value]['Total_Labor']
    except Exception as e:
        Trace.Write('Error:{}'.format(e))
        
add_row1()'''

#-----------new----------------------------
'''def info():
    sale_price = 0
    hours = 0
    marginAmt = 0
    labor_rate = 0
    for product in context.Quote.GetAllItems():
        if len(product.RolledUpQuoteItem) == 1:
            Trace.Write('prod Desc:{}'.format(product.Description))
            # SolFam_Sale, SolFam_Hour, SolFam_Cost, SolFam_MarginAmt, SolFam_Labor = 0, 0, 0, 0, 0
            
            for sol_family in context.Quote.GetItemByItemId(product.Id).AsMainItem.GetChildItems():
                m = len(sol_family.RolledUpQuoteItem.split('.'))
                #Trace.Write('m:{}'.format(m))
                
                if m == 2 and sol_family.Description == 'HVAC Controls (BMS)':
                    Trace.Write('sol_family.Desc:{}'.format(sol_family.Description))
                    
                    Trace.Write('HVAC:{}'.format(sol_family['QI_Yearly_Sell_Price']))
                    sale_price += sol_family['QI_Yearly_Sell_Price']
                    hours += sol_family['QI_hours']
                    labor_rate += sol_family['QI_Labor']
                    
    
    Trace.Write('HVAC FINAL SUM:{}'.format(sale_price))
    Trace.Write('HVAC hours:{}'.format(hours))
    Trace.Write('HVAC labor rate:{}'.format(labor_rate))
    
    return {'salePrice':sale_price, 'Hours':hours, 'Labor':labor_rate}
                        
info()



def add_row1():
    try:
        quote_table=context.Quote.QuoteTables['LABOR_SUMMARY']
        hr = info()
        hr1 = hr['Hours']
        #Trace.Write(hr1)
        lr =info()
        lr1 = lr['Labor']
        row_values = [{'Sr_no':1, 'Solution_Family':'HVAC Controls(BMS)','Hours':float(hr1), 'Rate':float(lr1), 'Total_Labor':float(hr1 * lr1)},
                      {'Sr_no':2, 'Solution_Family':'Fire','Hours':0, 'Rate':150, 'Total_Labor':0.00},
                      {'Sr_no':3, 'Solution_Family':'Security','Hours':2.19, 'Rate':97.03, 'Total_Labor':212.49},
                      {'Sr_no':4, 'Solution_Family':'Energy & Sustainability','Hours':8.21, 'Rate':97.03, 'Total_Labor':796.62},
                      {'Sr_no':5, 'Solution_Family':'ICT and Cyber Security','Hours':0, 'Rate':97.03, 'Total_Labor':0.00},
                      {'Sr_no':6, 'Solution_Family':'Emergency Service','Hours':14.56, 'Rate':97.03, 'Total_Labor':1412.76},
                      {'Sr_no':7, 'Solution_Family':'Comprehensive Supervisor','Hours':0, 'Rate':97.03, 'Total_Labor':0.00}]
        for value in range(len(row_values)):
            newRow = quote_table.AddNewRow()
            newRow['Sr_No_'] = row_values[value]['Sr_no']
            newRow['Solution_Family'] = row_values[value]['Solution_Family']
            newRow['Hours'] = row_values[value]['Hours']
            newRow['Rate'] = row_values[value]['Rate']
            newRow['Total_Labor'] = row_values[value]['Total_Labor']
    except Exception as e:
        Trace.Write('Error:{}'.format(e))
        
add_row1()'''