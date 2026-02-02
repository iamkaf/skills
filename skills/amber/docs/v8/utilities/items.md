# Item Utilities

Amber provides several utility classes for working with items, inventory, and item-related operations. These utilities help simplify common tasks and provide consistent behavior across platforms.

::: warning
Note: The utility classes described here are currently marked as deprecated and will be replaced with versioned alternatives in a future release. They are still functional but consider them as legacy APIs.
:::

## ItemHelper

The `ItemHelper` class provides various methods for item manipulation and attribute management.

### Item Repair

Repair items by a percentage of their maximum durability:

```java
import com.iamkaf.amber.api.inventory.ItemHelper;

// Repair an item by 25% of its max durability
ItemStack tool = player.getMainHandItem();
ItemHelper.repairBy(tool, 0.25f);

// Repair an item by 50% of its max durability
ItemHelper.repairBy(armor, 0.5f);

// Fully repair an item (100%)
ItemHelper.repairBy(item, 1.0f);
```

### Ingredient Display Names

Get user-friendly display names for recipe ingredients:

```java
public class RecipeHelper {
    public static void printIngredientInfo(Ingredient ingredient) {
        String displayName = ItemHelper.getIngredientDisplayName(ingredient);
        
        if (player != null) {
            player.sendSystemMessage(Component.literal("Required: " + displayName));
        }
    }
    
    public static Component getIngredientComponent(Ingredient ingredient) {
        String name = ItemHelper.getIngredientDisplayName(ingredient);
        return Component.literal(name).withStyle(ChatFormatting.GRAY);
    }
}
```

### Attribute Modifiers

Add and manage item attribute modifiers:

```java
import com.iamkaf.amber.api.inventory.ItemHelper;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.ai.attributes.AttributeModifier;
import net.minecraft.world.entity.EquipmentSlotGroup;

public class ItemEnchantment {
    public static void addSpeedBoost(ItemStack boots) {
        // Create a speed boost modifier
        AttributeModifier speedModifier = new AttributeModifier(
            ResourceLocation.fromNamespaceAndPath("mymod", "speed_boost"),
            0.1, // 10% speed increase
            AttributeModifier.Operation.ADD_MULTIPLIED_BASE
        );
        
        // Add the modifier to the boots
        ItemHelper.addModifier(
            boots,
            Attributes.MOVEMENT_SPEED,
            speedModifier,
            EquipmentSlotGroup.FEET
        );
    }
    
    public static void addAttackDamage(ItemStack sword) {
        // Create a damage modifier
        AttributeModifier damageModifier = new AttributeModifier(
            ResourceLocation.fromNamespaceAndPath("mymod", "extra_damage"),
            2.0, // +2 attack damage
            AttributeModifier.Operation.ADD_VALUE
        );
        
        // Add the modifier to the sword
        ItemHelper.addModifier(
            sword,
            Attributes.ATTACK_DAMAGE,
            damageModifier,
            EquipmentSlotGroup.MAINHAND
        );
    }
    
    public static boolean hasSpeedBoost(ItemStack boots) {
        return ItemHelper.hasModifier(boots, 
            ResourceLocation.fromNamespaceAndPath("mymod", "speed_boost"));
    }
    
    public static boolean hasCustomModifier(ItemStack stack, String modifierId) {
        return ItemHelper.hasModifier(stack, 
            ResourceLocation.fromNamespaceAndPath("mymod", modifierId));
    }
}
```

## InventoryHelper

The `InventoryHelper` class provides methods for checking and manipulating inventory contents.

### Checking Inventory Contents

Check if an inventory contains specific items:

```java
import com.iamkaf.amber.api.inventory.InventoryHelper;
import net.minecraft.world.item.Items;
import net.minecraft.tags.ItemTags;

public class InventoryChecks {
    public static boolean hasDiamondPickaxe(Player player) {
        return InventoryHelper.has(player.getInventory(), Items.DIAMOND_PICKAXE);
    }
    
    public static boolean hasWood(Player player) {
        return InventoryHelper.has(player.getInventory(), ItemTags.LOGS);
    }
    
    public static boolean hasMultipleItems(Player player, Item item, int count) {
        return InventoryHelper.has(player.getInventory(), item, count);
    }
    
    public static boolean hasIngredient(Player player, Ingredient ingredient) {
        return InventoryHelper.has(player.getInventory(), ingredient);
    }
    
    public static boolean hasIngredients(Player player, Ingredient ingredient, int count) {
        return InventoryHelper.has(player.getInventory(), ingredient, count);
    }
}
```

