#!/usr/bin/env python3
"""Generate the original, hand-authored starter reference as JSONL. No remote content."""
from pathlib import Path
import json,re,unicodedata
ROOT=Path(__file__).resolve().parents[1]
S=ROOT/'skills/market-analysis-atlas'
# Entries have original short explanations, not Investopedia article text.
SEEDS={
'chart_patterns':r'''
Head and Shoulders|Three price peaks with a higher central peak; a neckline break can signal a bearish trend reversal.
Inverse Head and Shoulders|Three troughs with the deepest in the middle; confirmation needs an upside break of the neckline.
Double Top|Two attempts to exceed a similar high separated by a pullback; a break below the intervening low confirms the bearish setup.
Double Bottom|Two tests of a price low separated by a rebound; the intervening high is the usual confirmation level.
Triple Top|Three tests of a resistance region that may precede a reversal when support fails.
Triple Bottom|Three defenses of a support region that may precede an upside reversal after resistance breaks.
Rounding Top|Gradual transition from rising prices to falling prices with a broad curved crest.
Rounding Bottom|Gradual shift from selling pressure to accumulation, producing a broad curved basin.
Cup and Handle|Rounded recovery followed by a smaller consolidation; an upside rim breakout is watched for continuation.
Ascending Triangle|Flat upper boundary with rising troughs; compression may precede an upside break, but direction is not guaranteed.
Descending Triangle|Flat lower boundary with falling peaks; often monitored for a downside break.
Symmetrical Triangle|Converging highs and lows signify contraction before an eventual directional break.
Rising Wedge|Converging rising trendlines imply weakening upward momentum; a lower-line break may be bearish.
Falling Wedge|Converging falling trendlines imply waning downward pressure; an upper-line break may be bullish.
Bull Flag|Sharp advance followed by a compact downward-sloping consolidation; continuation requires a breakout.
Bear Flag|Sharp decline followed by a short upward-sloping consolidation; continuation requires renewed downside movement.
Bull Pennant|Brief triangular compression after a strong advance; a breakout in the initial direction is the continuation hypothesis.
Bear Pennant|Brief triangular compression after a strong decline; downside continuation is contingent on confirmation.
Rectangle Range|Price oscillates between approximately horizontal support and resistance before resolving direction.
Ascending Channel|Price moves between rising roughly parallel trendlines; its boundaries describe trend structure, not certain turning points.
Descending Channel|Price follows falling roughly parallel trendlines, potentially providing contextual support and resistance.
Horizontal Channel|Sideways price oscillation between mostly flat boundaries, with no inherent directional forecast.
Broadening Formation|Successively higher highs and lower lows create an expanding range, signaling rising uncertainty.
Megaphone Pattern|An expanding price range with diverging boundaries, often associated with erratic volatility.
Diamond Top|Expanding then contracting swings after an advance may indicate distribution, though identification is subjective.
Diamond Bottom|Expanding then contracting swings after a decline may indicate stabilization and possible reversal.
Island Reversal|Price cluster isolated by gaps on each side; interpretation depends on direction and market context.
Gap Up|A session opens above the prior traded range, leaving an untraded interval in the chosen timeframe.
Gap Down|A session opens below the preceding traded range, leaving a gap in the chosen timeframe.
Breakaway Gap|Gap out of a base or range accompanied by evidence of new directional participation.
Runaway Gap|Gap during an established trend that sometimes marks trend acceleration.
Exhaustion Gap|Late-trend gap that can precede reversal; diagnosis is largely retrospective.
Dead Cat Bounce|Temporary rebound during a larger falling trend, not necessarily an enduring bottom.
V Bottom|Sharp drop followed by a sharp recovery with little basing; difficult to act on without hindsight.
V Top|Rapid transition from steep ascent to steep decline with minimal topping consolidation.
Bump and Run Reversal|Accelerated trend becomes unsustainable and reverses through its prior trendline.
Three Drives Pattern|Three directional pushes with specified swing relationships; rules depend on implementation.
ABCD Pattern|Four pivot points creating three price legs; traders compare leg symmetry and reversal zones.
Gartley Pattern|Five-point harmonic formation with Fibonacci ratios used to define a possible reversal area.
Bat Pattern|Harmonic XABCD geometry emphasizing a deep final retracement into a potential reversal zone.
Butterfly Pattern|Harmonic five-point structure whose terminal leg can extend beyond its initial anchor.
Crab Pattern|Harmonic XABCD formation featuring an extended terminal leg and potential reversal zone.
Shark Pattern|Multi-swing harmonic formation defined by specified extension relationships.
Wolfe Wave|Converging five-wave geometry used by some analysts to hypothesize a return toward an equilibrium line.
Elliott Impulse Wave|Five-wave directional labeling under Elliott Wave theory; labels are discretionary.
Elliott Corrective Wave|Counter-trend wave structures in Elliott theory; alternate counts can fit the same data.
Wyckoff Accumulation|Interpretive framework describing a possible transition from selling to demand dominance in a range.
Wyckoff Distribution|Interpretive framework describing possible transfer from demand to supply dominance near a top.
Spring (Wyckoff)|Temporary excursion below a trading range that quickly reverses, possibly indicating absorption of supply.
Upthrust (Wyckoff)|Temporary move over resistance that fails back into a trading range, possibly indicating supply.
Breakout|Price moves past a predefined boundary; confirmation should consider closing price, volume, and false breaks.
Breakdown|Price moves below a predefined support area, with follow-through needed to assess validity.
Pullback|Countertrend move toward a prior level during an established price trend.
Throwback|Return toward a recently surpassed resistance level after an upside breakout.
Retest|A second encounter with a significant price level after it was broken or established.
Bull Trap|Initial upside break fails and price returns below the tested level, trapping breakout buyers.
Bear Trap|Initial downside break fails and price rebounds above the tested level, trapping sellers.
False Breakout|Transient boundary penetration without sustained follow-through; requires an explicit invalidation rule.
Trendline Break|Price crossing a fitted trendline; its value depends on how pivots and tolerances were chosen.
Golden Cross|Faster long-horizon moving average crosses above a slower one; lagging trend indicator.
Death Cross|Faster long-horizon moving average crosses below a slower one; lagging trend indicator.
Support Level|Price region where demand has previously offset selling, without any promise it will hold again.
Resistance Level|Price region where supply has previously offset demand, without any guarantee of rejection.
''',
'candlesticks':r'''
Doji|Opening and closing prices are close relative to the full candle range, signaling local indecision.
Long-Legged Doji|Doji with long upper and lower wicks, reflecting a wide intraperiod contest.
Dragonfly Doji|Open and close near period high with a long lower shadow; interpretation depends on preceding trend.
Gravestone Doji|Open and close near period low with a long upper shadow, often studied near resistance.
Hammer|Small body near candle high with a long lower wick, potentially indicating a rejected selloff after a decline.
Hanging Man|Hammer-like shape after an advance; requires bearish confirmation rather than shape alone.
Inverted Hammer|Small body near candle low and long upper wick appearing after a decline.
Shooting Star|Small body near low with long upper wick after an advance, indicating rejection of higher prices.
Bullish Engulfing|Bullish real body envelops the prior bearish real body under the selected candle convention.
Bearish Engulfing|Bearish real body envelops the prior bullish real body, often evaluated after an advance.
Bullish Harami|Small bullish candle body sits within prior long bearish body, pointing to decreasing selling momentum.
Bearish Harami|Small bearish candle body stays inside prior long bullish body, suggesting slowing buying pressure.
Harami Cross|A doji contained within the previous candle body; color and trend define bullish or bearish interpretations.
Morning Star|Three-candle sequence with bearish body, small transition candle, and strong bullish follow-through.
Evening Star|Three-candle reversal hypothesis with bullish body, small transition, then bearish confirmation.
Morning Doji Star|Morning-star configuration in which the middle candle is a doji.
Evening Doji Star|Evening-star configuration with a doji as the middle candle.
Three White Soldiers|Three consecutive strong bullish bodies with progressive higher closes, often after weakness.
Three Black Crows|Three consecutive notable bearish candles, often interpreted as weakening price structure.
Piercing Pattern|Bearish candle followed by bullish close materially within prior bearish real body.
Dark Cloud Cover|Bullish candle followed by bearish candle closing into a substantial portion of prior body.
Tweezer Top|Adjacent candles show closely matched highs; may mark resistance but needs context.
Tweezer Bottom|Adjacent candles show closely matched lows; may mark defended support.
Marubozu|Candle with negligible shadows, suggesting one-sided intraperiod trading.
Spinning Top|Small real body with noticeable shadows, often interpreted as indecision.
Inside Bar|Candle's high-low range is contained within its predecessor's range.
Outside Bar|Candle's trading range exceeds both the previous high and low.
Bullish Abandoned Baby|Three-candle bullish reversal pattern with an isolated middle doji and gaps.
Bearish Abandoned Baby|Three-candle bearish reversal pattern with an isolated middle doji and gaps.
Three Inside Up|Bullish harami context followed by an upside confirmation candle.
Three Inside Down|Bearish harami context followed by a downside confirmation candle.
Three Outside Up|Bullish engulfing context followed by additional bullish confirmation.
Three Outside Down|Bearish engulfing context followed by additional bearish confirmation.
Rising Three Methods|A strong bullish candle followed by small countertrend candles and eventual bullish continuation.
Falling Three Methods|A strong bearish candle followed by small countertrend candles and bearish continuation.
Kicking Pattern|Opposing marubozu-like candles separated by a gap, indicating abrupt sentiment change.
Belt Hold|Long real-body candle with an opening near one extreme, examined for momentum shifts.
''',
'indicators':r'''
Simple Moving Average (SMA)|Unweighted mean of the last n observed prices; smooths fluctuations but reacts with lag.
Exponential Moving Average (EMA)|Recursively smoothed price average with greater weight on recent observations.
Weighted Moving Average (WMA)|Average assigning explicitly chosen weights to recent price observations.
Double Exponential Moving Average (DEMA)|Combination of EMAs intended to reduce lag compared with a standard EMA.
Triple Exponential Moving Average (TEMA)|Smoothed moving-average combination designed to respond faster while retaining filtering.
Volume Weighted Average Price (VWAP)|Aggregate traded value divided by traded volume over an interval; depends on session reset convention.
Anchored VWAP|VWAP accumulated from a chosen event or timestamp rather than a default session open.
Relative Strength Index (RSI)|Bounded momentum oscillator built from averaged upward and downward price changes.
Stochastic Oscillator|Locates the latest close within a recent high-low range, usually expressed as a percentage.
Stochastic RSI|Applies stochastic normalization to RSI values, increasing sensitivity to momentum changes.
MACD|Difference between two EMAs, analyzed with a signal EMA and histogram.
MACD Histogram|MACD minus its signal line; conveys changes in the gap between momentum estimates.
Bollinger Bands|A moving-average centerline plus upper and lower volatility bands using standard deviations.
Bollinger Band Width|Normalized gap between Bollinger upper and lower bands; used to gauge compression.
Bollinger Percent B|Scaled placement of price relative to Bollinger upper and lower bands.
Average True Range (ATR)|Smoothed measure of price range including gaps; describes volatility, not direction.
Average Directional Index (ADX)|Trend-strength metric derived from directional movement measurements, without directional sign.
Directional Movement Index (DMI)|Positive and negative directional indicators alongside ADX for directional structure.
Commodity Channel Index (CCI)|Deviation of typical price from its moving average, scaled by mean absolute deviation.
Williams Percent R|Momentum oscillator comparing recent close against the range high over a lookback window.
Rate of Change (ROC)|Percentage or point change of a series over a selected lookback window.
Momentum Indicator|Difference or ratio between current and earlier price, depending on the chosen convention.
On-Balance Volume (OBV)|Cumulative signed volume using whether the close rose or fell versus the prior close.
Accumulation/Distribution Line|Cumulative volume-weighted measure based on closing location within the candle range.
Chaikin Money Flow (CMF)|Windowed sum of close-location-weighted volume divided by total volume.
Chaikin Oscillator|Difference of short and long EMAs applied to the accumulation/distribution line.
Money Flow Index (MFI)|RSI-like oscillator that incorporates typical price and trading volume.
Aroon Indicator|Measures elapsed bars since the highest high and lowest low over a lookback.
Aroon Oscillator|Difference between Aroon Up and Aroon Down for trend timing comparisons.
Ichimoku Cloud|Set of midpoint-based lines and projected cloud boundaries for trend and level context.
Keltner Channel|EMA-centered price envelope whose width commonly scales with ATR.
Donchian Channel|Bands tracking the rolling highest high and lowest low, often used in breakout systems.
Parabolic SAR|Trailing stop-and-reversal reference that evolves with the trend; whipsaws in ranges.
Supertrend|ATR-based directional overlay whose signal depends on multiplier and switching rule.
Fibonacci Retracement|Selected ratios applied to a prior price swing to mark hypothetical reaction zones.
Fibonacci Extension|Projected ratios beyond a measured price swing to define possible target areas.
Pivot Points|Levels derived from prior period high, low, and close using a chosen formula family.
Standard Deviation Indicator|Dispersion of observations around their mean for a chosen interval.
Historical Volatility|Annualized realized dispersion of returns computed using explicit frequency and estimator.
Implied Volatility|Volatility parameter that reconciles an option model with observed market option prices.
Volatility Index (VIX)|Index designed to infer near-term expected equity-market volatility from option prices.
Choppiness Index|Range-versus-sum-of-ranges indicator attempting to distinguish trends from consolidation.
Relative Vigor Index (RVI)|Oscillator relating close-open movement to the full trading range over time.
Klinger Oscillator|Volume-based trend indicator combining directional price-volume force with smoothing.
Know Sure Thing (KST)|Weighted combination of smoothed rates of change across multiple horizons.
TRIX|One-period percentage change of a triple-smoothed EMA, used as a momentum oscillator.
Ultimate Oscillator|Momentum oscillator combining buying pressure over several time horizons.
Balance of Power|Compares close-open displacement with high-low range to approximate intrabar control.
Ease of Movement|Price displacement adjusted for volume and range, intended to capture volume needed to move price.
Elder-Ray Index|Bull and bear power components compare high and low against a selected EMA.
Force Index|Price change multiplied by volume, commonly smoothed for trend assessment.
Arms Index (TRIN)|Ratio of advancing/declining issues adjusted by advancing/declining share volume.
Advance-Decline Line|Cumulative number of advancing issues minus declining issues, used for market breadth.
McClellan Oscillator|Difference between short and long smoothed advances-minus-declines measures.
Put-Call Ratio|Relative option put versus call activity or open interest; interpretation depends on market and data.
Coppock Curve|Long-horizon momentum measure based on weighted average of summed rates of change.
Zig Zag Indicator|Filters price moves below a chosen percentage or point threshold; repaints until pivots finalize.
Heikin-Ashi|Transformed OHLC representation that smooths candles and cannot be treated as executable prices.
Renko Chart|Price-block chart that ignores elapsed time to emphasize moves above a fixed block size.
Point and Figure Chart|Price-only chart of rising X and falling O columns based on box and reversal sizes.
Market Profile|Distribution of time or activity by price levels for session structure analysis.
Volume Profile|Histogram of traded volume by price rather than by clock time.
Order Book Imbalance|Relative size of displayed bid and ask interest; spoofing and cancellations can distort it.
Cumulative Volume Delta|Cumulative buy-initiated minus sell-initiated volume using a trade-signing convention.
''',
'fundamentals':r'''
Revenue|Value of ordinary sales or services recognized under the applicable accounting rules.
Gross Profit|Revenue minus cost of goods sold under the reporting basis.
Gross Margin|Gross profit relative to revenue, used to compare unit-level profitability.
EBIT|Earnings before interest and income taxes, with reconciliation needed for differing company definitions.
EBITDA|Earnings before interest, taxes, depreciation and amortization; excludes capital expenditure needs.
Adjusted EBITDA|Management-defined EBITDA adjusted for specified items; comparability requires reviewing add-backs.
Net Income|Profit after recognized costs, financing charges and income taxes.
Earnings Per Share (EPS)|Earnings attributable to common shareholders divided by a relevant weighted share count.
Diluted EPS|Per-share earnings reflecting potential dilution from eligible convertible instruments or equity awards.
Free Cash Flow (FCF)|Operating cash flow less capital expenditures in a commonly used convention.
Operating Cash Flow (CFO)|Cash generated or used by operations, subject to accounting classifications.
Investing Cash Flow (CFI)|Cash from investing activities, including asset purchases, disposals and certain investments.
Financing Cash Flow (CFF)|Cash movements with lenders and owners, including borrowings and distributions.
Capital Expenditure (CapEx)|Spending to acquire, improve or maintain long-lived operating assets.
Operating Expenditure (OpEx)|Recurring expenses incurred to operate a business rather than capitalized investment.
Depreciation|Systematic allocation of tangible asset cost over its estimated useful life.
Amortization|Systematic allocation of intangible asset or principal cost using the relevant convention.
Working Capital|Current assets less current liabilities, a measure of short-term funding tied to operations.
Net Working Capital|Usually current assets minus current liabilities, sometimes adjusted to operating items only.
Cash Conversion Cycle|Days inventory plus days receivables minus days payables, with industry-specific interpretation.
Days Sales Outstanding (DSO)|Average collection period approximated from receivables and credit sales.
Days Payable Outstanding (DPO)|Approximate days a firm takes to pay suppliers from payable balances and purchases/COGS.
Days Inventory Outstanding (DIO)|Average inventory holding period inferred from inventory and cost of sales.
Inventory Turnover|Cost of sales divided by average inventory, estimating how often stock is replenished.
Asset Turnover|Revenue divided by average assets, expressing asset utilization.
Return on Equity (ROE)|Net income relative to average shareholders' equity; leverage can mechanically amplify it.
Return on Assets (ROA)|Profit relative to average total assets; definitions vary for banks and industrial firms.
Return on Invested Capital (ROIC)|After-tax operating profit divided by invested capital, with adjustments carefully documented.
Weighted Average Cost of Capital (WACC)|Capital-weighted required returns on debt and equity after relevant tax effects.
Cost of Equity|Investor-required expected return on residual equity risk, often estimated rather than observed.
Cost of Debt|Effective financing cost for borrowing, adjusted when measuring after-tax cost.
Price-to-Earnings (P/E)|Market price relative to earnings per share; unstable or meaningless with losses.
Forward P/E|Share price divided by forecast earnings per share, sensitive to estimates.
Price-to-Book (P/B)|Market equity value divided by book equity; differs across sectors and accounting models.
Price-to-Sales (P/S)|Market capitalization divided by reported revenue; ignores differences in profitability.
Enterprise Value (EV)|Equity value plus net debt and relevant non-equity claims, adjusted for cash and other items.
EV/EBITDA|Enterprise value divided by EBITDA, requiring consistency in lease and debt adjustments.
EV/Revenue|Enterprise value divided by revenue; a rough valuation ratio when earnings are weak.
PEG Ratio|P/E scaled by an assumed earnings growth rate; units and growth assumptions matter.
Dividend Yield|Annual dividend per share relative to share price, without guaranteeing future payments.
Dividend Payout Ratio|Dividends relative to earnings or cash flow, depending on chosen denominator.
Dividend Discount Model (DDM)|Equity valuation from discounted expected dividends, sensitive to growth assumptions.
Gordon Growth Model|Perpetuity model for dividends growing at a constant rate below discount rate.
Discounted Cash Flow (DCF)|Discounts projected distributable cash flows with a rate consistent with cash-flow risk.
Terminal Value|Value beyond an explicit forecast horizon, usually calculated from perpetual growth or exit multiples.
Net Present Value (NPV)|Present value of expected future cash flows net of initial investment.
Internal Rate of Return (IRR)|Discount rate at which project NPV equals zero; nonstandard flows may have multiple roots.
Modified Internal Rate of Return (MIRR)|Return metric assuming separate financing and reinvestment rates.
Payback Period|Time needed for cumulative project cash inflows to offset investment, often excluding time value.
Economic Value Added (EVA)|Operating return net of a capital charge on capital employed.
Altman Z-Score|Weighted ratio model intended to flag financial distress in particular firm populations.
Piotroski F-Score|Nine-signal accounting quality framework based on profitability, leverage and operating efficiency.
DuPont Analysis|Decomposes ROE into margin, turnover and leverage components.
Current Ratio|Current assets divided by current liabilities; sensitive to asset liquidity.
Quick Ratio|Highly liquid current assets relative to current liabilities, excluding illiquid stock.
Cash Ratio|Cash and near-cash items divided by current liabilities.
Debt-to-Equity Ratio|Debt relative to book equity under a stated definition of debt.
Net Debt/EBITDA|Net borrowings divided by EBITDA, an imperfect leverage proxy when cash flow is volatile.
Interest Coverage Ratio|Earnings measure divided by financing interest expense to gauge service capacity.
Debt Service Coverage Ratio (DSCR)|Cash available for debt service divided by scheduled principal and interest payments.
Capital Adequacy Ratio|Eligible regulatory capital relative to risk-weighted assets under a specified rulebook.
Common Equity Tier 1 (CET1)|Highest-quality bank regulatory capital after defined adjustments and deductions.
Loan-to-Deposit Ratio|Credit balances divided by deposit balances, with limited meaning without funding mix.
Net Interest Margin (NIM)|Net interest income divided by average interest-earning assets.
Cost-to-Income Ratio (CIR)|Operating expenses relative to operating income; numerator/denominator definitions vary.
Nonperforming Loan (NPL)|Loan classified as impaired or past due under the applicable supervisory definition.
Cost of Risk (CoR)|Period credit-loss charge relative to average loan exposure under an explicit definition.
Expected Credit Loss (ECL)|Probability-weighted estimate of discounted contractual cash shortfalls across scenarios.
Provision Coverage Ratio|Loan loss allowances compared with nonperforming loans, depending on reporting basis.
''',
'macro':r'''
Gross Domestic Product (GDP)|Value added produced within an economy over a period, measured under national-accounts standards.
Real GDP|GDP adjusted for price-level changes to isolate changes in production volume.
Nominal GDP|GDP at current prices, affected by both output and price movements.
GDP Deflator|Implicit price index for domestically produced final output derived from nominal versus real GDP.
GDP per Capita|GDP divided by population; a coarse average not a measure of income distribution.
Potential GDP|Estimated sustainable production consistent with stable inflation over a medium horizon.
Output Gap|Difference between actual and estimated potential output, often expressed as a share of potential.
Nowcasting|Inference of current-period economic activity before complete official data are released.
Recession|Broad, material contraction in economic activity assessed through multiple indicators and duration.
Expansion|Phase of a business cycle with rising overall output and employment.
Business Cycle|Alternation of expansion and contraction in aggregate economic activity.
Leading Economic Index|Composite of variables intended to anticipate changes in economic activity.
Coincident Indicator|Series tending to move with current economic activity rather than predict it.
Lagging Indicator|Series usually reacting after economic conditions have already changed.
Consumer Price Index (CPI)|Index tracking the price of a specified household consumption basket and its changes.
Core CPI|Consumer inflation measure excluding selected volatile components, often food and energy.
Personal Consumption Expenditures Price Index (PCE)|Consumption price index constructed from expenditure-based national-account data.
Producer Price Index (PPI)|Index measuring price movements received by producers for selected goods and services.
Headline Inflation|Price growth measured using a broad overall price index.
Core Inflation|Inflation measure excluding or downweighting components considered unusually volatile.
Disinflation|Decline in the rate of inflation while the general price level can keep rising.
Deflation|Persistent decrease in the general price level rather than just slower inflation.
Stagflation|Combination of weak real activity, elevated inflation and often high unemployment.
Hyperinflation|Extreme self-reinforcing price-level increase; formal definitions use specific thresholds.
Inflation Expectations|Beliefs or market-inferred forecasts for future inflation; survey and market measures differ.
Breakeven Inflation|Nominal Treasury yield minus inflation-linked yield as an approximation including risk premia.
Real Interest Rate|Nominal interest rate adjusted for inflation, ex ante or ex post under specified timing.
Nominal Interest Rate|Rate quoted without removing inflation over the investment period.
Policy Rate|Central-bank instrument or target that guides short-term money-market interest rates.
Federal Funds Rate|Overnight unsecured rate on reserve balance transactions in the US federal funds market.
Monetary Policy|Central-bank actions affecting money, credit and interest-rate conditions in pursuit of mandates.
Fiscal Policy|Government spending and taxation choices influencing demand and distribution.
Quantitative Easing (QE)|Central-bank large-scale asset purchases to ease financial conditions when conventional room is limited.
Quantitative Tightening (QT)|Runoff or sales of central-bank securities holdings that withdraw accommodation.
Yield Curve|Term structure of yields on comparable bonds across different maturities.
Inverted Yield Curve|Shorter maturity yields exceed longer maturity yields for a chosen set of tenors.
Steepening Yield Curve|Long-minus-short yield spread widens, through short-end decline or long-end increase.
Flattening Yield Curve|Long-minus-short spread narrows, for potentially different macroeconomic reasons.
Term Premium|Extra expected compensation required for bearing longer-term rate exposure.
Neutral Rate (r-star)|Unobservable real short-rate estimate compatible with balanced demand and stable inflation.
Taylor Rule|Policy-rate guideline combining inflation deviation and economic slack with specified coefficients.
Phillips Curve|Empirical or theoretical association between inflation pressures and labor-market slack.
NAIRU|Estimated unemployment rate compatible with stable inflation, difficult to observe in real time.
Unemployment Rate|Share of labor force lacking jobs, available and actively searching under official definitions.
Labor Force Participation Rate|Labor force as a proportion of working-age population under chosen age thresholds.
Nonfarm Payrolls (NFP)|Monthly US employer payroll employment estimate excluding specified sectors.
ADP National Employment Report|Private-sector employment estimate derived from ADP payroll microdata and methods.
JOLTS|US survey of vacancies, hires and separations that sheds light on labor-market tightness.
Initial Jobless Claims|Weekly count of new claims for unemployment insurance in the relevant jurisdiction.
Purchasing Managers Index (PMI)|Diffusion index of surveyed business conditions; above 50 often indicates expansion.
ISM Manufacturing Index|US manufacturing survey diffusion measure covering activity indicators.
Industrial Production|Quantity index of output by industry segments such as manufacturing and mining.
Capacity Utilization|Realized production relative to estimated sustainable industrial productive capacity.
Retail Sales|Reported sales activity for retail establishments; inflation adjustment may be necessary.
Durable Goods Orders|Orders for long-lived manufactured goods, often volatile due to aircraft or defense.
Consumer Confidence|Survey-based evaluation and expectations of household economic conditions.
Housing Starts|Number of residential construction projects initiated during a reported period.
Building Permits|Government authorizations for new construction, a forward-looking housing indicator.
Balance of Payments (BoP)|Accounting framework for transactions between residents and nonresidents.
Current Account|Trade in goods and services plus primary and secondary income flows with the rest of world.
Capital Account|Balance-of-payments account for capital transfers and nonproduced nonfinancial assets.
Financial Account|Cross-border acquisition and disposal of financial assets and liabilities.
Trade Balance|Exports minus imports of goods under the defined statistical basis.
Exchange Rate|Relative price of two currencies, with quotation direction explicitly specified.
Nominal Effective Exchange Rate (NEER)|Trade-weighted currency index before inflation adjustments.
Real Effective Exchange Rate (REER)|Trade-weighted nominal currency index adjusted for relative price levels.
Purchasing Power Parity (PPP)|Long-run concept relating exchange rates to relative prices of comparable baskets.
Interest Rate Parity|No-arbitrage relation linking spot/forward exchange rates and interest rates under assumptions.
Covered Interest Parity|Hedged cross-currency returns should align after basis, collateral and funding costs.
Currency Basis Swap|Cross-currency swap whose basis spread captures financing and market-friction conditions.
Currency Devaluation|Official reduction of a fixed or managed currency parity.
Currency Depreciation|Market decrease in currency value under a floating or managed exchange-rate system.
Sovereign Debt|Liabilities incurred by a national government in local or foreign currency.
Debt-to-GDP Ratio|Government debt stock divided by nominal annual GDP, sensitive to both growth and rates.
Budget Deficit|Government expenditures exceeding revenues over a stated period and institutional perimeter.
Primary Balance|Fiscal balance excluding interest payments on existing debt.
Fiscal Multiplier|Estimated change in output per unit of fiscal impulse; varies with context and horizon.
Automatic Stabilizers|Tax and benefit mechanisms that cushion cycles without fresh legislative action.
Money Supply (M2)|Broad monetary aggregate combining currency and eligible deposits, jurisdiction-specific.
Monetary Base|Central-bank monetary liabilities such as reserves and currency under national definitions.
Velocity of Money|Nominal expenditure divided by selected money stock, an accounting ratio not fixed in time.
Credit Impulse|Change in new credit extension relative to GDP, used as an approximate cyclical demand gauge.
Commodity Supercycle|Prolonged commodity price uptrend linked to structural supply-demand forces.
Baltic Dry Index|Shipping charter-rate index often used as one imperfect proxy for bulk trade conditions.
''',
'fixed_income':r'''
Bond Price|Present value of promised cash flows discounted at yields matching risk and timing.
Yield to Maturity (YTM)|Single discount rate equating a bond's promised cash flows to its observed price.
Current Yield|Annual coupon income divided by current bond price, ignoring price convergence.
Yield to Worst|Lowest conventionally calculated yield among permitted early redemption scenarios.
Coupon Rate|Contractual periodic interest relative to bond face value.
Zero-Coupon Bond|Bond without intermediate coupons, usually priced below face value when yields are positive.
Floating Rate Note (FRN)|Debt instrument with coupon reset to a reference index plus contractual spread.
Fixed Rate Bond|Debt security with pre-specified periodic coupon amount or rate.
Inflation-Linked Bond|Debt whose payments adjust with a referenced inflation index under contractual rules.
Credit Spread|Yield premium over a reference security or curve, affected by risk and liquidity.
Option-Adjusted Spread (OAS)|Spread estimated after modeling embedded option exercise effects.
Z-Spread|Constant spread added to the spot curve to match a bond's market price.
Asset Swap Spread|Spread implied by swapping fixed bond cash flows into a floating-rate structure.
Duration|Approximate sensitivity of price to small changes in yield, requiring a convention.
Macaulay Duration|Present-value-weighted average time until bond cash-flow receipts.
Modified Duration|Macaulay duration scaled for compounding convention to approximate yield sensitivity.
Effective Duration|Model-based price sensitivity when cash flows themselves depend on interest rates.
DV01 (PV01)|Approximate currency price change from one basis-point yield movement.
Convexity|Second-order curvature of the bond price-yield relationship.
Key Rate Duration|Price sensitivity to a localized yield-curve node shift under a chosen curve method.
Yield Curve Bootstrapping|Sequential recovery of discount factors or spot rates from priced instruments.
Spot Rate|Yield applied to a single future cash flow of a stated tenor and compounding basis.
Forward Rate|Interest rate for a future period inferred or contracted from the current term structure.
Forward Rate Agreement (FRA)|Derivative settling the difference between a contracted and reference future short rate.
Interest Rate Swap (IRS)|Contract exchanging interest-payment streams according to reference indices and notionals.
Overnight Index Swap (OIS)|Swap exchanging fixed interest against compounded or otherwise specified overnight rates.
Cross Currency Swap|Exchange of payments denominated in distinct currencies with defined principal mechanics.
Repurchase Agreement (Repo)|Secured cash financing backed by securities subject to repurchase terms.
Reverse Repo|Cash lending against collateral securities from the cash lender's perspective.
Haircut|Collateral market-value discount used to protect a lender against valuation and liquidation risk.
Credit Default Swap (CDS)|Derivative transferring specified reference-entity credit-event risk for periodic or upfront premium.
CDS Spread|Premium of credit protection under a standard tenor and recovery convention.
Recovery Rate|Fraction of exposure recovered after default, varying with collateral and seniority.
Probability of Default (PD)|Likelihood of a borrower defaulting over a specified horizon conditional on definition.
Loss Given Default (LGD)|Loss severity as fraction of exposure in a default scenario after expected recovery.
Exposure at Default (EAD)|Expected amount owed when a credit default occurs under a specified framework.
Expected Loss (EL)|Average modeled credit loss, commonly approximated as PD times LGD times EAD.
Liquidity Coverage Ratio (LCR)|Regulatory stock of high-quality liquid assets relative to modeled net stressed outflows.
Net Stable Funding Ratio (NSFR)|Regulatory available stable funding relative to required stable funding.
High Quality Liquid Assets (HQLA)|Liquid and eligible assets subject to prescribed liquidity and haircuts for coverage.
Funds Transfer Pricing (FTP)|Internal prices charged or credited to business units for funding and liquidity characteristics.
Liquidity Transfer Pricing (LTP)|Internal allocation of liquidity costs and benefits over funding horizons.
Value at Risk (VaR)|Statistical threshold for portfolio loss at specified confidence and horizon, not a worst-case loss.
Expected Shortfall (ES)|Average tail loss conditional on losses beyond a specified VaR threshold.
Stress Testing|Evaluation of portfolio or institutional outcomes under severe but coherent hypothetical shocks.
''',
'quantitative':r'''
Arithmetic Return|Percentage change in value adjusted for distributions under the stated convention.
Log Return|Natural logarithm of current to prior value ratio, additive across time.
Compound Annual Growth Rate (CAGR)|Constant annualized geometric rate linking start and end values.
Geometric Mean Return|Compound growth-equivalent mean of periodic returns, rather than arithmetic average.
Volatility|Dispersion of returns over a chosen frequency and horizon, often annualized.
Beta|Sensitivity coefficient from a regression of asset returns on market returns.
Alpha|Performance unexplained by a defined benchmark model, not inherently evidence of skill.
Sharpe Ratio|Excess return over a risk-free reference divided by return volatility.
Sortino Ratio|Excess return over a target divided by downside deviation.
Information Ratio|Active return relative to tracking-error volatility against a benchmark.
Treynor Ratio|Excess portfolio return per unit of market beta risk.
Calmar Ratio|Annualized performance divided by maximum drawdown magnitude over a stated sample.
Maximum Drawdown|Largest peak-to-trough percentage decline observed in an equity curve.
Recovery Factor|Cumulative profit relative to maximum drawdown under an explicit convention.
Profit Factor|Gross trading gains divided by gross trading losses, undefined with zero losses.
Win Rate|Fraction of closed observations counted as winners under the strategy accounting policy.
Payoff Ratio|Average winning trade divided by absolute average losing trade.
Expectancy|Expected gain or loss per trade estimated from win probability and conditional payoffs.
Kelly Criterion|Position fraction maximizing expected logarithmic wealth under highly restrictive known-probability assumptions.
Correlation|Normalized measure of linear co-movement, not proof of causation.
Covariance|Joint dispersion of two series about their means, scale-dependent.
Autocorrelation|Association between a series and its lagged values.
Partial Autocorrelation|Correlation at a selected lag after adjusting for intervening shorter lags.
Stationarity|Property that chosen statistical distribution features remain stable over time.
Unit Root|Nonstationary stochastic-process feature associated with persistent shocks under an assumed model.
Cointegration|Stationary linear relationship among otherwise nonstationary integrated series under assumptions.
Heteroskedasticity|Variation of error variance across observations or conditions.
ARCH Effect|Conditional error variance depends on prior squared disturbances.
GARCH|Model allowing time-varying conditional variance to respond to past shocks and volatility.
ARIMA|Autoregressive integrated moving average family for univariate time-series behavior.
Vector Autoregression (VAR)|System of equations where each series depends on lags of several series.
Impulse Response Function|Model-derived path of variables after a specified structural or reduced-form shock.
Granger Causality|Forecast information test based on lags; not necessarily real-world causation.
Kalman Filter|Recursive estimate of hidden states from noisy observations in a state-space model.
Monte Carlo Simulation|Repeated sampling of random scenarios to approximate distributions of possible outcomes.
Bootstrap Resampling|Sampling with replacement from observed data to approximate estimator uncertainty.
Walk-Forward Validation|Repeated refitting on past windows and testing on subsequent out-of-sample windows.
Backtesting|Simulation of historical trading rules with realistic information availability and execution assumptions.
Look-Ahead Bias|Leakage of future-known data into historical model construction or trading decisions.
Survivorship Bias|Distortion caused by omitting entities that disappeared before current observation.
Data Snooping|Apparent findings produced by repeatedly trying choices against the same dataset.
Overfitting|Model adapting to historical noise rather than generalizable patterns.
Cross Validation|Partitioned estimation and evaluation process that must respect temporal ordering for time series.
Regime Switching Model|Model describing transitions among latent market or economic states.
Principal Component Analysis (PCA)|Orthogonal transformation that summarizes maximum observed variance in fewer factors.
Factor Model|Representation of asset returns through exposures to shared systematic drivers and residuals.
Capital Asset Pricing Model (CAPM)|Model relating expected return to systematic market risk under restrictive assumptions.
Fama-French Three Factor Model|Equity return model with market, size and value factors.
Fama-French Five Factor Model|Factor model adding profitability and investment factors to market, size and value.
Arbitrage Pricing Theory (APT)|Framework expressing expected returns through common factor risk premiums.
Black-Scholes Model|Option valuation framework under assumptions about price dynamics, rates and hedging.
Binomial Option Model|Discrete branching approach to derivative valuation and early-exercise choices.
Put-Call Parity|No-arbitrage relation among comparable European calls, puts, forward exposure and discounting.
Delta|First derivative of option value with respect to underlying price under a specified pricing model.
Gamma|Sensitivity of option delta to a change in underlying price.
Vega|Sensitivity of option value to a unit change in implied volatility.
Theta|Option value sensitivity to elapsed time under a stated convention.
Rho|Option value sensitivity to a change in interest rate input.
Volatility Smile|Implied volatilities differ across strikes, contradicting constant-volatility simplifications.
Volatility Skew|Asymmetry of implied volatility across strikes and/or deltas.
''',
'markets':r'''
Market Capitalization|Share price multiplied by shares outstanding, subject to share-class and float conventions.
Free Float|Shares available for public trading after excluding defined strategic or restricted holdings.
Bid-Ask Spread|Difference between best available quoted ask and bid prices at a moment.
Market Order|Instruction seeking immediate execution at prevailing available prices without a price cap.
Limit Order|Instruction permitting execution only at the stated limit price or more favorable.
Stop Order|Conditional instruction triggered by a level, with execution price not guaranteed afterward.
Stop-Limit Order|Triggered limit instruction that may not execute during a fast price move.
Slippage|Difference between intended benchmark price and actual execution price.
Market Impact|Price change associated with placing or executing an order in the market.
Order Book|Collection of standing buy and sell quotations, often only visible for selected venues.
Liquidity|Ability to trade meaningful size quickly without an excessive price concession.
Market Depth|Displayed or inferred executable quantity across successive price levels.
Volume|Quantity of units traded over a defined interval and market perimeter.
Open Interest|Outstanding derivative contract count after netting opened and closed positions.
Short Interest|Shares sold short and remaining unclosed under reporting conventions.
Short Squeeze|Price rise amplified when short sellers close positions, increasing buy demand.
Gamma Squeeze|Price feedback mechanism linked to option-dealer hedge adjustments as spot moves.
Market Maker|Participant posting bids and offers to facilitate trading, subject to venue obligations.
Dark Pool|Non-displayed trading venue; execution transparency varies by rules and jurisdiction.
Price Discovery|Process by which trading and information aggregate into observed transaction prices.
Efficient Market Hypothesis (EMH)|Hypothesis that asset prices reflect certain information sets, with several testable forms.
Behavioral Finance|Study of systematic psychological and institutional effects on financial decisions.
Herding|Market participants imitating others rather than acting solely on independent information.
Momentum Effect|Empirical tendency for past relative winners to keep outperforming over selected horizons.
Mean Reversion|Statistical tendency of a series or spread to return toward an estimated level.
Carry Trade|Funding a higher-return exposure with a lower-cost liability, incurring currency and liquidation risks.
Risk-On Risk-Off|Market shorthand for changes in appetite for risky assets and defensive positions.
Flight to Quality|Reallocation toward perceived safer assets during stress, not a universal correlation law.
Contango|Futures curve where later delivery contracts trade above nearer contracts, under the selected comparison.
Backwardation|Futures curve where nearer contracts exceed later delivery prices, not synonymous with positive carry.
Roll Yield|Futures return component from movement along a term structure under a specified rolling rule.
Basis|Difference between related prices such as spot and futures, with sign convention explicit.
Basis Risk|Residual mismatch when hedge instrument does not perfectly offset the underlying exposure.
Hedging|Risk mitigation through offsetting positions, often leaving basis, liquidity and counterparty exposures.
Arbitrage|Attempt to capture inconsistent relative prices, after allowing for timing, costs and constraints.
Diversification|Combining imperfectly correlated exposures to change portfolio risk composition.
Rebalancing|Adjusting portfolio weights back toward chosen targets on a rule or schedule.
Dollar-Cost Averaging (DCA)|Investing fixed amounts on a schedule, regardless of short-term price level.
Sector Rotation|Adjusting industry exposures based on cycle, valuation, trend or other signals.
Top-Down Investing|Allocation starting from macro and market factors before choosing securities.
Bottom-Up Investing|Security selection based first on individual issuer economics and valuations.
Value Investing|Seeking assets priced below an estimated intrinsic worth with uncertain realization timing.
Growth Investing|Emphasizing businesses with high expected expansion, often requiring valuation discipline.
Quality Investing|Preferring firms with durable profitability, balance sheets and operational consistency.
Passive Investing|Rules-based benchmark replication rather than discretionary security selection.
Active Investing|Discretionary or systematic deviations from a reference portfolio to seek excess return.
''',
'derivatives':r'''
Call Option|Contractual right, not obligation, to buy underlying exposure at a specified strike under set terms.
Put Option|Contractual right, not obligation, to sell underlying exposure at a specified strike under set terms.
Option Premium|Amount paid for option rights, depending on intrinsic and time-related risk factors.
Strike Price|Contractual price used to determine option exercise payoff.
Expiration Date|Last contractual date for exercising or settling a derivative right.
American Option|Option exercisable at any permitted time until expiry, subject to contract terms.
European Option|Option exercisable only at expiry, regardless of geographical trading venue.
At The Money|Option with underlying reference near its strike under an agreed convention.
In The Money|Option with positive immediate exercise value under the prevailing reference price.
Out Of The Money|Option with no immediate positive exercise payoff at a given reference price.
Covered Call|Long underlying combined with short call; sacrifices upside for premium and retains downside.
Protective Put|Long underlying combined with long put, providing a strike-dependent downside floor before costs.
Collar|Options overlay combining downside protection with limited upside, often around a held underlying.
Bull Call Spread|Long lower-strike call and short higher-strike call with matching expiry.
Bear Put Spread|Long higher-strike put and short lower-strike put with matching expiry.
Bull Put Spread|Short higher-strike put and long lower-strike put, typically net credit with defined risk.
Bear Call Spread|Short lower-strike call and long higher-strike call with matching expiry.
Long Straddle|Buy put and call at a common strike and expiry to gain exposure to large absolute moves.
Short Straddle|Sell put and call at common strike/expiry, earning premium while accepting large tail exposures.
Long Strangle|Buy out-of-money call and put with common expiry; generally needs larger movement than straddle.
Iron Condor|Defined-risk combination of a short put spread and short call spread around a range.
Iron Butterfly|Defined-risk short-straddle-like option structure with protective wings.
Butterfly Spread|Three-strike defined-risk option combination concentrated around a central strike.
Calendar Spread|Longer- and shorter-dated option positions often with a common strike, exposing term volatility.
Diagonal Spread|Option spread using different strikes and expiries, combining directional and term structure risk.
Barrier Option|Option that activates or expires when underlying touches a specified barrier under contract rules.
Binary Option|Contract with a predefined contingent payoff if a specified condition is fulfilled.
Variance Swap|Derivative linked to realized variance over a period, with significant convexity and gap risk.
Volatility Swap|Derivative settling according to realized volatility versus an agreed strike under contract terms.
Forward Contract|Bilateral agreement to exchange an asset or settle value at a future date at pre-agreed terms.
Futures Contract|Standardized margined derivative with settlement arrangements governed by an exchange or clearinghouse.
Margin Requirement|Collateral posted to cover trading and counterparty exposure, potentially subject to change.
Mark to Market|Revaluation of positions using observable or model prices at a specified observation time.
Counterparty Risk|Potential loss when a trading partner fails to perform contractual obligations.
Central Counterparty (CCP)|Clearing institution interposed between trades, managing member margin and default risk.
''',
'crypto':r'''
Bitcoin|Decentralized digital asset network employing proof-of-work consensus under its protocol.
Ethereum|Programmable blockchain supporting smart contracts and tokenized applications.
Blockchain|Append-only ledger structure linking blocks through cryptographic hashes and consensus rules.
Smart Contract|Program executed under a blockchain's deterministic execution environment.
Proof of Work|Consensus mechanism selecting blocks through computational puzzle effort and network validation.
Proof of Stake|Consensus family using staked value and protocol rules for participation and penalties.
Hash Rate|Estimated computing effort per time unit devoted to a proof-of-work algorithm.
Mining Difficulty|Protocol parameter controlling expected work needed to produce an accepted block.
Halving|Programmed reduction in issuance reward under a specified cryptocurrency protocol.
Stablecoin|Token intended to track a reference value via collateral, redemption or algorithmic mechanisms.
Depeg|Sustained departure of a pegged token or exchange rate from its target value.
Decentralized Finance (DeFi)|Blockchain-based financial applications using smart contracts, with code and governance risks.
Total Value Locked (TVL)|Value attributed to assets deposited in protocols, subject to double counting and price swings.
Automated Market Maker (AMM)|Smart-contract mechanism quoting trades based on pool balances or liquidity rules.
Impermanent Loss|Liquidity-provider return gap versus simply holding deposited assets after price changes.
Liquidity Pool|Assets collectively supplied to on-chain contracts to facilitate trading or other activities.
Layer 2|Scaling environment processing transactions beyond a base chain and inheriting some security properties.
Rollup|System posting proofs or transaction data summaries to an underlying blockchain.
Tokenomics|Design of token issuance, supply, incentives and utility as drivers of participant behavior.
On-Chain Analysis|Use of publicly observable ledger activity to study flows, holders or market structure.
MVRV Ratio|Market capitalization divided by estimated realized value of coins under a specified method.
Realized Cap|Token valuation measure pricing units at the value associated with their last on-chain movement.
Funding Rate|Periodic payment mechanism between perpetual-futures longs and shorts tied to basis conditions.
Perpetual Futures|Derivative resembling a futures contract without a fixed expiry, using funding to anchor prices.
Liquidation Cascade|Forced position closures that trigger additional adverse price movements and margin calls.
Wallet|Software or hardware for holding and using private keys to authorize blockchain transactions.
Private Key|Secret cryptographic signing credential controlling authorization on a blockchain.
Public Address|Public identifier used to receive cryptocurrency on a specified network.
Cold Storage|Key custody isolated from normal online systems to reduce attack surface.
Hot Wallet|Wallet key material connected to online systems for transaction convenience.
''',
}
FORMULAS={
'Gross Margin':'(revenue - COGS) / revenue', 'Return on Equity (ROE)':'net_income / average_equity',
'Return on Assets (ROA)':'net_income / average_assets','Return on Invested Capital (ROIC)':'NOPAT / average_invested_capital',
'EBITDA':'EBIT + depreciation + amortization','Net Working Capital':'current_assets - current_liabilities',
'Cash Conversion Cycle':'DIO + DSO - DPO','Price-to-Earnings (P/E)':'price_per_share / earnings_per_share',
'Price-to-Book (P/B)':'market_cap / book_equity','EV/EBITDA':'enterprise_value / EBITDA',
'Dividend Yield':'annual_dividend_per_share / share_price','Net Present Value (NPV)':'sum(CF_t/(1+r)^t) - initial_investment',
'Debt-to-Equity Ratio':'total_debt / total_equity','Current Ratio':'current_assets / current_liabilities',
'Quick Ratio':'(cash + marketable_securities + receivables) / current_liabilities',
'Net Interest Margin (NIM)':'net_interest_income / average_earning_assets','Cost-to-Income Ratio (CIR)':'operating_expenses / operating_income',
'Gross Domestic Product (GDP)':'consumption + investment + government_spending + net_exports',
'Real GDP':'nominal_GDP / (GDP_deflator / 100)','GDP Deflator':'100 * nominal_GDP / real_GDP',
'Output Gap':'(actual_GDP - potential_GDP) / potential_GDP',
'Breakeven Inflation':'nominal_yield - inflation_linked_real_yield',
'Debt-to-GDP Ratio':'government_debt / annual_nominal_GDP',
'Simple Moving Average (SMA)':'sum(price_t for last n periods) / n',
'Exponential Moving Average (EMA)':'alpha*price_t + (1-alpha)*EMA_(t-1), alpha=2/(n+1)',
'Relative Strength Index (RSI)':'100 - 100/(1 + average_gain / average_loss)',
'MACD':'EMA_12 - EMA_26 (common default)','Bollinger Bands':'SMA_n ± k*std_n',
'Average True Range (ATR)':'MA(max(H-L, abs(H-prevClose), abs(L-prevClose)))',
'Volume Weighted Average Price (VWAP)':'sum(trade_price*trade_volume) / sum(trade_volume)',
'On-Balance Volume (OBV)':'OBV_(t-1) ± volume_t by close direction',
'Rate of Change (ROC)':'100 * (price_t/price_(t-n) - 1)',
'Yield to Maturity (YTM)':'P = sum(CF_t / (1+y/m)^(m*t))',
'Modified Duration':'- (1/P) * dP/dy','DV01 (PV01)':'-dP/dy * 0.0001',
'Expected Loss (EL)':'PD * LGD * EAD','Loan-to-Deposit Ratio':'total_loans / total_deposits',
'Log Return':'ln(price_t / price_(t-1))','Compound Annual Growth Rate (CAGR)':'(end_value/start_value)^(1/years) - 1',
'Volatility':'stdev(period_returns) * sqrt(periods_per_year)',
'Beta':'cov(asset_returns, market_returns) / var(market_returns)',
'Sharpe Ratio':'(portfolio_return - risk_free_return) / volatility',
'Sortino Ratio':'(portfolio_return - target_return) / downside_deviation',
'Information Ratio':'mean(active_return) / stdev(active_return)',
'Maximum Drawdown':'min(equity_t/running_max_equity_t - 1)',
'Expectancy':'win_rate*average_win - loss_rate*average_loss',
'Market Capitalization':'share_price * diluted_or_basic_share_count',
'Bid-Ask Spread':'best_ask - best_bid',
'Put-Call Parity':'C - P = S - PV(K) (European, no distributions)',
'MVRV Ratio':'market_cap / realized_cap',
}
PITFALLS={
'chart_patterns':'Shapes are subjective; test a deterministic pivot, breakout, volume and invalidation rule before interpreting them.',
'candlesticks':'One to three candles are weak standalone evidence; verify liquidity, timeframe, surrounding trend and follow-through.',
'indicators':'Signals depend on sampling, lookback and data quality; avoid treating thresholds as calibrated probabilities.',
'fundamentals':'Accounting choices, one-offs, seasonality and sector structure limit comparability; reconcile statements.',
'macro':'Check vintage, revisions, units, seasonal adjustment and release time; correlation is not causation.',
'fixed_income':'Pricing conventions, day counts, spreads, curve shapes and credit assumptions must be made explicit.',
'quantitative':'Require out-of-sample tests, transaction costs and uncertainty bands; reject look-ahead and survivorship bias.',
'markets':'Market structure differs by venue, asset and time; distinguish quotes, trades and executable prices.',
'derivatives':'Options carry non-linear and sometimes unlimited risks; confirm expiry, multiplier, settlement and collateral.',
'crypto':'On-chain data do not reveal beneficial ownership; custody, smart-contract and market-manipulation risks remain.',
}
CATEGORY_NAME={k:k.replace('_',' ').title() for k in SEEDS}
def slugify(v):
 v=unicodedata.normalize('NFKD',v).encode('ascii','ignore').decode('ascii').lower()
 v=re.sub(r'\([^)]*\)','',v)
 return re.sub(r'[^a-z0-9]+','-',v).strip('-')
def main():
 records=[]; names=set()
 for cat,lines in SEEDS.items():
  for line in lines.strip().splitlines():
   term,definition=line.split('|',1)
   assert term not in names,term
   names.add(term)
   entry={'id':slugify(term), 'term':term, 'category':cat,'definition':definition,
          'pitfall':PITFALLS[cat], 'provenance':'original-authored',
          'investopedia_index':('https://www.investopedia.com/terms-beginning-with-'+term[0].lower()+'-'+str(4769351+ord(term[0].lower())-97)) if term[0].isalpha() else 'https://www.investopedia.com/financial-term-dictionary-4769738'}
   if term in FORMULAS:entry['formula']=FORMULAS[term]
   records.append(entry)
 ids=[r['id'] for r in records]
 assert len(ids)==len(set(ids)),[x for x in set(ids) if ids.count(x)>1]
 out=S/'data/terms.jsonl'
 out.write_text(''.join(json.dumps(x,ensure_ascii=False,sort_keys=True)+'\n' for x in records),encoding='utf-8')
 print('Built',len(records),'original entries; categories:',{k:sum(r['category']==k for r in records) for k in SEEDS})
if __name__=='__main__':main()
