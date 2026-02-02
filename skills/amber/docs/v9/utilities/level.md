# Level Utilities

Amber provides utilities for working with game levels/worlds, including scheduled tasks, item drops, and world-level operations. These utilities help simplify common world tasks and provide consistent behavior across platforms.

::: warning Deprecated
The `LevelHelper` class is **deprecated** and will be removed in Amber 10.0.

Use `com.iamkaf.amber.api.functions.v1.WorldFunctions` instead. See [Functions API → WorldFunctions](functions/world) for the new API.
:::

## LevelHelper

The `LevelHelper` class provides methods for scheduled tasks and item drops in the world.

### Scheduled Tasks

Run tasks at regular intervals in the world:

```java
import com.iamkaf.amber.api.level.LevelHelper;

public class WorldScheduler {
    // Run every 100 ticks (5 seconds)
    public static void tickEvent(Level level) {
        LevelHelper.runEveryXTicks(level, 100, gameTime -> {
            // Check all players in the level
            level.players().forEach(player -> {
                // Apply periodic effect
                if (player.hasEffect(MobEffects.REGENERATION)) {
                    player.addEffect(new MobEffectInstance(
                        MobEffects.REGENERATION, 
                        200, // 10 seconds
                        0,    // Amplifier
                        true, // Ambient particles
                        true  // Show icon
                    ));
                }
            });
        });
        
        // Run every 20 ticks (1 second)
        LevelHelper.runEveryXTicks(level, 20, gameTime -> {
            // Update world time display
            if (level instanceof ServerLevel serverLevel) {
                updateWorldClock(serverLevel);
            }
        });
        
        // Run every 1200 ticks (1 minute)
        LevelHelper.runEveryXTicks(level, 1200, gameTime -> {
            // Save world data periodically
            if (level instanceof ServerLevel serverLevel) {
                saveCustomData(serverLevel, gameTime);
            }
        });
        
        // Run every 6000 ticks (5 minutes)
        LevelHelper.runEveryXTicks(level, 6000, gameTime -> {
            // Cleanup old entities
            if (level instanceof ServerLevel serverLevel) {
                cleanupOldEntities(serverLevel);
            }
        });
    }
    
    private static void updateWorldClock(ServerLevel level) {
        // Custom clock update logic
        long dayTime = level.getDayTime() % 24000;
        int hours = (int) ((dayTime + 6000) / 1000) % 24;
        int minutes = (int) ((dayTime % 1000) * 60 / 1000);
        
        String timeString = String.format("%02d:%02d", hours, minutes);
        
        // Update all players with time
        level.players().forEach(player -> {
            ActionBarMessages.showStatus(player, "Time: " + timeString);
        });
    }
    
    private static void saveCustomData(ServerLevel level, long gameTime) {
        // Custom data saving logic
        Constants.LOG.info("Saving world data at time: " + gameTime);
    }
    
    private static void cleanupOldEntities(ServerLevel level) {
        // Remove old item entities
        level.getEntitiesOfClass(ItemEntity.class, 
            entity -> entity.age > 6000 // 5 minutes
        ).forEach(Entity::discard);
        
        Constants.LOG.info("Cleaned up old entities");
    }
}
```

### Item Drops

Drop items in the world:

