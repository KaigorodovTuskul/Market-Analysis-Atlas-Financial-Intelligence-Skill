---
name: market-analysis-atlas
description: Research, explain, cross-check and illustrate technical patterns, candlesticks, indicators, corporate valuation, macroeconomics, fixed income, portfolio statistics, derivatives and crypto market structure. Use for chart pattern identification, financial terminology, ratios, macro releases, market analysis or evidence-based investment research. Includes an offline original 533-concept glossary, 100 self-drawn schematics, formulas, references and optional title-index tooling.
license: MIT
metadata:
  version: "1.0.0"
  category: financial-research
  language: en
---

# Market Analysis Atlas

**Explain the mechanism, specify assumptions, test competing interpretations, and keep sources and confidence visible.** This skill is an analytical reference, not a trading-signal engine or a copy of any website.

## Choose the working lens

1. **Chart, candle, momentum, volatility, market structure:** read [Technical analysis](references/technical.md) and, for shape identification, [Patterns](references/patterns.md) or the [100 illustrated pattern cards](references/pattern-index.md).
2. **Company accounts, valuation or bank profitability:** read [Fundamentals](references/fundamental.md).
3. **Inflation, growth, central banks, employment, FX, releases:** read [Macroeconomics](references/macro.md).
4. **Duration, yield, spreads, liquidity, FTP, credit:** read [Fixed income](references/fixed-income.md).
5. **Factors, backtesting, econometrics, options Greeks:** read [Quantitative methods](references/quant.md).
6. **Crypto structure / on-chain metrics:** read [Crypto](references/crypto.md).
7. **Evidence quality and reporting:** always apply [Evidence standard](references/evidence.md); for consequential conclusions also use [Risk checks](references/risk.md).

Only open the relevant references, not the full encyclopedia into context.

## Search the offline reference

From repository root:

```bash
python scripts/atlas.py "head and shoulders" --detail
python scripts/atlas.py "duration" --limit 12
python scripts/atlas.py --category macro --limit 100
python scripts/atlas.py --stats
python scripts/atlas.py "bond" --json
```

The substantive offline reference is [data/terms.jsonl](data/terms.jsonl) (533 original short definitions across ten subjects). [data/patterns.json](data/patterns.json) maps 100 chart/candlestick concepts to original local SVGs in [assets/charts](assets/charts). Use the diagram only for illustration; it is schematic synthetic data, **not** a chart from Investopedia and not a certified classifier.

## Non-negotiable method

**Define** — State instrument, currency, benchmark, timestamp, timeframe, unit, data vintage, adjusted/unadjusted prices, and a crisp definition. If the entry lacks a formula, derive it with assumptions or verify against an authoritative primary source; do not invent it.

**Observe** — Separate visible data and measured levels from inferred relationships. For a chart: specify exact pivot rules, lookback and tolerance. For macro: use release dates and revision vintages. For statements: align accounting periods and standards.

**Test** — Try the competing interpretation, invalidate conditions, false-positive risk, costs, and alternative explanations. Correlation ≠ causation. A plausible pattern ≠ measured edge.

**Quantify** — Give a calculation or scenario when data exist. Missing data → say what inputs are required; no fabricated prices, forecasts, market caps or model performance.

**Communicate** — Use a compact answer with finding, evidence, conditional interpretation, risks, and source dates/links. Distinguish fact from hypothesis and confidence.

## Chart pattern protocol

- Choose the market and bar frequency. Confirm OHLCV completeness, splits/roll adjustments and session policy.
- Define pivot high/low (e.g., neighborhood bars), equality tolerance, breakout threshold, volume condition and expiry.
- Draw candidate boundaries and **invalidation**; no hindsight labeling as an executed signal.
- Measure prior base rates and strategy outcomes only on out-of-sample data, with slippage and fees.
- Avoid doubling up highly collinear indicators as though they were independent confirmations.

## Macro protocol

- Document geographic scope, release agency, first publication versus latest revision, frequency and units.
- Separate nominal from real, level from growth, month-over-month from year-over-year, seasonally adjusted from raw.
- Model transmission separately through rates, yields, credit, FX, expectations and valuation rather than assuming a single asset-price sign.
- For live claims, fetch current information; offline reference content does not provide updated macro series or securities prices.

## Evidence and licensing boundaries

- Our included descriptions, methods and diagrams are **originally authored** and may be revised independently.
- Investopedia's [dictionary index](https://www.investopedia.com/financial-term-dictionary-4769738) is an external discovery reference. Its article descriptions and pictures are **not bundled or mirrored**.
- `investopedia_index` is a **letter index URL**, not proof of a verified article-level match. `source_url` exists only when a direct link was independently verified or supplied.
- The optional `sync_index.py` can catalog public *titles and links only*, **only after explicit opt-in** and if robots/site permissions allow; it does not import article bodies or images.
- No unsourced success rates, invented backtest statistics, certainty claims, or personalized position sizing.

## Example tasks

- “Show a conditional head-and-shoulders read on this uploaded chart and draw neckline / invalidation.”
- “Compare ROIC and ROE across three companies; explain leverage distortions.”
- “Explain why an inverted yield curve need not mechanically cause falling equities.”
- “Audit this RSI strategy for look-ahead bias and out-of-sample leakage.”
- “Decompose CNY loan funding, forward hedge costs and effective RUB APR.”

For deeper scenarios see [example analyses](../../examples) in the repository; tests and installation are described in the root README.
