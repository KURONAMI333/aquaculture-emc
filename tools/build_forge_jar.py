"""Package the Forge 1.20.1 lowcodefml data jar (no compilation, no Gradle).

Zips forge-1.20.1/src/** plus LICENSE (as LICENSE_aquaculture_emc) with fixed
timestamps, so the same sources always give the same bytes. Output:
forge-1.20.1/build/emc-for-aquaculture-<version>+forge-1.20.1.jar

Usage: python3 tools/build_forge_jar.py
"""

import hashlib
import os
import tomllib
import zipfile

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "forge-1.20.1", "src")
BUILD = os.path.join(ROOT, "forge-1.20.1", "build")
MOD_ID = "aquaculture_emc"


def collect() -> dict[str, bytes]:
    entries = {f"LICENSE_{MOD_ID}": open(os.path.join(ROOT, "LICENSE"), "rb").read()}
    for base, _dirs, files in os.walk(SRC):
        for name in files:
            full = os.path.join(base, name)
            entries[os.path.relpath(full, SRC).replace(os.sep, "/")] = open(full, "rb").read()
    return entries


def main() -> None:
    with open(os.path.join(SRC, "META-INF", "mods.toml"), "rb") as f:
        mod = tomllib.load(f)["mods"][0]
    if mod["modId"] != MOD_ID:
        raise SystemExit(f"unexpected modId {mod['modId']}")
    entries = collect()
    os.makedirs(BUILD, exist_ok=True)
    out = os.path.join(BUILD, f"emc-for-aquaculture-{mod['version']}+forge-1.20.1.jar")
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as jar:
        for name in sorted(entries):
            info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.external_attr = 0o100644 << 16
            jar.writestr(info, entries[name], compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    with zipfile.ZipFile(out) as jar:
        if jar.testzip() is not None or sorted(jar.namelist()) != sorted(entries):
            raise SystemExit("jar entry or CRC mismatch")
    data = open(out, "rb").read()
    print(f"{os.path.relpath(out, ROOT)}: {len(data)} bytes, SHA-256 {hashlib.sha256(data).hexdigest()}")


if __name__ == "__main__":
    main()
