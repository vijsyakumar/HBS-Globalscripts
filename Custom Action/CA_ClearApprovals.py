def function_approval():
    quote_table=context.Quote.QuoteTables['Functional_Approval']
    for i in quote_table.Rows:
        i['Required'] = False
        i['Approval_Status'] = ''
function_approval()