'''SalesOrg = context.Quote.GetCustomField('CF_Sales_Org')
country = context.Quote.GetCustomField('CF_Account_Country')
for i in context.Quote.GetAllItems():
    if i.PartNumber:
        part_nbr = i.PartNumber
        query_desc = SqlHelper.GetList("SELECT * FROM CT_PRICEBOOK_THIRDPARTY WHERE Part_No = '"+str(part_nbr)+"' Sales_org = '"+str(SalesOrg)+"' Country = '"+str(country)+"'  ")
        if query_desc:
            for qry in query_desc:
                i.ListPrice = str(qry.List_Price)'''
               
