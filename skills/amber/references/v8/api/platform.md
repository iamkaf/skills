# Platform API

The Platform API provides a unified way to access platform-specific information and functionality across Fabric, Forge, and NeoForge. It abstracts away the differences between mod loaders, allowing you to write code that works consistently across all platforms.

## Overview

The Platform API consists of several key components:

- **Platform Class**: Main utility class for platform information and environment detection
- **ModInfo Interface**: Provides information about loaded mods
- **Environment Detection**: Client/server environment detection
- **Path Management**: Cross-platform access to game directories
- **Mod Discovery**: Query loaded mods and their information

## Platform Class

The main utility class for platform operations. All methods are static and work by calling the appropriate platform service behind the scenes.

### Environment Detection

#### `getEnvironment()`

Gets the current runtime environment type.

```java
public static Env getEnvironment()
```

**Returns:**
- `Env.CLIENT` - Running on the client
- `Env.SERVER` - Running on the dedicated server

#### `isClient()` / `isServer()`

Convenience methods for environment checking.

```java
public static boolean isClient()
public static boolean isServer()
```

**Example:**
```java
public class ClientServerLogic {
    public static void initialize() {
        if (Platform.isClient()) {
            // Initialize client-side features
            setupClientRendering();
            setupKeybinds();
        } else {
            // Initialize server-side features
            setupServerLogic();
            setupWorldGen();
        }
        
        // Common initialization
        setupCommonFeatures();
    }
}
```

### Platform Information

#### `getPlatformName()`

Gets the name of the current platform.

```java
public static String getPlatformName()
```

**Returns:** "Fabric", "Forge", or "NeoForge"

#### Platform Check Methods

```java
public static boolean isFabric()
public static boolean isForge()
public static boolean isNeoForge()
```

**Example:**
```java
public class PlatformSpecificFeatures {
    public static void registerFeatures() {
        // Common features for all platforms
        registerCommonFeatures();
        
        // Platform-specific features
        if (Platform.isFabric()) {
            registerFabricFeatures();
        } else if (Platform.isForge()) {
            registerForgeFeatures();
        } else if (Platform.isNeoForge()) {
            registerNeoForgeFeatures();
        }
    }
    
    private static void registerFabricFeatures() {
        // Fabric-specific registrations
    }
    
    private static void registerForgeFeatures() {
        // Forge-specific registrations
    }
    
    private static void registerNeoForgeFeatures() {
        // NeoForge-specific registrations
    }
}
```

#### `isDevelopmentEnvironment()`

Checks if running in a development environment.

```java
public static boolean isDevelopmentEnvironment()
```

**Example:**
```java
public class DevelopmentFeatures {
    public static void setupFeatures() {
        if (Platform.isDevelopmentEnvironment()) {
            // Enable debug features
            enableDebugLogging();
            registerDebugCommands();
            setupTestingHooks();
        }
        
        // Always enable in production
        setupProductionFeatures();
    }
    
    private static void enableDebugLogging() {
        // Enable verbose logging
        Logger.getLogger("mymod").setLevel(Level.DEBUG);
    }
    
    private static void registerDebugCommands() {
        // Register commands only available in development
    }
}
```

### Path Management

The Platform API provides convenient access to common Minecraft directories.

#### Game Directory

```java
public static Path getGameFolder()
```

Returns the main Minecraft game directory (usually `.minecraft`).

#### Config Directory

```java
public static Path getConfigFolder()
```

Returns the config directory where mod settings are stored.

#### Specialized Directories

```java
public static Path getModsFolder()      // mods folder
public static Path getLogsFolder()      // logs folder
public static Path getScreenshotsFolder() // screenshots folder
public static Path getResourcePacksFolder() // resourcepacks folder
public static Path getShaderPacksFolder()   // shaderpacks folder
public static Path getSavesFolder()     // saves folder
```

