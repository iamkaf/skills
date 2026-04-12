# Math Utilities

Amber provides utilities for mathematical operations, probability calculations, and random number generation. These utilities help simplify common math tasks and provide consistent behavior across platforms.

::: warning
Note: The utility classes described here are currently marked as deprecated and will be replaced with versioned alternatives in a future release. They are still functional but consider them as legacy APIs.
:::

## Chance

The `Chance` class provides methods for probability calculations and random events.

### Basic Probability

Calculate random events with specific probabilities:

```java
import com.iamkaf.amber.api.math.Chance;

public class RandomEvents {
    // 25% chance of critical hit
    public static boolean tryCriticalHit() {
        return Chance.of(0.25f);
    }
    
    // 5% chance of rare drop
    public static boolean tryRareDrop() {
        return Chance.of(0.05f);
    }
    
    // 75% chance of common event
    public static boolean tryCommonEvent() {
        return Chance.of(0.75f);
    }
    
    // 100% chance (always true)
    public static boolean tryGuaranteedEvent() {
        return Chance.of(1.0f);
    }
    
    // 0% chance (always false)
    public static boolean tryImpossibleEvent() {
        return Chance.of(0.0f);
    }
}
```

### Random Rewards

Process random rewards based on probability:

```java
public class RewardSystem {
    public static void processRandomRewards(Player player) {
        if (Chance.of(0.1f)) { // 10% chance
            // Rare reward
            player.getInventory().add(new ItemStack(Items.DIAMOND));
            FeedbackHelper.message(player, Component.literal("Rare reward!"));
        } else if (Chance.of(0.5f)) { // 50% chance
            // Common reward
            player.getInventory().add(new ItemStack(Items.GOLD_INGOT));
            FeedbackHelper.message(player, Component.literal("Common reward!"));
        }
        // 40% chance of no reward
    }
    
    public static void processMultipleRewards(Player player) {
        // Multiple independent chances
        if (Chance.of(0.3f)) { // 30% chance for item 1
            player.getInventory().add(new ItemStack(Items.IRON_INGOT));
        }
        
        if (Chance.of(0.2f)) { // 20% chance for item 2
            player.getInventory().add(new ItemStack(Items.GOLD_INGOT));
        }
        
        if (Chance.of(0.1f)) { // 10% chance for item 3
            player.getInventory().add(new ItemStack(Items.DIAMOND));
        }
    }
    
    public static ItemStack processRandomEnchantment() {
        Random random = new Random();
        
        // Choose enchantment type
        if (Chance.of(0.5f)) { // 50% chance for protection
            return new ItemStack(Items.ENCHANTED_BOOK);
        } else if (Chance.of(0.3f)) { // 30% chance for sharpness
            return new ItemStack(Items.ENCHANTED_BOOK);
        } else { // 20% chance for efficiency
            return new ItemStack(Items.ENCHANTED_BOOK);
        }
    }
}
```

### Environmental Randomness

Apply randomness to environmental events:

```java
public class EnvironmentalRandomness {
    public static boolean shouldSpawnMob(Level level) {
        // Higher chance at night, lower during day
        boolean isNight = level.isNight();
        float chance = isNight ? 0.3f : 0.1f;
        return Chance.of(chance);
    }
    
    public static boolean shouldGrowPlant(Level level, BlockPos pos) {
        // Base growth chance
        float baseChance = 0.1f;
        
        // Increase chance if raining
        if (level.isRaining()) {
            baseChance += 0.1f;
        }
        
        // Increase chance if day time
        if (level.isDay()) {
            baseChance += 0.05f;
        }
        
        // Check for bonemeal nearby
        for (int x = -2; x <= 2; x++) {
            for (int z = -2; z <= 2; z++) {
                BlockPos checkPos = pos.offset(x, 0, z);
                if (level.getBlockState(checkPos).is(Blocks.WHITE_CONCRETE_POWDER)) {
                    baseChance += 0.2f;
                    break;
                }
            }
        }
        
        // Clamp to maximum of 0.8 (80%)
        baseChance = Math.min(baseChance, 0.8f);
        
        return Chance.of(baseChance);
    }
    
    public static boolean shouldTriggerLightning(Level level) {
        // Only during thunderstorms
        if (!level.isThundering()) {
            return false;
        }
        
        // Base chance during thunderstorm
        float baseChance = 0.02f; // 2%
        
        // Increase chance in specific biomes
        BlockPos pos = BlockPos.containing(level.getSharedSpawnPos());
        Biome biome = level.getBiome(pos).value();
        
        if (biome.getBiomeCategory() == Biome.BiomeCategory.LUKEWARM_OCEAN ||
            biome.getBiomeCategory() == Biome.BiomeCategory.COLD_OCEAN) {
            baseChance += 0.03f; // +3% in oceans
        }
        
        return Chance.of(baseChance);
    }
}
```

## Advanced Math Operations

### Weighted Random Selection

Create weighted random selection systems:

