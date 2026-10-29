# nixport-store

> 简体中文说明见 [README.cn.md](README.cn.md)。

Nixport's Port catalog repository (the data source behind the in-app Store).
**This repository only holds links and metadata** — each entry points to the
Port author's own GitHub repository and releases. No Port packages (`.zip`,
`.AppImage`, or any executable artifact) MUST ever be committed here.

The Nixport app fetches `store.json` from this repository to render Store
cards: cover, name, description, and the verified badge. Tapping a card opens
the Port's GitHub page in the user's browser. Downloads always happen in the
user's own browser; installation goes through the app's local import channel.

## Repository layout

```
store.json            ← the catalog itself (nixport.catalog.v1)
schema/               ← JSON Schema (what CI validates against)
covers/               ← covers: covers/<id>.webp|png|jpg
.github/workflows/    ← CI: a PR must pass validation before it can merge
```

## Listing a Port (overview)

1. Fork this repository;
2. Add an entry to `ports[]` in `store.json` (fields documented in
   [SCHEMA.md](SCHEMA.md));
3. Add a cover `covers/<id>.webp` (≤512×512, ≤150KB) and point the entry's
   `cover` at it;
4. Open a PR (the [PR template](.github/PULL_REQUEST_TEMPLATE.md) applies
   automatically; it asks for a self-test statement);
5. CI green + maintainer review = merge, and the entry goes live.

Details and rules in [CONTRIBUTING.md](CONTRIBUTING.md).

## The verified badge

`verified: true` means **the repository maintainers have personally run the
current version of this Port on a real device (Adreno)**. It is never
self-reported — PR authors always set `false`; the maintainer flips it to
`true` at merge time after verifying. When a Port ships a new version
(`version` changes), the badge is considered stale and must be re-verified.
This is the Store's only trust signal: better to under-mark than to mis-mark.
