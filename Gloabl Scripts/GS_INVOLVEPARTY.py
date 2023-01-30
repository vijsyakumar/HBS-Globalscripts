#Log.Info('GetInvolvedParties--->')
for val in context.Quote.GetInvolvedParties():
    if val.PartnerFunctionName == "Bill-to party":
        context.Quote.GetCustomField('CF_INVOLVED_PARTY_BILLID').Value = val.Id
    elif val.PartnerFunctionName == "Ship-to party":
        context.Quote.GetCustomField('CF_INVOLVED_PARTY_SHIPID').Value = val.Id
    elif val.PartnerFunctionName == "Sold-to party":
        context.Quote.GetCustomField('CF_INVOLVED_PARTY_SOLDID').Value = val.Id