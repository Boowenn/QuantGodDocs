# Frontend API Client Rules

## 规则

Frontend 只能调用：

```text
/api/*
```

Frontend 禁止调用：

```text
/QuantGod_*.json
/QuantGod_*.csv
C:\...\MQL5\Files\...
../QuantGodBackend/...
```

## 为什么禁止直接读文件

直接读 runtime 文件会造成：

1. 前端和 backend 文件布局耦合。
2. CSV/JSON schema 改动无法统一 envelope。
3. CI 很难检测真实数据路径漂移。
4. 拆仓库后 frontend 无法独立开发和测试。

## 推荐 service wrapper

```js
async function fetchJson(url, fallback = null) {
  const response = await fetch(url, {
    headers: { Accept: 'application/json' },
    cache: 'no-store',
  })
  if (!response.ok) return fallback
  return response.json()
}

export function loadGovernanceAdvisor() {
  return fetchJson('/api/governance/advisor')
}
```

## CI Guard

`QuantGodFrontend` 应运行：

```powershell
npm run contract
npm test
npm run build
```

Contract guard 应允许 UI 展示 `QuantGod_*.json` 这种文件名文本，但必须禁止 `/QuantGod_*.json` 或 `/QuantGod_*.csv` 本地路径读取。
