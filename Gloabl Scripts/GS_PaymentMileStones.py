# -----------------------------------------------------------------------------
#            Change History Log
# -----------------------------------------------------------------------------
# Description:
# This script is used for payment milestone calculation
# -----------------------------------------------------------------------------
# Date            Name                Version        Comments(Changes done)
# -----------------------------------------------------------------------------
# 07/25/2022    Ayushi Shrivastav          0             -Initial Version
# 10/18/2022    Ishika Bhattacharya        33            -Replaced Hardcodings
#                                                        -Incorporated Translation
# 11/03/2022	Srinivasan Dorairaj		   37			 -Script and SQL Translation changes
# 11/05/2022	Ishika Bhattacharya		   38			 -corrections-removed few harcodings and correction in one query
#modified query to get required columns
# 01/11/2023	Dhruv Bhatnagar			   63    		 -CXCPQ-36801 Translation changes
# -----------------------------------------------------------------------------

import GM_TRANSLATIONS  # Added by Ishika

lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)  # Added by Ishika
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '')  # Modified by Srinivasan Dorairaj
lc_milestone_desc = GM_TRANSLATIONS.GetText('000184', lv_LanguageKey, '', '', '', '', '')  # Modified by ishika
lc_Milestone = GM_TRANSLATIONS.GetText('000185', lv_LanguageKey, '', '', '', '', '')  # Modified by  ishika
lc_Milestone_Percentage = GM_TRANSLATIONS.GetText('000186', lv_LanguageKey, '', '', '', '', '')  # Modified by  ishika

def setAccessReadonly(table):
    table.AccessLevel = table.AccessLevel.ReadOnly
    # table.Save()


def setAccessHidden(table):
    table.AccessLevel = table.AccessLevel.Hidden
    # table.Save()


def setAccessEditable(table):
    table.AccessLevel = table.AccessLevel.Editable
    # table.Save()


def deleteTableRows(table):
    for row in table.Rows:
        table.DeleteRow(row.Id)
    # table.Save()


def editableQuoteTableColumn(table, column):
    table.GetColumnByName(column).AccessLevel = table.AccessLevel.Editable


def readonlyQuoteTableColumn(table, column):
    table.GetColumnByName(column).AccessLevel = table.AccessLevel.ReadOnly


def hideQuoteTableColumn(table, column):
    table.GetColumnByName(column).AccessLevel = table.AccessLevel.Hidden


def getCfValue(cfName):
    return context.Quote.GetCustomField(cfName).Value


