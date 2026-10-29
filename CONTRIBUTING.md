# Submitting a Port entry

Thanks for listing! The whole flow runs through GitHub PRs — no private
channels.

## How to list

1. **Fork** this repository;
2. **Add a cover**: put `covers/<id>.webp` (or `.png` / `.jpg`) under
   `covers/`. Requirements: ≤512×512 pixels, ≤150KB; it must be the Port's
   real cover art, not an upscaled stretch;
3. **Edit `store.json`**: append an entry to the `ports[]` array (field
   reference in [SCHEMA.md](SCHEMA.md)):
   - `id` MUST be **exactly** the `id` in your Port package's `port.json`
     (the app matches its "Installed" badge on it);
   - `release` should be `https://github.com/<you>/<repo>/releases/latest`
     so shipping a new version doesn't require a catalog change;
   - `verified` is always `false` — only repository maintainers set it;
4. **Open a PR**: title suggestion `add: <id> <name>`; the PR template asks
   you to confirm each item;
5. **CI green**: validation failures come back with reasons (JSON syntax,
   field over limits, cover over limits, path mismatches…); fix until green;
6. **Human review**: a maintainer confirms the links are real and the package
   follows the [Port packaging rules](https://github.com/NixPort), then
   merges. Catalog updates reach users within minutes (the app refreshes on
   entering the Store).

## Shipping a new version

After publishing a new Port release, open a small PR: bump `version` (a
`releases/latest` link needs no change), swap the cover if needed. The
maintainer re-verifies before restoring / keeping `verified`.

## Delisting

Deleting an entry removes it from the catalog (explain why in the PR). Cached
copies on devices disappear at the next successful refresh; Port authors
should note the removal in their own repository's README.

## Red lines

- This repository MUST NOT contain any distributable Port artifacts
  (`.zip` / `.AppImage` / executables) — violations are rejected and the
  entry removed;
- `id` conflicts with an existing entry (one id, one Port);
- Cover art infringement (stealing other stores' art, or clearly copyrighted
  assets without permission).
