# Frontend API client policy

## Rule

All application data comes from backend `/api/*` endpoints.

Forbidden patterns:

```js
fetch('/QuantGod_Dashboard.json')
fetch('/QuantGod_TradeJournal.csv')
```

Allowed pattern:

```js
fetch('/api/dashboard/state')
fetch('/api/trades/journal?limit=200')
```

## Dev proxy

`vite.config.js` should proxy:

```js
'/api': 'http://127.0.0.1:8080'
'/QuantGod_': 'http://127.0.0.1:8080'
```

`/QuantGod_` is only a legacy fallback and should not be used by new code.