### Consuming Items

Consume items from inventory if available:

```java
public class ItemConsumption {
    public static boolean consumeDiamond(Player player) {
        return InventoryHelper.consumeIfAvailable(player.getInventory(), Items.DIAMOND);
    }
    
    public static boolean consumeMultipleItems(Player player, Item item, int count) {
        return InventoryHelper.consumeIfAvailable(player.getInventory(), item, count);
    }
    
    public static boolean consumeWood(Player player) {
        return InventoryHelper.consumeIfAvailable(player.getInventory(), ItemTags.LOGS);
    }
    
    public static boolean consumeForCrafting(Player player, Ingredient ingredient) {
        return InventoryHelper.consumeIfAvailable(player.getInventory(), ingredient, 1);
    }
    
    public static boolean consumeWithCost(Player player, Item item, int cost) {
        if (InventoryHelper.consumeIfAvailable(player.getInventory(), item, cost)) {
            player.sendSystemMessage(Component.literal("Paid " + cost + " " + item.getName(new ItemStack(item)).getString()));
            return true;
        } else {
            player.sendSystemMessage(Component.literal("Not enough " + item.getName(new ItemStack(item)).getString() + "!"));
            return false;
        }
    }
}
```

### Inventory Iteration

Iterate through all items in an inventory:

```java
public class InventoryScanner {
    public static void findDamagedItems(Player player) {
        List<ItemStack> damagedItems = new ArrayList<>();
        
        InventoryHelper.forEach(player.getInventory(), stack -> {
            if (!stack.isEmpty() && stack.getDamageValue() > 0) {
                damagedItems.add(stack.copy());
            }
        });
        
        if (!damagedItems.isEmpty()) {
            player.sendSystemMessage(Component.literal("Found " + damagedItems.size() + " damaged items"));
        }
    }
    
    public static void countEnchantedItems(Player player) {
        AtomicInteger enchantedCount = new AtomicInteger(0);
        
        InventoryHelper.forEach(player.getInventory(), stack -> {
            if (!stack.isEmpty() && stack.isEnchanted()) {
                enchantedCount.incrementAndGet();
            }
        });
        
        player.sendSystemMessage(Component.literal("You have " + enchantedCount.get() + " enchanted items"));
    }
    
    public static List<ItemStack> getItemsOfType(Player player, Item targetItem) {
        List<ItemStack> items = new ArrayList<>();
        
        InventoryHelper.forEach(player.getInventory(), stack -> {
            if (!stack.isEmpty() && stack.is(targetItem)) {
                items.add(stack.copy());
            }
        });
        
        return items;
    }
}
```

## Player Feedback

The `FeedbackHelper` class provides methods for sending messages to players.

### Chat Messages

Send messages to player chat:

```java
import com.iamkaf.amber.api.player.FeedbackHelper;

public class PlayerMessaging {
    public static void sendWelcomeMessage(Player player) {
        FeedbackHelper.message(player, 
            Component.literal("Welcome to the server!")
                .withStyle(ChatFormatting.GREEN));
    }
    
    public static void sendErrorMessage(Player player, String error) {
        FeedbackHelper.message(player, 
            Component.literal("Error: " + error)
                .withStyle(ChatFormatting.RED));
    }
    
    public static void sendInfoMessage(Player player, String info) {
        FeedbackHelper.message(player, 
            Component.literal(info)
                .withStyle(ChatFormatting.GRAY));
    }
}
```

### Action Bar Messages

Send messages to the action bar:

```java
public class ActionBarMessages {
    public static void showEnergy(Player player, int energy, int maxEnergy) {
        String percentage = String.format("%.1f", (double) energy / maxEnergy * 100);
        FeedbackHelper.actionBarMessage(player, 
            Component.literal("Energy: " + energy + "/" + maxEnergy + " (" + percentage + "%)")
                .withStyle(ChatFormatting.YELLOW));
    }
    
    public static void showCooldown(Player player, int seconds) {
        FeedbackHelper.actionBarMessage(player, 
            Component.literal("Cooldown: " + seconds + "s")
                .withStyle(ChatFormatting.RED));
    }
    
    public static void showStatus(Player player, String status) {
        FeedbackHelper.actionBarMessage(player, 
            Component.literal(status)
                .withStyle(ChatFormatting.AQUA));
    }
}
```

