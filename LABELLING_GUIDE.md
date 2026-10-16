# Labeling Guide
Goal: Set rules for how price_usd is set based on edge cases where wording is not definitive
Rules (Case, price_usd value):
- (Cash plus equity (BMG/Concord: $1.16B cash plus 33% ownership), null)
- (Cash plus stated debt assumed, or an earn-out with a dollar cap, sum into an int if all are in dollars)
- ("Approximately $1B", 1000000000)
- ("More than $500M" or "up to $500M", null)
- (Non-USD amount (€, £), convert to dollar amount using current conversion rates if currency recognized)
- buyers and sellers if deal_type equals "merger"