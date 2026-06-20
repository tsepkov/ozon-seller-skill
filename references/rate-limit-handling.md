# Handling Ozon API Rate Limits (Turnover Analytics)

The `/v1/analytics/turnover/stocks` endpoint (used by `analytics_stocks_turnover.py`) is strictly limited to **1 request per minute**.

## The Problem
Attempting to gather turnover data for a full product catalog (e.g., 20+ SKUs) using standard sequential tool calls will trigger an `Error 429 (Too Many Requests)` and block the agent.

## The Solution: Throttled Background Collection

When you need data for a large set of SKUs, do not call the script repeatedly in the chat. Instead, create and run a background Python script.

### Implementation Pattern
1. **Map IDs to SKUs:** Use `product_info.py` to get the actual `sku` for each `product_id`.
2. **Create a Loop Script:** Write a script that:
   - Iterates through the SKU list.
   - Executes the `analytics_stocks_turnover.py` script via `subprocess`.
   - Appends results to a local JSON file.
   - **Crucially: `time.sleep(61)`** after every single request.
3. **Run in Background:** Start the script using `terminal(background=True)`.
4. **Poll/Wait:** Monitor the output file or wait for the process to complete before analyzing the data.

### Example Loop Logic (Python)
```python
import time, json, subprocess

skus = [...] # List of SKUs
results = []
for sku in skus:
    res = subprocess.run(["python", "analytics_stocks_turnover.py", "--sku", str(sku)], capture_output=True, text=True)
    if res.returncode == 0:
        results.append(json.loads(res.stdout))
    time.sleep(61) # Avoid 429

with open("results.json", "w") as f:
    json.dump(results, f)
```
