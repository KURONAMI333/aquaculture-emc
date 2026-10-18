# Value decisions — EMC for Aquaculture 2 0.1.0

The value table and the reason for every number live in `tools/generate_emc.py`
(`VALUES`). This file records the rules behind the table and how it was checked.

## Sources

- Ids and recipes: the CurseForge release jars `Aquaculture-1.21.1-2.7.21.jar`
  (SHA-512 `532571f9…557386d`) and `Aquaculture-1.20.1-2.5.7.jar`
  (SHA-512 `0ce772a8…093b4ed3`), fetched to `/tmp/emc-aquaculture-20261018/`. Read as
  jars, not as a branch checkout.
- Vanilla anchors: the ProjectE PE1.1.0 (1.21.1) and PE1.0.1 (1.20.1) jars (`defaults.json`,
  `metals.json`) and their runtime values. Fish 64 (cod/salmon/pufferfish/tropical_fish),
  bone meal 48, bone 144, gold nugget 227, iron nugget 28, gold ingot 2048, iron ingot 256,
  diamond 8192, nautilus shell 1024, clay ball 16, oak planks 8, brown/red mushroom 32,
  stick 4, leather 64.

## Rules

1. **One table, both cells.** 39 ids are written by hand and every one of them has the same
   value on NeoForge 1.21.1 and Forge 1.20.1. The survey of both host jars returns the same
   classification for every id, so there is nothing to branch on.
2. **Only primitives are written.** Nothing that a recipe makes is listed. Fish mounts,
   hooks, fishing lines and tackle boxes are crafted from vanilla materials, so ProjectE
   already values them without this add-on (add-on-absent dump: `iron_hook` 112,
   `fishing_line` 304, `tackle_box` 3650, `oak_fish_mount` 152). The products that resolve
   only because of this table are the 18 grounded in the primitives below:
   `fish_fillet_cooked`, `sushi`, `turtle_soup`, `neptunes_bounty`, the `neptunium_block`
   and `neptunium_nugget`, and the 12 neptunium tools, armour, rods, knives and bows.
3. **The raw fillet is written because ProjectE cannot derive it.** `FishFilletRecipe`
   extends `CustomRecipe`, and ProjectE's `CraftingMapper` skips `recipe.isSpecial()`
   recipes, so `fish_fillet_raw` is a primitive here and `fish_fillet_cooked` and `sushi`
   derive from it.
4. **A fish must cover the fillets inside it.** The fillet recipe returns the fish's fillet
   count, and a neptunium knife multiplies that by 1.25 and floors it. The worst case is
   vanilla cod: 4 fillets become `int(4 × 1.25) = 5`, so the fillet has to stay at or below
   64 / 5 = 12, and every one of the 25 fillet-bearing fish is worth at least its knife
   fillet count × 12. `generate_emc.py`'s `check()` enforces both directions.
5. **Junk is priced against what it becomes**, so that using it never drags a vanilla value
   down: `fish_bones` 144 is exactly 3 bone meal, `tin_can` 196 exactly 7 iron nuggets,
   `driftwood` 32 exactly 4 oak planks, `goldfish` 227 exactly the gold nugget it smelts
   into, and the two shrooma fish 160 exactly the 5 mushrooms they craft from.
6. **The metal is a root with a clean round trip.** Neptunium has no ore: the ingot comes
   from the Neptune's Bounty loot box and from blasting neptunium gear. The ingot is 4608
   (9 × 512), so the block (41472) and the nugget (512) round-trip at 1:9:81 with no cheaper
   direction, and the nugget is above the gold nugget (227). 4608 is below diamond's 8192.
   `neptunes_bounty` is derived from its 8-ingot recipe, so it is worth exactly what it
   costs to craft (36864). Opening one never returns more than that: the best single
   outcome is the neptunium chestplate at 36864, and the expected haul is about 15477
   (42% of the craft cost), so the box is a fishing reward rather than a source of EMC.
7. **Gear is not written.** ProjectE gives crafted tools, rods, knives, bows and armour their
   own value. A hand value would be a second definition.
8. **A fish with no fillet is priced as food or as its other use.** The three turtles are 64
   / 64 / 128 and `box_turtle` at 64 keeps `turtle_soup` from gaining EMC over the turtle it
   is made from.
