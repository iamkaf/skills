# Enchantment Helpers

Amber provides utility classes for working with enchantments across all mod loaders. The EnchantmentUtils class offers methods to check and manipulate enchantments on items in a platform-independent way.

## Overview

The enchantment helper includes:

- **Cross-platform compatibility**: Works consistently on Fabric, Forge, and NeoForge
- **Enchantment checking**: Verify if an item has specific enchantments
- **Resource location support**: Work with enchantments by their resource location

## Basic Usage

### Checking for Enchantments

Use `EnchantmentUtils.containsEnchantment()` to check if an item has a specific enchantment:

```java
import com.iamkaf.amber.api.enchantment.EnchantmentUtils;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;

public class EnchantmentExample {
    public static boolean hasSharpness(ItemStack stack) {
        // Check if item has Sharpness enchantment
        return EnchantmentUtils.containsEnchantment(
            stack, 
            ResourceLocation.fromNamespaceAndPath("minecraft", "sharpness")
        );
    }
    
    public static boolean hasCustomEnchantment(ItemStack stack) {
        // Check for custom mod enchantment
        return EnchantmentUtils.containsEnchantment(
            stack, 
            ResourceLocation.fromNamespaceAndPath("mymod", "magic_enchant")
        );
    }
    
    public static void checkPlayerEnchantments(ServerPlayer player) {
        ItemStack mainHand = player.getMainHandItem();
        
        if (hasSharpness(mainHand)) {
            player.sendSystemMessage(
                Component.literal("Your weapon is sharp!")
            );
        }
        
        if (hasCustomEnchantment(mainHand)) {
            player.sendSystemMessage(
                Component.literal("Your weapon has magic powers!")
            );
        }
    }
}
```

## Advanced Usage

### Enchantment Filtering

Filter items based on their enchantments:

```java
public class EnchantmentFiltering {
    public static List<ItemStack> getEnchantedItems(List<ItemStack> items) {
        return items.stream()
            .filter(stack -> !stack.isEmpty() && stack.isEnchanted())
            .collect(Collectors.toList());
    }
    
    public static List<ItemStack> getItemsWithEnchantment(
            List<ItemStack> items, 
            ResourceLocation enchantment) {
        return items.stream()
            .filter(stack -> EnchantmentUtils.containsEnchantment(stack, enchantment))
            .collect(Collectors.toList());
    }
    
    public static void processInventory(Player player) {
        List<ItemStack> enchantedItems = getEnchantedItems(
            player.getInventory().items
        );
        
        player.sendSystemMessage(
            Component.literal("You have " + enchantedItems.size() + " enchanted items")
        );
    }
}
```

### Enchantment Counting

Count enchantments on items:

```java
public class EnchantmentCounter {
    public static int getEnchantmentCount(ItemStack stack) {
        if (!stack.isEnchanted() || stack.getEnchantments().isEmpty()) {
            return 0;
        }
        
        return stack.getEnchantments().size();
    }
    
    public static int getSpecificEnchantmentCount(
            List<ItemStack> items, 
            ResourceLocation enchantment) {
        return (int) items.stream()
            .filter(stack -> EnchantmentUtils.containsEnchantment(stack, enchantment))
            .count();
    }
    
    public static void analyzeEnchantments(Player player) {
        int totalEnchanted = 0;
        int totalEnchantments = 0;
        
        for (ItemStack stack : player.getInventory().items) {
            if (stack.isEnchanted()) {
                totalEnchanted++;
                totalEnchantments += getEnchantmentCount(stack);
            }
        }
        
        player.sendSystemMessage(
            Component.literal("You have " + totalEnchanted + " enchanted items with " + 
                totalEnchantments + " total enchantments")
        );
    }
}
```

### Custom Enchantment Logic

Implement custom logic based on enchantments:

```java
public class CustomEnchantmentLogic {
    public static boolean isWeaponEffective(ItemStack weapon, EntityType<?> targetType) {
        // Check for specific enchantments that affect certain entity types
        if (targetType == EntityType.UNDEAD) {
            return EnchantmentUtils.containsEnchantment(
                weapon, 
                ResourceLocation.fromNamespaceAndPath("minecraft", "smite")
            );
        }
        
        if (targetType == EntityType.ARTHROPOD) {
            return EnchantmentUtils.containsEnchantment(
                weapon, 
                ResourceLocation.fromNamespaceAndPath("minecraft", "bane_of_arthropods")
            );
        }
        
        return false;
    }
    
    public static float getMiningSpeed(ItemStack tool, BlockState block) {
        float speed = tool.getDestroySpeed(block);
        
        // Check for efficiency enchantment
        if (EnchantmentUtils.containsEnchantment(
                tool, 
                ResourceLocation.fromNamespaceAndPath("minecraft", "efficiency"))) {
            // Add bonus based on enchantment level
            int level = getEnchantmentLevel(tool, "minecraft:efficiency");
            speed += level * 2.0F;
        }
        
        return speed;
    }
    
    private static int getEnchantmentLevel(ItemStack stack, String enchantmentId) {
        // This is a simplified example - you'd need to implement proper level checking
        if (EnchantmentUtils.containsEnchantment(
                stack, 
                ResourceLocation.fromNamespaceAndPath(enchantmentId))) {
            return 1; // Default to level 1 for demonstration
        }
        return 0;
    }
}
```

## ResourceLocation Usage

The EnchantmentUtils class uses ResourceLocation to identify enchantments. Since the ResourceLocation constructor is private, you must use factory methods:

