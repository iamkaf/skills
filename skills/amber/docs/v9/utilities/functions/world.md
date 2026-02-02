# WorldFunctions

World/level operations including item spawning, sounds, entities, biomes, time, and geometry.

**Package**: `com.iamkaf.amber.api.functions.v1`

## Level Operations

### runEveryXTicks()

Execute code every N ticks. Use in tick methods.

```java
@Override
public void tick(Level level) {
    // Run every 20 ticks (1 second)
    WorldFunctions.runEveryXTicks(level, 20, (gameTime) -> {
        // Do something
    });
}
```

## Item Spawning

```java
// Drop item (with default upward velocity)
WorldFunctions.dropItem(level, new ItemStack(Items.DIAMOND), pos);

// Drop ItemLike
WorldFunctions.dropItem(level, Items.DIAMOND, pos);

// With custom velocity
WorldFunctions.dropItem(level, stack, pos, new Vec3(0, 0.5, 0));
```

## Raytracing

### raytrace()

Get what the player is looking at.

```java
BlockHitResult result = WorldFunctions.raytrace(level, player);
BlockPos pos = result.getBlockPos();
```

## Sound

### playSoundAt() - Position-based sounds

```java
// Simple
WorldFunctions.playSoundAt(level, pos, SoundEvents.EXPERIENCE_ORB_PICKUP);

// With source
WorldFunctions.playSoundAt(
    level,
    pos,
    SoundEvents.AMBIENT_CAVE,
    SoundSource.AMBIENT
);

// With volume/pitch
WorldFunctions.playSoundAt(
    level,
    pos,
    sound,
    SoundSource.BLOCKS,
    1.0f,  // volume
    1.0f   // pitch
);

// At BlockPos
WorldFunctions.playSoundAt(level, blockPos, sound, SoundSource.BLOCKS);
WorldFunctions.playSoundAt(level, blockPos, sound, SoundSource.BLOCKS, 1.0f, 1.0f);
```

::: tip Sound vs Player Sound
- `WorldFunctions.playSoundAt()` - For sounds at a position in the world (all players nearby can hear)
- `PlayerFunctions.playSound()` - For sounds directed at a specific player
:::

## Dimension Checks

```java
boolean isOverworld = WorldFunctions.isOverworld(level);
boolean isNether = WorldFunctions.isNether(level);
boolean isEnd = WorldFunctions.isEnd(level);
```

## Distance Calculations

```java
// Between positions
double dist = WorldFunctions.distanceBetween(pos1, pos2);
double dist = WorldFunctions.distanceBetween(blockPos1, blockPos2);
double dist = WorldFunctions.distanceBetween(entity1, entity2);

// Squared (faster, no sqrt)
double distSq = WorldFunctions.distanceSquaredBetween(pos1, pos2);
double distSq = WorldFunctions.distanceSquaredBetween(blockPos1, blockPos2);

// Horizontal only
double hDist = WorldFunctions.horizontalDistanceBetween(pos1, pos2);
```

## Time

```java
// Time of day (0-24000)
long time = WorldFunctions.getTimeOfDay(level);

// Time in hours (0.0-24.0)
double hours = WorldFunctions.getTimeOfDayInHours(level);

// Day/Night check
boolean isDay = WorldFunctions.isDaytime(level);
boolean isNight = WorldFunctions.isNighttime(level);

// Moon phase
int phase = WorldFunctions.getMoonPhase(level); // 0-7

// Day count
long days = WorldFunctions.getDayCount(level);
long totalGameTime = WorldFunctions.getTotalGameTime(level);
```

## Difficulty

```java
// Get difficulty at position
DifficultyInstance diff = WorldFunctions.getCurrentDifficulty(level, blockPos);
DifficultyInstance diff = WorldFunctions.getCurrentDifficulty(level, pos);

// Check if hard
boolean isHard = WorldFunctions.isHardDifficulty(level, blockPos);
boolean isHard = WorldFunctions.isHardDifficulty(level, pos);
```

## Entities

### Get Players

```java
// All players in level
List<Player> players = WorldFunctions.getPlayers(level);
```

### Get Entities in Radius

```java
// All entities
List<Entity> entities = WorldFunctions.getEntitiesInRadius(level, center, 10.0);

// By type
List<Zombie> zombies = WorldFunctions.getEntitiesInRadius(
    level,
    center,
    10.0,
    EntityType.ZOMBIE
);

// With predicate
List<Entity> entities = WorldFunctions.getEntitiesInRadius(
    level,
    center,
    10.0,
    (entity) -> entity instanceof Player
);

// With BlockPos center
List<Entity> entities = WorldFunctions.getEntitiesInRadius(
    level,
    blockPos,
    10.0
);

// Specific type with BlockPos
List<ItemEntity> items = WorldFunctions.getEntitiesInRadius(
    level,
    blockPos,
    5.0,
    EntityType.ITEM
);
```

### Nearest Entity

```java
Entity nearest = WorldFunctions.getNearestEntity(level, center, 10.0);
```

## Biomes

```java
// Get biome at position (Holder)
Holder<Biome> biome = WorldFunctions.getBiomeAtPosition(level, blockPos);
Holder<Biome> biome = WorldFunctions.getBiomeAtPosition(level, pos);

// Get biome value (direct access)
Biome biomeValue = WorldFunctions.getBiomeValueAtPosition(level, blockPos);
Biome biomeValue = WorldFunctions.getBiomeValueAtPosition(level, pos);

// Check precipitation
boolean hasRain = WorldFunctions.hasPrecipitation(
    level,
    blockPos,
    Biome.Precipitation.RAIN
);
boolean hasRain = WorldFunctions.hasPrecipitation(
    level,
    pos,
    Biome.Precipitation.RAIN
);
```

## Geometry

### mergeBoundingBoxes()

Merge adjacent block positions into larger AABBs for optimization.

```java
Collection<BlockPos> positions = List.of(
    new BlockPos(0, 0, 0),
    new BlockPos(1, 0, 0),
    new BlockPos(0, 0, 1)
);

Collection<AABB> boxes = WorldFunctions.mergeBoundingBoxes(
    positions,
    referencePoint
);
```

## Migration

Replaces `LevelHelper`, `SoundHelper`, `CommonUtils`, and `BoundingBoxMerger`:

| Old | New |
|-----|-----|
| `LevelHelper.runEveryXTicks()` | `WorldFunctions.runEveryXTicks()` |
| `LevelHelper.dropItem()` | `WorldFunctions.dropItem()` |
| `CommonUtils.raytrace()` | `WorldFunctions.raytrace()` |
| `SoundHelper.sendClientSound()` | `PlayerFunctions.playSound()` or `WorldFunctions.playSoundAt()` |
| `BoundingBoxMerger.merge()` | `WorldFunctions.mergeBoundingBoxes()` |
