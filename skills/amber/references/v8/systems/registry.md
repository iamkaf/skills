# Registry System

Amber provides a unified registry system that works across all mod loaders, allowing you to register items, blocks, entities, and other game objects with a consistent API. The system uses deferred registration, which means your objects are registered at the appropriate time during mod loading.

## Overview

The registry system consists of:

- **DeferredRegister**: Manages registration for a specific registry type
- **RegistrySupplier**: Provides lazy access to registered objects
- **RegistrarManager**: Handles the actual registration process
- **Cross-platform compatibility**: Works identically on Fabric, Forge, and NeoForge

## Basic Usage

### Setting Up Deferred Registers

Create deferred registers for each type of object you want to register:

```java
import com.iamkaf.amber.api.registry.v1.DeferredRegister;
import com.iamkaf.amber.api.registry.v1.RegistrySupplier;
import net.minecraft.core.registries.Registries;

public class MyRegistries {
    public static final String MOD_ID = "mymod";
    
    // Deferred registers for different object types
    public static final DeferredRegister<Item> ITEMS = 
        DeferredRegister.create(MOD_ID, Registries.ITEM);
    
    public static final DeferredRegister<Block> BLOCKS = 
        DeferredRegister.create(MOD_ID, Registries.BLOCK);
    
    public static final DeferredRegister<EntityType<?>> ENTITIES = 
        DeferredRegister.create(MOD_ID, Registries.ENTITY_TYPE);
    
    public static final DeferredRegister<SoundEvent> SOUNDS = 
        DeferredRegister.create(MOD_ID, Registries.SOUND_EVENT);
    
    public static final DeferredRegister<CreativeModeTab> CREATIVE_TABS =
        DeferredRegister.create(MOD_ID, Registries.CREATIVE_MODE_TAB);
    
    // Initialize all registers
    public static void init() {
        ITEMS.register();
        BLOCKS.register();
        ENTITIES.register();
        SOUNDS.register();
        CREATIVE_TABS.register();
    }
}
```

### Registering Items

Register various types of items:

```java
public class MyItems {
    // Basic item
    public static final RegistrySupplier<Item> RUBY = MyRegistries.ITEMS.register("ruby",
        () -> new Item(new Item.Properties()));
    
    // Tool with custom properties
    public static final RegistrySupplier<SwordItem> RUBY_SWORD = MyRegistries.ITEMS.register("ruby_sword",
        () -> new SwordItem(
            MyTiers.RUBY,           // Custom tier
            3,                      // Attack damage
            -2.4F,                  // Attack speed
            new Item.Properties()
        ));
    
    // Food item
    public static final RegistrySupplier<Item> MAGIC_APPLE = MyRegistries.ITEMS.register("magic_apple",
        () -> new Item(new Item.Properties()
            .food(Foods.GOLDEN_APPLE)
            .stacksTo(16)));
    
    // Block item (automatically creates item for block)
    public static final RegistrySupplier<BlockItem> RUBY_BLOCK_ITEM = MyRegistries.ITEMS.register("ruby_block",
        () -> new BlockItem(MyBlocks.RUBY_BLOCK.get(), new Item.Properties()));
    
    // Custom item class
    public static final RegistrySupplier<MagicWandItem> MAGIC_WAND = MyRegistries.ITEMS.register("magic_wand",
        () -> new MagicWandItem(new Item.Properties()
            .stacksTo(1)
            .durability(500)));
    
    // Armor
    public static final RegistrySupplier<Item> RUBY_HELMET = MyRegistries.ITEMS.register("ruby_helmet",
        () -> new ArmorItem(MyArmorMaterials.RUBY, ArmorItem.Type.HELMET, new Item.Properties()));
    
    public static final RegistrySupplier<Item> RUBY_CHESTPLATE = MyRegistries.ITEMS.register("ruby_chestplate",
        () -> new ArmorItem(MyArmorMaterials.RUBY, ArmorItem.Type.CHESTPLATE, new Item.Properties()));
}
```

### Registering Blocks

Register blocks with various properties:

```java
public class MyBlocks {
    // Basic block
    public static final RegistrySupplier<Block> RUBY_BLOCK = MyRegistries.BLOCKS.register("ruby_block",
        () -> new Block(BlockBehaviour.Properties.of()
            .mapColor(MapColor.COLOR_RED)
            .strength(5.0F, 6.0F)
            .sound(SoundType.METAL)));
    
    // Ore block with experience drops
    public static final RegistrySupplier<Block> RUBY_ORE = MyRegistries.BLOCKS.register("ruby_ore",
        () -> new DropExperienceBlock(
            UniformInt.of(3, 7),    // XP drop range
            BlockBehaviour.Properties.of()
                .mapColor(MapColor.STONE)
                .strength(3.0F, 3.0F)
                .requiresCorrectToolForDrops()));
    
    // Custom block with special behavior
    public static final RegistrySupplier<MagicCraftingTableBlock> MAGIC_CRAFTING_TABLE = 
        MyRegistries.BLOCKS.register("magic_crafting_table",
            () -> new MagicCraftingTableBlock(BlockBehaviour.Properties.of()
                .mapColor(MapColor.WOOD)
                .strength(2.5F)
                .sound(SoundType.WOOD)));
    
    // Stairs and slabs
    public static final RegistrySupplier<StairBlock> RUBY_STAIRS = MyRegistries.BLOCKS.register("ruby_stairs",
        () -> new StairBlock(
            RUBY_BLOCK.get().defaultBlockState(),
            BlockBehaviour.Properties.copy(RUBY_BLOCK.get())));
    
    public static final RegistrySupplier<SlabBlock> RUBY_SLAB = MyRegistries.BLOCKS.register("ruby_slab",
        () -> new SlabBlock(BlockBehaviour.Properties.copy(RUBY_BLOCK.get())));
    
    // Redstone block
    public static final RegistrySupplier<PressurePlateBlock> MAGIC_PRESSURE_PLATE = 
        MyRegistries.BLOCKS.register("magic_pressure_plate",
            () -> new PressurePlateBlock(
                Sensitivity.MOBS,
                BlockBehaviour.Properties.of()
                    .mapColor(MapColor.COLOR_PURPLE)
                    .strength(0.5F)
                    .noCollission()
                    .noLootTable()));
}
```

### Registering Entities

Register custom entity types:

```java
public class MyEntities {
    // Custom mob
    public static final RegistrySupplier<EntityType<RubyGolemEntity>> RUBY_GOLEM = 
        MyRegistries.ENTITIES.register("ruby_golem",
            () -> EntityType.Builder.of(RubyGolemEntity::new, MobCategory.CREATURE)
                .sized(0.6F, 1.95F)  // Width, Height
                .clientTrackingRange(8)
                .updateInterval(3)
                .build("ruby_golem"));
    
    // Projectile
    public static final RegistrySupplier<EntityType<MagicBoltEntity>> MAGIC_BOLT = 
        MyRegistries.ENTITIES.register("magic_bolt",
            () -> EntityType.Builder.<MagicBoltEntity>of(MagicBoltEntity::new, MobCategory.MISC)
                .sized(0.25F, 0.25F)
                .clientTrackingRange(4)
                .updateInterval(10)
                .build("magic_bolt"));
    
    // Item entity (custom behavior)
    public static final RegistrySupplier<EntityType<MagicItemEntity>> MAGIC_ITEM =
        MyRegistries.ENTITIES.register("magic_item",
            () -> EntityType.Builder.<MagicItemEntity>of(MagicItemEntity::new, MobCategory.MISC)
                .sized(0.25F, 0.25F)
                .clientTrackingRange(6)
                .updateInterval(20)
                .build("magic_item"));
}
```

### Registering Sounds

Register custom sound events:

```java
public class MySounds {
    public static final RegistrySupplier<SoundEvent> MAGIC_CAST = MyRegistries.SOUNDS.register("magic_cast",
        () -> SoundEvent.createVariableRangeEvent(
            ResourceLocation.fromNamespaceAndPath(MyRegistries.MOD_ID, "magic_cast")));
    
    public static final RegistrySupplier<SoundEvent> RUBY_BREAK = MyRegistries.SOUNDS.register("ruby_break",
        () -> SoundEvent.createVariableRangeEvent(
            ResourceLocation.fromNamespaceAndPath(MyRegistries.MOD_ID, "ruby_break")));
    
    public static final RegistrySupplier<SoundEvent> MAGIC_AMBIENT = MyRegistries.SOUNDS.register("magic_ambient",
        () -> SoundEvent.createVariableRangeEvent(
            ResourceLocation.fromNamespaceAndPath(MyRegistries.MOD_ID, "magic_ambient")));
}
```

### Registering Creative Tabs

Register custom creative mode tabs:

```java
public class MyCreativeTabs {
    public static final RegistrySupplier<CreativeModeTab> MY_TAB = 
        MyRegistries.CREATIVE_TABS.register("my_tab", () -> CreativeModeTab.builder()
            .icon(() -> new ItemStack(MyItems.RUBY.get()))
            .title(Component.translatable("itemGroup.mymod.my_tab"))
            .displayItems((parameters, output) -> {
                // Items
                output.accept(MyItems.RUBY.get());
                output.accept(MyItems.RUBY_SWORD.get());
                output.accept(MyItems.MAGIC_WAND.get());
                
                // Blocks
                output.accept(MyBlocks.RUBY_BLOCK.get());
                output.accept(MyBlocks.RUBY_ORE.get());
                output.accept(MyBlocks.MAGIC_CRAFTING_TABLE.get());
                
                // Building blocks
                output.accept(MyBlocks.RUBY_STAIRS.get());
                output.accept(MyBlocks.RUBY_SLAB.get());
            })
            .build());
    
    public static final RegistrySupplier<CreativeModeTab> MAGIC_TAB =
        MyRegistries.CREATIVE_TABS.register("magic_tab", () -> CreativeModeTab.builder()
            .icon(() -> new ItemStack(MyItems.MAGIC_WAND.get()))
            .title(Component.translatable("itemGroup.mymod.magic_tab"))
            .displayItems((parameters, output) -> {
                // Magic items
                output.accept(MyItems.MAGIC_WAND.get());
                output.accept(MyItems.MAGIC_APPLE.get());
                
                // Magic blocks
                output.accept(MyBlocks.MAGIC_CRAFTING_TABLE.get());
                output.accept(MyBlocks.MAGIC_PRESSURE_PLATE.get());
            })
            .withTabFactory(MagicCreativeTab::new) // Custom tab class
            .build());
}
```

## Advanced Patterns

### Block and Item Pairs

Create blocks with their corresponding items automatically:

```java
public class BlockItemPairs {
    // Helper method for creating block-item pairs
    public static <T extends Block> RegistrySupplier<T> registerBlockWithItem(
            String name, 
            Supplier<T> blockSupplier) {
        
        // Register the block
        RegistrySupplier<T> block = MyRegistries.BLOCKS.register(name, blockSupplier);
        
        // Register the corresponding item
        MyRegistries.ITEMS.register(name, () -> new BlockItem(block.get(), new Item.Properties()));
        
        return block;
    }
    
    // Usage
    public static final RegistrySupplier<Block> DECORATED_RUBY_BLOCK = 
        registerBlockWithItem("decorated_ruby_block",
            () -> new Block(BlockBehaviour.Properties.copy(MyBlocks.RUBY_BLOCK.get())));
    
    public static final RegistrySupplier<Block> RUBY_FENCE = 
        registerBlockWithItem("ruby_fence",
            () -> new FenceBlock(BlockBehaviour.Properties.copy(MyBlocks.RUBY_BLOCK.get())));
    
    public static final RegistrySupplier<Block> RUBY_WALL = 
        registerBlockWithItem("ruby_wall",
            () -> new WallBlock(BlockBehaviour.Properties.copy(MyBlocks.RUBY_BLOCK.get())));
}
```

### Tool Tiers

Create custom tool tiers:

```java
public enum MyTiers implements Tier {
    RUBY(2, 500, 7.0F, 2.5F, 16, () -> Ingredient.of(MyItems.RUBY.get())),
    MAGIC(3, 750, 8.0F, 3.0F, 20, () -> Ingredient.of(MyItems.MAGIC_INGOT.get()));
    
    private final int level;
    private final int uses;
    private final float speed;
    private final float damage;
    private final int enchantmentValue;
    private final Supplier<Ingredient> repairIngredient;
    
    MyTiers(int level, int uses, float speed, float damage, int enchantmentValue, 
            Supplier<Ingredient> repairIngredient) {
        this.level = level;
        this.uses = uses;
        this.speed = speed;
        this.damage = damage;
        this.enchantmentValue = enchantmentValue;
        this.repairIngredient = repairIngredient;
    }
    
    @Override public int getUses() { return uses; }
    @Override public float getSpeed() { return speed; }
    @Override public float getAttackDamageBonus() { return damage; }
    @Override public int getLevel() { return level; }
    @Override public int getEnchantmentValue() { return enchantmentValue; }
    @Override public Ingredient getRepairIngredient() { return repairIngredient.get(); }
}
```

### Armor Materials

Create custom armor materials:

