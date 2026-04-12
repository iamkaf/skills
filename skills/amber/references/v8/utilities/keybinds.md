# Keybind Helpers

Amber provides a utility class for managing keybinds across all mod loaders. The KeybindHelper simplifies the registration of custom keybindings and handles platform differences automatically.

## Overview

The keybind helper includes:

- **Cross-platform registration**: Works consistently on Fabric, Forge, and NeoForge
- **Client-side only**: Automatically handles environment checks
- **Forge compatibility**: Manages Forge-specific event timing requirements
- **Centralized management**: Keeps track of all registered keybinds

## Basic Usage

### Registering a Keybind

Use `KeybindHelper.register()` to register a custom keybind:

```java
import com.iamkaf.amber.api.keymapping.KeybindHelper;
import net.minecraft.client.KeyMapping;
import net.minecraft.client.Minecraft;
import com.mojang.blaze3d.platform.InputConstants;
import net.minecraft.client.KeyMapping;

public class MyModKeybinds {
    // Create keybind instances using KeyMapping constructors
    public static final KeyMapping ABILITY_KEY = new KeyMapping(
        "key.mymod.ability",           // Translation key
        InputConstants.Type.KEYSYM,    // Input type
        InputConstants.KEY_R,          // Key code
        KeyMapping.Category.MISC       // Category
    );
    
    public static final KeyMapping MENU_KEY = new KeyMapping(
        "key.mymod.menu",
        InputConstants.Type.KEYSYM,
        InputConstants.KEY_M,
        KeyMapping.Category.INVENTORY
    );
    
    // Register keybinds
    public static void registerKeybinds() {
        KeybindHelper.register(ABILITY_KEY);
        KeybindHelper.register(MENU_KEY);
    }
    
    // Check if keybind is pressed
    public static void onClientTick() {
        Minecraft mc = Minecraft.getInstance();
        
        // Check if ability key is pressed
        if (ABILITY_KEY.consumeClick()) {
            activateAbility();
        }
        
        // Check if menu key is pressed
        if (MENU_KEY.consumeClick()) {
            toggleMenu();
        }
    }
    
    private static void activateAbility() {
        // Ability logic
    }
    
    private static void toggleMenu() {
        // Menu toggle logic
    }
}
```

### Client-Side Registration

Register keybinds in your client-side initialization:

```java
// For Fabric
@Environment(EnvType.CLIENT)
public class MyModClient implements ClientModInitializer {
    @Override
    public void onInitializeClient() {
        MyModKeybinds.registerKeybinds();
    }
}

// For Forge/NeoForge
@Mod(MyMod.MOD_ID)
public class MyMod {
    public MyMod() {
        // Register on client bus
        FMLJavaModLoadingContext.get().getModEventBus().addListener(this::clientSetup);
    }
    
    @OnlyIn(Dist.CLIENT)
    private void clientSetup(final FMLClientSetupEvent event) {
        MyModKeybinds.registerKeybinds();
    }
}
```

## Advanced Usage

### Keybind with Modifier Keys

KeyMapping doesn't directly support modifier keys in its constructor, but you can check for them in your keybind handler:

```java
public class AdvancedKeybinds {
    public static final KeyMapping DASH_KEY = new KeyMapping(
        "key.mymod.dash",
        InputConstants.Type.KEYSYM,
        InputConstants.KEY_R,
        KeyMapping.Category.MOVEMENT
    );
    
    public static final KeyMapping SPECTATOR_KEY = new KeyMapping(
        "key.mymod.spectator",
        InputConstants.Type.KEYSYM,
        InputConstants.KEY_G,
        KeyMapping.Category.MISC
    );
    
    public static void registerKeybinds() {
        KeybindHelper.register(DASH_KEY);
        KeybindHelper.register(SPECTATOR_KEY);
    }
    
    public static void onClientTick() {
        Minecraft mc = Minecraft.getInstance();
        
        // Check for modifier keys when handling keybind
        if (DASH_KEY.consumeClick()) {
            // Check if Shift is held down
            if (mc.options.keyShift.isDown()) {
                performEnhancedDash();
            } else {
                performDash();
            }
        }
    }
    
    private static void performDash() {
        // Regular dash
    }
    
    private static void performEnhancedDash() {
        // Enhanced dash with Shift
    }
}
```

### Context-Aware Keybinds

Create keybinds that behave differently based on context:

```java
public class ContextKeybinds {
    public static final KeyMapping ACTION_KEY = new KeyMapping(
        "key.mymod.action",
        InputConstants.Type.KEYSYM,
        InputConstants.KEY_F,
        KeyMapping.Category.GAMEPLAY
    );
    
    public static void registerKeybinds() {
        KeybindHelper.register(ACTION_KEY);
    }
    
    public static void onClientTick() {
        Minecraft mc = Minecraft.getInstance();
        
        if (ACTION_KEY.consumeClick()) {
            if (mc.player == null) return;
            
            // Different behavior based on context
            if (mc.player.isSpectator()) {
                toggleSpectatorMode();
            } else if (mc.player.isCreative()) {
                openCreativeMenu();
            } else {
                performAbility();
            }
        }
    }
    
    private static void toggleSpectatorMode() {
        // Spectator mode logic
    }
    
    private static void openCreativeMenu() {
        // Creative menu logic
    }
    
    private static void performAbility() {
        // Regular ability logic
    }
}
```

### Keybind with Toggle State

While KeyMapping doesn't have built-in toggle support, you can implement toggle behavior:

