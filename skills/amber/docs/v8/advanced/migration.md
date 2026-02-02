# Migration Guide

This guide helps you migrate existing mods to use Amber, whether you're coming from Fabric, Forge, or another modding library.

## From Fabric to Amber

### 1. Project Setup

Update your build.gradle to include Amber:

```gradle
// Remove Fabric API dependency if it's only for features Amber provides
// implementation "net.fabricmc.fabric-api:fabric-api:0.89.0+1.20.1"

// Add Amber dependencies
implementation "com.iamkaf:amber-fabric:8.3.2+1.21.10"
```

### 2. Mod Entry Point

Update your mod entry point:

```java
// Before (Fabric)
public class MyMod implements ModInitializer {
    @Override
    public void onInitialize() {
        // Your initialization code
    }
}

// After (with Amber)
public class MyModFabric implements ModInitializer {
    @Override
    public void onInitialize() {
        MyMod.init();
    }
}

// Common initialization class
public class MyMod {
    public static final String MOD_ID = "mymod";
    private static AmberModInfo modInfo;
    
    public static void init() {
        // Initialize with Amber
        modInfo = AmberInitializer.initialize(MOD_ID);
        
        // Your common initialization code
        registerItems();
        registerBlocks();
        registerEvents();
    }
    
    public static AmberModInfo getModInfo() {
        return modInfo;
    }
}
```

### 3. Registry System

Replace Fabric's registry with Amber's:

```java
// Before (Fabric)
public class MyItems {
    public static final Item MY_ITEM = Registry.register(
        Registries.ITEM,
        new Identifier("mymod", "my_item"),
        new Item(new Item.Settings())
    );
    
    public static void registerItems() {
        // Registration happens in static initialization
    }
}

// After (with Amber)
public class MyItems {
    public static final DeferredRegister<Item> ITEMS = 
        DeferredRegister.create("mymod", Registries.ITEM);
    
    public static final RegistrySupplier<Item> MY_ITEM = ITEMS.register("my_item",
        () -> new Item(new Item.Properties()));
    
    public static void registerItems() {
        ITEMS.register();
    }
}
```

### 4. Event System

Replace Fabric's event callbacks with Amber's events:

```java
// Before (Fabric)
UseBlockCallback.EVENT.register((player, world, hand, hitResult) -> {
    // Event handling
    return ActionResult.PASS;
});

// After (with Amber)
BlockEvents.BLOCK_INTERACT.register((player, level, hand, hitResult) -> {
    // Event handling
    return InteractionResult.PASS;
});
```

### 5. Configuration

Replace Fabric's configuration with Amber's:

```java
// Before (Fabric)
public class MyModConfig implements ConfigData {
    public boolean enableFeature = true;
    public int maxEnergy = 1000;
}

// After (with Amber)
public class MyModConfig {
    public boolean enableFeature = true;
    public int maxEnergy = 1000;
}

public class ConfigManager {
    private static JsonConfigManager<MyModConfig> configManager;
    private static MyModConfig config;
    
    public static void init() {
        configManager = new JsonConfigManager<>("mymod", new MyModConfig(), null, null);
        config = configManager.getConfig();
    }
    
    public static MyModConfig get() {
        return config;
    }
}
```

## From Forge to Amber

### 1. Project Setup

Update your build.gradle to include Amber:

```gradle
// Add Amber dependencies
implementation "com.iamkaf:amber-forge:8.3.2+1.21.10"
```

### 2. Mod Entry Point

Update your mod entry point:

```java
// Before (Forge)
@Mod("mymod")
public class MyMod {
    public MyMod() {
        // Your initialization code
    }
}

// After (with Amber)
@Mod("mymod")
public class MyModForge {
    public MyModForge() {
        MyMod.init();
    }
}

// Common initialization class
public class MyMod {
    public static final String MOD_ID = "mymod";
    
    public static void init() {
        // Initialize with Amber
        AmberInitializer.initialize(MOD_ID);
        
        // Your common initialization code
        registerItems();
        registerBlocks();
        registerEvents();
    }
}
```

### 3. Registry System

Replace Forge's registry with Amber's:

```java
// Before (Forge)
public class MyItems {
    public static final RegistryObject<Item> MY_ITEM = ITEMS.register("my_item",
        () -> new Item(new Item.Properties()));
    
    public static final DeferredRegister<Item> ITEMS = 
        DeferredRegister.create(ForgeRegistries.ITEMS, "mymod");
}

// After (with Amber)
public class MyItems {
    public static final DeferredRegister<Item> ITEMS = 
        DeferredRegister.create("mymod", Registries.ITEM);
    
    public static final RegistrySupplier<Item> MY_ITEM = ITEMS.register("my_item",
        () -> new Item(new Item.Properties()));
}
```

### 4. Event System

Replace Forge's event system with Amber's:

```java
// Before (Forge)
@SubscribeEvent
public void onBlockRightClick(PlayerInteractEvent.RightClickBlock event) {
    // Event handling
}

// After (with Amber)
BlockEvents.BLOCK_INTERACT.register((player, level, hand, hitResult) -> {
    // Event handling
    return InteractionResult.PASS;
});
```

### 5. Configuration

Replace Forge's configuration with Amber's:

```java
// Before (Forge)
public class MyModConfig {
    public static final ForgeConfigSpec.Builder BUILDER = new ForgeConfigSpec.Builder();
    public static final ForgeConfigSpec.BooleanValue ENABLE_FEATURE = 
        BUILDER.define("enableFeature", true);
    public static final ForgeConfigSpec.IntValue MAX_ENERGY = 
        BUILDER.define("maxEnergy", 1000);
    
    public static final ForgeConfigSpec SPEC = BUILDER.build();
}

// After (with Amber)
public class MyModConfig {
    public boolean enableFeature = true;
    public int maxEnergy = 1000;
}

public class ConfigManager {
    private static JsonConfigManager<MyModConfig> configManager;
    private static MyModConfig config;
    
    public static void init() {
        configManager = new JsonConfigManager<>("mymod", new MyModConfig(), null, null);
        config = configManager.getConfig();
    }
}
```

