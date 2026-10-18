Puts Aquaculture 2's catch into ProjectE: 32 fish, the fishing junk they come with, raw fillets and neptunium, so a fisher can turn a full tackle box into EMC and buy the gear they are still missing.

Without it, the whole fishing loop has no value in ProjectE. Fish, junk and neptunium come out of loot tables rather than recipes, and fillets come out of Aquaculture's own fillet recipe type, which ProjectE does not map. Every one of those reads as 0 EMC.

## How the values are set

Fish are banded by the species' size and rarity, following vanilla's 64 for cod and salmon. Minnows and other tiny catch sit at 16 to 32; the big tuna and halibut at 384 to 512. Mushroom fish are worth exactly the five mushrooms they craft into (160), and the goldfish exactly the gold nugget it smelts into (227).

Fillets are the delicate part. Aquaculture's fillet recipe is a custom recipe type, so ProjectE cannot derive it and this mod prices the raw fillet itself. That creates one thing to guard: if a fish is cheaper than the fillets inside it, you could buy the fish and fillet it for a profit, and a neptunium knife multiplies the fillet count by 1.25 on top. The fillet is pegged at 12 EMC, just under what a single vanilla cod fillets into, and every one of Aquaculture's 25 fillet-bearing fish is worth at least what its fillets are, knife included. A fish that fillets into nothing (minnow, turtles, the mushroom fish) is priced as food or as its other use.

The junk is priced against what it becomes, so that smelting or crafting it never drags a vanilla value down: fish bones at the three bone meal they make, a tin can at the seven iron nuggets it yields, driftwood at four oak planks.

Neptunium is the endgame metal and appears as loot rather than ore. The ingot, block and nugget round-trip at 1:9:81 so none of the three is a cheaper source than the others, and Neptune's Bounty is worth less than the eight ingots it takes to craft it, so there is no free loot.

## What is deliberately left out

Loot boxes (box, lockbox and treasure chest) have no EMC, even though you can catch them. They open into items drawn from the treasure pool, and any price low enough to be a fishing reward would let a Transmutation Table turn EMC into loot. Catching one and selling what is inside still works normally.

The worm has no EMC. Its worm farm is a composter, so valuing the worm at anything at all would make composting cheap plants a source of EMC.

The leech and the jellyfish have no EMC. Aquaculture brews the vanilla Healing potion from a leech and the vanilla Poison potion from a jellyfish, and ProjectE takes an item's value from the cheapest route to it, so any fishing-tier value on these two would drag down the vanilla potions that use them. Leaving the two out keeps those potions at their vanilla value, and both fish still brew as normal.

Six hook names in the files, obsidian_hook, double_obsidian_hook, obsidian_note_hook, glowstone_hook, quartz_hook and soul_sand_hook, have no item behind them at all: they only ever existed as a name and a texture. They are not valued, and they will not show up in the Transmutation Table.

Tools, rods, knives, bows and armour are left to ProjectE, which already prices crafted gear itself.

## Compatibility

Requires [ProjectE](https://www.curseforge.com/minecraft/mc-mods/projecte) and [Aquaculture 2](https://www.curseforge.com/minecraft/mc-mods/aquaculture) 2.7.21 or newer on 1.21.1 (2.5.7 or newer on 1.20.1). This is an unofficial add-on that ships only EMC data; it is not affiliated with either project. Server-friendly: install it on both sides, or on the server in a pack where the client already has ProjectE.

Aquaculture 2 is made by Shadowclaimer and TeamMetallurgy; ProjectE is made by sinkillerj and contributors.

Source code: https://github.com/KURONAMI333/aquaculture-emc
