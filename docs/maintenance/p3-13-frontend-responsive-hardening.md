# P3-13 前端响应式运营台加固

## 背景

P3-12 自动化链路已经接入 Dashboard，但全局响应式检查仍暴露了窄屏、小窗口和内嵌浏览器下的布局问题。P3-13 先做全局 CSS 兜底，保证运营台能在手机宽度、平板宽度和桌面窗口缩小时保持可读。

## 改动范围

- Frontend 新增 `src/styles/responsive-hardening.css`。
- Frontend 新增响应式守护脚本与测试。
- Frontend `src/main.js` 引入响应式兜底样式。
- 文档补充响应式验收方式。

## 验收要求

Frontend 需要通过：

```powershell
npm run responsive-hardening
npm run test:responsive-hardening
npm test
npm run build
npm run responsive:check
```

`responsive:check` 默认检查 `http://127.0.0.1:4173/vue/`，因此需要先启动 `npm run preview`。如果检查其他地址，使用 `QUANTGOD_RESPONSIVE_URL` 指定。

## 后续维护规则

- 不要为了通过检查隐藏内容或跳过路由。
- 如果检查失败，先看 `runtime/responsive-check/report.json`，再按具体 selector 修对应 workspace。
- 表格可以横向滚动，但页面整体不应横向溢出。
- 长英文策略名、中文说明、JSON 摘要都必须可换行。

## 安全边界

- 不新增交易执行入口。
- 不修改 MT5 实盘 preset。
- 不接收 Telegram 交易命令。
- 不直接读取本地 `QuantGod_*.json` 或 CSV。
