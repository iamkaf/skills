# Inventory Utilities

Amber provides utilities for working with player inventories, item management, and inventory-related operations. These utilities help simplify common inventory tasks and provide consistent behavior across platforms.

::: warning
Note: The utility classes described here are currently marked as deprecated and will be replaced with versioned alternatives in a future release. They are still functional but consider them as legacy APIs.
:::

## InventoryHelper

The `InventoryHelper` class provides methods for checking, consuming, and iterating through inventory contents.

### Checking Inventory Contents

Check if an inventory contains specific items, ingredients, or tags:

```java
import com.iamkaf.amber.api.inventory.InventoryHelper;
import net.minecraft.world.item.Items;
import net.minecraft.tags.ItemTags;
import net.minecraft.world.item.crafting.Ingredient;

public class InventoryChecks {
    // Check for specific items
    public static boolean hasDiamondPickaxe(Player player) {
        return InventoryHelper.has(player.getInventory(), Items.DIAMOND_PICKAXE);
    }
    
    // Check for items with tags
    public static boolean hasWood(Player player) {
        return InventoryHelper.has(player.getInventory(), ItemTags.LOGS);
    }
    
    // Check for specific quantities
    public static boolean hasMultipleItems(Player player, Item item, int count) {
        return InventoryHelper.has(player.getInventory(), item, count);
    }
    
    // Check for recipe ingredients
    public static boolean hasCraftingMaterials(Player player, Ingredient ingredient) {
        return InventoryHelper.has(player.getInventory(), ingredient);
    }
    
    // Check for ingredients with specific count
    public static boolean hasEnoughForCrafting(Player player, Ingredient ingredient, int count) {
        return InventoryHelper.has(player.getInventory(), ingredient, count);
    }
    
    // Check for tag-based items with count
    public static boolean hasEnoughWood(Player player, int count) {
        return InventoryHelper.has(player.getInventory(), ItemTags.LOGS, count);
    }
}
```

### Consuming Items

Consume items from inventory if available:

```java
public class ItemConsumption {
    // Consume single item
    public static boolean consumeDiamond(Player player) {
        return InventoryHelper.consumeIfAvailable(player.getInventory(), Items.DIAMOND);
    }
    
    // Consume multiple items
    public static boolean consumeMultipleItems(Player player, Item item, int count) {
        if (InventoryHelper.consumeIfAvailable(player.getInventory(), item, count)) {
            player.sendSystemMessage(Component.literal("Consumed " + count + " " + 
                item.getName(new ItemStack(item)).getString()));
            return true;
        } else {
            player.sendSystemMessage(Component.literal("Not enough items!"));
            return false;
        }
    }
    
    // Consume tag-based items
    public static boolean consumeWood(Player player) {
        return InventoryHelper.consumeIfAvailable(player.getInventory(), ItemTags.LOGS);
    }
    
    // Consume recipe ingredients
    public static boolean consumeForCrafting(Player player, Ingredient ingredient) {
        return InventoryHelper.consumeIfAvailable(player.getInventory(), ingredient, 1);
    }
    
    // Consume with cost and feedback
    public static boolean consumeWithCost(Player player, Item item, int cost) {
        if (InventoryHelper.consumeIfAvailable(player.getInventory(), item, cost)) {
            player.sendSystemMessage(Component.literal("Paid " + cost + " " + 
                item.getName(new ItemStack(item)).getString()));
            return true;
        } else {
            player.sendSystemMessage(Component.literal("Not enough " + 
                item.getName(new ItemStack(item)).getString() + "!"));
            return false;
        }
    }
    
    // Consume multiple different items
    public static boolean consumeRecipeItems(Player player, Map<Item, Integer> recipe) {
        boolean hasAllItems = true;
        
        // Check if player has all required items
        for (Map.Entry<Item, Integer> entry : recipe.entrySet()) {
            if (!InventoryHelper.has(player.getInventory(), entry.getKey(), entry.getValue())) {
                hasAllItems = false;
                break;
            }
        }
        
        // If player has all items, consume them
        if (hasAllItems) {
            for (Map.Entry<Item, Integer> entry : recipe.entrySet()) {
                InventoryHelper.consumeIfAvailable(player.getInventory(), entry.getKey(), entry.getValue());
            }
            return true;
        }
        
        return false;
    }
}
```

