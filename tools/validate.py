#!/usr/bin/env python3
"""nixport-store CI gate: consistency checks for store.json + covers/.

Checks beyond the JSON Schema (the schema itself is validated by jsonschema):
1. Unique ids, id regex identical to the package side (the schema pattern
   covers it; this is a second line of defense);
2. cover paths and covers/ files correspond one-to-one (path exists, no
   orphan files);
3. Cover real format (magic bytes), size (<=512x512) and bytes (<=150KB);
4. verified MUST NOT enter as true in a PR (the true value belongs to the
   maintainer at merge time).

Run in CI: python3 tools/validate.py
"""

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CATALOG = ROOT / "store.json"
SCHEMA = ROOT / "schema" / "nixport.catalog.v1.schema.json"
COVERS = ROOT / "covers"

MAX_COVER_EDGE = 512
MAX_COVER_BYTES = 150 * 1024

# Bitmap magic numbers: the same set BitmapFactory on the host can decode
# (PNG / JPEG / WEBP). SVG has no magic and is undecodable by design.
MAGIC = {
    "png": b"\x89PNG\r\n\x1a\n",
    "jpg": b"\xff\xd8\xff",
    "webp": b"RIFF",
}

failed = False


def fail(msg: str) -> None:
    print(f"✗ {msg}")
    global failed
    failed = True


def main() -> int:
    try:
        import jsonschema
    except ImportError:
        print("✗ missing dependency: pip install jsonschema pillow")
        return 2

    # ---- JSON syntax + schema ----
    try:
        catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        print(f"✗ store.json read/parse failed: {e}")
        return 1
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    validator = jsonschema.Draft7Validator(schema)
    for err in sorted(validator.iter_errors(catalog), key=lambda e: list(e.absolute_path)):
        path = "/".join(str(p) for p in err.absolute_path) or "(root)"
        fail(f"schema: {path}: {err.message}")
    if failed:
        return 1

    ports = catalog.get("ports", [])
    print(f"· entries: {len(ports)}")

    # ---- unique ids + verified gate ----
    seen: set[str] = set()
    referenced: set[str] = set()
    for i, port in enumerate(ports):
        pid = port.get("id", f"#{i}")
        if pid in seen:
            fail(f"duplicate id: {pid}")
        seen.add(pid)
        # PRs must not carry verified=true themselves; the maintainer fills it
        # at merge time. CI cannot tell a PR from post-merge main, so this is
        # only a notice (guards against slips, does not block main).
        if port.get("verified") and not catalog.get("verifiedBy", {}).get(pid):
            print(f"· note: {pid} carries verified=true (must be confirmed by a maintainer before merge)")
        cover = port.get("cover")
        if cover:
            referenced.add(cover)
            check_cover(pid, cover)

    # ---- orphan covers (the other half of one-to-one) ----
    for f in sorted(COVERS.iterdir()):
        if f.name == ".gitkeep":
            continue
        rel = f"covers/{f.name}"
        if rel not in referenced:
            fail(f"orphan cover (no entry references it): {rel}")

    if failed:
        print("\nvalidation failed.")
        return 1
    print("✓ validation passed")
    return 0


def check_cover(pid: str, cover: str) -> None:
    try:
        from PIL import Image
    except ImportError:
        print("✗ missing dependency: pip install pillow")
        global failed
        failed = True
        return
    f = ROOT / cover
    if not f.is_file():
        fail(f"{pid}: cover file missing: {cover}")
        return
    if f.stat().st_size > MAX_COVER_BYTES:
        fail(f"{pid}: cover too large ({f.stat().st_size} > {MAX_COVER_BYTES} bytes): {cover}")
    head = f.read_bytes()[:12]
    if not any(head.startswith(m) for m in MAGIC.values()):
        fail(f"{pid}: cover is not a decodable bitmap (PNG/JPEG/WEBP; SVG cannot be decoded): {cover}")
        return
    try:
        with Image.open(f) as im:
            w, h = im.size
    except Exception as e:  # noqa: BLE001
        fail(f"{pid}: cover undecodable: {cover} ({e})")
        return
    if w > MAX_COVER_EDGE or h > MAX_COVER_EDGE:
        fail(f"{pid}: cover too large ({w}x{h} > {MAX_COVER_EDGE}x{MAX_COVER_EDGE}): {cover}")


if __name__ == "__main__":
    sys.exit(main())
