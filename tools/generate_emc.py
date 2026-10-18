"""Generate the ProjectE custom-conversion JSON for both cells.

    NeoForge 1.21.1 (ProjectE PE1.1.0):
        src/main/resources/data/aquaculture_emc/pe_custom_conversions/aquaculture_emc.json
    Forge 1.20.1 (ProjectE PE1.0.1):
        forge-1.20.1/src/data/aquaculture_emc/pe_custom_conversions/aquaculture_emc.json

The value table below is the single source for both cells; no id differs between them.

Only primitives are written here: items that no recipe makes (fish, fishing junk). Fish
mounts, hooks, fishing lines and tackle boxes are crafted from vanilla materials, so
ProjectE already values them without this add-on; the products that need this table are
the derived fish_fillet_cooked, sushi, turtle_soup, neptunes_bounty, the neptunium block
and nugget, and the 12 neptunium tools, armour, rods, knives and bows. Fish fillets come
from FishFilletRecipe (a CustomRecipe, which ProjectE does not map), so fish_fillet_raw is
written here and fish_fillet_cooked / sushi are derived from it.

Deliberately NOT valued (no line below):
- box / lockbox / treasure_chest: right-click opens them and spends the item, and the
  contents are drawn from the fishing junk and treasure pools. Any value low enough to be
  a fishing reward would let a Transmutation Table turn EMC into loot, so they stay
  unvalued. Opening a caught one and selling the contents is still the normal income.
- worm: WormFarmBlock is a ComposterBlock that drops a worm for each compostable item put
  in, so any value at all makes compost (cheap plants) a source of EMC.
- leech and jellyfish: Aquaculture brews the vanilla Healing potion from a leech and the
  vanilla Poison potion from a jellyfish, and ProjectE takes a vanilla item's value from its
  cheapest route, so a low value here lowers a vanilla value. Measured 2026-10-18 (1.20.1
  pregenerated_emc.json, addon vs no addon): leech 32 took potion{healing} from 619 to 19 and
  potion{poison} from 51 to 30, and the whole harming/poison family with it. Keeping Healing
  at 619 would need leech >= 1830, about eight gold nuggets, far above any fishing tier, so
  neither is valued.
- The six ids that exist only as lang keys and models (obsidian_hook, double_obsidian_hook,
  obsidian_note_hook, glowstone_hook, quartz_hook, soul_sand_hook): Hooks only ever defines
  EMPTY, IRON, GOLD, DIAMOND, LIGHT, HEAVY, DOUBLE, REDSTONE, NOTE and NETHER_STAR, and no
  class or registry mentions the six, so they are dead assets with no item behind them.
- Tools, rods, knives, armour and bows: ProjectE gives crafted gear EMC itself (and gear is
  not a fishing primitive). A hand value here would be a second definition.

Usage: python3 tools/generate_emc.py [--check]
"""

import argparse
import json
import os
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
REL = os.path.join("data", "aquaculture_emc", "pe_custom_conversions", "aquaculture_emc.json")
OUT_NF = os.path.join(ROOT, "src", "main", "resources", REL)
OUT_FORGE = os.path.join(ROOT, "forge-1.20.1", "src", REL)

# (suffix, emc, reason). Written to both cells.
VALUES = [
    # Fish. Bands follow vanilla fish (64), the size/rarity of the species, and the weight
    # range Aquaculture gives it (FishWeightHandler). A fish is also the input of
    # FishFilletRecipe, so its value must cover its fillets: no fish may be worth less than
    # its fillet count x 12 (see fish_fillet_raw).
    ("minnow", 16, "smallest fish, 0-1.5 lb, no fillets"),
    ("atlantic_herring", 24, "0.5-2.4 lb, one fillet"),
    ("synodontis", 24, "0.5-2.5 lb, one fillet"),
    ("bluegill", 24, "0.8-4.5 lb, one fillet"),
    ("boulti", 32, "1-9.5 lb, one fillet"),
    ("perch", 32, "0.5-6 lb, one fillet"),
    ("piranha", 32, "0.5-7.7 lb, one fillet"),
    ("blackfish", 48, "1-28 lb, two fillets"),
    ("pink_salmon", 64, "1.5-15 lb, two fillets, vanilla salmon band"),
    ("rainbow_trout", 64, "2-27 lb, two fillets"),
    ("brown_trout", 64, "1.5-44 lb, two fillets"),
    ("carp", 64, "2-40 lb, two fillets"),
    ("smallmouth_bass", 64, "1-12 lb, two fillets"),
    ("pollock", 64, "3-46 lb, two fillets"),
    ("box_turtle", 64, "turtle, no fillet; 64 keeps turtle_soup from gaining EMC"),
    ("starshell_turtle", 64, "turtle, no fillet"),
    ("muskellunge", 96, "5-70 lb, three fillets"),
    ("red_grouper", 96, "4-50 lb, three fillets"),
    ("tambaqui", 96, "7-97 lb, three fillets"),
    ("bayad", 128, "5-145 lb, four fillets"),
    ("gar", 128, "8-100 lb, four fillets"),
    ("arrau_turtle", 128, "turtle, no fillet; largest of the three"),
    ("atlantic_cod", 192, "10-211 lb, six fillets; cod band, three times vanilla cod"),
    ("catfish", 192, "10-220 lb, six fillets"),
    ("capitaine", 256, "20-440 lb, ten fillets"),
    ("arapaima", 256, "20-440 lb, ten fillets"),
    ("pacific_halibut", 384, "25-550 lb, twelve fillets"),
    ("atlantic_halibut", 448, "50-710 lb, fourteen fillets; the largest fillet count"),
    ("tuna", 512, "30-1508 lb, ten fillets; the heaviest fish"),
    ("brown_shrooma", 160, "5 brown mushrooms (5 x 32) in one shapeless craft, so 160 is exact"),
    ("red_shrooma", 160, "5 red mushrooms (5 x 32), same craft"),
    ("goldfish", 227, "one gold nugget (227); below that the nugget's value would fall"),
    # Fishing junk
    ("algae", 8, "junk item and tackle_box_green input; cheap plant"),
    ("driftwood", 32, "4 oak planks (4 x 8) from one shapeless craft, so 32 is exact"),
    ("fish_bones", 144, "3 bone meal (3 x 48); below that bone meal's value would fall"),
    ("tin_can", 196, "7 iron nuggets (7 x 28) when smelted or blasted, so 196 is exact"),
    ("message_in_a_bottle", 8, "junk item; right-click only prints a message and spends it"),
    # Fillets (FishFilletRecipe is a CustomRecipe, ProjectE does not map it)
    ("fish_fillet_raw", 12, "vanilla cod fillets into 4, 5 with a neptunium knife (x1.25 rounded "
                            "down), so the fillet must stay at or below 64 / 5 = 12"),
    # Metal. The Neptunium ingot is only obtained from the Neptune's Bounty loot box and from
    # blasting neptunium tools, so it is set here as the root of the metal.
    ("neptunium_ingot", 4608, "endgame loot metal, far above iron (256) and still below "
                              "diamond (8192); 4608 = 9 x 512 so ingot, block (41472) and "
                              "nugget (512) round-trip exactly, and 512 > 227 gold nugget"),
]


