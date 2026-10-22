# Taxonomy

All offline curated entries use one primary `category` field. Some concepts naturally span more than one domain; cross-domain analysis uses search rather than pretending classification is mutually exclusive in substance.

- `chart_patterns`: geometric price formation, continuation, reversal, breakouts and Wyckoff / harmonic descriptors.
- `candlesticks`: OHLC candle or multi-candle silhouettes, with context-dependent interpretations.
- `indicators`: trend, volatility, breadth, volume, technical transformed price representations.
- `fundamentals`: corporate financials, valuation, performance, bank-specific KPIs.
- `macro`: national accounts, inflation, labor, rates, currencies and fiscal/external statistics.
- `fixed_income`: bond valuation, spreads, credit loss, liquidity and internal treasury pricing.
- `quantitative`: return measures, empirical models, portfolio risk and option risk sensitivities.
- `markets`: venues, orders, liquidity, styles and market structure.
- `derivatives`: contracts and options payoffs/strategies.
- `crypto`: network mechanics, derivatives, DeFi and on-chain concepts.
- `unclassified`: reserved for **unreviewed title-only** optional external indexes. Never treat as a curated domain.

## Machine-readable record

```json
{
  "id": "relative-strength-index",
  "term": "Relative Strength Index (RSI)",
  "category": "indicators",
  "definition": "Original short explanation...",
  "formula": "Optional explicit formula...",
  "pitfall": "Interpretive limitation...",
  "provenance": "original-authored",
  "investopedia_index": "https://www.investopedia.com/terms-beginning-with-r-4769368"
}
```

The JSON above is a **schema illustration**, not a literal copy of an entry or a verified article URL. `data/patterns.json` relates a subset of `id`s to synthetic diagrams. `verified-links.json` stores independently validated direct URLs; arbitrary slug generation is prohibited.
