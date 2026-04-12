# Command System

Amber provides utilities to simplify command creation and registration across all mod loaders. While the command system uses Minecraft's native Brigadier library, Amber offers helper methods to reduce boilerplate and ensure consistent behavior across platforms.

## Overview

The command utilities include:

- **SimpleCommands**: Helper class for creating base commands
- **Cross-platform registration**: Works consistently on Fabric, Forge, and NeoForge
- **Reduced boilerplate**: Less code for common command patterns
- **Platform abstraction**: Handles platform differences automatically

## Basic Usage

### Creating a Base Command

Use `SimpleCommands.createBaseCommand()` to create a base command that shows mod information:

```java
import com.iamkaf.amber.api.commands.v1.SimpleCommands;
import com.mojang.brigadier.Command;
import com.mojang.brigadier.builder.LiteralArgumentBuilder;
import net.minecraft.commands.CommandSourceStack;
import net.minecraft.commands.Commands;

public class MyModCommands {
    public static void registerCommands() {
        // Create base command that shows mod info
        LiteralArgumentBuilder<CommandSourceStack> baseCommand = 
            SimpleCommands.createBaseCommand("mymod");
        
        // Add subcommands
        baseCommand.then(createReloadCommand());
        baseCommand.then(createConfigCommand());
        baseCommand.then(createDebugCommand());
        
        // Register command (platform-specific)
        registerOnPlatform(baseCommand);
    }
    
    private static void registerOnPlatform(LiteralArgumentBuilder<CommandSourceStack> command) {
        // This would be registered through your platform's command registration event
        CommandRegistrationEvent.EVENT.register(
            (dispatcher, registry, environment) -> dispatcher.register(command)
        );
    }
}
```

### Adding Subcommands

Add subcommands to extend functionality:

```java
private static LiteralArgumentBuilder<CommandSourceStack> createReloadCommand() {
    return Commands.literal("reload")
        .requires(source -> source.hasPermission(2)) // Require OP level 2
        .executes(context -> {
            // Reload configuration
            ConfigManager.reload();
            
            context.getSource().sendSuccess(
                () -> Component.literal("Configuration reloaded successfully!"),
                true
            );
            
            return Command.SINGLE_SUCCESS;
        });
}

private static LiteralArgumentBuilder<CommandSourceStack> createConfigCommand() {
    return Commands.literal("config")
        .then(Commands.literal("get")
            .then(Commands.argument("key", StringArgumentType.string())
                .executes(context -> {
                    String key = StringArgumentType.getString(context, "key");
                    Object value = ConfigManager.get().getConfigValue(key);
                    
                    if (value != null) {
                        context.getSource().sendSuccess(
                            () -> Component.literal(key + " = " + value),
                            true
                        );
                        return Command.SINGLE_SUCCESS;
                    } else {
                        context.getSource().sendFailure(
                            Component.literal("Unknown config key: " + key)
                        );
                        return 0;
                    }
                })))
        .then(Commands.literal("set")
            .requires(source -> source.hasPermission(2))
            .then(Commands.argument("key", StringArgumentType.string())
                .then(Commands.argument("value", StringArgumentType.greedyString())
                    .executes(context -> {
                        String key = StringArgumentType.getString(context, "key");
                        String value = StringArgumentType.getString(context, "value");
                        
                        try {
                            ConfigManager.setConfigValue(key, value);
                            context.getSource().sendSuccess(
                                () -> Component.literal("Set " + key + " = " + value),
                                true
                            );
                            return Command.SINGLE_SUCCESS;
                        } catch (Exception e) {
                            context.getSource().sendFailure(
                                Component.literal("Error: " + e.getMessage())
                            );
                            return 0;
                        }
                    })))));
}

private static LiteralArgumentBuilder<CommandSourceStack> createDebugCommand() {
    return Commands.literal("debug")
        .requires(source -> source.hasPermission(4)) // Require OP level 4
        .then(Commands.literal("info")
            .executes(context -> {
                CommandSourceStack source = context.getSource();
                ServerPlayer player = source.getPlayer();
                
                if (player != null) {
                    // Send debug information
                    player.sendSystemMessage(Component.literal("=== Debug Info ==="));
                    player.sendSystemMessage(Component.literal("Platform: " + Platform.getPlatformName()));
                    player.sendSystemMessage(Component.literal("Environment: " + Platform.getEnvironment()));
                    player.sendSystemMessage(Component.literal("Position: " + player.blockPosition()));
                    player.sendSystemMessage(Component.literal("Dimension: " + player.level().dimension().location()));
                }
                
                return Command.SINGLE_SUCCESS;
            }))
        .then(Commands.literal("spawn")
            .then(Commands.argument("entity", EntityArgumentType.entity())
                .executes(context -> {
                    ServerPlayer player = context.getSource().getPlayer();
                    Entity entity = EntityArgumentType.getEntity(context, "entity");
                    
                    if (player != null && entity != null) {
                        // Spawn entity at player position
                        Entity newEntity = entity.getType().create(player.level());
                        if (newEntity != null) {
                            newEntity.setPos(player.getX(), player.getY(), player.getZ());
                            player.level().addFreshEntity(newEntity);
                            
                            context.getSource().sendSuccess(
                                () -> Component.literal("Spawned " + entity.getType().getDescription()),
                                true
                            );
                            return Command.SINGLE_SUCCESS;
                        }
                    }
                    
                    return 0;
                })));
}
```