```java
public class WorldDrops {
    // Drop single item
    public static void dropReward(Level level, Vec3 pos, Item item, int count) {
        ItemStack stack = new ItemStack(item, count);
        LevelHelper.dropItem(level, stack, pos);
    }
    
    // Drop with custom velocity
    public static void dropWithVelocity(Level level, Vec3 pos, ItemStack stack, Vec3 velocity) {
        LevelHelper.dropItem(level, stack, pos, velocity);
    }
    
    // Create explosion drops
    public static void createExplosionDrops(Level level, Vec3 center, List<ItemStack> drops) {
        Random random = new Random();
        
        for (ItemStack drop : drops) {
            // Random position within explosion radius
            double angle = random.nextDouble() * 2 * Math.PI;
            double distance = random.nextDouble() * 3.0; // 3 block radius
            
            Vec3 dropPos = center.add(
                Math.cos(angle) * distance,
                0.5, // Slight upward offset
                Math.sin(angle) * distance
            );
            
            // Random velocity away from center
            Vec3 velocity = new Vec3(
                Math.cos(angle) * 0.3,
                random.nextDouble() * 0.2 + 0.1,
                Math.sin(angle) * 0.3
            );
            
            LevelHelper.dropItem(level, drop, dropPos, velocity);
        }
    }
    
    // Drop from loot table
    public static void dropLootTable(Level level, Vec3 pos, ResourceLocation lootTableId, LootContextParamSet parameters) {
        LootParams.Builder builder = new LootParams.Builder((ServerLevel) level);
        
        // Build context parameters based on what you need
        if (level instanceof ServerLevel serverLevel) {
            builder.withParameter(LootContextParams.ORIGIN, Vec3.atCenterOf(BlockPos.containing(pos)));
        }
        
        LootParams lootParams = builder.build(parameters);
        LootTable lootTable = level.getServer().getLootData().getLootTable(lootTableId);
        
        // Generate and drop items
        lootTable.getRandomItems(lootParams).forEach(stack -> {
            LevelHelper.dropItem(level, stack, pos);
        });
    }
    
    // Drop with chance
    public static void dropWithChance(Level level, Vec3 pos, Item item, float chance) {
        if (level.random.nextFloat() < chance) {
            LevelHelper.dropItem(level, item, pos);
        }
    }
    
    // Drop multiple items with different chances
    public static void dropMultipleWithChance(Level level, Vec3 pos, Map<Item, Float> drops) {
        for (Map.Entry<Item, Float> entry : drops.entrySet()) {
            if (level.random.nextFloat() < entry.getValue()) {
                LevelHelper.dropItem(level, entry.getKey(), pos);
            }
        }
    }
    
    // Drop in circle pattern
    public static void dropInCircle(Level level, Vec3 center, Item item, int count, double radius) {
        for (int i = 0; i < count; i++) {
            double angle = (double) i / count * 2 * Math.PI;
            Vec3 dropPos = center.add(
                Math.cos(angle) * radius,
                0.5,
                Math.sin(angle) * radius
            );
            
            LevelHelper.dropItem(level, item, dropPos);
        }
    }
}
```

## Advanced World Operations

### World Generation

Modify world generation:

```java
public class WorldGeneration {
    // Generate custom structure
    public static void generateCustomStructure(Level level, BlockPos origin) {
        // Generate a simple tower
        for (int y = 0; y < 5; y++) {
            for (int x = -1; x <= 1; x++) {
                for (int z = -1; z <= 1; z++) {
                    BlockPos pos = origin.offset(x, y, z);
                    
                    if (x == 0 && z == 0) {
                        // Center column
                        level.setBlock(pos, Blocks.STONE_BRICKS.defaultBlockState(), 3);
                    } else if (y == 0) {
                        // Foundation
                        level.setBlock(pos, Blocks.STONE_BRICKS.defaultBlockState(), 3);
                    } else {
                        // Walls
                        level.setBlock(pos, Blocks.AIR.defaultBlockState(), 3);
                    }
                }
            }
        }
        
        // Add roof
        for (int x = -2; x <= 2; x++) {
            for (int z = -2; z <= 2; z++) {
                BlockPos pos = origin.offset(x, 5, z);
                level.setBlock(pos, Blocks.STONE_SLAB.defaultBlockState(), 3);
            }
        }
    }
    
    // Generate ore vein
    public static void generateOreVein(Level level, BlockPos center, Block ore, int size) {
        Random random = new Random(center.asLong());
        
        for (int i = 0; i < size; i++) {
            // Random position within vein
            int x = center.getX() + random.nextInt(7) - 3;
            int y = center.getY() + random.nextInt(5) - 2;
            int z = center.getZ() + random.nextInt(7) - 3;
            
            BlockPos pos = new BlockPos(x, y, z);
            
            // Only replace stone
            if (level.getBlockState(pos).is(Blocks.STONE)) {
                level.setBlock(pos, ore.defaultBlockState(), 3);
            }
        }
    }
    
    // Generate tree
    public static void generateCustomTree(Level level, BlockPos pos) {
        // Generate trunk
        for (int y = 0; y < 6; y++) {
            level.setBlock(pos.above(y), Blocks.OAK_LOG.defaultBlockState(), 3);
        }
        
        // Generate leaves
        for (int x = -2; x <= 2; x++) {
            for (int y = 3; y <= 5; y++) {
                for (int z = -2; z <= 2; z++) {
                    BlockPos leafPos = pos.above(y).offset(x, 0, z);
                    
                    // Skip trunk area
                    if (Math.abs(x) <= 1 && Math.abs(z) <= 1 && y < 5) {
                        continue;
                    }
                    
                    // Random leaf placement
                    if (level.random.nextFloat() < 0.8f) {
                        level.setBlock(leafPos, Blocks.OAK_LEAVES.defaultBlockState(), 3);
                    }
                }
            }
        }
    }
}
```

