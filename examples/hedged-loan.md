# Example — FX-hedged loan economics

**Prompt:** "A corporate has a three-month CNY loan at 7.25% plus 2.5% hedge charge, versus a RUB loan. Is the currency risk eliminated?"

**Method:** Confirm fixed/reset coupon and day count, date-matched forwards, notional plus interest coverage, CNY/RUB quote, closeout, collateral and repayments. Effective synthetic funding economics include loan interest, origination fees, forward points, bid/ask, credit charges and any mismatch. Model both appreciation/depreciation with and without a full-maturity hedge. Do not add a quoted 2.5 percentage-point fee *again* if it already embeds forward cost; request a cash-flow schedule and all-in APR convention. Explain basis and liquidity risk that survives a hedge.
