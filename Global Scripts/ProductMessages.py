import sys
import GM_TRANSLATIONS #Added by Payal

lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User) #Added by Payal
Log.Info('55-write in product--')
lv_WIMsg = GM_TRANSLATIONS.GetText('000199', lv_LanguageKey, '', '', '', '', '') #Added by Payal
lv_QMsg = GM_TRANSLATIONS.GetText('000200', lv_LanguageKey, '', '', '', '', '') #Added by Payal
lv_UOMMsg = GM_TRANSLATIONS.GetText('000201', lv_LanguageKey, '', '', '', '', '') #Added by Payal

Product.Attr('Incomplete_Flag').AssignValue('')
Product.Attr('Product_Message').AssignValue('')
def populateMessage(row,i,message):
    if Product.Messages.Contains(message):
        Product.Attr('Incomplete_Flag').AssignValue('1')
        row.Product.Attr('Incomplete_Flag').AssignValue('1')
        return
    Product.Attr('Incomplete_Flag').AssignValue('1')
    Product.Attr('Product_Message').AssignValue("Row[{}], {}".format(i,message))
    row.Product.Attr('Incomplete_Flag').AssignValue('1')
    row.Product.Attr('Product_Message').AssignValue(message)
    Log.Info(message)

packageContainerName = "WriteInProduct"
packageContainer = Product.GetContainerByName(packageContainerName)
i=0
Log.Info('inside writein container')
try:
    for row in packageContainer.Rows:
        i +=1
        data = row.Product.Attr("Selected_WriteIn").SelectedValue
        if data == '' or data == 'Product':
            #populateMessage(row, i,"WriteInProducts is not Valid") #Commented by Payal
            populateMessage(row, i,lv_WIMsg) #Added by Payal
            break
        data = row.Product.Attr("ItemQuantity").GetValue() if row.Product.Attr("ItemQuantity").GetValue() else 0
        if int(float(data)) <= 0:
            #populateMessage(row, i,"Quantity is not Valid")#Commented by Payal
            populateMessage(row, i,lv_QMsg) #Added by Payal
            break
        '''data = row.Product.Attr("Price").GetValue() if row.Product.Attr("Price").GetValue() else 0
        if int(float(data)) <= 0:
            populateMessage(row, i,"Unit List Price is not Valid")
            break'''
        '''data = row.Product.Attr("cost").GetValue() if row.Product.Attr("cost").GetValue() else 0
        if int(float(data)) <= 0:
            populateMessage(row, i,"Unit Regional Cost is not Valid")
            break'''
        data = row.Product.Attr("Unit of Measure").GetValue()
        if data.strip() == "":
            #populateMessage(row, i,"Unit of Measure is not Valid") #Commented by Payal
            populateMessage(row, i,lv_UOMMsg) #Added by Payal
            break
        row.Product.Attr('Incomplete_Flag').AssignValue('')
        row.Product.Attr('Product_Message').AssignValue('')
except Exception, e:
    Log.Error("WriteIn::ProductMessages::Exception: {} at line {}".format(sys.exc_info()[-1].tb_lineno, str(e)))