'''quote_table=context.Quote.QuoteTables['QT_Quote_Summary']
newRow = quote_table.AddNewRow()
for r in quote_table.Rows:
    pType = r['Product_Type_Rows']
    Trace.Write("SK : "+ str(pType))
    for i in context.Quote.GetAllItems():
        pr_Type = i.ProductTypeName
        
        Trace.Write("SM : "+ str(pr_Type))
        if str(pr_Type) != str(pType):
            Trace.Write("if condition is true")
            newRow = quote_table.AddNewRow()
            newRow['Product_Type_Rows'] = i.ProductTypeName
            newRow['Sell_Price'] = i.NetPrice
            newRow['Discount_Amount'] = i.DiscountAmount
            newRow['Recommended_Price'] = i["QI_Recommended_Sell_Price"]
            newRow['Discount_'] = i.DiscountPercent
            Trace.Write("df"+str(pType))
        else :
            
            r['Sell_Price'] = int(r['Sell_Price']) + i.NetPrice
            r['Discount_Amount'] = int(r['Discount_Amount']) + i.DiscountAmount
            r['Recommended_Price'] = r['Recommended_Price'] + i["QI_Recommended_Sell_Price"]
            #r['Discount_'] = (int(r['Discount_Amount'])/ int(r['Recommended_Price']))*100'''