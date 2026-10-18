# EMC for Aquaculture 2

ProjectE EMC values for Aquaculture 2's fish, fillets and fishing junk. Everything
crafted from them (fish mounts, hooks, fishing lines, tackle boxes, turtle soup,
neptunium blocks and nuggets) is derived by ProjectE itself.

Requires ProjectE and Aquaculture 2 (2.7.21+ on 1.21.1, 2.5.7+ on 1.20.1).
Download: [CurseForge](https://www.curseforge.com/minecraft/mc-mods/emc-for-aquaculture) or the GitHub Releases page.

## What it does

Fishing junk, fish and fillets are not made from recipes, so ProjectE has no way to
price them. This mod writes those values. Fish fillets come from a custom recipe
type that ProjectE does not map, so the raw fillet is priced directly and the
cooked fillet and sushi follow from it.

Loot boxes, the worm, the six dead hook assets and the two fish that brew vanilla potions
are deliberately left unvalued; see `VALUE_DECISION.md`.

## Build

```
_tools/gw . build                         # 1.21.1 NeoForge -> build/libs/emc-for-aquaculture-0.1.0+neoforge-1.21.1.jar
python3 tools/build_forge_jar.py          # 1.20.1 Forge   -> forge-1.20.1/build/emc-for-aquaculture-0.1.0+forge-1.20.1.jar
```

`tools/generate_emc.py` writes the value JSON for both cells from one table
(`--check` validates it).

## Credits

Aquaculture 2 is made by Shadowclaimer and TeamMetallurgy; ProjectE is made by
sinkillerj and contributors. This is an unofficial add-on that ships only EMC data.
