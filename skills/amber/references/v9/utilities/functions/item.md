# ItemFunctions

Item, inventory, enchantment, and armor operations.

**Package**: `com.iamkaf.amber.api.functions.v1`

## Inventory Operations

### has()

Check if inventory contains items.

```java
// By item
boolean hasItem = ItemFunctions.has(inventory, Items.DIAMOND);

// By ingredient
boolean hasIngredient = ItemFunctions.has(inventory, myIngredient);

// By tag
boolean hasTag = ItemFunctions.has(inventory, TagKey.create(Registries.ITEM, "c:ores"));

// With amount
boolean hasEnough = ItemFunctions.has(inventory, Items.DIAMOND, 5);
```

### consumeIfAvailable()

Consume items from inventory if available.

```java
// Consume 1 item
boolean consumed = ItemFunctions.consumeIfAvailable(inventory, Items.DIAMOND);

// Consume amount
boolean consumed = ItemFunctions.consumeIfAvailable(inventory, Items.DIAMOND, 5);

// By ingredient
boolean consumed = ItemFunctions.consumeIfAvailable(inventory, ingredient, 3);

// By tag
boolean consumed = ItemFunctions.consumeIfAvailable(inventory, tag, 1);
```

### forEach()

Execute action on each inventory slot.

```java
ItemFunctions.forEach(inventory, stack -> {
    // Process each stack
    if (!stack.isEmpty()) {
        // Do something
    }
});
```

## Item Operations

### repairBy()

Repair item by percentage of max durability.

```java
// Repair 25% of max durability
ItemFunctions.repairBy(itemStack, 0.25f);
```

### getIngredientDisplayName()

Get display name for ingredient.

```java
String name = ItemFunctions.getIngredientDisplayName(ingredient);
// Returns "Diamond" or "One of Diamond, Emerald, etc..."
```

### Attribute Modifiers

Add modifiers to items.

```java
ItemFunctions.addModifier(
    stack,
    Attributes.ATTACK_DAMAGE,
    modifier,
    EquipmentSlotGroup.MAINHAND
);

// Check for modifier
boolean hasMod = ItemFunctions.hasModifier(stack, modifierId);
```

## Enchantment Operations

### containsEnchantment()

Check if item has enchantment.

```java
// By Identifier
boolean hasSharpness = ItemFunctions.containsEnchantment(
    stack,
    Identifier.of("minecraft", "sharpness")
);

// By Enchantment object
boolean hasSharpness = ItemFunctions.containsEnchantment(
    stack,
    Enchantments.SHARPNESS
);
```

### getEnchantmentLevel()

Get enchantment level.

```java
// By Identifier
int level = ItemFunctions.getEnchantmentLevel(
    stack,
    Identifier.of("minecraft", "sharpness")
);

// By Enchantment object
int level = ItemFunctions.getEnchantmentLevel(
    stack,
    Enchantments.SHARPNESS
);
```

### isEnchanted()

Check if item has any enchantments.

```java
boolean enchanted = ItemFunctions.isEnchanted(stack);
```

### getEnchantments()

Get all enchantments as component.

```java
ItemEnchantments enchants = ItemFunctions.getEnchantments(stack);
```

## Armor Helpers

### repair()

Create repair ingredient supplier.

```java
Supplier<Ingredient> repairMaterial = ItemFunctions.repair(() -> MyItems.DIAMOND);

// Use in armor material
// armorMaterial.repairItem(repairMaterial.get())
```

### Vanilla Armor Values

Enums for vanilla armor properties:

```java
// Toughness
ItemFunctions.VanillaToughness.DIAMOND.fullSet     // 8
ItemFunctions.VanillaToughness.DIAMOND.helmet       // 2
ItemFunctions.VanillaToughness.NETHERITE.fullSet   // 13

// Knockback Resistance
ItemFunctions.VanillaKnockbackResistance.NETHERITE.knockbackResistance  // 0.1
ItemFunctions.VanillaKnockbackResistance.DIAMOND.knockbackResistance    // 0.02

// Enchantability
ItemFunctions.VanillaEnchantability.GOLD.enchantability  // 25
ItemFunctions.VanillaEnchantability.DIAMOND.enchantability // 10
```

## Equipment Slots

### getEquipmentSlot()

Get equipment slot for item type.

```java
EquipmentSlot slot = ItemFunctions.getEquipmentSlot(Items.DIAMOND_SWORD);
// Returns EquipmentSlot.MAINHAND

EquipmentSlot slot = ItemFunctions.getEquipmentSlot(Items.DIAMOND_HELMET);
// Returns EquipmentSlot.HEAD
```

### getDefaultSlot()

Get default equipment slot for an item.

```java
EquipmentSlot slot = ItemFunctions.getDefaultSlot(Items.DIAMOND_CHESTPLATE);
```

## Migration

Replaces `ItemHelper`, `InventoryHelper`, `EnchantmentUtils`, and `ArmorTierHelper`:

| Old | New |
|-----|-----|
| `ItemHelper.repairBy()` | `ItemFunctions.repairBy()` |
| `ItemHelper.getIngredientDisplayName()` | `ItemFunctions.getIngredientDisplayName()` |
| `ItemHelper.addModifier()` | `ItemFunctions.addModifier()` |
| `ItemHelper.hasModifier()` | `ItemFunctions.hasModifier()` |
| `InventoryHelper.consumeIfAvailable()` | `ItemFunctions.consumeIfAvailable()` |
| `InventoryHelper.has()` | `ItemFunctions.has()` |
| `InventoryHelper.forEach()` | `ItemFunctions.forEach()` |
| `EnchantmentUtils.containsEnchantment()` | `ItemFunctions.containsEnchantment()` |
| `EnchantmentUtils.getEnchantmentLevel()` | `ItemFunctions.getEnchantmentLevel()` |
| `ArmorTierHelper.repair()` | `ItemFunctions.repair()` |
| `ArmorTierHelper.VanillaToughness` | `ItemFunctions.VanillaToughness` |
