from Scripting.Quote import MessageLevel
#total milestone cross limit to 100%--start
a = context.Quote.QuoteTables
counter = 0
for i in a:
    if i.Name=='QT_Payment_MileStones':
        for x in i.Rows:
            counter = counter + x["Milestone_Percentage"]
aa = counter
if aa > 100:
    context.Quote.AddMessage("Payment MileStone does not add more than 100%",MessageLevel.Warning,True)
else:
    context.Quote.Messages.Clear()