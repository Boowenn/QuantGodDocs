# 四仓库联动 Contract

## 联动流

```text
Frontend source change
  -> npm run build
  -> dist/
  -> Infra sync-frontend-dist
  -> Backend Dashboard/vue-dist
  -> localhost:8080/vue/
```

```text
Backend API change
  -> backend route/test update
  -> Docs api-contract update
  -> Frontend service wrapper update
  -> Infra workspace verify/test
```

## API Base URL

开发时 Frontend 默认通过 Vite dev server 调用 backend：

```text
http://127.0.0.1:8080/api/*
```

构建后，Frontend 静态资源由 backend dashboard server 提供，API 仍然是同 origin `/api/*`。

## Manifest 规则

每个仓库可以维护自己的 `repo-manifest.json`，字段至少包括：

- `repo`
- `role`
- `apiContractVersion`
- `sourceOfTruth`
- `forbiddenContents`
- `linkedRepos`

Docs 仓库中的 `docs/contracts/repo-manifest.schema.json` 是轻量 schema，供人工 review 和脚本扩展使用。

## 破坏性变更流程

如果必须删除或重命名 endpoint：

1. Backend 先保留旧 endpoint 作为 alias，新增新 endpoint。
2. Docs 标记旧 endpoint 为 deprecated。
3. Frontend 迁移。
4. Infra/CI 通过后，再在下一轮删除 alias。

不要在同一提交里同时删除 endpoint 和迁移前端，否则 bisect 和回滚都会变困难。
