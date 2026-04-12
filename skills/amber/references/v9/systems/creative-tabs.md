# Creative Mode Tabs API

Amber provides a unified API for working with creative mode tabs that works across all mod loaders (Fabric, Forge, NeoForge). This API allows you to:

1. Register new custom creative mode tabs
2. Add items to existing tabs (vanilla or from other mods)
3. Configure tab properties like title, icon, and appearance

## Creating Custom Tabs

To create a custom creative mode tab, use the `CreativeModeTabRegistry` class:

```java
public class MyModTabs {
    public static final RegistrySupplier<CreativeModeTab> EXAMPLE_TAB = 
        CreativeModeTabRegistry.register(
            CreativeModeTabRegistry.builder("example")
                .title(Component.translatable("itemGroup.mymod.example"))
                .icon(MyItems.EXAMPLE_ITEM)
                .addItem(MyItems.EXAMPLE_ITEM)
                .addItem(MyBlocks.EXAMPLE_BLOCK)
        );
}
```

### Tab Builder Options

The `TabBuilder` class provides various methods to configure your tab:

| Method | Description | Default |
|--------|-------------|---------|
| `title(Component)` | Sets the tab's title | Component.empty() |
| `icon(Supplier<ItemStack>)` | Sets the tab's icon | () -> ItemStack.EMPTY |
| `icon(ItemLike)` | Sets the tab's icon | - |
| `addItem(Supplier<ItemLike>)` | Adds an item to the tab | - |
| `addItem(ItemLike)` | Adds an item to the tab | - |
| `addItems(ItemLike...)` | Adds multiple items to the tab | - |
| `backgroundTexture(ResourceLocation)` | Sets the background texture | Default items texture |
| `canScroll(boolean)` | Whether the tab can scroll | true |
| `showTitle(boolean)` | Whether to show the title | true |
| `alignedRight(boolean)` | Whether to align the tab right | false |
| `row(CreativeModeTab.Row)` | Sets the row position | TOP |
| `column(int)` | Sets the column position | 0 |

## Adding Items to Existing Tabs

To add items to existing tabs (vanilla or from other mods), use the `CreativeTabHelper` class:

```java
public class MyModTabRegistration {
    public static void registerTabEvents() {
        // Add to a vanilla tab
        ResourceKey<CreativeModeTab> ingredientsTab = ResourceKey.create(
            Registries.CREATIVE_MODE_TAB, 
            ResourceLocation.fromNamespaceAndPath("minecraft", "ingredients")
        );
        CreativeTabHelper.addItem(ingredientsTab, MyItems.SPECIAL_INGREDIENT);
        
        // Add to another mod's tab
        ResourceKey<CreativeModeTab> otherModTab = ResourceKey.create(
            Registries.CREATIVE_MODE_TAB, 
            ResourceLocation.fromNamespaceAndPath("othermod", "tab")
        );
        CreativeTabHelper.addItem(otherModTab, MyItems.COMPAT_ITEM);
        
        // Add multiple items
        CreativeTabHelper.addItems(ingredientsTab, 
            MyItems.SPECIAL_INGREDIENT_2, 
            MyItems.SPECIAL_INGREDIENT_3);
    }
}
```

### Common Tab Resource Keys

Here are some common vanilla tab resource keys you might use:

```java
// Building blocks
ResourceKey.create(Registries.CREATIVE_MODE_TAB, ResourceLocation.fromNamespaceAndPath("minecraft", "building_blocks"))

// Colored blocks
ResourceKey.create(Registries.CREATIVE_MODE_TAB, ResourceLocation.fromNamespaceAndPath("minecraft", "colored_blocks"))

// Natural blocks
ResourceKey.create(Registries.CREATIVE_MODE_TAB, ResourceLocation.fromNamespaceAndPath("minecraft", "natural_blocks"))

// Functional blocks
ResourceKey.create(Registries.CREATIVE_MODE_TAB, ResourceLocation.fromNamespaceAndPath("minecraft", "functional_blocks"))

// Redstone blocks
ResourceKey.create(Registries.CREATIVE_MODE_TAB, ResourceLocation.fromNamespaceAndPath("minecraft", "redstone_blocks"))

// Tools and utilities
ResourceKey.create(Registries.CREATIVE_MODE_TAB, ResourceLocation.fromNamespaceAndPath("minecraft", "tools_and_utilities"))

// Food and drinks
ResourceKey.create(Registries.CREATIVE_MODE_TAB, ResourceLocation.fromNamespaceAndPath("minecraft", "food_and_drinks"))

// Ingredients
ResourceKey.create(Registries.CREATIVE_MODE_TAB, ResourceLocation.fromNamespaceAndPath("minecraft", "ingredients"))

// Spawn eggs
ResourceKey.create(Registries.CREATIVE_MODE_TAB, ResourceLocation.fromNamespaceAndPath("minecraft", "spawn_eggs"))
```