## Advanced Command Examples

### Item Management Commands

Create commands for managing items:

```java
public class ItemCommands {
    public static LiteralArgumentBuilder<CommandSourceStack> createItemCommand() {
        return Commands.literal("item")
            .then(createGiveCommand())
            .then(createEnchantCommand())
            .then(createRepairCommand());
    }
    
    private static LiteralArgumentBuilder<CommandSourceStack> createGiveCommand() {
        return Commands.literal("give")
            .requires(source -> source.hasPermission(2))
            .then(Commands.argument("target", EntityArgumentType.player())
                .then(Commands.argument("item", ItemStackArgumentType.itemStack())
                    .executes(context -> {
                        ServerPlayer target = EntityArgumentType.getPlayer(context, "target");
                        ItemStack stack = ItemStackArgumentType.getItemStack(context, "item").create(1, false);
                        
                        target.getInventory().add(stack);
                        target.sendSystemMessage(
                            Component.literal("Given " + stack.getDisplayName().getString())
                        );
                        
                        context.getSource().sendSuccess(
                            () -> Component.literal("Gave " + stack.getDisplayName().getString() + 
                                " to " + target.getName().getString()),
                            true
                        );
                        
                        return Command.SINGLE_SUCCESS;
                    })
                    .then(Commands.argument("count", IntegerArgumentType.integer(1, 64))
                        .executes(context -> {
                            ServerPlayer target = EntityArgumentType.getPlayer(context, "target");
                            int count = IntegerArgumentType.getInteger(context, "count");
                            ItemStack stack = ItemStackArgumentType.getItemStack(context, "item").create(count, false);
                            
                            target.getInventory().add(stack);
                            
                            context.getSource().sendSuccess(
                                () -> Component.literal("Gave " + count + "x " + 
                                    stack.getDisplayName().getString() + " to " + 
                                    target.getName().getString()),
                                true
                            );
                            
                            return Command.SINGLE_SUCCESS;
                        })))));
    }
    
    private static LiteralArgumentBuilder<CommandSourceStack> createEnchantCommand() {
        return Commands.literal("enchant")
            .requires(source -> source.hasPermission(2))
            .then(Commands.argument("target", EntityArgumentType.player())
                .then(Commands.argument("enchantment", StringArgumentType.word())
                    .suggests((context, builder) -> {
                        // Suggest available enchantments
                        return SharedSuggestionProvider.suggest(
                            Stream.of(Enchantments.values())
                                .map(enchantment -> enchantment.getDescriptionId().replace("enchantment.minecraft.", "")),
                            builder
                        );
                    })
                    .then(Commands.argument("level", IntegerArgumentType.integer(1, 5))
                        .executes(context -> {
                            ServerPlayer target = EntityArgumentType.getPlayer(context, "target");
                            String enchantName = StringArgumentType.getString(context, "enchantment");
                            int level = IntegerArgumentType.getInteger(context, "level");
                            
                            // Find enchantment by name
                            Enchantment enchantment = findEnchantment(enchantName);
                            if (enchantment == null) {
                                context.getSource().sendFailure(
                                    Component.literal("Unknown enchantment: " + enchantName)
                                );
                                return 0;
                            }
                            
                            // Enchant held item
                            ItemStack heldItem = target.getMainHandItem();
                            if (heldItem.isEmpty()) {
                                context.getSource().sendFailure(
                                    Component.literal("Target must hold an item")
                                );
                                return 0;
                            }
                            
                            heldItem.enchant(enchantment, level);
                            
                            context.getSource().sendSuccess(
                                () -> Component.literal("Enchanted " + heldItem.getDisplayName().getString() + 
                                    " with " + enchantment.getFullname(level).getString()),
                                true
                            );
                            
                            return Command.SINGLE_SUCCESS;
                        })))));
    }
    
    private static Enchantment findEnchantment(String name) {
        for (Enchantment enchantment : Enchantments.values()) {
            String enchantName = enchantment.getDescriptionId().replace("enchantment.minecraft.", "");
            if (enchantName.equalsIgnoreCase(name)) {
                return enchantment;
            }
        }
        return null;
    }
}
```

