# Core API

The Core API provides the fundamental building blocks for working with Amber, including initialization, mod information management, and core utilities.

## AmberInitializer

The `AmberInitializer` class is the main entry point for initializing Amber in your mod. It automatically detects mod information from the platform and sets up the necessary infrastructure.

### Methods

#### `initialize(String modId)`

Initializes Amber for your mod and returns mod information.

```java
public static AmberModInfo initialize(String id)
```

**Parameters:**
- `modId` - The unique identifier of your mod

**Returns:**
- `AmberModInfo` - Information about your mod (ID, name, version)

**Example:**
```java
public class MyMod {
    public static final String MOD_ID = "mymod";
    public static AmberModInfo modInfo;
    
    public static void init() {
        // Initialize Amber and get mod info
        modInfo = AmberInitializer.initialize(MOD_ID);
        
        System.out.println("Initialized: " + modInfo.name() + " v" + modInfo.version());
    }
}
```

## AmberModInfo

A record containing information about your mod, automatically populated by Amber from platform metadata.

### Fields

```java
public record AmberModInfo(String id, String name, String version)
```

- `id` - The unique identifier of the mod
- `name` - The human-readable name of the mod  
- `version` - The version of the mod

### Example Usage

```java
public class MyMod {
    private static AmberModInfo modInfo;
    
    public static void init() {
        modInfo = AmberInitializer.initialize(MOD_ID);
        
        // Access mod information
        System.out.println("Mod ID: " + modInfo.id());
        System.out.println("Mod Name: " + modInfo.name());
        System.out.println("Mod Version: " + modInfo.version());
        
        // Use in other parts of your mod
        logger.info("Starting {} version {}", modInfo.name(), modInfo.version());
    }
    
    public static String getVersion() {
        return modInfo != null ? modInfo.version() : "unknown";
    }
}
```

## Platform Abstraction

The Platform API provides a unified way to access platform-specific information and functionality across Fabric, Forge, and NeoForge.

### Platform Class

The main utility class for platform information and environment detection.

#### Environment Detection

```java
// Check current environment
boolean isClient = Platform.isClient();
boolean isServer = Platform.isServer();
Env environment = Platform.getEnvironment();
```

#### Platform Information

```java
// Get platform name
String platformName = Platform.getPlatformName();

// Check specific platforms
boolean isFabric = Platform.isFabric();
boolean isForge = Platform.isForge();
boolean isNeoForge = Platform.isNeoForge();

// Check if in development environment
boolean isDev = Platform.isDevelopmentEnvironment();
```

#### Path Management

```java
// Get common paths
Path gameFolder = Platform.getGameFolder();
Path configFolder = Platform.getConfigFolder();
Path modsFolder = Platform.getModsFolder();
Path logsFolder = Platform.getLogsFolder();
Path savesFolder = Platform.getSavesFolder();
```

#### Mod Information

```java
// Check if a mod is loaded
boolean isLoaded = Platform.isModLoaded("fabric-api");

// Get information about a mod
ModInfo modInfo = Platform.getModInfo("amber");
if (modInfo != null) {
    System.out.println("Amber version: " + modInfo.version());
}

// Get all loaded mod IDs
Collection<String> allMods = Platform.getModIds();
```

### ModInfo Interface

Provides information about a loaded mod.

```java
public interface ModInfo {
    String modId();
    String name();
    String version();
    String description();
}
```

## Usage Examples

### Basic Mod Initialization

```java
public class ExampleMod {
    public static final String MOD_ID = "examplemod";
    private static AmberModInfo modInfo;
    
    public static void initialize() {
        // Initialize Amber
        modInfo = AmberInitializer.initialize(MOD_ID);
        
        // Log initialization
        Constants.LOG.info("{} v{} initialized with Amber", 
            modInfo.name(), modInfo.version());
        
        // Initialize mod systems
        initializeConfig();
        initializeRegistries();
        initializeEvents();
    }
    
    private static void initializeConfig() {
        // Use platform config folder
        Path configPath = Platform.getConfigFolder().resolve(MOD_ID + ".json");
        // Initialize config...
    }
    
    private static void initializeRegistries() {
        // Registry initialization code...
    }
    
    private static void initializeEvents() {
        // Event initialization code...
    }
}
```