```java
public enum MyArmorMaterials implements ArmorMaterial {
    RUBY("ruby", 25, Map.of(
        EquipmentSlot.FEET, 2,
        EquipmentSlot.LEGS, 5,
        EquipmentSlot.CHEST, 7,
        EquipmentSlot.HEAD, 2
    ), 16, SoundEvents.ARMOR_EQUIP_DIAMOND, 1.0F, 0.0F, 
    () -> Ingredient.of(MyItems.RUBY.get())),
    
    MAGIC("magic", 30, Map.of(
        EquipmentSlot.FEET, 3,
        EquipmentSlot.LEGS, 6,
        EquipmentSlot.CHEST, 8,
        EquipmentSlot.HEAD, 3
    ), 20, MySounds.MAGIC_AMBIENT.get(), 2.0F, 0.1F,
    () -> Ingredient.of(MyItems.MAGIC_INGOT.get()));
    
    private final String name;
    private final int durabilityMultiplier;
    private final Map<EquipmentSlot, Integer> protectionAmounts;
    private final int enchantmentValue;
    private final SoundEvent equipSound;
    private final float toughness;
    private final float knockbackResistance;
    private final Supplier<Ingredient> repairIngredient;
    
    MyArmorMaterials(String name, int durabilityMultiplier, 
                     Map<EquipmentSlot, Integer> protectionAmounts,
                     int enchantmentValue, SoundEvent equipSound,
                     float toughness, float knockbackResistance,
                     Supplier<Ingredient> repairIngredient) {
        this.name = name;
        this.durabilityMultiplier = durabilityMultiplier;
        this.protectionAmounts = protectionAmounts;
        this.enchantmentValue = enchantmentValue;
        this.equipSound = equipSound;
        this.toughness = toughness;
        this.knockbackResistance = knockbackResistance;
        this.repairIngredient = repairIngredient;
    }
    
    @Override public int getDurabilityForSlot(EquipmentSlot slot) {
        return BASE_DURABILITY.get(slot) * durabilityMultiplier;
    }
    
    @Override public int getDefense(EquipmentSlot slot) {
        return protectionAmounts.get(slot);
    }
    
    @Override public int getEnchantmentValue() { return enchantmentValue; }
    @Override public SoundEvent getEquipSound() { return equipSound; }
    @Override public Ingredient getRepairIngredient() { return repairIngredient.get(); }
    @Override public String getName() { return MyRegistries.MOD_ID + ":" + name; }
    @Override public float getToughness() { return toughness; }
    @Override public float getKnockbackResistance() { return knockbackResistance; }
    
    private static final Map<EquipmentSlot, Integer> BASE_DURABILITY = Map.of(
        EquipmentSlot.FEET, 13,
        EquipmentSlot.LEGS, 15,
        EquipmentSlot.CHEST, 16,
        EquipmentSlot.HEAD, 11
    );
}
```

## Best Practices

### 1. Organization

Organize your registries logically:

```java
// Separate classes for different object types
public class MyItems { /* item registrations */ }
public class MyBlocks { /* block registrations */ }
public class MyEntities { /* entity registrations */ }

// Or group by feature
public class MagicRegistries { /* magic-related objects */ }
public class MiningRegistries { /* mining-related objects */ }
```

### 2. Naming Conventions

Use consistent naming:

```java
// Good - consistent naming
public static final RegistrySupplier<Item> RUBY_INGOT = ITEMS.register("ruby_ingot", ...);
public static final RegistrySupplier<Block> RUBY_BLOCK = BLOCKS.register("ruby_block", ...);
public static final RegistrySupplier<Item> RUBY_SWORD = ITEMS.register("ruby_sword", ...);

// Bad - inconsistent naming
public static final RegistrySupplier<Item> rubyIngot = ITEMS.register("RubyIngot", ...);
public static final RegistrySupplier<Block> Ruby_Block = BLOCKS.register("ruby-block", ...);
```

### 3. Lazy Initialization

Always use suppliers for object creation:

```java
// Good - lazy initialization
public static final RegistrySupplier<Item> MY_ITEM = ITEMS.register("my_item",
    () -> new MyItem(new Item.Properties()));

// Bad - immediate initialization (can cause issues)
private static final MyItem ITEM_INSTANCE = new MyItem(new Item.Properties());
public static final RegistrySupplier<Item> MY_ITEM = ITEMS.register("my_item",
    () -> ITEM_INSTANCE);
```

### 4. Resource Location Handling

Let the registry system handle resource locations:

```java
// Good - let the system handle namespacing
ITEMS.register("my_item", () -> new Item(...));

// Unnecessary - the system already uses your MOD_ID
ITEMS.register(ResourceLocation.fromNamespaceAndPath(MOD_ID, "my_item").toString(), ...);
```

## Migration from Platform-Specific Registration

### From Fabric Registration

```java
// Old Fabric way
public static final Item MY_ITEM = Registry.register(
    Registries.ITEM, 
    new Identifier("mymod", "my_item"), 
    new Item(new Item.Properties())
);

// New Amber way
public static final RegistrySupplier<Item> MY_ITEM = ITEMS.register("my_item",
    () -> new Item(new Item.Properties()));
```

### From Forge DeferredRegister

```java
// Old Forge way
public static final DeferredRegister<Item> ITEMS = 
    DeferredRegister.create(ForgeRegistries.ITEMS, MOD_ID);
public static final RegistryObject<Item> MY_ITEM = ITEMS.register("my_item",
    () -> new Item(new Item.Properties()));

// New Amber way (very similar!)
public static final DeferredRegister<Item> ITEMS = 
    DeferredRegister.create(MOD_ID, Registries.ITEM);
public static final RegistrySupplier<Item> MY_ITEM = ITEMS.register("my_item",
    () -> new Item(new Item.Properties()));
```

The migration from Forge is minimal - just change the registry reference and return type!

The registry system abstracts platform differences while providing a familiar API for developers coming from any platform.