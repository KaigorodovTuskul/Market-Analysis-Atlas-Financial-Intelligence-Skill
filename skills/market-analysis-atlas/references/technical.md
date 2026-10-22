# Technical analysis field guide

## Specify the bars before diagnosing a shape

OHLCV data require timestamp/timezone, trading calendar, corporate action and rollover policies, traded venue, session boundaries and missing-bar treatment. Log-price and arithmetic-price axes may alter apparent slopes. Daily, weekly and intraday shapes are not interchangeable.

## Primitive measurements

- Price return: `P_t/P_(t-1)-1`; log return `ln(P_t/P_(t-1))`.
- True range: `max(H-L, |H-C_prev|, |L-C_prev|)`; ATR is its smoothed series.
- EMA recursion: `EMA_t=alpha*P_t+(1-alpha)*EMA_(t-1)` with `alpha=2/(n+1)` for a conventional period setting.
- Bollinger bands: `SMA_n ± k × rolling_std_n`; specify sample/population estimator and `ddof`.
- RSI: smoothed gains and losses define `RS=avg_gain/avg_loss`; `RSI=100-100/(1+RS)`; zero-loss handling is implementation-dependent.
- MACD: commonly `EMA(12)-EMA(26)` with `EMA(9)` signal; conventions and warmup affect output.
- Stochastic: `100 × (C-L_n)/(H_n-L_n)`; define zero-range behavior and signal smoothing.
- VWAP: `sum(price×volume)/sum(volume)`, with trade/tick, typical-price and reset choices explicit.

## Detection, not wishful pattern naming

1. Freeze a deterministic peak/trough rule and minimum bar spacing.
2. Normalize tolerance by ATR or percentage; handle unequal shoulders/tops.
3. Require close beyond a selected boundary (optionally with hold/retest) rather than any intrabar wick.
4. Reject candidates with insufficient historical context, expired shape or structurally implausible geometry.
5. Log every candidate including invalidated examples; label after the fact for research but never backfill signals.

## Evidence hierarchy

Single visual match: **description**, not statistical support. Historical frequency on same in-sample chart: **exploratory**. Pre-registered detection rules, walk-forward holdout, sensitivity analysis, all costs, risk limits and Monte Carlo uncertainty: **stronger evidence**, still not a guaranteed return.

## Trading-system checks

For every chart setup explicitly state the actionable point, confirmation, invalidation, transaction costs, entry/exit timing, market impact and what would falsify the thesis. Use the 100 local schematics as illustrations, not as templates for automatic pixel matching.