## Advanced Usage

### Conditional Item Addition

You can conditionally add items based on the tab being modified:

```java
CreativeModeTabEvents.MODIFY_ENTRIES.register((tabKey, output) -> {
    // Only add to the ingredients tab
    if (tabKey.equals(ingredientsTab)) {
        output.accept(MyItems.SPECIAL_INGREDIENT);
    }
});
```

### Adding Items to Your Own Tabs During Registration

If you want to add items to your own tabs during registration (useful for organizing code):

```java
public class MyModTabs {
    public static final RegistrySupplier<CreativeModeTab> EXAMPLE_TAB = 
        CreativeModeTabRegistry.register(
            CreativeModeTabRegistry.builder("example")
                .title(Component.translatable("itemGroup.mymod.example"))
                .icon(MyItems.EXAMPLE_ITEM)
        );
    
    public static void registerTabItems() {
        // Add items to the tab
        CreativeTabHelper.addItemsToTab(
            ResourceLocation.fromNamespaceAndPath("mymod", "example"),
            MyItems.EXAMPLE_ITEM,
            MyBlocks.EXAMPLE_BLOCK
        );
    }
}
```

## Platform-Specific Notes

### Fabric
- Uses `ItemGroupEvents.modifyEntriesEvent` internally
- Works with Fabric's item group system

### Forge/NeoForge
- Uses `BuildCreativeModeTabContentsEvent` internally
- Works with Forge/NeoForge's creative tab system

## Translation Keys

Don't forget to add translation keys for your custom tabs in your language files:

```json
{
  "itemGroup.mymod.example": "Example Tab"
}
```

## Best Practices

1. **Register tabs during mod initialization**: Make sure to register your tabs early in the mod loading process.

2. **Use descriptive tab IDs**: Use clear, descriptive names for your tab IDs to avoid conflicts.

3. **Organize items logically**: Group related items together in your tabs for better user experience.

4. **Consider tab order**: Use the `row()` and `column()` methods to position your tabs logically in the creative inventory.

5. **Provide proper translations**: Always add translation keys for your tab titles.

## Complete Example

Here's a complete example of a mod with a custom creative mode tab:

```java
public class ExampleMod {
    public static final String MOD_ID = "examplemod";
    
    // Register the tab
    public static final RegistrySupplier<CreativeModeTab> EXAMPLE_TAB = 
        CreativeModeTabRegistry.register(
            CreativeModeTabRegistry.builder("example")
                .title(Component.translatable("itemGroup." + MOD_ID + ".example"))
                .icon(ExampleModItems.EXAMPLE_ITEM)
                .addItems(
                    ExampleModItems.EXAMPLE_ITEM,
                    ExampleModItems.EXAMPLE_ITEM_2,
                    ExampleModBlocks.EXAMPLE_BLOCK
                )
        );
    
    // Register tab events
    public static void registerTabEvents() {
        // Add our item to the ingredients tab as well
        ResourceKey<CreativeModeTab> ingredientsTab = ResourceKey.create(
            Registries.CREATIVE_MODE_TAB, 
            ResourceLocation.fromNamespaceAndPath("minecraft", "ingredients")
        );
        CreativeTabHelper.addItem(ingredientsTab, ExampleModItems.EXAMPLE_ITEM);
    }
}
```

With translation file:

```json
{
  "itemGroup.examplemod.example": "Example Mod Items"
}