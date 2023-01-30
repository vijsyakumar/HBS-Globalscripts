#-----------------------------------------------------------------------------
#			Change History Log
#-----------------------------------------------------------------------------
#Description:
# Auto generation of the document
#-----------------------------------------------------------------------------
# Date			Name				Version		Comments(Changes done)
#-----------------------------------------------------------------------------
# 08/09/2022	Anil Poply			0			-Initial Creation
# 10/14/2022	MarripudiKrishna	2			-Replaced Hardcodings
#				Chaitanya						-Incorporated Translation
#-----------------------------------------------------------------------------
import GM_TRANSLATIONS
lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)
lc_import = GM_TRANSLATIONS.GetText('000017', lv_LanguageKey, '', '', '', '', '')
q = QuoteHelper.Get(context.Quote.Id).QuoteTables
if q:
    for i in q:
        if i.Name == 'QT_ASSET_UPLOAD' and i.Rows.Count > 0:
            #context.Quote.GenerateDocument('IMPORTASSETS') #commented by Krishna
            context.Quote.GenerateDocument(lc_import) 	#Added by Krishna
            i.Rows.Clear()