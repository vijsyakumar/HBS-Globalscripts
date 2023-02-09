from Scripting.Quote import MessageLevel

amount = context.Quote.Totals.Amount

quote_type = context.Quote.GetCustomField('CF_Quote_Type').Value

user_ctry = User.Country

query = SqlHelper.GetFirst("SELECT * FROM CT_Quote_Limit WHERE Country = '"+str(user_ctry)+"' AND Quote_Type = '"+str(quote_type)+"' ")

if query:
    if query.Quote_Type  == str(quote_type) and float(amount) > float(query.Limit):
        message = "Amount: '"+str(query.Limit)+" value has exceeded for the quote type: '"+str(query.Quote_Type)+"' "
        exitmsg = context.Quote.Messages
        if exitmsg.Count > 0:
            for msge in exitmsg:
                if  "value has exceeded for the quote type:" in str(msge.Content):
                    context.Quote.DeleteMessage(msge.Id)
        context.Quote.AddMessage(message,MessageLevel.Error,False)
        context.Quote.ChangeStatus('Preparing')