### Platform-Specific Logic

```java
public class PlatformSpecificFeatures {
    public static void setupPlatformFeatures() {
        String platform = Platform.getPlatformName();
        
        switch (platform) {
            case "Fabric":
                setupFabricFeatures();
                break;
            case "Forge":
                setupForgeFeatures();
                break;
            case "NeoForge":
                setupNeoForgeFeatures();
                break;
        }
        
        // Common setup for all platforms
        setupCommonFeatures();
    }
    
    private static void setupFabricFeatures() {
        // Fabric-specific initialization
        if (Platform.isModLoaded("fabric-api")) {
            // Use Fabric API features
        }
    }
    
    private static void setupForgeFeatures() {
        // Forge-specific initialization
    }
    
    private static void setupNeoForgeFeatures() {
        // NeoForge-specific initialization
    }
    
    private static void setupCommonFeatures() {
        // Features that work on all platforms
        System.out.println("Running on " + Platform.getPlatformName());
        System.out.println("Environment: " + Platform.getEnvironment());
        System.out.println("Development mode: " + Platform.isDevelopmentEnvironment());
    }
}
```

### Development Environment Detection

```java
public class DevelopmentFeatures {
    public static void setupDevelopmentFeatures() {
        if (Platform.isDevelopmentEnvironment()) {
            // Enable development-only features
            enableDebugLogging();
            enableDebugCommands();
            setupTestingUtilities();
        }
    }
    
    private static void enableDebugLogging() {
        // Enable verbose logging for development
        System.setProperty("amber.debug", "true");
    }
    
    private static void enableDebugCommands() {
        // Register debug commands that shouldn't be in production
        // Command registration code...
    }
    
    private static void setupTestingUtilities() {
        // Setup utilities for testing and debugging
        // Testing utilities code...
    }
}
```

### Mod Compatibility Checking

```java
public class ModCompatibility {
    public static void checkDependencies() {
        // Check for required dependencies
        if (!Platform.isModLoaded("amber")) {
            throw new RuntimeException("Amber is required but not found!");
        }
        
        // Check for optional dependencies
        if (Platform.isModLoaded("fabric-api")) {
            System.out.println("Fabric API detected - enabling Fabric features");
        }
        
        if (Platform.isModLoaded("jei")) {
            System.out.println("JEI detected - enabling integration");
        }
        
        // Check for conflicting mods
        if (Platform.isModLoaded("conflicting-mod")) {
            Constants.LOG.warn("Conflicting mod detected! Some features may not work correctly.");
        }
    }
    
    public static boolean areAllDependenciesLoaded(String... modIds) {
        return Platform.areAllModsLoaded(modIds);
    }
    
    public static boolean isAnyDependencyLoaded(String... modIds) {
        return Platform.isAnyModLoaded(modIds);
    }
}
```

## Best Practices

1. **Initialize Early**: Call `AmberInitializer.initialize()` as early as possible in your mod's initialization
2. **Store Mod Info**: Keep the returned `AmberModInfo` for later use in your mod
3. **Use Platform Checks**: Always check the platform or environment before using platform-specific features
4. **Handle Missing Mods**: Gracefully handle situations where optional dependencies are not available
5. **Development Detection**: Use `Platform.isDevelopmentEnvironment()` to enable debug features only in development

## Migration from Direct Platform APIs

If you're migrating from direct platform-specific APIs:

### From Fabric

```java
// Old Fabric way
String platform = "Fabric";
Path configDir = FabricLoader.getInstance().getConfigDir();

// New Amber way
String platform = Platform.getPlatformName();
Path configDir = Platform.getConfigFolder();
```

### From Forge

```java
// Old Forge way
String platform = "Forge";
Path configDir = FMLPaths.CONFIGDIR.get();

// New Amber way
String platform = Platform.getPlatformName();
Path configDir = Platform.getConfigFolder();
```

The Platform API provides a unified interface that works across all platforms, eliminating the need for platform-specific code.