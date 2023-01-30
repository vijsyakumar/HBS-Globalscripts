######-----------------------Changes for CXCPQ-37498--------------------------#####

proposal_language = context.Quote.GetCustomField("CF_Language").AttributeValue
buying_method = context.Quote.GetCustomField("CF_Buying_Method").Value
value = 'True'

if 'GSA' in buying_method:
    default = 'GSA'
    default_value = SqlHelper.GetFirst("Select Value from CT_EMAIL_PROPOSAL WHERE  GSA = '{}' and DEFAULT_VALUE = '{}'".format(default, value))
    if default_value:
        context.Quote.GetCustomField("CF_ProposalName").Value = default_value.Value

else:
    Trace.Write('Pass')
    default_language = SqlHelper.GetFirst("Select Value from CT_EMAIL_PROPOSAL WHERE  Language = '{}' and DEFAULT_VALUE = '{}'".format(proposal_language, value))
    if default_language:
        context.Quote.GetCustomField("CF_ProposalName").Value = default_language.Value






