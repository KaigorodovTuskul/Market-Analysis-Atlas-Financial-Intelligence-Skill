# Fixed income, credit and bank treasury

## Bond maths

Clean versus dirty price: dirty price includes accrued interest, calculated under an instrument-specific day-count convention. Nominal versus effective yield and compounding frequency matter. Duration is local yield sensitivity, convexity a second-order term; non-parallel shifts require key-rate exposures. For optional bonds use effective duration with a model of exercise behavior.

`ΔP/P ≈ -D_mod × Δy + 0.5 × convexity × (Δy)^2` for small shocks and consistent conventions.

## Curves and relative value

Separate OIS/reference curve, govvie benchmark, credit spread, liquidity, tax, funding and optionality. YTM is not expected realized return when bond defaults or sale occurs before maturity. Asset swap spread, Z spread and OAS differ materially.

## Banking / FTP

For a currency loan with a matched forward hedge, reconstruct full synthetic cost: borrowed currency coupon, upfront and running fees, forward points/cross-currency basis, collateral and rollover, borrower currency cash flows and hedge coverage. Do not conclude exchange risk has vanished unless notional, interest, settlement dates, early repayment and future resets are matched. FTP allocates interest-rate funding **and** behavioral liquidity costs; headline product margin may exclude capital, impairment, OPEX and taxes.

## Credit loss

`EL ≈ PD × LGD × EAD` must specify horizon, stressed/unconditional state, vintage and regulatory/accounting basis. Expected loss does not replace stressed loss or unexpected capital. NPL and delinquency definitions differ.