## Level Utilities

The `LevelHelper` class provides methods for world-level operations.

### Scheduled Tasks

Run tasks at regular intervals:

```java
import com.iamkaf.amber.api.level.LevelHelper;

public class WorldScheduler {
    public static void tickEvent(Level level) {
        // Run every 100 ticks (5 seconds)
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
    }
    
    private static void updateWorldClock(ServerLevel level) {
        // Custom clock update logic
    }
    
    private static void saveCustomData(ServerLevel level, long gameTime) {
        // Custom data saving logic
    }
}
```

### Item Drops

Drop items in the world:

```java
public class WorldDrops {
    public static void dropReward(Level level, Vec3 pos, Item item, int count) {
        ItemStack stack = new ItemStack(item, count);
        LevelHelper.dropItem(level, stack, pos);
    }
    
    public static void dropWithVelocity(Level level, Vec3 pos, ItemStack stack, Vec3 velocity) {
        LevelHelper.dropItem(level, stack, pos, velocity);
    }
    
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
}
```

## Sound Utilities

The `SoundHelper` class provides methods for playing sounds.

### Playing Sounds

Play sounds for players:

```java
import com.iamkaf.amber.api.sound.SoundHelper;

public class SoundEffects {
    public static void playSuccessSound(Player player) {
        SoundHelper.sendClientSound(player, SoundEvents.UI_TOAST_CHALLENGE_COMPLETE);
    }
    
    public static void playErrorSound(Player player) {
        SoundHelper.sendClientSound(player, SoundEvents.UI_BUTTON_CLICK);
    }
    
    public static void playLevelUpSound(Player player) {
        SoundHelper.sendClientSound(player, SoundEvents.PLAYER_LEVELUP, SoundSource.MASTER, 1.0f, 1.0f);
    }
    
    public static void playCustomSound(Player player, SoundEvent sound, float volume, float pitch) {
        SoundHelper.sendClientSound(player, sound, SoundSource.PLAYERS, volume, pitch);
    }
    
    public static void playAmbientSound(Player player) {
        SoundHelper.sendClientSound(player, SoundEvents.AMBIENT_CAVE, SoundSource.AMBIENT, 0.5f, 1.0f);
    }
}
```

## Math Utilities

The `Chance` class provides probability calculations.

### Random Events

Calculate random event probabilities:

```java
import com.iamkaf.amber.api.math.Chance;

public class RandomEvents {
    public static boolean tryCriticalHit() {
        // 25% chance of critical hit
        return Chance.of(0.25f);
    }
    
    public static boolean tryRareDrop() {
        // 5% chance of rare drop
        return Chance.of(0.05f);
    }
    
    public static boolean tryCommonEvent() {
        // 75% chance of common event
        return Chance.of(0.75f);
    }
    
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
    
    public static boolean shouldSpawnMob(Level level) {
        // Higher chance at night, lower during day
        boolean isNight = level.isNight();
        float chance = isNight ? 0.3f : 0.1f;
        return Chance.of(chance);
    }
}
```

## Best Practices

### 1. Validation

Always validate items before operations:

```java
public static boolean safeConsume(Inventory inventory, Item item, int amount) {
    // Check if item exists first
    if (!InventoryHelper.has(inventory, item, amount)) {
        return false;
    }
    
    // Then consume
    return InventoryHelper.consumeIfAvailable(inventory, item, amount);
}
```

### 2. Null Safety

Check for null values when working with items:

```java
public static void repairItemSafely(ItemStack stack) {
    if (stack == null || stack.isEmpty()) {
        return;
    }
    
    if (stack.getMaxDamage() > 0) {
        ItemHelper.repairBy(stack, 0.1f);
    }
}
```

### 3. Side Awareness

Be aware of client/server side differences:

```java
public static void playSoundIfServer(Player player, SoundEvent sound) {
    if (player instanceof ServerPlayer) {
        SoundHelper.sendClientSound(player, sound);
    }
}
```

These utility classes provide helpful shortcuts for common operations while maintaining cross-platform compatibility.