```java
public class WeightedRandom {
    // Select item from weighted list
    public static <T> T selectWeighted(Map<T, Float> weights) {
        float totalWeight = weights.values().stream().reduce(0f, Float::sum);
        float random = new Random().nextFloat() * totalWeight;
        
        float currentWeight = 0;
        for (Map.Entry<T, Float> entry : weights.entrySet()) {
            currentWeight += entry.getValue();
            if (random <= currentWeight) {
                return entry.getKey();
            }
        }
        
        // Fallback (shouldn't happen if weights are valid)
        return weights.keySet().iterator().next();
    }
    
    // Example usage for drops
    public static ItemStack getRandomDrop() {
        Map<Item, Float> dropWeights = Map.of(
            Items.DIAMOND, 0.1f,    // 10% chance
            Items.GOLD_INGOT, 0.3f, // 30% chance
            Items.IRON_INGOT, 0.6f  // 60% chance
        );
        
        Item selectedItem = selectWeighted(dropWeights);
        return new ItemStack(selectedItem);
    }
    
    // Select with guaranteed minimum
    public static <T> T selectWeightedWithMinimum(Map<T, Float> weights, T minimum, float minimumChance) {
        if (Chance.of(minimumChance)) {
            return minimum;
        }
        
        return selectWeighted(weights);
    }
}
```

### Interpolation

Create interpolation utilities:

```java
public class Interpolation {
    // Linear interpolation
    public static float lerp(float start, float end, float t) {
        return start + (end - start) * t;
    }
    
    // Linear interpolation with clamping
    public static float lerpClamped(float start, float end, float t) {
        t = Math.max(0, Math.min(1, t));
        return lerp(start, end, t);
    }
    
    // Smooth interpolation (ease-in-out)
    public static float smoothLerp(float start, float end, float t) {
        t = Math.max(0, Math.min(1, t));
        return lerp(start, end, t * t * (3 - 2 * t));
    }
    
    // Vector interpolation
    public static Vec3 lerp(Vec3 start, Vec3 end, float t) {
        return new Vec3(
            lerp(start.x, end.x, t),
            lerp(start.y, end.y, t),
            lerp(start.z, end.z, t)
        );
    }
    
    // Color interpolation
    public static int lerpColor(int startColor, int endColor, float t) {
        int startA = (startColor >> 24) & 0xFF;
        int startR = (startColor >> 16) & 0xFF;
        int startG = (startColor >> 8) & 0xFF;
        int startB = startColor & 0xFF;
        
        int endA = (endColor >> 24) & 0xFF;
        int endR = (endColor >> 16) & 0xFF;
        int endG = (endColor >> 8) & 0xFF;
        int endB = endColor & 0xFF;
        
        int a = (int) lerp(startA, endA, t);
        int r = (int) lerp(startR, endR, t);
        int g = (int) lerp(startG, endG, t);
        int b = (int) lerp(startB, endB, t);
        
        return (a << 24) | (r << 16) | (g << 8) | b;
    }
    
    // Example usage for animation
    public static void animateValue(float from, float to, int durationTicks, Consumer<Float> setter) {
        // This would be used in a tick-based animation system
        for (int tick = 0; tick <= durationTicks; tick++) {
            float t = (float) tick / durationTicks;
            float value = smoothLerp(from, to, t);
            
            // Schedule setting the value at the appropriate tick
            // Implementation depends on your mod's tick system
        }
    }
}
```

### Math Utilities

Create general math utilities:

```java
public class MathUtils {
    // Clamp value between min and max
    public static float clamp(float value, float min, float max) {
        return Math.max(min, Math.min(max, value));
    }
    
    // Map value from one range to another
    public static float map(float value, float fromMin, float fromMax, float toMin, float toMax) {
        return toMin + (value - fromMin) * (toMax - toMin) / (fromMax - fromMin);
    }
    
    // Normalize angle to 0-360 degrees
    public static float normalizeAngle(float angle) {
        angle = angle % 360;
        if (angle < 0) {
            angle += 360;
        }
        return angle;
    }
    
    // Calculate distance between two points
    public static double distance(double x1, double y1, double x2, double y2) {
        return Math.sqrt(Math.pow(x2 - x1, 2) + Math.pow(y2 - y1, 2));
    }
    
    // Calculate distance between two 3D points
    public static double distance(double x1, double y1, double z1, double x2, double y2, double z2) {
        return Math.sqrt(Math.pow(x2 - x1, 2) + Math.pow(y2 - y1, 2) + Math.pow(z2 - z1, 2));
    }
    
    // Check if value is within range
    public static boolean isInRange(float value, float min, float max) {
        return value >= min && value <= max;
    }
    
    // Round to nearest multiple
    public static float roundToMultiple(float value, float multiple) {
        return Math.round(value / multiple) * multiple;
    }
    
    // Convert degrees to radians
    public static float degToRad(float degrees) {
        return (float) (degrees * Math.PI / 180);
    }
    
    // Convert radians to degrees
    public static float radToDeg(float radians) {
        return (float) (radians * 180 / Math.PI);
    }
    
    // Example usage
    public static void exampleUsage() {
        // Clamp value
        float clamped = clamp(150, 0, 100); // Returns 100
        
        // Map value
        float mapped = map(50, 0, 100, 0, 1); // Returns 0.5
        
        // Normalize angle
        float normalized = normalizeAngle(450); // Returns 90
        
        // Check range
        boolean inRange = isInRange(50, 0, 100); // Returns true
        
        // Round to multiple
        float rounded = roundToMultiple(23, 5); // Returns 25
    }
}
```

