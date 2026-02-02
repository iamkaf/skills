# PlayerFunctions

Player-specific operations including experience, abilities, inventory, messaging, and more.

**Package**: `com.iamkaf.amber.api.functions.v1`

## Experience & Progression

```java
// Add experience points/levels
PlayerFunctions.addExperience(player, 100);
PlayerFunctions.addLevels(player, 5);

// Set experience level
PlayerFunctions.setExperienceLevel(player, 30);

// Get experience info
int points = PlayerFunctions.getExperiencePoints(player);
int level = PlayerFunctions.getExperienceLevel(player);
float progress = PlayerFunctions.getExperienceProgress(player);

// Check if player has enough experience
boolean canAfford = PlayerFunctions.hasEnoughExperience(player, 50);
```

## Abilities (Flying, Invulnerability, etc.)

```java
// Flying
PlayerFunctions.setFlying(player, true);
boolean isFlying = PlayerFunctions.isFlying(player);
PlayerFunctions.setAllowFlight(player, true);
boolean canFly = PlayerFunctions.canFly(player);

// Invulnerability
PlayerFunctions.setInvulnerable(player, true);
boolean isInvulnerable = PlayerFunctions.isInvulnerable(player);

// Insta-build (creative mode cheat)
PlayerFunctions.setInstaBuild(player, true);
boolean hasInstaBuild = PlayerFunctions.hasInstaBuild(player);

// May build (adventure mode)
PlayerFunctions.setMayBuild(player, false);
boolean mayBuild = PlayerFunctions.mayBuild(player);

// Get abilities
Abilities abilities = PlayerFunctions.getAbilities(player);
```

## Game Mode

```java
// Get game mode
GameType mode = PlayerFunctions.getGameMode(player);

// Check specific modes
boolean isCreative = PlayerFunctions.isCreativeMode(player);
boolean isSurvival = PlayerFunctions.isSurvivalMode(player);
boolean isAdventure = PlayerFunctions.isAdventureMode(player);
boolean isSpectator = PlayerFunctions.isSpectatorMode(player);
```

## Inventory & Equipment

```java
// Get equipment
ItemStack mainHand = PlayerFunctions.getMainHandItem(player);
ItemStack offhand = PlayerFunctions.getOffhandItem(player);
ItemStack helmet = PlayerFunctions.getHelmet(player);
ItemStack chestplate = PlayerFunctions.getChestplate(player);
ItemStack leggings = PlayerFunctions.getLeggings(player);
ItemStack boots = PlayerFunctions.getBoots(player);

// Set equipment
PlayerFunctions.setMainHandItem(player, stack);
PlayerFunctions.setOffhandItem(player, stack);

// Hotbar access
int slot = PlayerFunctions.getSelectedSlot(player);
PlayerFunctions.setSelectedSlot(player, 4);
ItemStack hotbarItem = PlayerFunctions.getHotbarItem(player, 0);
PlayerFunctions.setHotbarItem(player, 0, stack);
```

## Combat

```java
// Attack strength
float strength = PlayerFunctions.getAttackStrength(player);
PlayerFunctions.resetAttackStrength(player);
boolean hasCooldown = PlayerFunctions.hasAttackCooldown(player);
float progress = PlayerFunctions.getAttackCooldownProgress(player);
```

## Messaging

```java
// Chat message
PlayerFunctions.sendMessage(player, Component.literal("Hello!"));

// Action bar
PlayerFunctions.sendActionBarMessage(player, Component.literal("Status: Active"));
PlayerFunctions.sendActionBar(player, Component.literal("Status: Active"));

// Title
PlayerFunctions.sendTitle(
    player,
    Component.literal("BOSS FIGHT"),
    Component.literal("Wave 1")
);

// Title with timing
PlayerFunctions.sendTitle(
    player,
    Component.literal("TITLE"),
    Component.literal("Subtitle"),
    20,  // fade in
    60,  // stay
    20   // fade out
);

// Clear title
PlayerFunctions.clearTitle(player);
```

## Sound

```java
// Play sound to player
PlayerFunctions.playSound(player, SoundEvents.EXPERIENCE_ORB_PICKUP);

// With source
PlayerFunctions.playSound(player, sound, SoundSource.PLAYERS);

// With volume/pitch
PlayerFunctions.playSound(
    player,
    sound,
    SoundSource.PLAYERS,
    1.0f,  // volume
    1.0f   // pitch
);
```

## Death & Respawn

```java
// Last death location
Optional<GlobalPos> deathPos = PlayerFunctions.getLastDeathLocation(player);
PlayerFunctions.setLastDeathLocation(player, position);

// Respawn player
PlayerFunctions.respawn(player);
```

## Sleeping

```java
boolean isSleeping = PlayerFunctions.isSleeping(player);
PlayerFunctions.startSleeping(player, pos);
PlayerFunctions.stopSleeping(player);
```

## Food & Hunger

```java
// Food level
int foodLevel = PlayerFunctions.getFoodLevel(player);
PlayerFunctions.setFoodLevel(player, 20);

// Saturation
float saturation = PlayerFunctions.getSaturationLevel(player);
PlayerFunctions.addExhaustion(player, 0.5f);

// Feed player
PlayerFunctions.feed(player, 5); // Add 5 food points
```

## Ender Chest

```java
// Get ender chest container
PlayerEnderChestContainer enderChest = PlayerFunctions.getEnderChest(player);

// Access specific slot
ItemStack stack = PlayerFunctions.getEnderChestItem(player, 0);
PlayerFunctions.setEnderChestItem(player, 0, stack);
```

## Persistent Data

```java
// Store string data
PlayerFunctions.setPersistentData(player, "myKey", "myValue");

// Retrieve string data
String value = PlayerFunctions.getPersistentData(player, "myKey");

// Check if has key
boolean hasKey = PlayerFunctions.hasPersistentData(player, "myKey");
```

## Containers

```java
// Get container (inventory, ender chest, etc.)
Container container = PlayerFunctions.getContainer(player, ContainerType.INVENTORY);
```

## Migration

Replaces `FeedbackHelper`:

| Old | New |
|-----|-----|
| `FeedbackHelper.message()` | `PlayerFunctions.sendMessage()` |
| `FeedbackHelper.actionBarMessage()` | `PlayerFunctions.sendActionBarMessage()` |
