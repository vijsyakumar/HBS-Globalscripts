# get value from the proposal validity custom field
proposal_validity = context.Quote.GetCustomField("CF_Proposal_Validity").AttributeValue
Trace.Write('proposal validity:{}'.format(proposal_validity))

# assign the proposal validity custom field value to quote validity custom field
context.Quote.GetCustomField("CF_Quote_Validity").Value = proposal_validity
quote_validity = context.Quote.GetCustomField("CF_Quote_Validity").Value
Trace.Write('quote validity:{}'.format(quote_validity))