## From NeoForge to Amber

### 1. Project Setup

Update your build.gradle to include Amber:

```gradle
// Add Amber dependencies
implementation "com.iamkaf:amber-neoforge:8.3.2+1.21.10"
```

### 2. Mod Entry Point

Update your mod entry point:

```java
// Before (NeoForge)
@Mod("mymod")
public class MyMod {
    public MyMod() {
        // Your initialization code
    }
}

// After (with Amber)
@Mod("mymod")
public class MyModNeoForge {
    public MyModNeoForge() {
        MyMod.init();
    }
}

// Common initialization class
public class MyMod {
    public static final String MOD_ID = "mymod";
    
    public static void init() {
        // Initialize with Amber
        AmberInitializer.initialize(MOD_ID);
        
        // Your common initialization code
        registerItems();
        registerBlocks();
        registerEvents();
    }
}
```

## Common Migration Patterns

### 1. Platform Detection

Replace platform-specific code with Amber's platform API:

```java
// Before
boolean isFabric = FabricLoader.getInstance().isModLoaded("fabric");
boolean isForge = FMLLoader.getLoadingModList().getModFileById("forge") != null;

// After
boolean isFabric = Platform.isFabric();
boolean isForge = Platform.isForge();
boolean isNeoForge = Platform.isNeoForge();
```

### 2. Path Management

Replace platform-specific path access with Amber's path API:

```java
// Before
Path configDir = FabricLoader.getInstance().getConfigDir(); // Fabric
Path configDir = FMLPaths.CONFIGDIR.get(); // Forge

// After
Path configDir = Platform.getConfigFolder();
Path gameDir = Platform.getGameFolder();
Path modsDir = Platform.getModsFolder();
```

### 3. Item Registration

Replace platform-specific item registration:

```java
// Before (Fabric)
public static final Item MY_ITEM = Registry.register(
    Registries.ITEM,
    new Identifier("mymod", "my_item"),
    new Item(new Item.Settings())
);

// Before (Forge)
public static final RegistryObject<Item> MY_ITEM = ITEMS.register("my_item",
    () -> new Item(new Item.Properties()));

// After (with Amber)
public static final RegistrySupplier<Item> MY_ITEM = ITEMS.register("my_item",
    () -> new Item(new Item.Properties()));
```

### 4. Event Registration

Replace platform-specific event registration:

```java
// Before (Fabric)
UseBlockCallback.EVENT.register((player, world, hand, hitResult) -> {
    return ActionResult.PASS;
});

// Before (Forge)
@SubscribeEvent
public void onBlockRightClick(PlayerInteractEvent.RightClickBlock event) {
    // Event handling
}

// After (with Amber)
BlockEvents.BLOCK_INTERACT.register((player, level, hand, hitResult) -> {
    return InteractionResult.PASS;
});
```

## Migration Checklist

### 1. Before Migration

- [ ] Backup your existing mod
- [ ] Document current mod features
- [ ] Identify platform-specific code
- [ ] Test current mod functionality

### 2. During Migration

- [ ] Add Amber dependencies
- [ ] Create common initialization class
- [ ] Migrate registry system
- [ ] Migrate event system
- [ ] Migrate configuration system
- [ ] Replace platform-specific APIs with Amber APIs
- [ ] Update platform-specific entry points

### 3. After Migration

- [ ] Test on all target platforms
- [ ] Verify all features work correctly
- [ ] Update documentation
- [ ] Test compatibility with other mods
- [ ] Performance test

## Troubleshooting

### 1. Registration Issues

**Problem**: Items/blocks not registering
**Solution**: Make sure you're calling `register()` on your DeferredRegister instances

```java
// Make sure to call this during initialization
ITEMS.register();
BLOCKS.register();
```

### 2. Event Issues

**Problem**: Events not firing
**Solution**: Make sure you're registering events after Amber initialization

```java
public static void init() {
    // Initialize Amber first
    AmberInitializer.initialize(MOD_ID);
    
    // Then register events
    BlockEvents.BLOCK_INTERACT.register(...);
}
```

### 3. Configuration Issues

**Problem**: Configuration not loading
**Solution**: Make sure you're calling `loadConfig()` or accessing the config

```java
public static void init() {
    // This loads the config
    MyModConfig config = ConfigManager.get();
}
```

### 4. Platform Detection Issues

**Problem**: Platform detection not working
**Solution**: Make sure you're using the correct Amber dependency for your platform

```gradle
// Fabric
implementation "com.iamkaf:amber-fabric:8.3.2+1.21.10"

// Forge
implementation "com.iamkaf:amber-forge:8.3.2+1.21.10"

// NeoForge
implementation "com.iamkaf:amber-neoforge:8.3.2+1.21.10"
```

## Getting Help

If you encounter issues during migration:

1. **Check the documentation**: Review the relevant Amber documentation
2. **Search existing issues**: Check GitHub for similar issues
3. **Ask for help**: Join the Amber Discord or GitHub Discussions
4. **Create a minimal example**: Create a minimal mod that reproduces the issue
5. **Include platform information**: Specify which platform you're targeting

Migration can be complex, but Amber's unified APIs make it much easier to create cross-platform mods. Take it step by step, and don't hesitate to ask for help when needed.