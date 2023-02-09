from Scripting.Quote import MessageLevel





#context.Quote.GetCustomField("CF_SFDC_STATUS").Value = context.Quote.StatusName





product = None
for i in context.Quote.GetAllItems():
    lv_part = i.ProductId
    
    if lv_part:
        product = SqlHelper.GetFirst("select PRODUCT_ACTIVE from Products  where Product_ID = '"+str(lv_part)+"'")
        
        if product.PRODUCT_ACTIVE  == False:
            msg = 'Quote has expired Product.'
            exitmsgs = context.Quote.Messages
            if exitmsgs.Count > 0:
                for msges in exitmsgs:
                    if  "Quote has expired Product." in str(msges.Content):
                        Trace.Write("mngkfh")
                        context.Quote.DeleteMessage(msges.Id)
            
            context.Quote.AddMessage(msg,MessageLevel.Error,True)
            context.Quote.ChangeStatus('Preparing')
        else:
            context.Quote.GetCustomField("CF_Status_Info").Value = context.Quote.StatusName