if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type:  # Modified by Srinivasan Dorairaj
    lc_Standard = GM_TRANSLATIONS.GetText('000129', lv_LanguageKey, '', '', '', '', '')  # Added by Ishika
    lc_Custom = GM_TRANSLATIONS.GetText('000046', lv_LanguageKey, '', '', '', '', '')  # Added by Ishika

    milestone = getCfValue("CF_Payment_MileStone")
    # fetch data from custom tale

    # ***** Start Logic to apply filter based on Total Sell Price ******
    CF_Total_Sell_Price = context.Quote.GetCustomField('CF_Total_Sell_Price').Value
    milestone_tab = SqlHelper.GetList("select * from CT_PAYMENT_MILESTONES where LanguageKey = '{}'".format(lv_LanguageKey))
    if (CF_Total_Sell_Price):
        CF_Total_Sell_Price = float(CF_Total_Sell_Price)
        # if CF_Total_Sell_Price >= 100000.0 and CF_Total_Sell_Price <= 150000.0:
        if CF_Total_Sell_Price >= 100000.0:
            milestone_tab = SqlHelper.GetList(
                "select Milestone_Description,Amount from CT_PAYMENT_MILESTONES WHERE QuoteValue_From = '100000' and QuoteValue_To = '150000' and LanguageKey = '" + lv_LanguageKey + "'")   
        elif CF_Total_Sell_Price >= 50000.0 and CF_Total_Sell_Price < 100000.0:
            milestone_tab = SqlHelper.GetList(
                "select Milestone_Description,Amount from CT_PAYMENT_MILESTONES WHERE QuoteValue_From = '50000' and QuoteValue_To = '100000' and LanguageKey = '" + lv_LanguageKey + "'")  
        elif CF_Total_Sell_Price >= 0 and CF_Total_Sell_Price < 50000.0:
            milestone_tab = SqlHelper.GetList(
                "select Milestone_Description,Amount from CT_PAYMENT_MILESTONES WHERE QuoteValue_From = '0' and QuoteValue_To = '50000' and LanguageKey = '" + lv_LanguageKey + "'")  
        else:
            milestone_tab = SqlHelper.GetList(
                "select Milestone_Description,Amount from CT_PAYMENT_MILESTONES WHERE QuoteValue_From = '100000' and QuoteValue_To = '150000' and LanguageKey = '" + lv_LanguageKey + "'")  
    
    else:
        milestone_tab = SqlHelper.GetList("select Milestone_Description,Amount from CT_PAYMENT_MILESTONES WHERE QuoteValue_From = '0' and QuoteValue_To = '50000' ")
    
    
    if (milestone_tab):
        Log.Info(" milestone_tab is not none lc_Standard--"+str(lc_Standard))
    # ********* End *********
    paymentMileStone = context.Quote.QuoteTables["QT_Payment_MileStones"]
    count = 1
    # if context.Quote.GetCustomField("CF_Payment_MileStone").Value == "Standard" or context.Quote.GetCustomField("CF_Payment_MileStone").Value == "" :  #Commented by Ishika
    if context.Quote.GetCustomField("CF_Payment_MileStone").Value == lc_Standard or context.Quote.GetCustomField(
            "CF_Payment_MileStone").Value == "":  # Added by Ishika
        deleteTableRows(paymentMileStone)
        if milestone_tab is not None:
            for entry in milestone_tab:
                row = paymentMileStone.AddNewRow()
                row['Milestone_Number'] = "Milestone {}".format(count)
                count = count + 1
                #CXCPQ-33115 start#
                if entry.Milestone_Description:
                    #row['Milestone_Description'] = entry.Milestone_Description						Commented by Dhruv CXCPQ-36801
                    row['Milestone_Description'] = Translation.Get(entry.Milestone_Description)		#Inserted by Dhruv CXCPQ-36801
               	#CXCPQ-33115 end#
                row['Milestone_Percentage'] = entry.Amount
            #hideQuoteTableColumn(paymentMileStone, "Milestone")  #Commented by ishika
            hideQuoteTableColumn(paymentMileStone, lc_Milestone)  #Added by ishika
        setAccessReadonly(paymentMileStone)
        paymentMileStone.CanAddRows = False
        paymentMileStone.CanDeleteRows = False
    # elif context.Quote.GetCustomField("CF_Payment_MileStone").Value == "Custom":  #Commented by Ishika
    elif context.Quote.GetCustomField("CF_Payment_MileStone").Value == lc_Custom:  # Added by Ishika
        setAccessEditable(paymentMileStone)
        # editableQuoteTableColumn(paymentMileStone,'Milestone_Description')
        # editableQuoteTableColumn(paymentMileStone, 'Milestone_Percentage')
        editableQuoteTableColumn(paymentMileStone, lc_Milestone_Percentage)  #added by ishika
        #editableQuoteTableColumn(paymentMileStone, 'Milestone')
        editableQuoteTableColumn(paymentMileStone, lc_Milestone)  #Added by ishika
        paymentMileStone.CanAddRows = True
        paymentMileStone.CanDeleteRows = True
        #CXCPQ-34395 start#
        for milstone_row in paymentMileStone.Rows:
            if milstone_row['Milestone'] != '' and milstone_row['Milestone'] != milstone_row['Milestone_Description']:
                milstone_row['Milestone'] = milstone_row['Milestone']##CXCPQ-34395 end
            else:
                milstone_row['Milestone'] = milstone_row['Milestone_Description']
        #hideQuoteTableColumn(paymentMileStone, 'Milestone_Description')   #Commented by ishika
        hideQuoteTableColumn(paymentMileStone, lc_milestone_desc)  #added by ishika
    context.Quote.GetCustomField("CF_Milestone_total").Value = ""
    sum = 0
    for row in paymentMileStone.Rows:
        sum = sum + row["Milestone_Percentage"]
        
    context.Quote.GetCustomField("CF_Milestone_total").Value = str(sum)