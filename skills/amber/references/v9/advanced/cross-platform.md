# Cross-Platform Development

Amber is designed to make cross-platform mod development easier by providing unified APIs that work across Fabric, Forge, and NeoForge. This guide covers best practices and considerations for developing mods that work consistently across all platforms.

## Platform Differences

### Mod Loading

Each mod loader has different entry points and initialization patterns:

```java
// Fabric entry point
public class MyModFabric implements ModInitializer {
    @Override
    public void onInitialize() {
        MyMod.init();
    }
}

// Forge entry point
@Mod(MyMod.MOD_ID)
public class MyModForge {
    public MyModForge() {
        MyMod.init();
    }
}

// NeoForge entry point
@Mod(MyMod.MOD_ID)
public class MyModNeoForge {
    public MyModNeoForge() {
        MyMod.init();
    }
}

// Common initialization
public class MyMod {
    public static final String MOD_ID = "mymod";
    
    public static void init() {
        // Initialize with Amber
        AmberInitializer.initialize(MOD_ID);
        
        // Common initialization code
        registerItems();
        registerBlocks();
        registerEvents();
    }
}
```

### Event Registration

Events are registered differently on each platform:

```java
// Fabric event registration
public class MyModFabric implements ModInitializer {
    @Override
    public void onInitialize() {
        UseBlockCallback.EVENT.register((player, world, hand, hitResult) -> {
            // Event handling
            return ActionResult.PASS;
        });
    }
}

// Forge event registration
@Mod(MyMod.MOD_ID)
public class MyModForge {
    public MyModForge() {
        MinecraftForge.EVENT_BUS.register(this);
    }
    
    @SubscribeEvent
    public void onBlockRightClick(PlayerInteractEvent.RightClickBlock event) {
        // Event handling
    }
}

// NeoForge event registration (similar to Forge)
@Mod(MyMod.MOD_ID)
public class MyModNeoForge {
    public MyModNeoForge() {
        NeoForge.EVENT_BUS.register(this);
    }
    
    @SubscribeEvent
    public void onBlockRightClick(PlayerInteractEvent.RightClickBlock event) {
        // Event handling
    }
}

// Cross-platform with Amber
public class MyMod {
    public static void init() {
        // Amber events work on all platforms
        BlockEvents.BLOCK_INTERACT.register((player, level, hand, hitResult) -> {
            // Event handling
            return InteractionResult.PASS;
        });
    }
}
```

## Platform Abstraction Strategies

### 1. Use Amber APIs First

Always prefer Amber's unified APIs over platform-specific ones:

```java
// Good - Use Amber's platform API
boolean isClient = Platform.isClient();
Path configDir = Platform.getConfigFolder();
boolean isModLoaded = Platform.isModLoaded("fabric-api");

// Avoid - Platform-specific code
// boolean isClient = FabricLoader.getInstance().isDevelopmentEnvironment(); // Fabric only
// Path configDir = FMLPaths.CONFIGDIR.get(); // Forge only
```

### 2. Conditional Platform Code

When platform-specific code is unavoidable, use platform checks:

```java
public class PlatformSpecificCode {
    public static void doPlatformSpecificThing() {
        if (Platform.isFabric()) {
            // Fabric-specific code
            doFabricThing();
        } else if (Platform.isForge()) {
            // Forge-specific code
            doForgeThing();
        } else if (Platform.isNeoForge()) {
            // NeoForge-specific code
            doNeoForgeThing();
        }
    }
    
    // For client-side only code
    public static void doClientThing() {
        if (Platform.isClient()) {
            // Client-specific initialization
            ClientInit.init();
        }
    }
}
```

### 3. Service-Based Architecture

Use Amber's service system for platform-specific implementations:

```java
// Define service interface
public interface MyModService {
    void doPlatformSpecificThing();
    boolean isFeatureSupported();
}

// Platform-specific implementations
public class FabricMyModService implements MyModService {
    @Override
    public void doPlatformSpecificThing() {
        // Fabric implementation
    }
    
    @Override
    public boolean isFeatureSupported() {
        return true;
    }
}

public class ForgeMyModService implements MyModService {
    @Override
    public void doPlatformSpecificThing() {
        // Forge implementation
    }
    
    @Override
    public boolean isFeatureSupported() {
        return false;
    }
}

// Common usage
public class MyModService {
    private static MyModService instance;
    
    public static MyModService get() {
        if (instance == null) {
            // Initialize platform-specific service
            if (Platform.isFabric()) {
                instance = new FabricMyModService();
            } else if (Platform.isForge()) {
                instance = new ForgeMyModService();
            } else if (Platform.isNeoForge()) {
                instance = new NeoForgeMyModService();
            }
        }
        return instance;
    }
}
```

## Cross-Platform Best Practices

### 1. Organize by Feature, Not Platform

Organize your code by feature rather than platform:

```
Good:
src/main/java/mymod/
├── common/
│   ├── items/
│   ├── blocks/
│   ├── events/
│   └── networking/
├── fabric/
│   └── MyModFabric.java
├── forge/
│   └── MyModForge.java
└── neoforge/
    └── MyModNeoForge.java

Bad:
src/main/java/mymod/
├── fabric/
│   ├── items/
│   ├── blocks/
│   └── events/
├── forge/
│   ├── items/
│   ├── blocks/
│   └── events/
└── neoforge/
    ├── items/
    ├── blocks/
    └── events/
```

### 2. Minimize Platform-Specific Code

Keep platform-specific code to a minimum:

```java
// Good - Minimal platform code
public class MyMod {
    public static void init() {
        // Common initialization
        registerItems();
        registerBlocks();
        registerEvents();
        
        // Only necessary platform-specific code
        if (Platform.isFabric()) {
            registerFabricNetworking();
        }
    }
}

// Bad - Lots of platform code
public class MyMod {
    public static void init() {
        if (Platform.isFabric()) {
            registerFabricItems();
            registerFabricBlocks();
            registerFabricEvents();
            registerFabricNetworking();
        } else if (Platform.isForge()) {
            registerForgeItems();
            registerForgeBlocks();
            registerForgeEvents();
            registerForgeNetworking();
        }
    }
}
```

### 3. Use Abstract Classes for Platform Differences

When you have small platform differences, use abstract classes:

```java
public abstract class MyAbstractBlock extends Block {
    public MyAbstractBlock(Properties properties) {
        super(properties);
    }
    
    // Common behavior
    @Override
    public void onPlace(Level level, BlockPos pos, BlockState state, LivingEntity placer, ItemStack stack) {
        super.onPlace(level, pos, state, placer, stack);
        // Common on-place logic
    }
    
    // Platform-specific behavior
    protected abstract void doPlatformSpecificThing(Level level, BlockPos pos);
}

// Platform-specific implementations
public class MyModBlock extends MyAbstractBlock {
    public MyModBlock(Properties properties) {
        super(properties);
    }
    
    @Override
    protected void doPlatformSpecificThing(Level level, BlockPos pos) {
        // Common implementation works on all platforms
    }
}
```

### 4. Test on All Platforms

Test your mod on all supported platforms:

```java
public class PlatformTests {
    public static void runTests() {
        testPlatformDetection();
        testEventFiring();
        testNetworking();
        testRegistration();
        
        String platform = Platform.getPlatformName();
        System.out.println("Tests completed on " + platform);
    }
    
    private static void testPlatformDetection() {
        assert Platform.getPlatformName() != null;
        assert Platform.isClient() || Platform.isServer();
    }
    
    private static void testEventFiring() {
        // Test that events fire correctly
        // Implementation depends on your testing framework
    }
}
```

## Common Cross-Platform Challenges

### 1. Networking

Networking is one of the most challenging areas for cross-platform development:

```java
// Amber provides unified networking
public class MyNetworking {
    public static final NetworkChannel CHANNEL = NetworkChannel.create(
        ResourceLocation.fromNamespaceAndPath("mymod", "main")
    );
    
    public static void init() {
        // Register packets
        CHANNEL.register(MyPacket.class, MyPacket::encode, MyPacket::decode, MyPacket::handle);
    }
}

// Without Amber, you'd need different implementations for each platform
// Fabric: use PacketByteBufs and ServerPlayNetworking
// Forge: use ChannelBuilder and SimpleChannel (different APIs for different versions)
// NeoForge: similar to Forge but with NeoForge's networking system
```