### World Management Commands

Create commands for world manipulation:

```java
public class WorldCommands {
    public static LiteralArgumentBuilder<CommandSourceStack> createWorldCommand() {
        return Commands.literal("world")
            .then(createTimeCommand())
            .then(createWeatherCommand())
            .then(createTeleportCommand());
    }
    
    private static LiteralArgumentBuilder<CommandSourceStack> createTimeCommand() {
        return Commands.literal("time")
            .requires(source -> source.hasPermission(2))
            .then(Commands.literal("set")
                .then(Commands.argument("time", IntegerArgumentType.integer(0, 24000))
                    .executes(context -> {
                        int time = IntegerArgumentType.getInteger(context, "time");
                        ServerLevel level = context.getSource().getLevel();
                        
                        level.setDayTime(time);
                        
                        context.getSource().sendSuccess(
                            () -> Component.literal("Set time to " + time),
                            true
                        );
                        
                        return Command.SINGLE_SUCCESS;
                    })))
            .then(Commands.literal("add")
                .then(Commands.argument("amount", IntegerArgumentType.integer(-24000, 24000))
                    .executes(context -> {
                        int amount = IntegerArgumentType.getInteger(context, "amount");
                        ServerLevel level = context.getSource().getLevel();
                        
                        level.setDayTime(level.getDayTime() + amount);
                        
                        context.getSource().sendSuccess(
                            () -> Component.literal("Added " + amount + " to time"),
                            true
                        );
                        
                        return Command.SINGLE_SUCCESS;
                    })))
            .then(Commands.literal("query")
                .executes(context -> {
                    ServerLevel level = context.getSource().getLevel();
                    long time = level.getDayTime();
                    long day = time / 24000;
                    long dayTime = time % 24000;
                    
                    context.getSource().sendSuccess(
                        () -> Component.literal("Day " + day + ", Time: " + dayTime),
                        true
                    );
                    
                    return Command.SINGLE_SUCCESS;
                }));
    }
    
    private static LiteralArgumentBuilder<CommandSourceStack> createWeatherCommand() {
        return Commands.literal("weather")
            .requires(source -> source.hasPermission(2))
            .then(Commands.literal("clear")
                .executes(context -> {
                    ServerLevel level = context.getSource().getLevel();
                    level.setWeatherParameters(6000, 0, false, false);
                    
                    context.getSource().sendSuccess(
                        () -> Component.literal("Set weather to clear"),
                        true
                    );
                    
                    return Command.SINGLE_SUCCESS;
                }))
            .then(Commands.literal("rain")
                .executes(context -> {
                    ServerLevel level = context.getSource().getLevel();
                    level.setWeatherParameters(0, 6000, true, false);
                    
                    context.getSource().sendSuccess(
                        () -> Component.literal("Set weather to rain"),
                        true
                    );
                    
                    return Command.SINGLE_SUCCESS;
                }))
            .then(Commands.literal("thunder")
                .executes(context -> {
                    ServerLevel level = context.getSource().getLevel();
                    level.setWeatherParameters(0, 6000, true, true);
                    
                    context.getSource().sendSuccess(
                        () -> Component.literal("Set weather to thunder"),
                        true
                    );
                    
                    return Command.SINGLE_SUCCESS;
                }));
    }
    
    private static LiteralArgumentBuilder<CommandSourceStack> createTeleportCommand() {
        return Commands.literal("tp")
            .requires(source -> source.hasPermission(2))
            .then(Commands.argument("target", EntityArgumentType.player())
                .then(Commands.argument("destination", EntityArgumentType.player())
                    .executes(context -> {
                        ServerPlayer target = EntityArgumentType.getPlayer(context, "target");
                        ServerPlayer destination = EntityArgumentType.getPlayer(context, "destination");
                        
                        target.teleportTo(
                            destination.level(),
                            destination.getX(),
                            destination.getY(),
                            destination.getZ(),
                            destination.getYRot(),
                            destination.getXRot()
                        );
                        
                        context.getSource().sendSuccess(
                            () -> Component.literal("Teleported " + target.getName().getString() + 
                                " to " + destination.getName().getString()),
                            true
                        );
                        
                        return Command.SINGLE_SUCCESS;
                    })))
            .then(Commands.argument("target", EntityArgumentType.player())
                .then(Commands.argument("position", Vec3ArgumentType.vec3())
                    .executes(context -> {
                        ServerPlayer target = EntityArgumentType.getPlayer(context, "target");
                        Vec3 pos = Vec3ArgumentType.getVec3(context, "position");
                        
                        target.teleportTo(
                            target.level(),
                            pos.x, pos.y, pos.z,
                            target.getYRot(),
                            target.getXRot()
                        );
                        
                        context.getSource().sendSuccess(
                            () -> Component.literal("Teleported " + target.getName().getString() + 
                                " to " + String.format("%.2f, %.2f, %.2f", pos.x, pos.y, pos.z)),
                            true
                        );
                        
                        return Command.SINGLE_SUCCESS;
                    })));
    }
}
```