9. **Two whole classes of ids are left out rather than valued** (details in the docstring of
   `tools/generate_emc.py`): the loot boxes (box, lockbox, treasure chest), where any value
   low enough to be a fishing reward would let a Transmutation Table turn EMC into loot; the
   worm, because `WormFarmBlock` is a composter and any value at all would make compost a
   source of EMC; and the six hook names (obsidian_hook, double_obsidian_hook,
   obsidian_note_hook, glowstone_hook, quartz_hook, soul_sand_hook) that have no item behind
   them.
10. **A host item that brews a vanilla potion is not valued.** Aquaculture brews the vanilla
    Healing potion from a leech and the vanilla Poison potion from a jellyfish, and ProjectE
    takes a vanilla item's value from its cheapest route, so a low value here lowers a
    vanilla value. Measured on both cells (full value dumps, below): with `leech` 32 and
    `jellyfish` 64 the add-on took `potion{healing}` from 619 to 19 and `potion{poison}` from
    51 to 30, and the whole harming/poison family with them. Keeping Healing at 619 would
    need `leech ≥ 1830`, about eight gold nuggets, far above any fishing tier, so neither is
    valued. Nothing else in the table is an input to a vanilla item.

## Checks run (2026-10-18, headless servers on JDK 21)

| Check | 1.21.1 NeoForge | 1.20.1 Forge |
|---|---|---|
| `emc_survey.py --verify-values` (ids exist in the host jar) | 39 / 39, 0 missing | 39 / 39, 0 missing |
| `emc_lint.py` confirmed findings (A) | 0 | 0 |
| `emc_lint.py` candidate findings (B) | 0 | 0 |
| Host ids already valued by ProjectE tags / forced to 0 by blacklist | 0 / 0 | 0 / 0 |
| ProjectE parse errors | 0 (after `/reload`) | 0 |
| EMC values registered (baseline → with add-on) | 1493 → 1550 | 1395 → 1452 |
| `EMC Exploit` log lines vs baseline | identical (3, all vanilla) | identical (4, all vanilla) |
| Value table entries matching their runtime value | 39 / 39 | 39 / 39 |
| Existing values changed (full value-file diff) | 0 | 0 |
| Values added / removed by the add-on | +57 / 0 | +57 / 0 |

The 57 added values are the 39 hand-set ids plus 18 derived ones (fish_fillet_cooked, sushi,
turtle_soup, neptunes_bounty, neptunium_block, neptunium_nugget and the 12 neptunium tools,
armour and bows). The baseline `EMC Exploit` lines are vanilla only (gold nugget 9→ingot,
iron nugget 9→ingot, andesite, and `disc_fragment_5` on 1.20.1); the add-on adds none.

## The potion deflation, and how it was caught

Rule 10 was found by the full-value diff, not by the checks that were expected to catch this
type. On 1.21.1 the log-level `EMC Exploit` line diff was **identical** with and without the
add-on while the add-on was deflating 28 vanilla potions, so that diff alone does not see
this class. The 1.20.1 `pregenerated_emc.json` diff did, and re-running the 1.21.1 server
with `usePregenerated = true` in `config/projecte/mapping.toml` (which does work on PE1.1.0;
it writes `config/ProjectE/pregenerated_emc.json`, a JSON list of `{item, emc, data?}`)
reproduced the same 28 entries with the same numbers on that cell.

- 1.20.1: baseline 1395 values; with the pre-fix add-on 1454 (28 changed, 59 added, 0
  removed); with the fixed add-on 1452 (0 changed, 57 added, 0 removed).
- 1.21.1: baseline 1493; pre-fix 1552 (28 changed, 59 added, 0 removed); fixed 1550
  (0 changed, 57 added, 0 removed).

Before concluding that the potion family is a run-to-run property of ProjectE's mapper (as was
recorded for another host in this series), the same configuration was run twice on this mod:
baseline 1 and baseline 2 were byte-identical (0 of 1395 changed), and add-on run 1 and run 2
were byte-identical (0 of 1454 changed). The difference therefore came from the add-on, and
the brewing recipes above name the cause.

## Known, not fixed here

- Aquaculture's leech and jellyfish are catchable and have no EMC. That is rule 10: their
  only use that reaches a vanilla item is brewing, and valuing them below the potion they
  brew would deflate it. A player who wants EMC for them can brew instead.
- Neptune's Bounty is worth exactly the 8 ingots it is crafted from (36864), and opening
  one never returns more than that. Its loot pool (one roll, 13 entries: the ingot at
  weight 2, each of the 12 neptunium gear items at weight 1) plus the two junk rolls
  average about 15477 EMC, 42% of the craft cost; the best single outcome is the
  neptunium chestplate at 36864. That is deliberate: the box is a fishing reward, not an
  EMC source.