### Inventory Iteration

Iterate through all items in an inventory:

```java
public class InventoryScanner {
    // Find damaged items
    public static void findDamagedItems(Player player) {
        List<ItemStack> damagedItems = new ArrayList<>();
        
        InventoryHelper.forEach(player.getInventory(), stack -> {
            if (!stack.isEmpty() && stack.getDamageValue() > 0) {
                damagedItems.add(stack.copy());
            }
        });
        
        if (!damagedItems.isEmpty()) {
            player.sendSystemMessage(Component.literal("Found " + damagedItems.size() + " damaged items"));
            
            // Print details of each damaged item
            for (ItemStack damaged : damagedItems) {
                int damage = damaged.getDamageValue();
                int maxDamage = damaged.getMaxDamage();
                double percentage = (double) damage / maxDamage * 100;
                
                player.sendSystemMessage(Component.literal(
                    "- " + damaged.getDisplayName().getString() + 
                    " (" + String.format("%.1f", percentage) + "% damaged)"
                ));
            }
        }
    }
    
    // Count enchanted items
    public static void countEnchantedItems(Player player) {
        AtomicInteger enchantedCount = new AtomicInteger(0);
        Map<Enchantment, Integer> enchantments = new HashMap<>();
        
        InventoryHelper.forEach(player.getInventory(), stack -> {
            if (!stack.isEmpty() && stack.isEnchanted()) {
                enchantedCount.incrementAndGet();
                
                // Count enchantments
                for (Map.Entry<Enchantment, Integer> entry : stack.getAllEnchantments().entrySet()) {
                    enchantments.merge(entry.getKey(), entry.getValue(), Integer::sum);
                }
            }
        });
        
        player.sendSystemMessage(Component.literal("You have " + enchantedCount.get() + " enchanted items"));
        
        // Show enchantment summary
        if (!enchantments.isEmpty()) {
            player.sendSystemMessage(Component.literal("Enchantments:"));
            for (Map.Entry<Enchantment, Integer> entry : enchantments.entrySet()) {
                player.sendSystemMessage(Component.literal(
                    "- " + entry.getKey().getFullname(entry.getValue()).getString() + 
                    " (x" + entry.getValue() + ")"
                ));
            }
        }
    }
    
    // Get items of specific type
    public static List<ItemStack> getItemsOfType(Player player, Item targetItem) {
        List<ItemStack> items = new ArrayList<>();
        
        InventoryHelper.forEach(player.getInventory(), stack -> {
            if (!stack.isEmpty() && stack.is(targetItem)) {
                items.add(stack.copy());
            }
        });
        
        return items;
    }
    
    // Calculate total value of items
    public static int calculateInventoryValue(Player player, Map<Item, Integer> itemValues) {
        AtomicInteger totalValue = new AtomicInteger(0);
        
        InventoryHelper.forEach(player.getInventory(), stack -> {
            if (!stack.isEmpty()) {
                Item item = stack.getItem();
                int count = stack.getCount();
                Integer value = itemValues.get(item);
                
                if (value != null) {
                    totalValue.addAndGet(value * count);
                }
            }
        });
        
        return totalValue.get();
    }
    
    // Find rare items
    public static void findRareItems(Player player) {
        List<ItemStack> rareItems = new ArrayList<>();
        
        // Define what makes an item "rare"
        Predicate<ItemStack> isRare = stack -> {
            if (stack.isEmpty()) return false;
            
            // Consider enchanted items rare
            if (stack.isEnchanted()) return true;
            
            // Consider items with custom names rare
            if (stack.hasCustomHoverName()) return true;
            
            // Consider specific items rare
            return stack.is(Items.DIAMOND) || stack.is(Items.EMERALD) || stack.is(Items.NETHER_STAR);
        };
        
        InventoryHelper.forEach(player.getInventory(), stack -> {
            if (isRare.test(stack)) {
                rareItems.add(stack.copy());
            }
        });
        
        if (!rareItems.isEmpty()) {
            player.sendSystemMessage(Component.literal("Found " + rareItems.size() + " rare items:"));
            
            for (ItemStack rare : rareItems) {
                Component name = rare.hasCustomHoverName() ? 
                    rare.getHoverName() : rare.getDisplayName();
                
                player.sendSystemMessage(Component.literal("- " + name.getString()));
            }
        }
    }
}
```

