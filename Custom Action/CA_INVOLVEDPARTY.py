getparties = context.Quote.GetInvolvedParties()
for val in getparties:
    if val.PartnerFunctionName == "Bill-to party":
        context.Quote.GetCustomField('CF_INVOLVED_PARTY_BILLID').Value = val.Id
    if val.PartnerFunctionName == "Sold-to party":
        context.Quote.GetCustomField('CF_INVOLVED_PARTY_SOLDID').Value = val.Id
    if val.PartnerFunctionName == "Ship-to party":
        context.Quote.GetCustomField('CF_INVOLVED_PARTY_SHIPID').Value = val.Id