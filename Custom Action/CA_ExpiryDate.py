 #adding validity days with currrent date
getdays = context.Quote.GetCustomField('CF_Proposal_Validity').AttributeValue
getexpirydate = SqlHelper.GetFirst("select DATEADD(day, {0}, GETDATE()) as Expirydate".format(getdays))
context.Quote.GetCustomField("Quote Expiration Date").Value = getexpirydate.Expirydate