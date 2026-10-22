# Chart and candle pattern taxonomy

## Reversal hypotheses

- Head-and-shoulders/inverse: identify three swing extremes, estimate a neckline through two intermediate pivots, then demand directional confirmation. Idealized necklines need not be horizontal.
- Double/triple top or bottom: use time separation and a tolerance band, not forced exact equality. Confirmation level is the relevant intervening reaction, not merely the second/third touch.
- Rounded transitions, diamonds, islands, V-turns: especially prone to discretionary drawing and hindsight bias.

## Continuation and compression hypotheses

- Ascending/descending/symmetrical triangles: explicitly estimate slopes of bounding highs and lows. Triangle direction is conditional, not guaranteed by nomenclature.
- Flags and pennants: demand a preceding fast move, limited consolidation relative to impulse, and follow-through after boundary break.
- Wedges and channels: document slope, convergence or parallelism; very different from a single wedge-shaped screenshot.
- Rectangles: check sufficient support/resistance tests, duration and volume behavior.
- Gaps: differentiate an actual untraded interval from an artifact of missing data, illiquidity or futures roll.

## Candlesticks

Candle is `(open, high, low, close)`. A doji has a small real body; hammer/shooting star depend on shadow-to-body ratios *and* preceding trend. Engulfing describes **bodies** unless using a stricter range rule. Multi-bar stars and soldiers depend on contextual trends, actual gap conventions and adequate follow-through.

## Researcher checklist

- What exact OHLCV thresholds identify the shape? Was the threshold selected before testing?
- How often does it occur by asset, liquidity, regime and lookback?
- Compare an out-of-sample event study with a baseline having similar risk exposure.
- Include non-trading time, fees, borrow cost, spread, funding, slippage and adverse selection.
- Distinguish occurrence likelihood from conditional forward return. Report distribution and confidence intervals, not only win rate.

## Diagrams

`assets/charts/*.svg`: exactly 63 original schematic chart-pattern diagrams and 37 standalone candlestick sketches. Diagrams favor legibility and geometric intent over mechanically valid real-world detection for every convention. The original diagram code is in `scripts/render_charts.py`.
