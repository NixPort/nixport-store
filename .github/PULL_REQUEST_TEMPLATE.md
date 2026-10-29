## List / update a Port entry

<!-- Title suggestion: add: <id> <name>  or  update: <id> <version> -->

### Entry details

<!-- Fill in each item; write "none" where it does not apply -->

- **id**: `<id>` (MUST match the id in the package's port.json)
- **name**:
- **version**:
- **repo**:
- **release**:
- **cover**: `covers/<id>.<ext>` (≤512×512, ≤150KB)

### Self-test statement (check as the PR author)

- [ ] I have imported and run this Port package on a real device with the current Nixport app (legacy flavor)
- [ ] The entry's `id` in `store.json` is exactly the `id` in the package's `port.json`
- [ ] The `release` link points to real Releases (a package can actually be downloaded there)
- [ ] The cover is this Port's real cover art, not infringing, within the size and byte limits
- [ ] The entry contains no distributable artifacts: package files live only in the Port repository's Releases

### Maintainer use only

- [ ] Links and package shape verified (follows the Port packaging rules)
- [ ] `verified` manually verified (runs on a real device at the current version) → set `true` at merge
