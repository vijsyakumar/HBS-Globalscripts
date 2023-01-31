"""partsQty = 0
validPartsCon = Product.GetContainerByName("AR_Product_Upload_Valid")

if validPartsCon.Rows.Count > 0:
    for row in validPartsCon.Rows:
        partsQty = int(str(row["Quantity"]))
        Product.SetQty('ItemQuantity', partsQty)
        #Product.AddToQuote(5)
        #for item in 
    #Trace.Write(RestClient.SerializeToJson(partsQty))
    
    #Product.SetQty('ItemQuantity', partsQty)
Product.UpdateQuote()
#context.Quote.Calculate()"""
"""partsQty = dict()
validPartsCon = Product.GetContainerByName("AR_Product_Upload_Valid")

if validPartsCon.Rows.Count > 0:
    for row in validPartsCon.Rows:
        partsQty[row.UniqueIdentifier] = int(row["Quantity"])

for item in eventArg.QuoteItemCollection:
    if partsQty.get(item.QuoteItemGuid):
        item.Quantity = partsQty[item.QuoteItemGuid]
Quote.Calculate(1)"""

validPartsCon = Product.GetContainerByName("AR_Product_Upload_Valid")

if validPartsCon.Rows.Count > 0:
    for row in validPartsCon.Rows:
        if row.IsSelected == True:
            ValidQuant = row.Columns["Quantity"]
            ValidPart = row.Columns["Part Number"]
            
            ValidProd = SqlHelper.GetFirst("select * from products where PRODUCT_CATALOG_CODE = '"+str(ValidPart.Value)+"'")
            ProductHelper.CreateProduct(int(ValidProd.PRODUCT_ID)).AddToQuote(int(ValidQuant.Value))

InvalidPartsCon = Product.GetContainerByName("AR_Product_Upload_Invalid")

if InvalidPartsCon.Rows.Count > 0:
    for row in InvalidPartsCon.Rows:
        if row.IsSelected == True:
            InValidQuant = row.Columns["Quantity"]
            #ProductHelper.CreateProduct(309).AddToQuote(int(InValidQuant.Value))
            #ProductHelper.CreateProduct(309).Attr('Description').SelectValue('DUMMY')
            #ProductHelper.CreateProduct(309).AddToQuote(int(InValidQuant.Value))
