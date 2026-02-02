# Functions API

The Functions API (`com.iamkaf.amber.api.functions.v1`) provides a consolidated set of utility classes for common operations in your mod. These replace the old "Helper" classes that are now deprecated.

## Overview

The Functions API consists of 5 main classes:

| Class | Purpose |
|-------|---------|
| [ClientFunctions](client) | Client-side rendering, HUD, tooltips, text writing |
| [ItemFunctions](item) | Item & inventory operations, enchantments, armor helpers |
| [MathFunctions](math) | Math utilities, random numbers, probability, clamping |
| [PlayerFunctions](player) | Player state, inventory, messaging, abilities, etc. |
| [WorldFunctions](world) | World/level operations, sounds, entities, biomes, time, geometry |

## Migration from Old Helper Classes

If you're using the old deprecated helper classes, see the [Migration Guide](../../advanced/migration#functions-api-migration) for details.

::: warning Deprecated Classes
The following classes are deprecated and will be removed in Amber 10.0:

- `KeybindHelper` → `registry.v1.KeybindHelper`
- `FeedbackHelper` → `PlayerFunctions`
- `Chance` → `MathFunctions`
- `CommonUtils` → `WorldFunctions`
- `SoundHelper` → `WorldFunctions` / `PlayerFunctions`
- `ItemHelper` → `ItemFunctions`
- `InventoryHelper` → `ItemFunctions`
- `EnchantmentUtils` → `ItemFunctions`
- `CommonClientUtils` → `ClientFunctions`
- `BoundingBoxMerger` → `WorldFunctions.mergeBoundingBoxes()`
- `SmartTooltip` → `ClientFunctions.SmartTooltip`
- `ArmorTierHelper` → `ItemFunctions`
:::

## Quick Examples

### Client Functions (HUD Rendering)

```java
// Check if HUD should render
if (ClientFunctions.shouldRenderHud()) {
    // Render text
    ClientFunctions.renderText(graphics, font,
        Component.literal("Hello"), 10, 10, ClientFunctions.WHITE);
}
```

### Math Functions (Probability)

```java
// 30% chance
if (MathFunctions.chance(0.3f)) {
    // Do something
}

// 1 in 100 chance
if (MathFunctions.oneIn(100)) {
    // Rare drop
}

// Random integer between 5 and 10 (inclusive)
int value = MathFunctions.nextIntInclusive(5, 10);
```

### Player Functions (Messaging)

```java
// Send a message
PlayerFunctions.sendMessage(player, Component.literal("Hello!"));

// Send action bar
PlayerFunctions.sendActionBar(player, Component.literal("Status: Active"));

// Check if flying
if (PlayerFunctions.isFlying(player)) {
    PlayerFunctions.setFlying(player, false);
}
```

### Item Functions (Enchantments)

```java
// Check for enchantment
if (ItemFunctions.containsEnchantment(stack,
    Enchantments.SHARPNESS)) {
    int level = ItemFunctions.getEnchantmentLevel(stack,
        Enchantments.SHARPNESS);
}
```

### World Functions (Entities & Sounds)

```java
// Get nearby players
List<Player> players = WorldFunctions.getPlayers(level);

// Play sound at position
WorldFunctions.playSoundAt(level, pos, SoundEvents.EXPERIENCE_ORB_PICKUP);

// Get time of day
boolean isDay = WorldFunctions.isDaytime(level);
```

## See Also

- [Migration Guide](../../advanced/migration#functions-api-migration)
- [Client Functions](client)
- [Item Functions](item)
- [Math Functions](math)
- [Player Functions](player)
- [World Functions](world)
