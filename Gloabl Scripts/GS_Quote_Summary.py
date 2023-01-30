def add_row1():
    quote_table=context.Quote.QuoteTables['QUOTE_SUMMARY']
    row_values = [{'Sr_No':1, 'Solution_Family':'HVAC Controls(BMS)','Cost':44759.19, 'Sell_Price':239116.18, 'Margin_':434, 'Margin_Amount':194406.99, 'Discount_':5, 'Discount_Amount':227.207},
                      {'Sr_No':2, 'Solution_Family':'Fire','Cost':2376.5, 'Sell_Price':10650.4, 'Margin_':354, 'Margin_Amount':564.8, 'Discount_':5, 'Discount_Amount':230.6},                     
                      {'Sr_No':3, 'Solution_Family':'Security','Cost':1345.6, 'Sell_Price':1736.78, 'Margin_':321, 'Margin_Amount':345.34, 'Discount_':5, 'Discount_Amount':227.207},                      
                      {'Sr_No':4, 'Solution_Family':'Energy & Sustainability','Cost':986.7, 'Sell_Price':1078.98, 'Margin_':213, 'Margin_Amount':245.99, 'Discount_':5, 'Discount_Amount':543.7},
                      {'Sr_No':5, 'Solution_Family':'ICT and Cyber Security','Cost':465.78, 'Sell_Price':606.7, 'Margin_':343, 'Margin_Amount':3456.7, 'Discount_':5,'Discount_Amount':254.5},                     
                      {'Sr_No':6, 'Solution_Family':'Emergency Service','Cost':456.8, 'Sell_Price':432.5, 'Margin_':12, 'Margin_Amount':856.7, 'Discount_':5, 'Discount_Amount':543.6}]
    for value in range(len(row_values)):
        newRow = quote_table.AddNewRow()
        newRow['Sr_No'] = row_values[value]['Sr_No']
        newRow['Solution_Family'] = row_values[value]['Solution_Family']
        newRow['Cost'] = row_values[value]['Cost']
        newRow['Sell_Price'] = row_values[value]['Sell_Price']
        newRow['Margin_'] = row_values[value]['Margin_']
        newRow['Margin_Amount'] = row_values[value]['Margin_Amount']
        newRow['Discount_'] = row_values[value]['Discount_']
        newRow['Discount_Amount'] = row_values[value]['Discount_Amount']
   #lastRow = quote_table.AddNewRow()
add_row1()
            
def add_total_row():
    Cost_sum, Sell_Price_sum, Margin_amount_sum, Discount_amount_sum= 0, 0, 0, 0
    quote_table=context.Quote.QuoteTables['QUOTE_SUMMARY']
    for i in quote_table.Rows:
        Cost_sum+= i['Cost']
        Sell_Price_sum+= i['Sell_Price']
        Margin_amount_sum += i['Margin_Amount']
        Discount_amount_sum += i['Discount_Amount']
    lastRow = quote_table.AddNewRow()
    lastRow['Solution_Family'] = 'Total'
    lastRow['Cost'] = Cost_sum
    lastRow['Sell_Price'] = Sell_Price_sum
    lastRow['Margin_'] = 0
    lastRow['Margin_Amount'] = Margin_amount_sum
    lastRow['Discount_'] = 1786.30
    lastRow['Discount_Amount'] =  Discount_amount_sum
add_total_row()