# Quantitative finance and reproducible research

## Return conventions

Distinguish simple versus log returns, total-return versus price-only, arithmetic versus geometric annualization, sample frequency, risk-free series matched by currency and tenor, and volatility as an estimated parameter rather than a known constant.

## Performance

Sharpe, Sortino, drawdown, information ratio, exposure and turnover each answer different questions. Sharpe is unreliable for heavily autocorrelated or skewed returns without adjustments. Use confidence intervals and multiple-testing controls.

## Backtesting

Maintain chronological train/validation/test partitions; point-in-time membership, delisting returns, market holidays, earnings release time, futures continuous-roll method and split-adjustment policy. Include commissions, spread, slippage, borrow availability, impact, margin calls and hedging resets. Log unsuccessful parameter sets.

## Models

VAR impulse responses rely on shock identification; Granger causality is predictive, not causal. Nonstationary regressions risk spurious significance. Kalman filters require an observation/state specification; EMAs are not Kalman filters by default. PCA factors maximize variance, not guaranteed explanatory causality.

## Options

Greeks are model sensitivities, not bounded risk measurements. Near expiry, discrete hedging and jumps dominate. Define market convention for 1-vol-point vega, theta in days or years, rates in bps, and the implied-volatility surface across tenor and moneyness.
