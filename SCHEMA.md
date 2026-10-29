# store.json — nixport.catalog.v1

The catalog is `store.json` at the repository root; the schema value is fixed
to `nixport.catalog.v1`. The machine-checkable JSON Schema lives at
[schema/nixport.catalog.v1.schema.json](schema/nixport.catalog.v1.schema.json).

## Top-level structure

```json
{
  "schema": "nixport.catalog.v1",
  "updated": "2026-10-29",
  "ports": [ { ...entry... } ]
}
```

| Field | Required | Description |
|---|---|---|
| `schema` | ✓ | Fixed `nixport.catalog.v1`; how the Nixport app recognizes the catalog |
| `updated` | — | Last catalog update date (ISO `YYYY-MM-DD`), presentational only |
| `ports` | ✓ | Entry array; capped at 500 entries |

## Entry fields

Entry vocabulary aligns with the in-package `port.json` (`nixport.port.v1`):
`id` / `name` / `version` / `description` / `upstream` carry identical
semantics — what a user sees in the Store matches the Library card after they
download and import the Port. Store-side fields are **presentational free
text or links**; the Nixport host never interprets their meaning.

```json
{
  "id": "spartanport-mhgu",
  "name": "MHGU",
  "version": "2.0.0",
  "description": "Monster Hunter GU port launcher: patches, cheats, graphics options",
  "upstream": "https://github.com/…",
  "repo": "https://github.com/NixPort/spartanport-mhgu",
  "release": "https://github.com/NixPort/spartanport-mhgu/releases/latest",
  "cover": "covers/spartanport-mhgu.webp",
  "author": "NixPort",
  "tags": ["monster-hunter", "launcher"],
  "compat": "Adreno 6xx+ · 8GB RAM+",
  "verified": false
}
```

| Field | Required | Description |
|---|---|---|
| `id` | ✓ | The Port identity, MUST match `^[a-z0-9][a-z0-9_-]*$`; **identical to the `id` in the package's `port.json`** (the app matches its "Installed" badge on it; importing the same id = update) |
| `name` | ✓ | Card title; ≤200 chars |
| `version` | — | Recommended; the Port's current release version. MUST be updated when a new version ships |
| `description` | — | One-line description; ≤2000 chars |
| `upstream` | — | Upstream project / original game info page |
| `repo` | ✓ | The Port's GitHub repository page (the tap-through fallback) |
| `release` | — | Direct link to Releases (tapping a card prefers it); `releases/latest` is recommended so version bumps don't touch the catalog |
| `cover` | ✓ | Relative path `covers/<id>.<ext>`; format webp / png / jpg, ≤512×512, ≤150KB |
| `author` | — | Author / maintainer name; ≤100 chars |
| `tags` | — | Tag array; ≤20 items, each ≤50 chars |
| `compat` | — | Device requirements in one line (free text); ≤200 chars |
| `verified` | — | See the [verified rules](README.md#the-verified-badge); always `false` in PRs |

Constraints (CI-enforced, plus defensive checks on the host side):

- `repo` / `release` / `upstream` MUST be `https://` links;
- `cover` MUST be a relative path, MUST NOT start with `/` or contain `..`,
  and MUST correspond to an actual file under `covers/` (one-to-one);
- Any field over its length cap fails validation (the host's parser enforces
  the same caps).

## Forward compatibility

Same policy as `port.json`: the host MUST ignore unknown fields — additive
evolution only. New fields do not bump the schema value; breaking changes do
(`nixport.catalog.v2`), and the host treats an unrecognized schema value as
"unparseable" and keeps its cache.
