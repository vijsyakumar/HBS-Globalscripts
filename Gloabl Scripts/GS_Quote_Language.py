context.Quote.GetCustomField("CFH_MODIFIED_BY").Value = str(User.Name) + " / " + str(User.UserName)
bp_country = context.Quote.GetCustomField("CF_Country").Value
value = 'True'
if bp_country:
    lv_user = SqlHelper.GetFirst("Select LANGUAGE from CT_Language_Data WHERE COUNTRY = '{}' and DEFAULT_VALUE = '{}'".format(bp_country, value))
    if lv_user:
        context.Quote.GetCustomField("Customer's Language").Value = lv_user.LANGUAGE
        context.Quote.GetCustomField("CF_Language").Value = lv_user.LANGUAGE