def entries() -> list[tuple[str, int]]:
    return [(s, v) for s, v, _ in VALUES]


def nf_doc() -> dict:
    return {
        "comment": "EMC for Aquaculture 2 (NeoForge 1.21.1, ProjectE PE1.1.0). "
                   "Hand-set primitives only; ProjectE derives the rest from recipes.",
        "values": {
            "before": [
                {"type": "projecte:item", "emc_value": v, "id": f"aquaculture:{s}"}
                for s, v in entries()
            ]
        },
    }


def forge_doc() -> dict:
    return {
        "comment": "EMC for Aquaculture 2 (Forge 1.20.1, ProjectE PE1.0.1). "
                   "Hand-set primitives only; ProjectE derives the rest from recipes.",
        "values": {"before": {f"aquaculture:{s}": v for s, v in entries()}},
    }


def check() -> list[str]:
    errors = []
    names = [s for s, *_ in VALUES]
    if len(names) != len(set(names)):
        errors.append("duplicate id in VALUES")
    for s, v, why in VALUES:
        if type(v) is not int or v <= 0:
            errors.append(f"{s}: value must be a positive int")
        if not why:
            errors.append(f"{s}: missing reason")
    if dict((a, b) for a, b, _ in VALUES)["neptunium_ingot"] % 9:
        errors.append("neptunium_ingot: value must be a multiple of 9")
    listed = set(names)
    forbidden = {"box", "lockbox", "treasure_chest", "worm", "leech", "jellyfish"}
    if forbidden & listed:
        errors.append(f"excluded ids were valued: {sorted(forbidden & listed)}")
    # Every filleted fish must be worth at least fillets x 12 (neptunium knife, x1.25 floor).
    fillets = {
        "atlantic_cod": 6, "blackfish": 2, "pacific_halibut": 12, "atlantic_halibut": 14,
        "atlantic_herring": 1, "pink_salmon": 2, "pollock": 2, "rainbow_trout": 2,
        "bayad": 4, "boulti": 1, "capitaine": 10, "synodontis": 1, "smallmouth_bass": 2,
        "bluegill": 1, "brown_trout": 2, "carp": 2, "catfish": 6, "gar": 4,
        "muskellunge": 3, "perch": 1, "arapaima": 10, "piranha": 1, "tambaqui": 3,
        "red_grouper": 3, "tuna": 10,
    }
    table = dict((a, b) for a, b, _ in VALUES)
    fr = table["fish_fillet_raw"]
    for fish, n in fillets.items():
        if fish not in table:
            errors.append(f"{fish}: filleted fish is not valued")
            continue
        got = int(n * 1.25)
        if table[fish] < got * fr:
            errors.append(f"{fish}: {table[fish]} < {got} fillets x {fr}")
    # Vanilla fish are filleted by the same recipe at their ProjectE values (64 each). These
    # counts are the fixed ones, valid while Aquaculture's `randomWeight` config is false
    # (the default); with randomWeight = true the count comes from the fish's weight instead,
    # so cod is not always 4.
    for item, n in (("minecraft:cod", 4), ("minecraft:salmon", 2), ("minecraft:pufferfish", 1)):
        if 64 < int(n * 1.25) * fr:
            errors.append(f"{item}: vanilla fish value 64 < {int(n * 1.25)} fillets x {fr}")
    return errors


def write(path: str, doc: dict) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(doc, f, indent=2)
        f.write("\n")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="validate the table, write nothing")
    args = ap.parse_args()
    errors = check()
    if errors:
        print("\n".join(errors))
        sys.exit(1)
    if args.check:
        print(f"ok: {len(entries())} ids in both cells")
        return
    write(OUT_NF, nf_doc())
    write(OUT_FORGE, forge_doc())
    for path in (OUT_NF, OUT_FORGE):
        with open(path, encoding="utf-8") as f:
            json.load(f)
    print(f"wrote {len(entries())} ids -> {os.path.relpath(OUT_NF, ROOT)}")
    print(f"wrote {len(entries())} ids -> {os.path.relpath(OUT_FORGE, ROOT)}")


if __name__ == "__main__":
    main()
