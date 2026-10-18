# EMC for Aquaculture 2

ProjectE EMC values for Aquaculture 2's fish, fillets, fishing junk and neptunium
ingot: the items that come from loot tables and custom crafting rather than ordinary
recipes, so ProjectE cannot price them on its own. Fish mounts, hooks, fishing lines
and tackle boxes are already valued from their vanilla materials; from the values
this add-on writes, ProjectE derives the cooked fillet, sushi, turtle soup,
Neptune's Bounty, the neptunium block and nugget, and the neptunium gear.

Requires ProjectE and Aquaculture 2 (2.7.21+ on 1.21.1, 2.5.7+ on 1.20.1).
Download: [CurseForge](https://www.curseforge.com/minecraft/mc-mods/emc-for-aquaculture) or the GitHub Releases page.
Bugs and questions: comment on the CurseForge page, or DM [@kuronami333 on X](https://x.com/kuronami333).

- Value table and reasons: `tools/generate_emc.py`; rules and checks: `VALUE_DECISION.md`.
- Store text: `_docs/STORE_BODY_EN.md`, `_docs/STORE_SUMMARY_EN.txt`.

## What it does

Fishing junk, fish and fillets are not made from recipes, so ProjectE has no way to
price them. This mod writes those values. Fish fillets come from a custom recipe
type that ProjectE does not map, so the raw fillet is priced directly and the
cooked fillet and sushi follow from it.

Loot boxes, the worm, the six dead hook assets and the two fish that brew vanilla potions
are deliberately left unvalued; see `VALUE_DECISION.md`.

## Build

```bash
python3 tools/generate_emc.py            # writes both cells' JSON from the table
python3 tools/build_forge_jar.py         # forge-1.20.1/build/emc-for-aquaculture-0.1.0+forge-1.20.1.jar
./gradlew build --no-build-cache         # build/libs/emc-for-aquaculture-0.1.0+neoforge-1.21.1.jar
```

## License

All Rights Reserved; free to include in any modpack. See `LICENSE`.
Aquaculture 2 is made by Shadowclaimer and TeamMetallurgy; ProjectE is made by sinkillerj and contributors.
