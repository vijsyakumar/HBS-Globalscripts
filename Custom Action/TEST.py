a=context.Quote.GetCustomField("CF_oppstatus").Value
from Scripting.Quote import MessageLevel
status = context.Quote.StatusName
qno=context.Quote.QuoteNumber
if context.Quote.GetCustomField("CF_oppstatus").Value == 'Closed Won' or context.Quote.GetCustomField("CF_oppstatus").Value=='HON Abandoned':
    if status == context.Quote.StatusName:
        context.Quote.AddMessage("Quote status cannot be changed for a closed opportunity",MessageLevel.Error,True)
        context.Quote.ChangeStatus(status)
        Log.Info('STATUS2----'+ status)