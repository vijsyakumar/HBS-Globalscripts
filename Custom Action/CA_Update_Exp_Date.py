#-----------------------------------------------------------------------------
#            Change History Log
#-----------------------------------------------------------------------------
#Description:
#This script is used for calculating expiry date based on proposal validity
#-----------------------------------------------------------------------------
# Date            Name                Version        Comments(Changes done)
#-----------------------------------------------------------------------------
# 08/04/2022    Shweta Kandwal             0             -Initial Version
# 10/19/2022    Ishika Bhattacharya        3             -Incorporated Translation
# 11/04/2022	Srinivasan Dorairaj		   4			 -Script and SQL Translation changes
#-----------------------------------------------------------------------------

import GM_TRANSLATIONS    # Added by Ishika
import datetime
lv_LanguageKey = GM_TRANSLATIONS.GetLanguageKey(User)   # Added by Ishika
lc_trans_type = GM_TRANSLATIONS.GetText('000063', lv_LanguageKey, '', '', '', '', '') #Modified by Srinivasan Dorairaj
if (context.Quote.GetCustomField('CF_TRANSACTION_TYPE').Value) == lc_trans_type : #Modified by Srinivasan Dorairaj
    pv_no = context.Quote.GetCustomField('CF_Proposal_Validity').Value
    QR = SqlHelper.GetFirst("SELECT CAST (ProposalValidity AS FLOAT) AS ProposalValidity FROM CT_Proposal_Validity WHERE CpqTableEntryId = {} AND LanguageKey='{}' ".format(pv_no,lv_LanguageKey))
    if QR.ProposalValidity:
        lv_expired_dat = context.Quote.DateCreated.AddDays(QR.ProposalValidity)
        context.Quote.GetCustomField("Quote Expiration Date").Value = lv_expired_dat