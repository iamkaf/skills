# Getting Started with Amber

This guide will help you set up Amber in your Minecraft mod project and demonstrate basic usage patterns.

## Prerequisites

- **Java 21** or higher
- **Minecraft 1.21.11** (or supported version)
- **Gradle** build system
- Basic knowledge of Minecraft modding

## Project Setup

### 1. Add Amber Repository

Add the Amber repository to your `build.gradle`:

```gradle
repositories {
    // Other repositories...
    maven {
        name = 'Amber Maven'
        url = 'https://raw.githubusercontent.com/iamkaf/modresources/main/maven/'
    }
}
```

### 2. Add Dependencies

Choose the appropriate dependencies for your target platforms:

#### For Multiloader Projects

```gradle
// In your common module
dependencies {
    implementation "com.iamkaf:amber-common:9.0.2+1.21.11"
}

// In your fabric module  
dependencies {
    implementation "com.iamkaf:amber-fabric:9.0.2+1.21.11"
}

// In your forge module
dependencies {
    implementation "com.iamkaf:amber-forge:9.0.2+1.21.11"
}

// In your neoforge module
dependencies {
    implementation "com.iamkaf:amber-neoforge:9.0.2+1.21.11"
}
```

#### For Single-Platform Projects

```gradle
dependencies {
    // Choose one based on your platform
    implementation "com.iamkaf:amber-fabric:9.0.2+1.21.11"
    // OR
    implementation "com.iamkaf:amber-forge:9.0.2+1.21.11"
    // OR  
    implementation "com.iamkaf:amber-neoforge:9.0.2+1.21.11"
}
```

## Basic Mod Setup

### 1. Main Mod Class

Create your main mod class that initializes with Amber:

```java
package com.example.mymod;

import com.iamkaf.amber.api.core.v2.AmberInitializer;

public class MyMod {
    public static final String MOD_ID = "mymod";
    
    // Call this from your platform-specific mod initializer
    public static void init() {
        // Initialize with Amber - automatically detects mod name and version
        AmberInitializer.initialize(MOD_ID);
        
        System.out.println("MyMod initialized with Amber!");
        
        // Initialize your mod features
        setupRegistries();
        setupEvents();
    }
    
    private static void setupRegistries() {
        // Registry setup (covered in registry documentation)
    }
    
    private static void setupEvents() {
        // Event handling (covered in events documentation)
    }
}
```

### 2. Platform-Specific Entry Points

#### Fabric Entry Point

```java
// src/main/java/.../MyModFabric.java
package com.example.mymod;

import net.fabricmc.api.ModInitializer;

public class MyModFabric implements ModInitializer {
    @Override
    public void onInitialize() {
        MyMod.init();
    }
}
```

#### Forge Entry Point

```java
// src/main/java/.../MyModForge.java
package com.example.mymod;

import net.minecraftforge.fml.common.Mod;

@Mod(MyMod.MOD_ID)
public class MyModForge {
    public MyModForge() {
        MyMod.init();
    }
}
```

#### NeoForge Entry Point

```java
// src/main/java/.../MyModNeoForge.java
package com.example.mymod;

import net.neoforged.fml.common.Mod;

@Mod(MyMod.MOD_ID)
public class MyModNeoForge {
    public MyModNeoForge() {
        MyMod.init();
    }
}
```

## Your First Amber Features

### 1. Platform Information

Use Amber's platform abstraction to get information about the environment:

```java
import com.iamkaf.amber.api.platform.v1.Platform;

public class PlatformExample {
    public static void printPlatformInfo() {
        System.out.println("Platform: " + Platform.getPlatformName());
        System.out.println("Is Client: " + Platform.isClient());
        System.out.println("Is Server: " + Platform.isServer());
        System.out.println("Is Development: " + Platform.isDevelopmentEnvironment());
        
        // Get platform-specific paths
        System.out.println("Game Directory: " + Platform.getGameFolder());
        System.out.println("Config Directory: " + Platform.getConfigFolder());
    }
}
```

### 2. Simple Configuration

Create a configuration system for your mod:

```java
import com.iamkaf.amber.api.config.v1.JsonConfigManager;

public class MyModConfig {
    // Configuration fields
    public int maxEnergy = 1000;
    public boolean enableFeature = true;
    public double multiplier = 1.5;
    
    private static MyModConfig instance;
    private static JsonConfigManager<MyModConfig> configManager;
    
    public static void init() {
        configManager = new JsonConfigManager<>(
            "mymod",           // Mod ID
            new MyModConfig(), // Initial config instance
            null,              // Config path (null = default)
            null               // Header comment (optional)
        );
        
        instance = configManager.getConfig();
        System.out.println("Config loaded: maxEnergy = " + instance.maxEnergy);
    }
    
    public static MyModConfig get() {
        return instance;
    }
    
    public static void save() {
        configManager.saveConfig();
    }
}
```

### 3. Simple Item Registration

Register items using Amber's registry system:

```java
import com.iamkaf.amber.api.registry.v1.DeferredRegister;
import com.iamkaf.amber.api.registry.v1.RegistrySupplier;
import net.minecraft.core.registries.Registries;
import net.minecraft.world.item.Item;

public class MyItems {
    // Create a deferred register for items
    public static final DeferredRegister<Item> ITEMS = 
        DeferredRegister.create(MyMod.MOD_ID, Registries.ITEM);
    
    // Register your items
    public static final RegistrySupplier<Item> MY_ITEM = ITEMS.register("my_item", 
        () -> new Item(new Item.Properties()));
    
    public static final RegistrySupplier<Item> SPECIAL_TOOL = ITEMS.register("special_tool",
        () -> new MySpecialTool(new Item.Properties().durability(500)));
    
    // Call this during mod initialization
    public static void init() {
        ITEMS.register(); // Register all items
    }
}
```

### 4. Event Handling

Set up event handlers using Amber's event system:

```java
import com.iamkaf.amber.api.event.v1.events.common.PlayerEvents;

public class MyEventHandlers {
    public static void init() {
        // Handle player interaction with entities
        PlayerEvents.ENTITY_INTERACT.register((player, level, hand, entity) -> {
            if (player.getItemInHand(hand).is(MyItems.SPECIAL_TOOL.get())) {
                // Special interaction logic
                System.out.println("Player used special tool on: " + entity.getName().getString());
                return InteractionResult.SUCCESS; // Cancel default interaction
            }
            return InteractionResult.PASS; // Allow default interaction
        });
    }
}
```

### 5. Client-Side Features

Add client-side functionality:

```java
import com.iamkaf.amber.api.common.client.CommonClientUtils;
import net.minecraft.client.gui.GuiGraphics;

public class MyClientFeatures {
    public static void init() {
        // Register HUD renderer
        setupHUD();
        
        // Register keybinds (covered in keybinds documentation)
        setupKeybinds();
    }
    
    private static void setupHUD() {
        // This would typically be registered through Amber's event system
        // Implementation depends on your specific needs
    }
    
    public static void renderHUD(GuiGraphics graphics, float partialTick) {
        if (CommonClientUtils.shouldShowHUD()) {
            // Render your HUD elements
            graphics.drawString(
                Minecraft.getInstance().font,
                "Energy: " + getCurrentEnergy(),
                10, 10,
                0xFFFFFF
            );
        }
    }
    
    private static int getCurrentEnergy() {
        // Return current energy value
        return 100;
    }
}
```

## Complete Example

Here's a complete minimal mod using Amber:

```java
// MyMod.java - Main mod class
public class MyMod {
    public static final String MOD_ID = "mymod";
    
    public static void init() {
        // Initialize with Amber - automatically detects mod name and version
        AmberInitializer.initialize(MOD_ID);
        
        // Initialize configuration
        MyModConfig.init();
        
        // Initialize registries
        MyItems.init();
        
        // Initialize events
        MyEventHandlers.init();
        
        System.out.println("MyMod initialized successfully!");
    }
}

// MyModConfig.java - Configuration
public class MyModConfig {
    public int maxItems = 64;
    public boolean enableSpecialFeature = true;
    
    private static MyModConfig instance;
    private static JsonConfigManager<MyModConfig> manager;
    
    public static void init() {
        manager = new JsonConfigManager<>("mymod", new MyModConfig(), null, null);
        instance = manager.getConfig();
    }
    
    public static MyModConfig get() { return instance; }
}

// MyItems.java - Item registration
public class MyItems {
    public static final DeferredRegister<Item> ITEMS = 
        DeferredRegister.create(MyMod.MOD_ID, Registries.ITEM);
    
    public static final RegistrySupplier<Item> MAGIC_WAND = ITEMS.register("magic_wand",
        () -> new Item(new Item.Properties().stacksTo(1)));
    
    public static void init() {
        ITEMS.register();
    }
}

// MyEventHandlers.java - Event handling
public class MyEventHandlers {
    public static void init() {
        PlayerEvents.ENTITY_INTERACT.register((player, level, hand, entity) -> {
            if (player.getItemInHand(hand).is(MyItems.MAGIC_WAND.get())) {
                // Cast magic spell
                return InteractionResult.SUCCESS;
            }
            return InteractionResult.PASS;
        });
    }
}
```

## Next Steps

Now that you have a basic Amber mod set up, explore these areas:

1. **[Event System](../systems/events)** - Handle game events effectively  
2. **[Commands](../systems/commands)** - Create custom commands
3. **[Registry System](../systems/registry)** - Advanced registration patterns
4. **[Networking](../systems/networking)** - Client-server communication

## Common Issues

### Build Issues

If you encounter build issues:

1. **Check Java version**: Ensure you're using Java 21+
2. **Verify Minecraft version**: Make sure all dependencies match your target version
3. **Clean build**: Run `./gradlew clean build`

### Runtime Issues

If your mod doesn't load:

1. **Check mod initialization**: Ensure `AmberInitializer.initialize()` is called
2. **Verify dependencies**: Make sure Amber is properly included
3. **Check logs**: Look for error messages in the game logs

### Getting Help

- Check the [troubleshooting section](../../README.md#troubleshooting) in the main README
- Look at the [example implementations](../../common/src/main/java/com/iamkaf/amber/api/) in the Amber source code
- Review the specific feature documentation for detailed usage patterns