**Example:**
```java
public class PathManager {
    public static void setupDirectories() {
        Path configDir = Platform.getConfigFolder();
        Path modConfigDir = configDir.resolve("mymod");
        
        // Create mod-specific config directory
        try {
            Files.createDirectories(modConfigDir);
        } catch (IOException e) {
            Logger.getLogger("mymod").error("Failed to create config directory", e);
        }
        
        // Setup other paths
        Path logFile = Platform.getLogsFolder().resolve("mymod.log");
        Path screenshotDir = Platform.getScreenshotsFolder();
        
        System.out.println("Config dir: " + modConfigDir);
        System.out.println("Log file: " + logFile);
    }
}
```

### Mod Discovery

#### `isModLoaded(String modId)`

Checks if a specific mod is currently loaded.

```java
public static boolean isModLoaded(String id)
```

#### `getModInfo(String modId)`

Gets information about a specific mod.

```java
public static ModInfo getModInfo(String modId)
```

#### `getModIds()`

Gets a collection of all loaded mod IDs.

```java
public static Collection<String> getModIds()
```

#### Convenience Methods

```java
public static String getModVersion(String modId)
public static String getModName(String modId)
public static boolean isAnyModLoaded(String... modIds)
public static boolean areAllModsLoaded(String... modIds)
```

**Example:**
```java
public class ModCompatibility {
    public static void checkDependencies() {
        // Check required dependencies
        if (!Platform.isModLoaded("amber")) {
            throw new RuntimeException("Amber is required but not found!");
        }
        
        // Check optional dependencies
        if (Platform.isModLoaded("jei")) {
            System.out.println("JEI detected - enabling integration");
            setupJEIIntegration();
        }
        
        if (Platform.isModLoaded("fabric-api")) {
            System.out.println("Fabric API detected - enabling Fabric features");
            setupFabricAPIFeatures();
        }
        
        // Check for alternative mods
        if (Platform.isAnyModLoaded("jei", "rei", "emi")) {
            System.out.println("Recipe viewer detected - enabling recipe integration");
            setupRecipeIntegration();
        }
        
        // Log all loaded mods (debug)
        if (Platform.isDevelopmentEnvironment()) {
            System.out.println("Loaded mods: " + String.join(", ", Platform.getModIds()));
        }
    }
    
    private static void setupJEIIntegration() {
        // JEI-specific integration code
    }
    
    private static void setupFabricAPIFeatures() {
        // Fabric API-specific features
    }
    
    private static void setupRecipeIntegration() {
        // Recipe viewer integration
    }
}
```

## ModInfo Interface

Provides information about a loaded mod.

```java
public interface ModInfo {
    String modId();       // The mod's unique identifier
    String name();        // The mod's display name
    String version();     // The mod's version
    String description(); // The mod's description (may be empty)
}
```

**Example:**
```java
public class ModInfoExample {
    public static void printModInfo(String modId) {
        ModInfo info = Platform.getModInfo(modId);
        if (info != null) {
            System.out.println("Mod ID: " + info.modId());
            System.out.println("Name: " + info.name());
            System.out.println("Version: " + info.version());
            System.out.println("Description: " + info.description());
        } else {
            System.out.println("Mod not found: " + modId);
        }
    }
    
    public static void checkAmberVersion() {
        ModInfo amberInfo = Platform.getModInfo("amber");
        if (amberInfo != null) {
            String version = amberInfo.version();
            System.out.println("Using Amber version: " + version);
            
            // Check for minimum version
            if (compareVersions(version, "8.3.2") < 0) {
                System.out.println("Warning: Amber version is too old!");
            }
        }
    }
    
    private static int compareVersions(String v1, String v2) {
        // Simple version comparison logic
        String[] parts1 = v1.split("\\.");
        String[] parts2 = v2.split("\\.");
        
        for (int i = 0; i < Math.min(parts1.length, parts2.length); i++) {
            int num1 = Integer.parseInt(parts1[i]);
            int num2 = Integer.parseInt(parts2[i]);
            
            if (num1 != num2) {
                return Integer.compare(num1, num2);
            }
        }
        
        return Integer.compare(parts1.length, parts2.length);
    }
}
```

