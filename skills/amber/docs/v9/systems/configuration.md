# Configuration System

Amber provides a simple yet powerful configuration system that works across all mod loaders. The system uses JSON files with automatic serialization, making it easy to manage mod settings without worrying about platform differences.

## Overview

The configuration system consists of:

- **JsonConfigManager**: Main class for managing configuration files
- **Automatic Serialization**: Handles JSON conversion automatically
- **Type Safety**: Full type safety for configuration values
- **Hot Reloading**: Runtime configuration updates (planned feature)
- **Cross-platform compatibility**: Works identically on all platforms

## Basic Usage

### Creating a Configuration Class

First, create a class to hold your configuration data:

```java
public class MyModConfig {
    // Basic configuration fields
    public boolean enableFeature = true;
    public int maxEnergy = 1000;
    public double multiplier = 1.5;
    public String mode = "normal";
    
    // Complex configuration fields
    public List<String> allowedItems = new ArrayList<>(List.of("diamond", "gold"));
    public Map<String, Integer> itemValues = new HashMap<>();
    public PositionConfig spawnPoint = new PositionConfig(0, 64, 0);
    
    // Nested configuration class
    public static class PositionConfig {
        public int x = 0;
        public int y = 64;
        public int z = 0;
        
        public PositionConfig() {}
        
        public PositionConfig(int x, int y, int z) {
            this.x = x;
            this.y = y;
            this.z = z;
        }
    }
    
    // Initialize default values
    public MyModConfig() {
        // Set default values for complex fields
        itemValues.put("diamond", 100);
        itemValues.put("gold", 50);
        itemValues.put("iron", 25);
    }
}
```

### Setting Up the Configuration Manager

Create a configuration manager for your mod:

```java
import com.iamkaf.amber.api.config.v1.JsonConfigManager;
import java.nio.file.Path;

public class ConfigManager {
    private static JsonConfigManager<MyModConfig> configManager;
    private static MyModConfig config;
    
    public static void init() {
        // Create configuration manager
        configManager = new JsonConfigManager<>(
            "mymod",                    // Mod ID
            new MyModConfig(),          // Initial config instance
            null,                       // Config path (null = default)
            "# MyMod Configuration\n" +  // Header comment
            "# This file contains settings for MyMod\n" +
            "# Modify values as needed\n"
        );
        
        // Load configuration
        config = configManager.getConfig();
        
        System.out.println("Configuration loaded: maxEnergy = " + config.maxEnergy);
    }
    
    public static MyModConfig get() {
        return config;
    }
    
    public static void save() {
        if (configManager != null) {
            configManager.saveConfig();
        }
    }
    
    public static void reload() {
        if (configManager != null) {
            configManager.loadConfig();
            config = configManager.getConfig();
        }
    }
}
```

### Using Configuration in Your Mod

Access configuration values throughout your mod:

```java
public class MyMod {
    public static void init() {
        // Initialize configuration
        ConfigManager.init();
        
        // Use configuration values
        MyModConfig config = ConfigManager.get();
        
        if (config.enableFeature) {
            System.out.println("Feature enabled with max energy: " + config.maxEnergy);
            setupEnergySystem(config.maxEnergy, config.multiplier);
        }
        
        // Setup item values
        setupItemValues(config.itemValues);
    }
    
    private static void setupEnergySystem(int maxEnergy, double multiplier) {
        // Setup energy system based on config
        EnergySystem.setMaxEnergy(maxEnergy);
        EnergySystem.setMultiplier(multiplier);
    }
    
    private static void setupItemValues(Map<String, Integer> values) {
        // Setup item values from config
        for (Map.Entry<String, Integer> entry : values.entrySet()) {
            ItemRegistry.setValue(entry.getKey(), entry.getValue());
        }
    }
}
```

## Advanced Configuration

### Custom Configuration Path

Specify a custom path for your configuration file:

```java
public class CustomConfigManager {
    public static void init() {
        // Create custom config path
        Path configPath = Platform.getConfigFolder().resolve("mymod").resolve("settings.json");
        
        // Create configuration manager with custom path
        JsonConfigManager<MyModConfig> configManager = new JsonConfigManager<>(
            "mymod",
            new MyModConfig(),
            configPath,  // Custom path
            "# Custom configuration file location\n"
        );
        
        // Load configuration
        MyModConfig config = configManager.getConfig();
    }
}
```

### Configuration Sections

Organize large configurations into sections:

```java
public class AdvancedModConfig {
    // General settings
    public GeneralSettings general = new GeneralSettings();
    
    // Feature toggles
    public FeatureSettings features = new FeatureSettings();
    
    // Network settings
    public NetworkSettings network = new NetworkSettings();
    
    public static class GeneralSettings {
        public String mode = "normal";
        public boolean debugMode = false;
        public int updateInterval = 20;
    }
    
    public static class FeatureSettings {
        public boolean enableEnergy = true;
        public boolean enableMagic = true;
        public boolean enableCrafting = true;
        public List<String> disabledFeatures = new ArrayList<>();
    }
    
    public static class NetworkSettings {
        public boolean enableNetworking = true;
        public int packetTimeout = 5000;
        public String serverAddress = "localhost";
        public int serverPort = 25565;
    }
}
```

