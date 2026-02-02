# Player Utilities

Amber provides utilities for interacting with players, sending messages, and managing player-related operations. These utilities help simplify common player tasks and provide consistent behavior across platforms.

::: warning Deprecated
The `FeedbackHelper` class is **deprecated** and will be removed in Amber 10.0.

Use `com.iamkaf.amber.api.functions.v1.PlayerFunctions` instead. See [Functions API → PlayerFunctions](functions/player) for the new API.
:::

## FeedbackHelper

The `FeedbackHelper` class provides methods for sending messages to players through chat and action bar.

### Chat Messages

Send messages to player chat:

```java
import com.iamkaf.amber.api.player.FeedbackHelper;

public class PlayerMessaging {
    // Send welcome message
    public static void sendWelcomeMessage(Player player) {
        FeedbackHelper.message(player, 
            Component.literal("Welcome to the server!")
                .withStyle(ChatFormatting.GREEN));
    }
    
    // Send error message
    public static void sendErrorMessage(Player player, String error) {
        FeedbackHelper.message(player, 
            Component.literal("Error: " + error)
                .withStyle(ChatFormatting.RED));
    }
    
    // Send info message
    public static void sendInfoMessage(Player player, String info) {
        FeedbackHelper.message(player, 
            Component.literal(info)
                .withStyle(ChatFormatting.GRAY));
    }
    
    // Send success message
    public static void sendSuccessMessage(Player player, String message) {
        FeedbackHelper.message(player, 
            Component.literal("✓ " + message)
                .withStyle(ChatFormatting.GREEN));
    }
    
    // Send warning message
    public static void sendWarningMessage(Player player, String message) {
        FeedbackHelper.message(player, 
            Component.literal("⚠ " + message)
                .withStyle(ChatFormatting.YELLOW));
    }
    
    // Send formatted message with multiple colors
    public static void sendFormattedMessage(Player player) {
        MutableComponent message = Component.literal("")
            .append(Component.literal("[System]").withStyle(ChatFormatting.DARK_GRAY))
            .append(Component.literal(" "))
            .append(Component.literal("Server restart").withStyle(ChatFormatting.YELLOW))
            .append(Component.literal(" in "))
            .append(Component.literal("5 minutes").withStyle(ChatFormatting.RED))
            .append(Component.literal("!"));
        
        FeedbackHelper.message(player, message);
    }
    
    // Send clickable message
    public static void sendClickableMessage(Player player, String text, String command) {
        Component message = Component.literal(text)
            .withStyle(style -> style
                .withColor(ChatFormatting.AQUA)
                .withClickEvent(new ClickEvent(ClickEvent.Action.RUN_COMMAND, command))
                .withHoverEvent(new HoverEvent(HoverEvent.Action.SHOW_TEXT, 
                    Component.literal("Click to run: " + command)))
            );
        
        FeedbackHelper.message(player, message);
    }
}
```

### Action Bar Messages

Send messages to the action bar:

```java
public class ActionBarMessages {
    // Show energy status
    public static void showEnergy(Player player, int energy, int maxEnergy) {
        String percentage = String.format("%.1f", (double) energy / maxEnergy * 100);
        FeedbackHelper.actionBarMessage(player, 
            Component.literal("Energy: " + energy + "/" + maxEnergy + " (" + percentage + "%)")
                .withStyle(ChatFormatting.YELLOW));
    }
    
    // Show cooldown
    public static void showCooldown(Player player, int seconds) {
        FeedbackHelper.actionBarMessage(player, 
            Component.literal("Cooldown: " + seconds + "s")
                .withStyle(ChatFormatting.RED));
    }
    
    // Show status
    public static void showStatus(Player player, String status) {
        FeedbackHelper.actionBarMessage(player, 
            Component.literal(status)
                .withStyle(ChatFormatting.AQUA));
    }
    
    // Show progress
    public static void showProgress(Player player, String task, int current, int total) {
        String percentage = String.format("%.1f", (double) current / total * 100);
        FeedbackHelper.actionBarMessage(player, 
            Component.literal(task + ": " + current + "/" + total + " (" + percentage + "%)")
                .withStyle(ChatFormatting.GREEN));
    }
    
    // Show timed message
    public static void showTimedMessage(Player player, String message, int duration) {
        // Send initial message
        FeedbackHelper.actionBarMessage(player, Component.literal(message));
        
        // Schedule message to clear after duration (server-side only)
        if (player.level() instanceof ServerLevel serverLevel) {
            serverLevel.getServer().schedule(() -> {
                FeedbackHelper.actionBarMessage(player, Component.literal(""));
            }, duration * 20); // Convert seconds to ticks
        }
    }
    
    // Show HUD element
    public static void showHUDElement(Player player) {
        MutableComponent hud = Component.literal("")
            .append(Component.literal("[ ").withStyle(ChatFormatting.DARK_GRAY))
            .append(Component.literal("HP").withStyle(ChatFormatting.RED))
            .append(Component.literal(": ").withStyle(ChatFormatting.DARK_GRAY))
            .append(Component.literal(String.valueOf(player.getHealth())).withStyle(ChatFormatting.WHITE))
            .append(Component.literal(" / ").withStyle(ChatFormatting.DARK_GRAY))
            .append(Component.literal(String.valueOf(player.getMaxHealth())).withStyle(ChatFormatting.WHITE))
            .append(Component.literal(" ]").withStyle(ChatFormatting.DARK_GRAY))
            .append(Component.literal(" "))
            .append(Component.literal("[ ").withStyle(ChatFormatting.DARK_GRAY))
            .append(Component.literal("Food").withStyle(ChatFormatting.GREEN))
            .append(Component.literal(": ").withStyle(ChatFormatting.DARK_GRAY))
            .append(Component.literal(String.valueOf(player.getFoodData().getFoodLevel())).withStyle(ChatFormatting.WHITE))
            .append(Component.literal(" / 20 ]").withStyle(ChatFormatting.DARK_GRAY));
        
        FeedbackHelper.actionBarMessage(player, hud);
    }
}
```

## Advanced Player Operations

### Player Data Management

Manage custom player data and state:

```java
public class PlayerDataManager {
    private static final Map<UUID, PlayerData> playerDataMap = new HashMap<>();
    
    // Store player data
    public static void setPlayerData(Player player, String key, Object value) {
        UUID uuid = player.getUUID();
        PlayerData data = playerDataMap.computeIfAbsent(uuid, id -> new PlayerData());
        data.setData(key, value);
    }
    
    // Get player data
    public static <T> T getPlayerData(Player player, String key, Class<T> type) {
        UUID uuid = player.getUUID();
        PlayerData data = playerDataMap.get(uuid);
        
        if (data != null) {
            return data.getData(key, type);
        }
        
        return null;
    }
    
    // Player data class
    public static class PlayerData {
        private final Map<String, Object> data = new HashMap<>();
        
        public void setData(String key, Object value) {
            data.put(key, value);
        }
        
        @SuppressWarnings("unchecked")
        public <T> T getData(String key, Class<T> type) {
            Object value = data.get(key);
            
            if (value != null && type.isInstance(value)) {
                return (T) value;
            }
            
            return null;
        }
    }
    
    // Example usage
    public static void setPlayerHome(Player player, BlockPos pos) {
        setPlayerData(player, "home", pos);
        FeedbackHelper.message(player, Component.literal("Home set!")
            .withStyle(ChatFormatting.GREEN));
    }
    
    public static BlockPos getPlayerHome(Player player) {
        return getPlayerData(player, "home", BlockPos.class);
    }
    
    public static void teleportToHome(Player player) {
        BlockPos home = getPlayerHome(player);
        
        if (home != null) {
            player.teleportTo(home.getX() + 0.5, home.getY() + 1, home.getZ() + 0.5, 
                player.getYRot(), player.getXRot());
            FeedbackHelper.message(player, Component.literal("Teleported to home!")
                .withStyle(ChatFormatting.GREEN));
        } else {
            FeedbackHelper.message(player, Component.literal("No home set!")
                .withStyle(ChatFormatting.RED));
        }
    }
}
```

### Player Effects and Abilities

Apply and manage player effects:

