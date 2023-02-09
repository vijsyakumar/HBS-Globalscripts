# Order Confirmation
context.Quote.GetCustomField('PO Number').Value = context.Quote.GetCustomField('CF_Customer_PO_Number').Value
context.Quote.ChangeStatus('Order Confirmation Pending')