## Command Registration

### Platform-Specific Registration

Register commands through your platform's command registration event:

```java
public class CommandRegistrar {
    public static void registerCommands() {
        // Create command tree
        LiteralArgumentBuilder<CommandSourceStack> root = 
            SimpleCommands.createBaseCommand("mymod");
        
        // Add subcommands
        root.then(ItemCommands.createItemCommand());
        root.then(WorldCommands.createWorldCommand());
        root.then(ConfigCommands.createConfigCommand());
        
        // Register on platform
        registerOnPlatform(root);
    }
    
    // Fabric registration
    private static void registerOnPlatform(LiteralArgumentBuilder<CommandSourceStack> command) {
        // This would be called from your mod initializer
        // The actual registration depends on the platform
    }
}
```

### Client-Side Commands

Create commands that only work on the client:

```java
public class ClientCommands {
    public static void registerClientCommands() {
        if (!Platform.isClient()) return;
        
        LiteralArgumentBuilder<CommandSourceStack> command = 
            Commands.literal("mymodclient")
                .then(Commands.literal("hud")
                    .executes(context -> {
                        // Toggle HUD
                        HudManager.toggle();
                        
                        Minecraft.getInstance().player.sendSystemMessage(
                            Component.literal("HUD " + (HudManager.isEnabled() ? "enabled" : "disabled"))
                        );
                        
                        return Command.SINGLE_SUCCESS;
                    }))
                .then(Commands.literal("particles")
                    .then(Commands.argument("enabled", BoolArgumentType.bool())
                        .executes(context -> {
                            boolean enabled = BoolArgumentType.getBool(context, "enabled");
                            ParticleManager.setEnabled(enabled);
                            
                            Minecraft.getInstance().player.sendSystemMessage(
                                Component.literal("Particles " + (enabled ? "enabled" : "disabled"))
                            );
                            
                            return Command.SINGLE_SUCCESS;
                        })));
        
        // Register client command (platform-specific)
        registerClientCommand(command);
    }
}
```

## Best Practices

### 1. Permission Levels

Always check permissions for administrative commands:

```java
// Good - Check permissions
Commands.literal("admin")
    .requires(source -> source.hasPermission(2)) // Require OP level 2
    .executes(context -> {
        // Admin command logic
    });

// Bad - No permission check
Commands.literal("admin")
    .executes(context -> {
        // Anyone can run this!
    });
```

### 2. Error Handling

Provide clear error messages:

```java
.executes(context -> {
    try {
        // Command logic
        return Command.SINGLE_SUCCESS;
    } catch (Exception e) {
        context.getSource().sendFailure(
            Component.literal("Error: " + e.getMessage())
        );
        return 0;
    }
});
```

### 3. Feedback

Always provide feedback to the user:

```java
// Good - Provide feedback
context.getSource().sendSuccess(
    () -> Component.literal("Command executed successfully!"),
    true
);

// Also notify affected players
target.sendSystemMessage(
    Component.literal("Something happened to you!")
);
```

### 4. Argument Validation

Validate arguments before using them:

```java
.then(Commands.argument("count", IntegerArgumentType.integer(1, 64))
    .executes(context -> {
        int count = IntegerArgumentType.getInteger(context, "count");
        // Count is guaranteed to be between 1 and 64
    }));
```

### 5. Suggestions

Provide helpful suggestions for arguments:

```java
.then(Commands.argument("enchantment", StringArgumentType.word())
    .suggests((context, builder) -> {
        return SharedSuggestionProvider.suggest(
            Arrays.asList("sharpness", "protection", "fire_aspect"),
            builder
        );
    }));
```

The command utilities in Amber provide a foundation for creating cross-platform commands while leveraging Minecraft's powerful Brigadier system.