## Advanced Inventory Operations

### Inventory Management

Create more complex inventory management systems:

```java
public class InventoryManager {
    // Sort inventory by item value
    public static void sortInventoryByValue(Player player, Map<Item, Integer> itemValues) {
        List<ItemStack> items = new ArrayList<>();
        
        // Collect all non-empty items
        InventoryHelper.forEach(player.getInventory(), stack -> {
            if (!stack.isEmpty()) {
                items.add(stack.copy());
            }
        });
        
        // Sort by value (highest first)
        items.sort((a, b) -> {
            Integer valueA = itemValues.get(a.getItem());
            Integer valueB = itemValues.get(b.getItem());
            
            if (valueA == null && valueB == null) return 0;
            if (valueA == null) return 1;
            if (valueB == null) return -1;
            
            return Integer.compare(valueB, valueA);
        });
        
        // Clear inventory and re-add sorted items
        player.getInventory().clearContent();
        
        for (ItemStack stack : items) {
            player.getInventory().add(stack);
        }
        
        player.sendSystemMessage(Component.literal("Inventory sorted by value"));
    }
    
    // Transfer items between inventories
    public static int transferItems(Inventory source, Inventory target, Item item, int maxAmount) {
        int transferred = 0;
        
        // Find items in source inventory
        for (int i = 0; i < source.getContainerSize() && transferred < maxAmount; i++) {
            ItemStack sourceStack = source.getItem(i);
            
            if (!sourceStack.isEmpty() && sourceStack.is(item)) {
                int available = sourceStack.getCount();
                int toTransfer = Math.min(available, maxAmount - transferred);
                
                // Try to add to target inventory
                ItemStack toAdd = sourceStack.copy();
                toAdd.setCount(toTransfer);
                
                boolean added = false;
                for (int j = 0; j < target.getContainerSize(); j++) {
                    ItemStack targetStack = target.getItem(j);
                    
                    if (targetStack.isEmpty()) {
                        // Empty slot - add directly
                        target.setItem(j, toAdd);
                        added = true;
                        break;
                    } else if (targetStack.is(item) && targetStack.getCount() < targetStack.getMaxStackSize()) {
                        // Existing stack - merge if possible
                        int space = targetStack.getMaxStackSize() - targetStack.getCount();
                        int canAdd = Math.min(toTransfer, space);
                        
                        targetStack.grow(canAdd);
                        toAdd.shrink(canAdd);
                        
                        if (toAdd.isEmpty()) {
                            added = true;
                            break;
                        }
                    }
                }
                
                if (added) {
                    sourceStack.shrink(toTransfer);
                    transferred += toTransfer;
                }
            }
        }
        
        return transferred;
    }
    
    // Check inventory capacity
    public static boolean hasSpaceFor(Inventory inventory, ItemStack stack) {
        int needed = stack.getCount();
        
        // Check existing stacks
        for (int i = 0; i < inventory.getContainerSize(); i++) {
            ItemStack existing = inventory.getItem(i);
            
            if (existing.isEmpty()) {
                // Empty slot can fit entire stack
                return true;
            } else if (ItemStack.isSameItemSameTags(existing, stack)) {
                // Can merge with existing stack
                int space = existing.getMaxStackSize() - existing.getCount();
                needed -= space;
                
                if (needed <= 0) {
                    return true;
                }
            }
        }
        
        return false;
    }
    
    // Get inventory summary
    public static Component getInventorySummary(Player player) {
        Map<Item, Integer> itemCounts = new HashMap<>();
        int totalItems = 0;
        int totalValue = 0;
        
        // Count items
        InventoryHelper.forEach(player.getInventory(), stack -> {
            if (!stack.isEmpty()) {
                Item item = stack.getItem();
                int count = stack.getCount();
                
                itemCounts.merge(item, count, Integer::sum);
                totalItems += count;
                
                // Calculate value (example calculation)
                totalValue += calculateItemValue(stack);
            }
        });
        
        // Create summary component
        MutableComponent summary = Component.literal("Inventory Summary:\n");
        summary.append(Component.literal("Total items: " + totalItems + "\n"));
        summary.append(Component.literal("Unique items: " + itemCounts.size() + "\n"));
        summary.append(Component.literal("Estimated value: " + totalValue + " gold\n"));
        
        // Add top 5 most common items
        List<Map.Entry<Item, Integer>> sorted = itemCounts.entrySet().stream()
            .sorted(Map.Entry.<Item, Integer>comparingByValue().reversed())
            .limit(5)
            .toList();
        
        summary.append(Component.literal("Top items:\n"));
        for (Map.Entry<Item, Integer> entry : sorted) {
            Component itemName = entry.getKey().getName(new ItemStack(entry.getKey()));
            summary.append(Component.literal("- " + itemName.getString() + ": " + entry.getValue() + "\n"));
        }
        
        return summary;
    }
    
    private static int calculateItemValue(ItemStack stack) {
        // Simple value calculation based on item type and properties
        Item item = stack.getItem();
        int baseValue = 0;
        
        // Base values for common items
        if (item == Items.DIAMOND) baseValue = 100;
        else if (item == Items.GOLD_INGOT) baseValue = 50;
        else if (item == Items.IRON_INGOT) baseValue = 25;
        else if (item == Items.EMERALD) baseValue = 150;
        
        // Adjust for enchantments
        if (stack.isEnchanted()) {
            baseValue *= 1.5;
        }
        
        // Adjust for damage
        if (stack.getMaxDamage() > 0) {
            double condition = 1.0 - (double) stack.getDamageValue() / stack.getMaxDamage();
            baseValue = (int) (baseValue * condition);
        }
        
        return baseValue * stack.getCount();
    }
}
```

## Best Practices

### 1. Validation

Always validate inventory operations:

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

Check for null values when working with inventories:

```java
public static void safeInventoryIteration(Inventory inventory) {
    if (inventory == null) {
        return;
    }
    
    InventoryHelper.forEach(inventory, stack -> {
        // Safe iteration logic
    });
}
```

### 3. Side Awareness

Be aware of client/server side differences:

```java
public static void updateInventoryOnServer(Player player) {
    if (player instanceof ServerPlayer) {
        // Server-side inventory updates
        player.getInventory().setChanged();
        player.containerMenu.broadcastChanges();
    }
}
```

### 4. Performance

Consider performance for large inventories:

```java
public static void efficientInventoryCheck(Inventory inventory, Predicate<ItemStack> predicate) {
    // Stop early if condition is met
    for (int i = 0; i < inventory.getContainerSize(); i++) {
        ItemStack stack = inventory.getItem(i);
        if (!stack.isEmpty() && predicate.test(stack)) {
            // Found what we're looking for
            return;
        }
    }
}
```

These inventory utilities provide helpful shortcuts for common inventory operations while maintaining cross-platform compatibility.