### World Effects

Apply effects to the world:

```java
public class WorldEffects {
    // Create weather effect
    public static void createWeatherEffect(Level level, BlockPos center, int radius, WeatherEffect effect) {
        for (int x = -radius; x <= radius; x++) {
            for (int z = -radius; z <= radius; z++) {
                BlockPos pos = center.offset(x, 0, z);
                
                if (pos.distSqr(center) <= radius * radius) {
                    effect.apply(level, pos);
                }
            }
        }
    }
    
    // Weather effect interface
    public interface WeatherEffect {
        void apply(Level level, BlockPos pos);
    }
    
    // Rain effect
    public static final WeatherEffect RAIN_EFFECT = (level, pos) -> {
        if (level.isRaining() && level.canSeeSky(pos)) {
            // Place water at position if it's air
            if (level.getBlockState(pos).isAir()) {
                level.setBlock(pos, Blocks.WATER.defaultBlockState(), 3);
            }
        }
    };
    
    // Lightning effect
    public static final WeatherEffect LIGHTNING_EFFECT = (level, pos) -> {
        if (level instanceof ServerLevel serverLevel && level.random.nextFloat() < 0.1f) {
            LightningBolt lightning = EntityType.LIGHTNING_BOLT.create(serverLevel);
            if (lightning != null) {
                lightning.setPos(Vec3.atBottomCenterOf(pos));
                serverLevel.addFreshEntity(lightning);
                
                // Create fire
                if (level.getBlockState(pos).isAir()) {
                    level.setBlock(pos, Blocks.FIRE.defaultBlockState(), 3);
                }
            }
        }
    };
    
    // Create particle effect
    public static void createParticleEffect(Level level, Vec3 center, ParticleOptions particle, int count, double radius) {
        for (int i = 0; i < count; i++) {
            // Random position within radius
            double angle = level.random.nextDouble() * 2 * Math.PI;
            double distance = level.random.nextDouble() * radius;
            
            Vec3 particlePos = center.add(
                Math.cos(angle) * distance,
                level.random.nextDouble() * 2 - 1, // Random height
                Math.sin(angle) * distance
            );
            
            level.addParticle(particle, particlePos.x, particlePos.y, particlePos.z, 
                0, 0, 0); // No velocity
        }
    }
    
    // Create explosion effect
    public static void createExplosionEffect(Level level, Vec3 center, float power, boolean causeFire) {
        level.explode(null, center.x, center.y, center.z, power, 
            causeFire ? Level.ExplosionInteraction.MOB : Level.ExplosionInteraction.BLOCK);
        
        // Add particles
        createParticleEffect(level, center, ParticleTypes.EXPLOSION, 20, power);
    }
}
```

### World Scanning

Scan and analyze the world:

```java
public class WorldScanner {
    // Find blocks in area
    public static List<BlockPos> findBlocks(Level level, BlockPos center, int radius, Block targetBlock) {
        List<BlockPos> found = new ArrayList<>();
        
        for (int x = -radius; x <= radius; x++) {
            for (int y = -radius; y <= radius; y++) {
                for (int z = -radius; z <= radius; z++) {
                    BlockPos pos = center.offset(x, y, z);
                    
                    if (level.getBlockState(pos).is(targetBlock)) {
                        found.add(pos);
                    }
                }
            }
        }
        
        return found;
    }
    
    // Count blocks in area
    public static Map<Block, Integer> countBlocks(Level level, BlockPos center, int radius) {
        Map<Block, Integer> counts = new HashMap<>();
        
        for (int x = -radius; x <= radius; x++) {
            for (int y = -radius; y <= radius; y++) {
                for (int z = -radius; z <= radius; z++) {
                    BlockPos pos = center.offset(x, y, z);
                    Block block = level.getBlockState(pos).getBlock();
                    
                    counts.merge(block, 1, Integer::sum);
                }
            }
        }
        
        return counts;
    }
    
    // Find nearest block
    public static BlockPos findNearestBlock(Level level, BlockPos center, Block targetBlock, int maxRadius) {
        BlockPos nearest = null;
        double nearestDistance = maxRadius * maxRadius;
        
        for (int x = -maxRadius; x <= maxRadius; x++) {
            for (int y = -maxRadius; y <= maxRadius; y++) {
                for (int z = -maxRadius; z <= maxRadius; z++) {
                    BlockPos pos = center.offset(x, y, z);
                    
                    if (level.getBlockState(pos).is(targetBlock)) {
                        double distance = pos.distSqr(center);
                        
                        if (distance < nearestDistance) {
                            nearest = pos;
                            nearestDistance = distance;
                        }
                    }
                }
            }
        }
        
        return nearest;
    }
    
    // Check if area is safe for player
    public static boolean isSafeArea(Level level, BlockPos center, int radius) {
        for (int x = -radius; x <= radius; x++) {
            for (int y = -radius; y <= radius; y++) {
                for (int z = -radius; z <= radius; z++) {
                    BlockPos pos = center.offset(x, y, z);
                    BlockState state = level.getBlockState(pos);
                    
                    // Check for dangerous blocks
                    if (state.is(Blocks.LAVA) || state.is(Blocks.FIRE) || 
                        state.getBlock() instanceof AbstractFireBlock) {
                        return false;
                    }
                }
            }
        }
        
        return true;
    }
    
    // Generate world statistics
    public static Component generateWorldStats(Level level, BlockPos center, int radius) {
        Map<Block, Integer> counts = countBlocks(level, center, radius);
        
        // Sort by count
        List<Map.Entry<Block, Integer>> sorted = counts.entrySet().stream()
            .sorted(Map.Entry.<Block, Integer>comparingByValue().reversed())
            .limit(10)
            .toList();
        
        MutableComponent stats = Component.literal("World Statistics (" + radius + " block radius):\n");
        
        for (Map.Entry<Block, Integer> entry : sorted) {
            Component blockName = Component.translatable(entry.getKey().getDescriptionId());
            stats.append(Component.literal("- " + blockName.getString() + ": " + entry.getValue() + "\n"));
        }
        
        return stats;
    }
}
```

## Best Practices

### 1. Performance

Consider performance when affecting large areas:

```java
public static void efficientWorldOperation(Level level, BlockPos center, int radius, WorldOperation operation) {
    // Use chunk loading to avoid loading too many chunks
    ChunkPos centerChunk = new ChunkPos(center);
    int chunkRadius = (radius + 15) / 16; // Convert to chunk radius
    
    for (int chunkX = -chunkRadius; chunkX <= chunkRadius; chunkX++) {
        for (int chunkZ = -chunkRadius; chunkZ <= chunkRadius; chunkZ++) {
            ChunkPos chunkPos = new ChunkPos(centerChunk.x + chunkX, centerChunk.z + chunkZ);
            
            // Only operate if chunk is loaded
            if (level.hasChunk(chunkPos.x, chunkPos.z)) {
                operation.operateOnChunk(level, chunkPos);
            }
        }
    }
}

public interface WorldOperation {
    void operateOnChunk(Level level, ChunkPos chunkPos);
}
```

### 2. Side Safety

Always check which side you're on:

```java
public static void safeWorldOperation(Level level, Runnable operation) {
    if (level.isClientSide()) {
        // Client-side only
        operation.run();
    } else {
        // Server-side
        if (level instanceof ServerLevel) {
            operation.run();
        }
    }
}
```

### 3. Validation

Validate world operations:

```java
public static boolean safeBlockPlacement(Level level, BlockPos pos, BlockState state) {
    // Check if position is loaded
    if (!level.hasChunkAt(pos)) {
        return false;
    }
    
    // Check if position is valid
    if (pos.getY() < level.getMinBuildHeight() || pos.getY() > level.getMaxBuildHeight()) {
        return false;
    }
    
    // Place block
    level.setBlock(pos, state, 3);
    return true;
}
```

### 4. Randomness

Use consistent random seeds for predictable results:

```java
public static void predictableWorldGeneration(Level level, BlockPos pos, long seed) {
    Random random = new Random(seed);
    
    // Use random for consistent generation
    for (int i = 0; i < 10; i++) {
        BlockPos genPos = pos.offset(
            random.nextInt(11) - 5,
            random.nextInt(11) - 5,
            random.nextInt(11) - 5
        );
        
        // Generate something at genPos
    }
}
```

These level utilities provide helpful shortcuts for common world operations while maintaining cross-platform compatibility.