Amber's networking implementation handles the complexities of different Forge versions:

- **Forge 60.0.0+**: Uses the new ChannelBuilder API with VersionTest
- **Forge 47.x-59.x**: Uses the traditional SimpleChannel API
- **Fabric**: Uses Fabric's networking API
- **NeoForge**: Uses NeoForge's payload system

All implementations ensure thread-safe packet handling and proper network transmission.

### 2. Configuration

Configuration systems vary between platforms:

```java
// Amber provides unified configuration
public class MyModConfig {
    private static JsonConfigManager<MyModConfig> manager;
    
    public static void init() {
        manager = new JsonConfigManager<>("mymod", new MyModConfig(), null, null);
    }
    
    public static MyModConfig get() {
        return manager.getConfig();
    }
}

// Without Amber, you'd need different implementations
// Fabric: use FabricLoader.getConfigDir() and manual JSON handling
// Forge: use ForgeConfigSpec
// NeoForge: similar to Forge but with NeoForge's configuration system
```

### 3. Creative Tabs

Creative tab registration differs between platforms:

```java
// Amber provides unified creative tab registration
public static final RegistrySupplier<CreativeModeTab> MY_TAB = 
    DeferredRegister.create("mymod", Registries.CREATIVE_MODE_TAB)
        .register("my_tab", () -> CreativeModeTab.builder()
            .icon(() -> new ItemStack(MyItems.MY_ITEM))
            .displayItems((params, output) -> {
                output.accept(MyItems.MY_ITEM.get());
            })
            .build());

// Without Amber, you'd need different implementations
// Fabric: use FabricItemGroupBuilder
// Forge: use CreativeModeTab.Builder
// NeoForge: similar to Forge but with NeoForge's creative tab system
```

## Migration Guide

### From Single-Platform to Cross-Platform

If you're migrating an existing mod to be cross-platform:

1. **Separate Platform-Specific Code**
   ```java
   // Before
   public class MyMod implements ModInitializer {
       @Override
       public void onInitialize() {
           // All initialization code
       }
   }
   
   // After
   public class MyMod {
       public static void init() {
           // Common initialization code
       }
   }
   
   // Platform-specific entry points
   public class MyModFabric implements ModInitializer {
       @Override
       public void onInitialize() {
           MyMod.init();
       }
   }
   ```

2. **Replace Platform APIs with Amber APIs**
   ```java
   // Before
   if (FabricLoader.getInstance().isModLoaded("fabric-api")) {
       // Do something
   }
   
   // After
   if (Platform.isModLoaded("fabric-api")) {
       // Do something
   }
   ```

3. **Use Unified Event System**
   ```java
   // Before
   UseBlockCallback.EVENT.register((player, world, hand, hitResult) -> {
       // Event handling
   });
   
   // After
   BlockEvents.BLOCK_INTERACT.register((player, level, hand, hitResult) -> {
       // Event handling
   });
   ```

4. **Test on All Platforms**
   - Test your mod on Fabric, Forge, and NeoForge
   - Ensure all features work correctly on each platform
   - Handle platform-specific edge cases

## Platform-Specific Tips

### Fabric Tips

- Fabric has a more modular architecture
- Use Fabric API for additional functionality
- Be aware of Fabric's different entity spawn system

### Forge Tips

- Forge has a more monolithic architecture
- Use Forge's capabilities system for custom functionality
- Be aware of Forge's different event firing order
- **Networking**: Forge 60.0.0+ uses a new ChannelBuilder API that differs significantly from older versions
- **Version Compatibility**: Amber handles Forge version differences automatically

### NeoForge Tips

- NeoForge is similar to Forge but with modernized APIs
- Use NeoForge's new registry system
- Be aware of NeoForge's different networking system

## Conclusion

Cross-platform mod development with Amber requires careful planning and organization, but the benefits are significant:

- **Wider Audience**: Your mod works on more platforms
- **Easier Maintenance**: Less code to maintain across platforms
- **Future-Proof**: Your mod is more likely to work with future versions

By following these best practices and using Amber's unified APIs, you can create robust cross-platform mods with minimal platform-specific code.