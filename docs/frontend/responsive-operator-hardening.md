# P3-13 前端响应式运营台加固

## 目标

P3-13 只解决前端响应式问题：窄屏横向溢出、标题裁剪、表格不可滚动、Dashboard 自动化链路长文本溢出、MT5/Research 等页面在 320/360/390/612/900 宽度下布局压力过大。

## 范围

新增 `src/styles/responsive-hardening.css`，并在 `src/main.js` 中导入。该文件只做 CSS 层面的响应式兜底，不改变业务 API，不读本地文件，不引入交易入口。

## 验收

Frontend 需要通过：

```powershell
npm run responsive-hardening
npm run test:responsive-hardening
npm test
npm run build
npm run responsive:check
```

如果 `responsive:check` 仍失败，应查看 `runtime/responsive-check/report.json` 中的具体 selector，再做 workspace 级精修；不要为了通过检查隐藏内容或跳过 route。

## 安全边界

- 前端仍然只通过 `/api/*` 获取数据。
- 不新增 Quick Trade、OrderSend、Telegram command 或 live preset 修改入口。
- 表格可以横向滚动，但不能直接读取 `QuantGod_*.json` 或 CSV。
