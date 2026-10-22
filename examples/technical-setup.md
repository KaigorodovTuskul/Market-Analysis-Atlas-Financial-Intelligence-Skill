# Example — pattern read with falsification

**Prompt:** "Is this head-and-shoulders pattern actionable on a provided OHLCV series?"

**Required process:** (1) state timeframe, adjustment, dates and completeness; (2) define a pivot rule and tolerance; (3) find candidate head/shoulders and neckline from actual OHLCV, not an abstract picture; (4) require chosen close/volume confirmation; (5) specify invalidate level and failed cases; (6) never invent a success probability; (7) optionally backtest on a clearly segregated holdout with trading costs.

**Bad answer:** "It looks like head and shoulders; 80% chance price falls." No sample, identification rule or outcome base rates support that number.