## Advanced Usage

### Conditional Feature Loading

```java
public class ConditionalFeatures {
    public static void loadFeatures() {
        // Load based on platform
        if (Platform.isFabric()) {
            loadFabricFeatures();
        } else if (Platform.isForge()) {
            loadForgeFeatures();
        } else if (Platform.isNeoForge()) {
            loadNeoForgeFeatures();
        }
        
        // Load based on environment
        if (Platform.isClient()) {
            loadClientFeatures();
        }
        
        // Load based on available mods
        if (Platform.isModLoaded("cloth-config")) {
            loadClothConfigIntegration();
        }
        
        // Load based on development mode
        if (Platform.isDevelopmentEnvironment()) {
            loadDevelopmentFeatures();
        }
    }
    
    private static void loadFabricFeatures() {
        // Fabric-specific feature loading
    }
    
    private static void loadForgeFeatures() {
        // Forge-specific feature loading
    }
    
    private static void loadNeoForgeFeatures() {
        // NeoForge-specific feature loading
    }
    
    private static void loadClientFeatures() {
        // Client-only features
    }
    
    private static void loadClothConfigIntegration() {
        // Cloth Config integration
    }
    
    private static void loadDevelopmentFeatures() {
        // Development-only features
    }
}
```

### Configuration Management

```java
public class PlatformConfig {
    private static final Path CONFIG_DIR = Platform.getConfigFolder();
    private static final Path MOD_CONFIG_DIR = CONFIG_DIR.resolve("mymod");
    private static final Path CONFIG_FILE = MOD_CONFIG_DIR.resolve("config.json");
    
    public static void loadConfig() {
        try {
            // Create directories if they don't exist
            Files.createDirectories(MOD_CONFIG_DIR);
            
            // Load configuration
            if (Files.exists(CONFIG_FILE)) {
                String content = Files.readString(CONFIG_FILE);
                // Parse configuration
            } else {
                // Create default configuration
                createDefaultConfig();
            }
        } catch (IOException e) {
            Logger.getLogger("mymod").error("Failed to load configuration", e);
        }
    }
    
    private static void createDefaultConfig() throws IOException {
        String defaultConfig = """
            {
              "enabled": true,
              "debugMode": false,
              "features": {
                "feature1": true,
                "feature2": false
              }
            }
            """;
        
        Files.writeString(CONFIG_FILE, defaultConfig);
    }
}
```

## Best Practices

1. **Always Check Environment**: Use `isClient()` and `isServer()` before accessing client/server-only code
2. **Use Platform Abstraction**: Avoid platform-specific APIs when possible
3. **Handle Missing Mods**: Always check if optional mods are loaded before using them
4. **Development Detection**: Use `isDevelopmentEnvironment()` for debug features
5. **Path Safety**: Always ensure directories exist before writing files
6. **Version Compatibility**: Check mod versions when integrating with other mods

## Migration Guide

### From Fabric Loader

```java
// Old Fabric way
if (FabricLoader.getInstance().isModLoaded("jei")) {
    // Do something
}
Path configDir = FabricLoader.getInstance().getConfigDir();

// New Amber way
if (Platform.isModLoaded("jei")) {
    // Do something
}
Path configDir = Platform.getConfigFolder();
```

### From Forge

```java
// Old Forge way
if (ModList.get().isLoaded("jei")) {
    // Do something
}
Path configDir = FMLPaths.CONFIGDIR.get();

// New Amber way
if (Platform.isModLoaded("jei")) {
    // Do something
}
Path configDir = Platform.getConfigFolder();
```

The Platform API provides a consistent interface across all platforms, making your code more maintainable and portable.