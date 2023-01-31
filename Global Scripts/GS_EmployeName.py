def employename(eid):
    val = SqlHelper.GetFirst("select Employee_Name from TAB_INCENTIVE where Employee_ID = '{0}'".format(eid))#CXCPQ-37640 start
    if val:
        return val.Employee_Name
    else:
        return ''#CXCPQ-37640 end
EID1= context.Quote.GetCustomField('CF_EID_1').Value
EID2= context.Quote.GetCustomField('CF_EID_2').Value
EID3= context.Quote.GetCustomField('CF_EID_3').Value
EID4= context.Quote.GetCustomField('CF_EID_4').Value
EID5= context.Quote.GetCustomField('CF_EID_5').Value
if EID1:
    e1 = employename(EID1)
    context.Quote.GetCustomField('CF_EID_NAME_1').Value = str(e1)
else:
    context.Quote.GetCustomField('CF_EID_NAME_1').Value = ""
if EID2:
    context.Quote.GetCustomField('CF_EID_NAME_2').Value = str(employename(EID2))
else:
    context.Quote.GetCustomField('CF_EID_NAME_2').Value = ""
if EID3:
    context.Quote.GetCustomField('CF_EID_NAME_3').Value = str(employename(EID3))
else:
    context.Quote.GetCustomField('CF_EID_NAME_3').Value = ""
if EID4:
    context.Quote.GetCustomField('CF_EID_NAME_4').Value = str(employename(EID4))
else:
    context.Quote.GetCustomField('CF_EID_NAME_4').Value = ""
if EID5:
    context.Quote.GetCustomField('CF_EID_NAME_5').Value = str(employename(EID5))
else:
    context.Quote.GetCustomField('CF_EID_NAME_5').Value = ""