```java
public class ToggleKeybinds {
    public static final KeyMapping TOGGLE_HUD_KEY = new KeyMapping(
        "key.mymod.toggle_hud",
        InputConstants.Type.KEYSYM,
        InputConstants.KEY_H,
        KeyMapping.Category.MISC
    );
    
    private static boolean hudVisible = true;
    
    public static void registerKeybinds() {
        KeybindHelper.register(TOGGLE_HUD_KEY);
    }
    
    public static void onClientTick() {
        if (TOGGLE_HUD_KEY.consumeClick()) {
            hudVisible = !hudVisible;
            
            // Show feedback
            Minecraft.getInstance().player.sendSystemMessage(
                Component.literal("HUD " + (hudVisible ? "enabled" : "disabled"))
            );
        }
    }
    
    public static boolean isHudVisible() {
        return hudVisible;
    }
}
```

## KeyMapping Categories

KeyMapping includes several predefined categories for organizing keybinds:

```java
// Available categories
KeyMapping.Category.MOVEMENT     // Movement controls
KeyMapping.Category.MISC          // Miscellaneous
KeyMapping.Category.MULTIPLAYER   // Multiplayer functions
KeyMapping.Category.GAMEPLAY      // General gameplay
KeyMapping.Category.INVENTORY     // Inventory management
KeyMapping.Category.CREATIVE      // Creative mode
KeyMapping.Category.SPECTATOR     // Spectator mode
```

## Best Practices

### 1. Translation Keys

Always use translation keys for keybind names:

```java
// Good - Uses translation key
public static final KeyMapping ABILITY_KEY = new KeyMapping(
    "key.mymod.ability",           // Translation key
    InputConstants.Type.KEYSYM,    // Input type
    InputConstants.KEY_R,          // Key code
    KeyMapping.Category.MISC       // Category
);

// Bad - Hardcoded strings (not supported by KeyMapping)
```

### 2. Unique Key Codes

Choose key codes that don't conflict with vanilla controls:

```java
// Good - Less commonly used keys
InputConstants.KEY_R              // Reasonably common
InputConstants.KEY_G              // Less common
InputConstants.KEY_H              // Less common

// Avoid - Commonly used keys
InputConstants.KEY_W              // Movement
InputConstants.KEY_A              // Movement
InputConstants.KEY_S              // Movement
InputConstants.KEY_D              // Movement
InputConstants.KEY_SPACE          // Jump
```

### 3. Environment Checks

The KeybindHelper automatically handles client-side checks, but you should still ensure your keybind logic is client-side only:

```java
// Good - Client-side only
@OnlyIn(Dist.CLIENT)
public class MyModKeybinds {
    public static void registerKeybinds() {
        KeybindHelper.register(ABILITY_KEY);
    }
}

// Unnecessary - KeybindHelper already checks environment
public class MyModKeybinds {
    public static void registerKeybinds() {
        if (Platform.isClient()) {  // Not needed
            KeybindHelper.register(ABILITY_KEY);
        }
    }
}
```

### 4. Keybind Storage

Store keybind references for easy access:

```java
// Good - Centralized storage
public class MyModKeybinds {
    public static final KeyMapping ABILITY_KEY = createKeybind("ability", InputConstants.KEY_R);
    public static final KeyMapping MENU_KEY = createKeybind("menu", InputConstants.KEY_M);
    
    private static KeyMapping createKeybind(String name, int key) {
        return new KeyMapping(
            "key.mymod." + name,
            InputConstants.Type.KEYSYM,
            key,
            KeyMapping.Category.MISC
        );
    }
    
    public static void registerKeybinds() {
        KeybindHelper.register(ABILITY_KEY);
        KeybindHelper.register(MENU_KEY);
    }
}
```

## KeyMapping API

The KeyMapping class provides several useful methods:

```java
KeyMapping keybind = new KeyMapping("key.test", InputConstants.Type.KEYSYM, InputConstants.KEY_T, KeyMapping.Category.MISC);

// Check if key is currently pressed
boolean isDown = keybind.isDown();

// Consume a click event (returns true if there was a click to consume)
if (keybind.consumeClick()) {
    // Handle keybind press
}

// Get the keybind name
String name = keybind.getName();

// Get the translated key message
Component keyName = keybind.getTranslatedKeyMessage();

// Check if keybind is unbound
boolean isUnbound = keybind.isUnbound();

// Check if keybind uses default key
boolean isDefault = keybind.isDefault();

// Save keybind configuration
String saveString = keybind.saveString();
```

## Migration from Platform-Specific Keybinds

### From Fabric KeyBindingRegistry

```java
// Old Fabric way
KeyBindingRegistry.registerKeyBinding(new KeyBinding(
    "key.mymod.ability",
    InputUtil.Type.KEYSYM,
    GLFW.GLFW_KEY_R,
    "category.mymod"
));

// New Amber way
public static final KeyMapping ABILITY_KEY = new KeyMapping(
    "key.mymod.ability",
    InputConstants.Type.KEYSYM,
    InputConstants.KEY_R,
    KeyMapping.Category.MISC
);

// In your client initializer
KeybindHelper.register(ABILITY_KEY);
```

### From Forge KeyMapping

```java
// Old Forge way
private static final DeferredRegister<KeyMapping> KEY_BINDINGS = 
    DeferredRegister.create(ForgeRegistries.KEY_MAPPINGS, MOD_ID);

public static final RegistryObject<KeyMapping> ABILITY_KEY = KEY_BINDINGS.register(
    "ability_key",
    () -> new KeyMapping("key.mymod.ability", GLFW.GLFW_KEY_R, "category.mymod")
);

// New Amber way (simpler!)
public static final KeyMapping ABILITY_KEY = new KeyMapping(
    "key.mymod.ability",
    InputConstants.Type.KEYSYM,
    InputConstants.KEY_R,
    KeyMapping.Category.MISC
);

// In your client setup
KeybindHelper.register(ABILITY_KEY);
```

The KeybindHelper abstracts platform differences while providing a simpler API that works across all mod loaders.