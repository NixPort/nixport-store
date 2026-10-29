# nixport-store（简体中文说明）

> English documentation in [README.md](README.md)。两份 README 内容一致，以
> 英文版为准；其余文档（SCHEMA / CONTRIBUTING / PR 模板）仅英文。

Nixport 的 Port 目录仓库（商店数据源）。**这里只存链接与元信息**——每个条目
指向 Port 作者自己的 GitHub 仓库与 Releases，本仓库 MUST NOT 存放任何 Port
分发包（`.zip` / `.AppImage` 或任何可执行产物）。

Nixport 应用从本仓库拉取 `store.json` 渲染商店卡片：封面、名称、描述、
verified 角标；点按卡片经浏览器跳转到对应 Port 的 GitHub 页面。下载始终
发生在用户自己的浏览器里，导入走 Nixport 应用的本地导入通道。

## 仓库结构

```
store.json            ← 目录本体（nixport.catalog.v1）
schema/               ← JSON Schema（CI 校验依据）
covers/               ← 封面：covers/<id>.webp|png|jpg
.github/workflows/    ← CI：PR 必须过校验才能 merge
```

## 上架一个 Port（概览）

1. fork 本仓库；
2. 在 `store.json` 的 `ports[]` 加一个条目（字段见 [SCHEMA.md](SCHEMA.md)）；
3. 放一张封面 `covers/<id>.webp`（≤512×512、≤150KB），条目 `cover` 指向它；
4. 提 PR（会自动套 [PR 模板](.github/PULL_REQUEST_TEMPLATE.md)，需填写
   自测声明）；
5. CI 全绿 + 维护者 review 通过即 merge 上架。

细节与规范见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## verified 标记

`verified: true` 表示**仓库维护者已在本机真机（Adreno）亲自跑通**该 Port
的当前版本。它不由 PR 作者自行填写——PR 里一律写 `false`，维护者验证通过
后在 merge 时改置 `true`；Port 发新版（`version` 变更）后原标记视为过期，
须重新验证。这是商店唯一的信任背书，宁可少标，不可错标。
