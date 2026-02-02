---
layout: home

hero:
  name: Amber
  text: A comprehensive multiloader library for Minecraft mod development
  tagline: Write once, run everywhere - Unified APIs for Fabric, Forge, and NeoForge
  image:
    src: /icon.png
    alt: Amber
  actions:
    - theme: brand
      text: Get Started
      link: /v9/guide/getting-started
    - theme: alt
      text: View on Modrinth
      link: https://modrinth.com/mod/amber
    - theme: alt
      text: View on CurseForge
      link: https://www.curseforge.com/minecraft/mc-mods/amber-lib
    - theme: alt
      text: View on GitHub
      link: https://github.com/iamkaf/amber

features:
  - icon: 🌐
    title: Cross-Platform Compatibility
    details: Unified APIs that work identically across Fabric, Forge, and NeoForge platforms
  - icon: 🔧
    title: Core Systems
    details: Registry, Events, Configuration, and Networking systems designed for modern Minecraft modding
  - icon: 🎮
    title: Game Integration
    details: Commands, HUD rendering, keybinds, and sound system utilities
  - icon: 🛠️
    title: Developer Utilities
    details: Item helpers, level utilities, player feedback, and math utilities
  - icon: 📦
    title: Modern Architecture
    details: Service-based architecture with platform abstraction handles differences automatically
  - icon: 🚀
    title: Easy to Use
    details: Simple, intuitive APIs that get you modding faster with less boilerplate

---

## What is Amber?

Amber is a powerful foundation library that provides unified APIs for common modding tasks across **Fabric**, **Forge**, and **NeoForge** platforms. Built with cross-platform compatibility in mind, Amber eliminates the complexity of managing platform-specific code while offering modern, easy-to-use APIs for Minecraft mod development.

## Why Amber?

### 🎯 Write Once, Run Everywhere
With Amber's unified APIs, you can write your mod once and it will work on all major mod loaders without platform-specific code.

### 🚀 Modern Design
Built for Minecraft 1.21.11 with modern Java practices, Amber provides clean, intuitive APIs that reduce boilerplate and speed up development.

### 🔧 Comprehensive Toolkit
From registry management to networking, events to configuration, Amber provides all the tools you need for modern mod development.

### 🌟 Community Driven
Open source and community-focused, Amber is designed to evolve with the needs of mod developers.

## Quick Start

### 1. Add Amber to Your Project

```gradle
repositories {
    maven { url = 'https://raw.githubusercontent.com/iamkaf/modresources/main/maven/' }
}

dependencies {
    implementation "com.iamkaf:amber-common:9.0.2+1.21.11"
    // Platform-specific dependencies
    implementation "com.iamkaf:amber-fabric:9.0.2+1.21.11"
    // OR implementation "com.iamkaf:amber-forge:9.0.2+1.21.11"
    // OR implementation "com.iamkaf:amber-neoforge:9.0.2+1.21.11"
}
```

### 2. Initialize Amber

```java
public class YourMod {
    public static final String MOD_ID = "yourmod";
    
    public static void init() {
        // Initialize with Amber - automatically detects mod name and version
        AmberInitializer.initialize(MOD_ID);
        
        // Your mod initialization code here
        System.out.println("YourMod initialized with Amber!");
    }
}
```

### 3. Start Building

```java
// Register items
public static final DeferredRegister<Item> ITEMS = 
    DeferredRegister.create(MOD_ID, Registries.ITEM);

public static final RegistrySupplier<Item> MY_ITEM = ITEMS.register("my_item", 
    () -> new Item(new Item.Properties()));

// Handle events
PlayerEvents.ENTITY_INTERACT.register((player, level, hand, entity) -> {
    // Your interaction logic here
    return InteractionResult.PASS;
});
```

## Core Features

### 🌐 Platform Abstraction
- **Environment Detection**: Automatically detect client/server environments
- **Platform Information**: Get details about the current mod loader
- **Path Management**: Cross-platform access to game directories

### 📋 Registry System
- **Deferred Registration**: Queue objects for registration at the right time
- **Cross-Platform**: Works identically on all mod loaders
- **Type Safety**: Full type safety for registered objects

### 🎪 Event System
- **Fabric-Inspired**: Clean, familiar event API
- **Cross-Platform Events**: Events work consistently across platforms
- **Performance Optimized**: Efficient event dispatching

### 🌐 Networking
- **Type-Safe Packets**: Compile-time safety for network messages
- **Simple API**: Easy to send and receive packets
- **Platform Abstracted**: Same API works on all platforms

### ⚙️ Configuration
- **JSON-Based**: Simple JSON configuration files
- **Automatic Serialization**: No manual serialization needed
- **Hot Reloading**: Runtime configuration updates

## Documentation

- **[Getting Started](guide/getting-started)** - Set up your first Amber mod
- **[API Reference](api/core)** - Detailed API documentation
- **[Examples](systems/events)** - Practical code examples
- **[Systems](systems/)** - Core system documentation
  - **[Creative Mode Tabs](systems/creative-tabs)** - Custom creative tabs
  - **[Events](systems/events)** - Event handling
  - **[Commands](systems/commands)** - Command registration
  - **[Configuration](systems/configuration)** - JSON configuration
  - **[Networking](systems/networking)** - Network communication
  - **[Registry](systems/registry)** - Object registration
- **[Best Practices](advanced/best-practices)** - Tips for effective modding

## Version Information

- **Current Version**: 9.0.2+1.21.11
- **Minecraft Version**: 1.21.11
- **Supported Platforms**: Fabric, Forge, NeoForge
- **License**: MIT

---

Ready to get started? Check out the **[Getting Started Guide](guide/getting-started)** to begin using Amber in your mod development projects.