```java
public class PlayerEffects {
    // Apply effect with feedback
    public static void applyEffect(Player player, MobEffect effect, int duration, int amplifier) {
        player.addEffect(new MobEffectInstance(effect, duration, amplifier));
        
        Component effectName = effect.getDisplayName().copy();
        FeedbackHelper.message(player, Component.literal("Applied: " + effectName.getString())
            .withStyle(ChatFormatting.GREEN));
    }
    
    // Apply temporary ability
    public static void applyFlight(Player player, int duration) {
        player.getAbilities().mayfly = true;
        player.onUpdateAbilities();
        
        FeedbackHelper.actionBarMessage(player, 
            Component.literal("Flight enabled for " + duration/20 + " seconds")
                .withStyle(ChatFormatting.AQUA));
        
        // Schedule ability removal
        if (player.level() instanceof ServerLevel serverLevel) {
            serverLevel.getServer().schedule(() -> {
                player.getAbilities().mayfly = false;
                player.getAbilities().flying = false;
                player.onUpdateAbilities();
                
                if (player.isAlive()) {
                    FeedbackHelper.actionBarMessage(player, 
                        Component.literal("Flight disabled")
                            .withStyle(ChatFormatting.RED));
                }
            }, duration);
        }
    }
    
    // Heal player with feedback
    public static void healPlayer(Player player, float amount) {
        float oldHealth = player.getHealth();
        player.heal(amount);
        float newHealth = player.getHealth();
        
        float actualHealed = newHealth - oldHealth;
        
        if (actualHealed > 0) {
            FeedbackHelper.actionBarMessage(player, 
                Component.literal("+" + String.format("%.1f", actualHealed) + " HP")
                    .withStyle(ChatFormatting.RED));
        }
    }
    
    // Apply saturation
    public static void feedPlayer(Player player, int foodLevel, float saturation) {
        FoodData foodData = player.getFoodData();
        
        int oldFood = foodData.getFoodLevel();
        foodData.setFoodLevel(foodLevel);
        foodData.setSaturation(saturation);
        
        int foodGained = foodLevel - oldFood;
        
        if (foodGained > 0) {
            FeedbackHelper.actionBarMessage(player, 
                Component.literal("+" + foodGained + " Food")
                    .withStyle(ChatFormatting.GREEN));
        }
    }
}
```

### Player Permissions and Checks

Check player permissions and capabilities:

```java
public class PlayerPermissions {
    // Check if player has permission
    public static boolean hasPermission(Player player, String permission, int level) {
        if (player instanceof ServerPlayer serverPlayer) {
            return serverPlayer.hasPermissions(level);
        }
        
        // Client-side fallback
        return false;
    }
    
    // Execute command with permission check
    public static void executeWithPermission(Player player, String command, int level, Runnable action) {
        if (hasPermission(player, command, level)) {
            action.run();
        } else {
            FeedbackHelper.message(player, Component.literal(
                "You don't have permission to use this command!")
                .withStyle(ChatFormatting.RED));
        }
    }
    
    // Check if player is in creative mode
    public static boolean isCreative(Player player) {
        return player.getAbilities().instabuild;
    }
    
    // Check if player is operator
    public static boolean isOperator(Player player) {
        if (player instanceof ServerPlayer serverPlayer) {
            return serverPlayer.getServer().getPlayerList().isOp(serverPlayer.getGameProfile());
        }
        
        return false;
    }
    
    // Check if player can fly
    public static boolean canFly(Player player) {
        return player.getAbilities().mayfly || player.getAbilities().flying;
    }
    
    // Get player's effective permission level
    public static int getPermissionLevel(Player player) {
        if (player instanceof ServerPlayer serverPlayer) {
            return serverPlayer.getServer().getOperatorUserPermissionLevel(serverPlayer.getGameProfile());
        }
        
        return 0;
    }
}
```

### Player Location and Teleportation

Manage player location and teleportation:

```java
public class PlayerLocation {
    // Save player location
    public static void saveLocation(Player player, String name) {
        BlockPos pos = player.blockPosition();
        ResourceKey<Level> dimension = player.level().dimension();
        
        LocationData location = new LocationData(pos, dimension);
        PlayerDataManager.setPlayerData(player, "location_" + name, location);
        
        FeedbackHelper.message(player, Component.literal("Location '" + name + "' saved!")
            .withStyle(ChatFormatting.GREEN));
    }
    
    // Load player location
    public static void loadLocation(Player player, String name) {
        LocationData location = PlayerDataManager.getPlayerData(player, "location_" + name, LocationData.class);
        
        if (location != null) {
            teleportPlayer(player, location.position(), location.dimension());
            FeedbackHelper.message(player, Component.literal("Teleported to '" + name + "'!")
                .withStyle(ChatFormatting.GREEN));
        } else {
            FeedbackHelper.message(player, Component.literal("Location '" + name + "' not found!")
                .withStyle(ChatFormatting.RED));
        }
    }
    
    // Teleport player safely
    public static void teleportPlayer(Player player, BlockPos pos, ResourceKey<Level> dimension) {
        if (player.level().dimension() == dimension) {
            // Same dimension - teleport directly
            player.teleportTo(pos.getX() + 0.5, pos.getY() + 1, pos.getZ() + 0.5, 
                player.getYRot(), player.getXRot());
        } else {
            // Different dimension - find server level and teleport
            if (player.level() instanceof ServerLevel serverLevel) {
                ServerLevel targetLevel = serverLevel.getServer().getLevel(dimension);
                
                if (targetLevel != null) {
                    player.teleportTo(targetLevel, pos.getX() + 0.5, pos.getY() + 1, pos.getZ() + 0.5, 
                        player.getYRot(), player.getXRot());
                } else {
                    FeedbackHelper.message(player, Component.literal("Dimension not found!")
                        .withStyle(ChatFormatting.RED));
                }
            }
        }
    }
    
    // Location data class
    public static class LocationData {
        private final BlockPos position;
        private final ResourceKey<Level> dimension;
        
        public LocationData(BlockPos position, ResourceKey<Level> dimension) {
            this.position = position;
            this.dimension = dimension;
        }
        
        public BlockPos position() { return position; }
        public ResourceKey<Level> dimension() { return dimension; }
    }
    
    // Get distance between players
    public static double getDistance(Player player1, Player player2) {
        return player1.distanceToSqr(player2);
    }
    
    // Find nearest player
    public static Player findNearestPlayer(Player center, double maxDistance) {
        return center.level().getNearestPlayer(center, maxDistance);
    }
    
    // Get all players within radius
    public static List<Player> getPlayersInRadius(Player center, double radius) {
        return center.level().getEntitiesOfClass(Player.class, 
            new AABB(center.blockPosition()).inflate(radius),
            player -> player != center);
    }
}
```

## Best Practices

### 1. Side Safety

Always check which side you're on:

```java
public static void safeMessage(Player player, Component message) {
    if (player.level().isClientSide()) {
        // Client-side only
        player.displayClientMessage(message, false);
    } else {
        // Server-side
        FeedbackHelper.message(player, message);
    }
}
```

### 2. Null Safety

Check for null values when working with players:

```java
public static void safePlayerOperation(Player player) {
    if (player == null || !player.isAlive()) {
        return;
    }
    
    // Safe player operation
}
```

### 3. Performance

Consider performance when affecting many players:

```java
public static void broadcastToAll(ServerLevel level, Component message) {
    for (ServerPlayer player : level.getServer().getPlayerList().getPlayers()) {
        if (player.level() == level) {
            FeedbackHelper.message(player, message);
        }
    }
}
```

### 4. Validation

Validate player operations:

```java
public static boolean safeTeleport(Player player, BlockPos pos) {
    // Check if position is safe
    BlockState state = player.level().getBlockState(pos);
    
    if (!state.isAir() && !state.getCollisionShape(player.level(), pos).isEmpty()) {
        FeedbackHelper.message(player, Component.literal("Cannot teleport - unsafe location!")
            .withStyle(ChatFormatting.RED));
        return false;
    }
    
    // Perform teleport
    player.teleportTo(pos.getX() + 0.5, pos.getY() + 1, pos.getZ() + 0.5, 
        player.getYRot(), player.getXRot());
    return true;
}
```

These player utilities provide helpful shortcuts for common player operations while maintaining cross-platform compatibility.