### Configuration Validation

Add validation to ensure configuration values are valid:

```java
public class ValidatedConfigManager {
    public static void validateAndInit() {
        JsonConfigManager<MyModConfig> configManager = new JsonConfigManager<>(
            "mymod",
            new MyModConfig(),
            null,
            null
        );
        
        MyModConfig config = configManager.getConfig();
        
        // Validate configuration
        List<String> errors = validateConfig(config);
        
        if (!errors.isEmpty()) {
            // Log validation errors
            Constants.LOG.error("Configuration validation failed:");
            errors.forEach(error -> Constants.LOG.error("  - " + error));
            
            // Use defaults for invalid values
            fixInvalidValues(config);
            
            // Save corrected configuration
            configManager.saveConfig();
        }
    }
    
    private static List<String> validateConfig(MyModConfig config) {
        List<String> errors = new ArrayList<>();
        
        if (config.maxEnergy < 0) {
            errors.add("maxEnergy cannot be negative");
        }
        
        if (config.multiplier <= 0) {
            errors.add("multiplier must be positive");
        }
        
        if (!Arrays.asList("easy", "normal", "hard").contains(config.mode)) {
            errors.add("mode must be one of: easy, normal, hard");
        }
        
        return errors;
    }
    
    private static void fixInvalidValues(MyModConfig config) {
        if (config.maxEnergy < 0) {
            config.maxEnergy = 1000;
        }
        
        if (config.multiplier <= 0) {
            config.multiplier = 1.0;
        }
        
        if (!Arrays.asList("easy", "normal", "hard").contains(config.mode)) {
            config.mode = "normal";
        }
    }
}
```

### Runtime Configuration Updates

Update configuration values at runtime:

```java
public class RuntimeConfigManager {
    private static JsonConfigManager<MyModConfig> configManager;
    
    public static void updateConfig(String key, Object value) {
        MyModConfig config = configManager.getConfig();
        
        // Update configuration based on key
        switch (key) {
            case "maxEnergy" -> {
                if (value instanceof Integer intValue && intValue > 0) {
                    config.maxEnergy = intValue;
                    EnergySystem.setMaxEnergy(intValue);
                }
            }
            case "enableFeature" -> {
                if (value instanceof Boolean boolValue) {
                    config.enableFeature = boolValue;
                    if (boolValue) {
                        FeatureManager.enable();
                    } else {
                        FeatureManager.disable();
                    }
                }
            }
            case "multiplier" -> {
                if (value instanceof Double doubleValue && doubleValue > 0) {
                    config.multiplier = doubleValue;
                    EnergySystem.setMultiplier(doubleValue);
                }
            }
        }
        
        // Save updated configuration
        configManager.saveConfig();
    }
    
    public static void resetToDefaults() {
        // Create new default config
        MyModConfig defaultConfig = new MyModConfig();
        
        // Update current config with defaults
        MyModConfig currentConfig = configManager.getConfig();
        currentConfig.enableFeature = defaultConfig.enableFeature;
        currentConfig.maxEnergy = defaultConfig.maxEnergy;
        currentConfig.multiplier = defaultConfig.multiplier;
        
        // Save and apply
        configManager.saveConfig();
        applyConfig(currentConfig);
    }
    
    private static void applyConfig(MyModConfig config) {
        // Apply configuration to game systems
        EnergySystem.setMaxEnergy(config.maxEnergy);
        EnergySystem.setMultiplier(config.multiplier);
        
        if (config.enableFeature) {
            FeatureManager.enable();
        } else {
            FeatureManager.disable();
        }
    }
}
```

## Configuration Commands

Create commands to manage configuration:

```java
public class ConfigCommands {
    public static void registerCommands() {
        // Create base command
        LiteralArgumentBuilder<CommandSourceStack> baseCommand = 
            Commands.literal("mymodconfig");
        
        // Get command
        LiteralArgumentBuilder<CommandSourceStack> getCommand = 
            Commands.literal("get")
                .then(Commands.argument("key", StringArgumentType.string())
                    .executes(context -> {
                        String key = StringArgumentType.getString(context, "key");
                        return executeGet(context.getSource(), key);
                    }));
        
        // Set command
        LiteralArgumentBuilder<CommandSourceStack> setCommand = 
            Commands.literal("set")
                .then(Commands.argument("key", StringArgumentType.string())
                    .then(Commands.argument("value", StringArgumentType.greedyString())
                        .executes(context -> {
                            String key = StringArgumentType.getString(context, "key");
                            String value = StringArgumentType.getString(context, "value");
                            return executeSet(context.getSource(), key, value);
                        })));
        
        // Reload command
        LiteralArgumentBuilder<CommandSourceStack> reloadCommand = 
            Commands.literal("reload")
                .executes(context -> {
                    ConfigManager.reload();
                    context.getSource().sendSuccess(
                        () -> Component.literal("Configuration reloaded"), 
                        true
                    );
                    return Command.SINGLE_SUCCESS;
                });
        
        // Build command tree
        baseCommand.then(getCommand);
        baseCommand.then(setCommand);
        baseCommand.then(reloadCommand);
        
        // Register command (platform-specific)
        CommandRegistrationEvent.EVENT.register(
            (dispatcher, registry, environment) -> dispatcher.register(baseCommand)
        );
    }
    
    private static int executeGet(CommandSourceStack source, String key) {
        MyModConfig config = ConfigManager.get();
        
        Object value = getConfigValue(config, key);
        if (value != null) {
            source.sendSuccess(() -> Component.literal(key + " = " + value), true);
            return Command.SINGLE_SUCCESS;
        } else {
            source.sendFailure(Component.literal("Unknown config key: " + key));
            return 0;
        }
    }
    
    private static int executeSet(CommandSourceStack source, String key, String value) {
        try {
            Object parsedValue = parseValue(key, value);
            RuntimeConfigManager.updateConfig(key, parsedValue);
            
            source.sendSuccess(() -> 
                Component.literal("Set " + key + " = " + value), true);
            return Command.SINGLE_SUCCESS;
        } catch (Exception e) {
            source.sendFailure(Component.literal("Invalid value: " + e.getMessage()));
            return 0;
        }
    }
    
    private static Object getConfigValue(MyModConfig config, String key) {
        return switch (key) {
            case "enableFeature" -> config.enableFeature;
            case "maxEnergy" -> config.maxEnergy;
            case "multiplier" -> config.multiplier;
            case "mode" -> config.mode;
            default -> null;
        };
    }
    
    private static Object parseValue(String key, String value) {
        return switch (key) {
            case "enableFeature" -> Boolean.parseBoolean(value);
            case "maxEnergy" -> Integer.parseInt(value);
            case "multiplier" -> Double.parseDouble(value);
            default -> value;
        };
    }
}
```

## Best Practices

### 1. Default Values

Always provide sensible defaults:

```java
public class GoodConfig {
    // Good - sensible defaults
    public boolean enableFeature = true;
    public int maxEnergy = 1000;
    public double multiplier = 1.0;
    public String mode = "normal";
    
    // Initialize collections
    public List<String> allowedItems = new ArrayList<>(List.of("diamond", "gold"));
    public Map<String, Integer> values = new HashMap<>();
    
    public GoodConfig() {
        // Set default map values
        values.put("diamond", 100);
        values.put("gold", 50);
    }
}
```

### 2. Documentation

Add comments to your configuration:

```java
public class DocumentedConfig {
    /**
     * Whether to enable the energy system.
     * Set to false to disable all energy-related features.
     */
    public boolean enableEnergy = true;
    
    /**
     * Maximum energy storage capacity.
     * Higher values allow more energy storage but may affect balance.
     * Range: 100 - 100000
     */
    public int maxEnergy = 1000;
    
    /**
     * Energy transfer multiplier.
     * Affects how quickly energy transfers between components.
     * Range: 0.1 - 10.0
     */
    public double energyMultiplier = 1.0;
}
```

### 3. Type Safety

Use appropriate types for configuration values:

```java
public class TypeSafeConfig {
    // Use specific types
    public int count = 5;                    // Not double
    public boolean enabled = true;           // Not String
    public List<String> items = new ArrayList<>(); // Not Object
    public Map<String, Integer> values = new HashMap<>(); // Specific generic types
    
    // Use enums for fixed sets of values
    public Difficulty difficulty = Difficulty.NORMAL;
    
    public enum Difficulty {
        EASY, NORMAL, HARD
    }
}
```

### 4. Error Handling

Handle configuration errors gracefully:

```java
public class SafeConfigManager {
    public static void safeInit() {
        try {
            ConfigManager.init();
        } catch (Exception e) {
            Constants.LOG.error("Failed to load configuration, using defaults", e);
            
            // Use in-memory defaults
            useDefaultConfig();
        }
    }
    
    private static void useDefaultConfig() {
        // Create default config in memory
        MyModConfig defaultConfig = new MyModConfig();
        
        // Apply to systems
        applyConfig(defaultConfig);
        
        // Notify user
        if (Platform.isClient()) {
            Minecraft.getInstance().player.sendSystemMessage(
                Component.literal("Using default configuration due to load error")
            );
        }
    }
}
```

## Configuration File Format

The configuration system creates JSON5 files (JSON with comments):

```json5
// MyMod Configuration
// This file contains settings for MyMod
// Modify values as needed

{
  // Feature settings
  "enableFeature": true,
  "maxEnergy": 1000,
  "multiplier": 1.5,
  "mode": "normal",
  
  // Item settings
  "allowedItems": [
    "diamond",
    "gold",
    "iron"
  ],
  
  // Item values
  "itemValues": {
    "diamond": 100,
    "gold": 50,
    "iron": 25
  },
  
  // Spawn point
  "spawnPoint": {
    "x": 0,
    "y": 64,
    "z": 0
  }
}
```

The configuration system provides a clean, type-safe way to manage mod settings across all platforms without worrying about platform-specific APIs or file handling.