## Random Number Generation

### Advanced Random Systems

Create more sophisticated random number systems:

```java
public class RandomSystems {
    // Random with seed
    public static class SeededRandom {
        private final Random random;
        
        public SeededRandom(long seed) {
            this.random = new Random(seed);
        }
        
        public float nextFloat(float min, float max) {
            return min + random.nextFloat() * (max - min);
        }
        
        public int nextInt(int min, int max) {
            return random.nextInt(max - min + 1) + min;
        }
        
        public boolean nextBoolean(float chance) {
            return random.nextFloat() < chance;
        }
        
        public Vec3 nextVec3(Vec3 center, double radius) {
            double angle = random.nextDouble() * 2 * Math.PI;
            double distance = random.nextDouble() * radius;
            
            return center.add(
                Math.cos(angle) * distance,
                0,
                Math.sin(angle) * distance
            );
        }
    }
    
    // Gaussian random
    public static double nextGaussian(Random random, double mean, double stddev) {
        return random.nextGaussian() * stddev + mean;
    }
    
    // Perlin noise approximation
    public static float noise(int x, int y, int seed) {
        int n = x + y * 57 + seed * 131;
        n = (n << 13) ^ n;
        return (1.0f - ((n * (n * n * 15731 + 789221) + 1376312589) & 0x7fffffff) / 1073741824.0f);
    }
    
    // Example usage
    public static void exampleUsage() {
        SeededRandom seeded = new SeededRandom(12345);
        
        // Generate random position
        Vec3 center = new Vec3(0, 64, 0);
        Vec3 randomPos = seeded.nextVec3(center, 10);
        
        // Generate random value with Gaussian distribution
        Random random = new Random();
        double gaussian = nextGaussian(random, 50, 10); // Mean 50, stddev 10
        
        // Generate noise value
        float noiseValue = noise(10, 20, 54321);
    }
}
```

## Best Practices

### 1. Seed Management

Use consistent seeds for predictable results:

```java
public class SeedManagement {
    private static final long STRUCTURE_SEED = 12345L;
    private static final long LOOT_SEED = 67890L;
    
    public static void generateStructure(Level level, BlockPos pos) {
        SeededRandom random = new RandomSystems.SeededRandom(
            STRUCTURE_SEED + pos.asLong()
        );
        
        // Use random for consistent structure generation
    }
    
    public static void generateLoot(Level level, BlockPos pos) {
        SeededRandom random = new RandomSystems.SeededRandom(
            LOOT_SEED + pos.asLong()
        );
        
        // Use random for consistent loot generation
    }
}
```

### 2. Performance

Consider performance for frequent random operations:

```java
public class PerformanceRandom {
    // Reuse Random instance
    private static final Random SHARED_RANDOM = new Random();
    
    // Fast random for non-critical uses
    public static boolean fastChance(float percent) {
        return SHARED_RANDOM.nextFloat() < percent;
    }
    
    // Thread-safe random
    private static final ThreadLocalRandom THREAD_LOCAL_RANDOM = ThreadLocalRandom.current();
    
    public static boolean threadSafeChance(float percent) {
        return THREAD_LOCAL_RANDOM.nextFloat() < percent;
    }
}
```

### 3. Validation

Validate probability values:

```java
public class Validation {
    public static boolean isValidProbability(float probability) {
        return probability >= 0.0f && probability <= 1.0f;
    }
    
    public static float clampProbability(float probability) {
        return Math.max(0.0f, Math.min(1.0f, probability));
    }
    
    public static boolean safeChance(float probability) {
        return Chance.of(clampProbability(probability));
    }
}
```

### 4. Testing

Create testable random systems:

```java
public class TestableRandom {
    private final Random random;
    private final List<Float> recordedChances = new ArrayList<>();
    
    public TestableRandom(long seed) {
        this.random = new Random(seed);
    }
    
    public boolean chance(float probability) {
        recordedChances.add(probability);
        return random.nextFloat() < probability;
    }
    
    // For testing - verify that specific chances were tested
    public boolean wasChanceTested(float probability) {
        return recordedChances.contains(probability);
    }
    
    // For testing - get all tested chances
    public List<Float> getTestedChances() {
        return new ArrayList<>(recordedChances);
    }
}
```

These math utilities provide helpful shortcuts for common mathematical operations while maintaining cross-platform compatibility.