```java
// Creating ResourceLocations with factory methods
ResourceLocation sharpness = ResourceLocation.fromNamespaceAndPath("minecraft", "sharpness");
ResourceLocation customEnchant = ResourceLocation.fromNamespaceAndPath("mymod", "magic_enchant");

// Alternative creation methods
ResourceLocation efficiency = ResourceLocation.parse("minecraft:efficiency");
ResourceLocation protection = ResourceLocation.bySeparator("minecraft:protection", ':');

// Default namespace (minecraft)
ResourceLocation unbreaking = ResourceLocation.withDefaultNamespace("unbreaking");
```

## Best Practices

### 1. Resource Location Usage

Always use factory methods to create ResourceLocation instances:

```java
// Good - Uses factory method
EnchantmentUtils.containsEnchantment(
    stack, 
    ResourceLocation.fromNamespaceAndPath("minecraft", "sharpness")
);

// Bad - Constructor is private, this won't compile
new ResourceLocation("minecraft", "sharpness")
```

### 2. Null Safety

Always check for null or empty ItemStacks:

```java
// Good - Checks for null/empty
public static boolean hasEnchantment(ItemStack stack) {
    if (stack == null || stack.isEmpty()) {
        return false;
    }
    
    return stack.isEnchanted() && 
           EnchantmentUtils.containsEnchantment(
               stack, 
               ResourceLocation.fromNamespaceAndPath("minecraft", "sharpness")
           );
}

// Bad - No null check
public static boolean hasEnchantment(ItemStack stack) {
    return EnchantmentUtils.containsEnchantment(
        stack, 
        ResourceLocation.fromNamespaceAndPath("minecraft", "sharpness")
    );
}
```

### 3. Performance Considerations

Batch operations when checking multiple enchantments:

```java
// Good - Check once, use multiple times
public static void analyzeItem(ItemStack stack) {
    if (!stack.isEnchanted()) return;
    
    boolean hasSharpness = EnchantmentUtils.containsEnchantment(
        stack, 
        ResourceLocation.fromNamespaceAndPath("minecraft", "sharpness")
    );
    boolean hasFireAspect = EnchantmentUtils.containsEnchantment(
        stack, 
        ResourceLocation.fromNamespaceAndPath("minecraft", "fire_aspect")
    );
    boolean hasKnockback = EnchantmentUtils.containsEnchantment(
        stack, 
        ResourceLocation.fromNamespaceAndPath("minecraft", "knockback")
    );
    
    // Use the results
    if (hasSharpness && hasFireAspect) {
        // Special case
    }
}

// Bad - Multiple checks
public static void analyzeItem(ItemStack stack) {
    if (EnchantmentUtils.containsEnchantment(stack, ResourceLocation.fromNamespaceAndPath("minecraft", "sharpness")) &&
        EnchantmentUtils.containsEnchantment(stack, ResourceLocation.fromNamespaceAndPath("minecraft", "fire_aspect")) &&
        EnchantmentUtils.containsEnchantment(stack, ResourceLocation.fromNamespaceAndPath("minecraft", "knockback"))) {
        // Multiple iterations through enchantments
    }
}
```

## Migration Note

The current `EnchantmentUtils` class is deprecated and will be replaced by a versioned alternative in a future release. While the current implementation works, consider the following when planning for future updates:

```java
// Current usage (deprecated)
EnchantmentUtils.containsEnchantment(stack, enchantment);

// Future implementation will likely be versioned
// EnchantmentUtilsV1.containsEnchantment(stack, enchantment);
```

The future version will provide improved functionality and better performance, but will maintain a similar API to minimize migration effort.

## Examples

### Enchantment-Based Abilities

Create abilities that activate based on enchantments:

```java
public class EnchantmentAbilities {
    public static void onEntityAttack(Player player, Entity target) {
        ItemStack weapon = player.getMainHandItem();
        
        // Fire damage bonus
        if (target instanceof LivingEntity living) {
            if (EnchantmentUtils.containsEnchantment(
                    weapon, 
                    ResourceLocation.fromNamespaceAndPath("minecraft", "fire_aspect"))) {
                living.setSecondsOnFire(3);
            }
        }
        
        // Special damage against specific types
        float damageBonus = 0;
        if (EnchantmentUtils.containsEnchantment(
                weapon, 
                ResourceLocation.fromNamespaceAndPath("minecraft", "smite")) && 
            target.getType() == EntityType.ZOMBIE) {
            damageBonus += 2.5F;
        }
        
        if (damageBonus > 0) {
            target.hurt(player.damageSources().playerAttack(player), damageBonus);
        }
    }
}
```

### Enchantment Display

Show enchantment information to players:

```java
public class EnchantmentDisplay {
    public static Component getEnchantmentTooltip(ItemStack stack) {
        if (!stack.isEnchanted()) {
            return Component.literal("No enchantments");
        }
        
        MutableComponent tooltip = Component.literal("Enchantments: ");
        
        // Check for common enchantments
        String[] commonEnchantments = {
            "minecraft:sharpness",
            "minecraft:protection",
            "minecraft:efficiency",
            "minecraft:fortune"
        };
        
        boolean first = true;
        for (String enchantmentId : commonEnchantments) {
            String[] parts = enchantmentId.split(":");
            if (parts.length == 2) {
                ResourceLocation enchantment = ResourceLocation.fromNamespaceAndPath(parts[0], parts[1]);
                if (EnchantmentUtils.containsEnchantment(stack, enchantment)) {
                    if (!first) {
                        tooltip.append(", ");
                    }
                    tooltip.append(Component.literal(parts[1]));
                    first = false;
                }
            }
        }
        
        return tooltip;
    }
}
```

The enchantment utilities provide a foundation for working with enchantments across all platforms while abstracting platform-specific implementation details.