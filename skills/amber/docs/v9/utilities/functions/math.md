# MathFunctions

Mathematical operations, probability calculations, and random number generation.

**Package**: `com.iamkaf.amber.api.functions.v1`

## Probability Operations

### chance() / of()

Returns true with the specified probability (0.0 to 1.0).

```java
// 30% chance
if (MathFunctions.chance(0.3f)) {
    // Do something
}

// of() is an alias
if (MathFunctions.of(0.5f)) {
    // 50% chance
}
```

### clampProbability()

Clamps a probability value between 0 and 1.

```java
float valid = MathFunctions.clampProbability(percent);
```

### oneIn()

Returns true with a 1 in N chance.

```java
// 1 in 100 chance (1%)
if (MathFunctions.oneIn(100)) {
    // Rare drop
}
```

### chanceOf()

Returns true with approximately N in M chance.

```java
// 3 in 10 chance (30%)
if (MathFunctions.chanceOf(3, 10)) {
    // Do something
}
```

## Random Number Generation

### Integers

```java
// 0 to bound (exclusive)
int value = MathFunctions.nextInt(100); // 0-99

// Range (origin inclusive, bound exclusive)
int value = MathFunctions.nextInt(10, 20); // 10-19

// Inclusive range
int value = MathFunctions.nextIntInclusive(5, 10); // 5-10
```

### Floats & Doubles

```java
// Float 0.0 to 1.0
float f = MathFunctions.nextFloat();

// Float range
float f = MathFunctions.nextFloat(1.5f, 3.5f);

// Double 0.0 to 1.0
double d = MathFunctions.nextDouble();

// Double range
double d = MathFunctions.nextDouble(10.0, 20.0);
```

### Boolean

```java
// Random true/false
bool b = MathFunctions.nextBoolean();

// True with 30% probability
bool b = MathFunctions.nextBoolean(0.3f);
```

### Gaussian Distribution

```java
// Normal distribution (mean=0, stddev=1)
double value = MathFunctions.nextGaussian();

// Clamped Gaussian
double value = MathFunctions.nextGaussianClamped(50, 10, 0, 100);
```

## Choice Operations

### pick()

Randomly select an element.

```java
// From array
String choice = MathFunctions.pick("A", "B", "C");

// From list
ItemStack item = MathFunctions.pick(itemList);
```

### pickWeighted()

Select with weighted probabilities.

```java
Map<Item, Double> drops = new HashMap<>();
drops.put(Items.DIAMOND, 0.1);   // 10% chance
drops.put(Items.IRON_INGOT, 0.5); // 50% chance
drops.put(Items.GOLD_INGOT, 0.4); // 40% chance

Item drop = MathFunctions.pickWeighted(drops);
```

## Utility Functions

### lerp()

Linear interpolation.

```java
double value = MathFunctions.lerp(start, end, t); // t from 0.0 to 1.0
```

### clamp()

Clamp a value between min and max.

```java
double value = MathFunctions.clamp(input, 0.0, 1.0);
```

### map()

Map a value from one range to another.

```java
// Map 0-100 to 0.0-1.0
double normalized = MathFunctions.map(value, 0, 100, 0.0, 1.0);
```

## Angle & Trigonometry

```java
// Conversions
double radians = MathFunctions.toRadians(degrees);
double degrees = MathFunctions.toDegrees(radians);

// Random angles
double rad = MathFunctions.randomAngle();     // 0 to 2π
double deg = MathFunctions.randomAngleDegrees(); // 0 to 360
```

## Migration

Replaces `Chance`:

| Old | New |
|-----|-----|
| `Chance.of(percent)` | `MathFunctions.chance(percent)` or `MathFunctions.of(percent)` |
