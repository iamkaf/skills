# Sound Utilities

Amber provides utilities for playing sounds to players, managing sound events, and creating audio feedback. These utilities help simplify common sound tasks and provide consistent behavior across platforms.

::: warning
Note: The utility classes described here are currently marked as deprecated and will be replaced with versioned alternatives in a future release. They are still functional but consider them as legacy APIs.
:::

## SoundHelper

The `SoundHelper` class provides methods for playing sounds to players.

### Basic Sound Playback

Play sounds to players:

```java
import com.iamkaf.amber.api.sound.SoundHelper;

public class SoundEffects {
    // Play success sound
    public static void playSuccessSound(Player player) {
        SoundHelper.sendClientSound(player, SoundEvents.UI_TOAST_CHALLENGE_COMPLETE);
    }
    
    // Play error sound
    public static void playErrorSound(Player player) {
        SoundHelper.sendClientSound(player, SoundEvents.UI_BUTTON_CLICK);
    }
    
    // Play level up sound
    public static void playLevelUpSound(Player player) {
        SoundHelper.sendClientSound(player, SoundEvents.PLAYER_LEVELUP, SoundSource.MASTER, 1.0f, 1.0f);
    }
    
    // Play custom sound with parameters
    public static void playCustomSound(Player player, SoundEvent sound, float volume, float pitch) {
        SoundHelper.sendClientSound(player, sound, SoundSource.PLAYERS, volume, pitch);
    }
    
    // Play ambient sound
    public static void playAmbientSound(Player player) {
        SoundHelper.sendClientSound(player, SoundEvents.AMBIENT_CAVE, SoundSource.AMBIENT, 0.5f, 1.0f);
    }
    
    // Play note block sound
    public static void playNoteSound(Player player, NoteBlockInstrument instrument, int note) {
        // Calculate pitch from note
        float pitch = (float) Math.pow(2.0, (note - 12) / 12.0);
        
        SoundHelper.sendClientSound(player, 
            SoundEvents.NOTE_BLOCK_HARP.get(), 
            SoundSource.RECORDS, 
            1.0f, 
            pitch);
    }
}
```

### Advanced Sound Control

Control sound playback with more options:

```java
public class AdvancedSoundEffects {
    // Play sound with distance attenuation
    public static void playPositionalSound(Player player, Vec3 position, SoundEvent sound, float maxDistance) {
        // Calculate volume based on distance
        double distance = player.position().distanceTo(position);
        float volume = (float) Math.max(0, 1.0 - (distance / maxDistance));
        
        if (volume > 0) {
            SoundHelper.sendClientSound(player, sound, SoundSource.PLAYERS, volume, 1.0f);
        }
    }
    
    // Play sound with random pitch variation
    public static void playVariablePitchSound(Player player, SoundEvent sound, float basePitch, float variation) {
        Random random = new Random();
        float pitch = basePitch + (random.nextFloat() - 0.5f) * variation;
        
        SoundHelper.sendClientSound(player, sound, SoundSource.PLAYERS, 1.0f, pitch);
    }
    
    // Play sound with fade in/out
    public static void playFadingSound(ServerPlayer player, SoundEvent sound, int fadeInTicks, int durationTicks, int fadeOutTicks) {
        // Initial volume (silently)
        float initialVolume = 0.0f;
        
        // Play initial sound
        SoundHelper.sendClientSound(player, sound, SoundSource.PLAYERS, initialVolume, 1.0f);
        
        // Schedule fade in
        if (fadeInTicks > 0) {
            scheduleFade(player, sound, initialVolume, 1.0f, fadeInTicks);
        }
        
        // Schedule fade out
        if (fadeOutTicks > 0) {
            scheduleFade(player, sound, 1.0f, 0.0f, durationTicks + fadeOutTicks);
        }
    }
    
    private static void scheduleFade(ServerPlayer player, SoundEvent sound, float startVolume, float endVolume, int duration) {
        if (player.level() instanceof ServerLevel serverLevel) {
            // This would require a more complex implementation with custom packets
            // For now, we'll just play the sound at the end volume
            serverLevel.getServer().schedule(() -> {
                SoundHelper.sendClientSound(player, sound, SoundSource.PLAYERS, endVolume, 1.0f);
            }, duration);
        }
    }
    
    // Play sound sequence
    public static void playSoundSequence(Player player, List<SoundEvent> sounds, int intervalTicks) {
        for (int i = 0; i < sounds.size(); i++) {
            final int index = i;
            
            if (player.level() instanceof ServerLevel serverLevel) {
                serverLevel.getServer().schedule(() -> {
                    SoundHelper.sendClientSound(player, sounds.get(index), SoundSource.PLAYERS, 1.0f, 1.0f);
                }, i * intervalTicks);
            }
        }
    }
}
```

## Sound Management

### Sound Categories

Organize sounds by category:

```java
public class SoundCategories {
    // UI sounds
    public static void playUISound(Player player, UISoundType type) {
        SoundEvent sound = switch (type) {
            case SUCCESS -> SoundEvents.UI_TOAST_CHALLENGE_COMPLETE;
            case ERROR -> SoundEvents.UI_BUTTON_CLICK;
            case WARNING -> SoundEvents.BLOCK_NOTE_BLOCK_BIT.get();
            case INFO -> SoundEvents.BLOCK_NOTE_BLOCK_HAT.get();
        };
        
        SoundHelper.sendClientSound(player, sound, SoundSource.UI, 0.5f, 1.0f);
    }
    
    public enum UISoundType {
        SUCCESS, ERROR, WARNING, INFO
    }
    
    // Ambient sounds
    public static void playAmbientSound(Player player, AmbientSoundType type) {
        SoundEvent sound = switch (type) {
            case CAVE -> SoundEvents.AMBIENT_CAVE;
            case UNDERWATER -> SoundEvents.AMBIENT_UNDERWATER_LOOP;
            case NETHER -> SoundEvents.AMBIENT_CRIMSON_FOREST_LOOP;
            case END -> SoundEvents.AMBIENT_THE_END_LOOP;
        };
        
        SoundHelper.sendClientSound(player, sound, SoundSource.AMBIENT, 0.3f, 1.0f);
    }
    
    public enum AmbientSoundType {
        CAVE, UNDERWATER, NETHER, END
    }
    
    // Action sounds
    public static void playActionSound(Player player, ActionSoundType type) {
        SoundEvent sound = switch (type) {
            case PICKUP -> SoundEvents.ITEM_PICKUP;
            case PLACE -> SoundEvents.BLOCK_STONE_PLACE;
            case BREAK -> SoundEvents.BLOCK_STONE_BREAK;
            case HIT -> SoundEvents.ENTITY_PLAYER_HURT;
        };
        
        SoundHelper.sendClientSound(player, sound, SoundSource.PLAYERS, 0.7f, 1.0f);
    }
    
    public enum ActionSoundType {
        PICKUP, PLACE, BREAK, HIT
    }
}
```

### Sound Events

Create and manage custom sound events:

```java
public class CustomSoundEvents {
    // Register custom sound events
    public static final RegistrySupplier<SoundEvent> MAGIC_CAST = 
        DeferredRegister.create("mymod", Registries.SOUND_EVENT)
            .register("magic_cast", () -> SoundEvent.createVariableRangeEvent(
                ResourceLocation.fromNamespaceAndPath("mymod", "magic_cast")));
    
    public static final RegistrySupplier<SoundEvent> MAGIC_EXPLOSION = 
        DeferredRegister.create("mymod", Registries.SOUND_EVENT)
            .register("magic_explosion", () -> SoundEvent.createVariableRangeEvent(
                ResourceLocation.fromNamespaceAndPath("mymod", "magic_explosion")));
    
    public static final RegistrySupplier<SoundEvent> LEVEL_UP_FANFARE = 
        DeferredRegister.create("mymod", Registries.SOUND_EVENT)
            .register("level_up_fanfare", () -> SoundEvent.createVariableRangeEvent(
                ResourceLocation.fromNamespaceAndPath("mymod", "level_up_fanfare")));
    
    // Play custom sounds
    public static void playMagicCast(Player player) {
        SoundHelper.sendClientSound(player, MAGIC_CAST.get(), SoundSource.PLAYERS, 1.0f, 1.0f);
    }
    
    public static void playMagicExplosion(Player player, Vec3 position) {
        // Play at specific position (requires custom implementation)
        SoundHelper.sendClientSound(player, MAGIC_EXPLOSION.get(), SoundSource.PLAYERS, 1.0f, 1.0f);
    }
    
    public static void playLevelUpFanfare(Player player) {
        SoundHelper.sendClientSound(player, LEVEL_UP_FANFARE.get(), SoundSource.MASTER, 0.8f, 1.0f);
    }
    
    // Play sound with random selection
    public static void playRandomMagicSound(Player player) {
        List<SoundEvent> magicSounds = Arrays.asList(
            MAGIC_CAST.get(),
            SoundEvents.ENTITY_EVOKER_CAST_SPELL,
            SoundEvents.ENTITY_ILLUSIONER_CAST_SPELL
        );
        
        SoundEvent sound = magicSounds.get(player.getRandom().nextInt(magicSounds.size()));
        SoundHelper.sendClientSound(player, sound, SoundSource.PLAYERS, 1.0f, 1.0f);
    }
}
```

## Sound Feedback Systems

### Interactive Sound Feedback

Create sound feedback for player interactions:

```java
public class SoundFeedback {
    // Play sound based on interaction result
    public static void playInteractionSound(Player player, InteractionResult result) {
        SoundEvent sound = switch (result) {
            case SUCCESS -> SoundEvents.UI_BUTTON_CLICK;
            case CONSUME -> SoundEvents.ITEM_PICKUP;
            case FAIL -> SoundEvents.BLOCK_NOTE_BLOCK_BASS.get();
            case PASS -> SoundEvents.BLOCK_NOTE_BLOCK_SNARE.get();
            default -> SoundEvents.UI_BUTTON_CLICK;
        };
        
        SoundHelper.sendClientSound(player, sound, SoundSource.UI, 0.5f, 1.0f);
    }
    
    // Play sound for tool durability
    public static void playToolDurabilitySound(Player player, ItemStack tool) {
        float damage = (float) tool.getDamageValue() / tool.getMaxDamage();
        
        if (damage > 0.8f) {
            // Tool almost broken
            SoundHelper.sendClientSound(player, SoundEvents.ENTITY_ITEM_BREAK, SoundSource.PLAYERS, 1.0f, 1.0f);
        } else if (damage > 0.5f) {
            // Tool damaged
            SoundHelper.sendClientSound(player, SoundEvents.BLOCK_STONE_HIT, SoundSource.PLAYERS, 0.5f, 1.0f);
        }
    }
    
    // Play sound for player health
    public static void playHealthSound(Player player) {
        float healthPercentage = player.getHealth() / player.getMaxHealth();
        
        if (healthPercentage < 0.2f) {
            // Critical health
            SoundHelper.sendClientSound(player, SoundEvents.ENTITY_PLAYER_HURT, SoundSource.PLAYERS, 1.0f, 0.8f);
        } else if (healthPercentage < 0.5f) {
            // Low health
            SoundHelper.sendClientSound(player, SoundEvents.BLOCK_NOTE_BLOCK_BIT.get(), SoundSource.PLAYERS, 0.3f, 1.0f);
        }
    }
    
    // Play sound for experience gain
    public static void playExperienceSound(Player player, int experience) {
        if (experience >= 100) {
            // Large amount of experience
            SoundHelper.sendClientSound(player, SoundEvents.ENTITY_PLAYER_LEVELUP, SoundSource.PLAYERS, 1.0f, 1.0f);
        } else if (experience >= 10) {
            // Medium amount of experience
            SoundHelper.sendClientSound(player, SoundEvents.EXPERIENCE_ORB_PICKUP, SoundSource.PLAYERS, 0.8f, 1.2f);
        } else {
            // Small amount of experience
            SoundHelper.sendClientSound(player, SoundEvents.EXPERIENCE_ORB_PICKUP, SoundSource.PLAYERS, 0.5f, 1.0f);
        }
    }
}
```

### Environmental Sounds

Create dynamic environmental sound effects:

```java
public class EnvironmentalSounds {
    // Play biome-specific ambient sounds
    public static void playBiomeAmbientSound(Player player) {
        Level level = player.level();
        BlockPos pos = player.blockPosition();
        
        Biome biome = level.getBiome(pos).value();
        
        if (biome.getBiomeCategory() == Biome.BiomeCategory.NETHER) {
            // Nether sounds
            if (player.getRandom().nextFloat() < 0.1f) {
                SoundHelper.sendClientSound(player, SoundEvents.AMBIENT_NETHER_WASTES_LOOP, 
                    SoundSource.AMBIENT, 0.2f, 1.0f);
            }
        } else if (biome.getBiomeCategory() == Biome.BiomeCategory.THEEND) {
            // End sounds
            if (player.getRandom().nextFloat() < 0.1f) {
                SoundHelper.sendClientSound(player, SoundEvents.AMBIENT_THE_END_LOOP, 
                    SoundSource.AMBIENT, 0.2f, 1.0f);
            }
        }
    }
    
    // Play weather sounds
    public static void playWeatherSound(Player player) {
        Level level = player.level();
        
        if (level.isRaining()) {
            // Rain sounds
            if (player.getRandom().nextFloat() < 0.05f) {
                SoundHelper.sendClientSound(player, SoundEvents.WEATHER_RAIN, 
                    SoundSource.WEATHER, 0.1f, 1.0f);
            }
        }
        
        if (level.isThundering()) {
            // Thunder sounds
            if (player.getRandom().nextFloat() < 0.02f) {
                SoundHelper.sendClientSound(player, SoundEvents.WEATHER_RAIN_ABOVE, 
                    SoundSource.WEATHER, 0.3f, 1.0f);
            }
        }
    }
    
    // Play time-based sounds
    public static void playTimeBasedSound(Player player) {
        Level level = player.level();
        long dayTime = level.getDayTime() % 24000;
        
        // Night sounds
        if (dayTime >= 13000 && dayTime <= 23000) {
            if (player.getRandom().nextFloat() < 0.02f) {
                SoundHelper.sendClientSound(player, SoundEvents.AMBIENT_CAVE, 
                    SoundSource.AMBIENT, 0.1f, 1.0f);
            }
        }
    }
}
```

## Best Practices

### 1. Volume Control

Use appropriate volume levels:

```java
public static void playAppropriateVolumeSound(Player player, SoundEvent sound, SoundSource source) {
    float volume = switch (source) {
        case MASTER -> 1.0f;
        case MUSIC -> 0.7f;
        case RECORDS -> 0.8f;
        case WEATHER -> 0.6f;
        case BLOCKS -> 0.5f;
        case HOSTILE -> 0.7f;
        case NEUTRAL -> 0.6f;
        case PLAYERS -> 0.8f;
        case AMBIENT -> 0.3f;
        case VOICE -> 1.0f;
    };
    
    SoundHelper.sendClientSound(player, sound, source, volume, 1.0f);
}
```

### 2. Pitch Variation

Add slight pitch variation for more natural sounds:

```java
public static void playNaturalSound(Player player, SoundEvent sound) {
    Random random = new Random();
    float pitch = 0.9f + random.nextFloat() * 0.2f; // 0.9 to 1.1
    
    SoundHelper.sendClientSound(player, sound, SoundSource.PLAYERS, 1.0f, pitch);
}
```

### 3. Side Safety

Check which side you're on:

```java
public static void safeSoundPlay(Player player, SoundEvent sound) {
    if (player.level().isClientSide()) {
        // Client-side - play directly
        SoundHelper.sendClientSound(player, sound);
    } else {
        // Server-side - only play to ServerPlayer
        if (player instanceof ServerPlayer) {
            SoundHelper.sendClientSound(player, sound);
        }
    }
}
```

### 4. Performance

Consider performance when playing many sounds:

```java
public static void playSoundToNearbyPlayers(Level level, Vec3 position, SoundEvent sound, double radius) {
    level.getNearbyPlayers(null, new AABB(position).inflate(radius), null)
        .forEach(player -> {
            // Calculate volume based on distance
            double distance = player.position().distanceTo(position);
            float volume = (float) Math.max(0, 1.0 - (distance / radius));
            
            if (volume > 0.1f) { // Only play if audible
                SoundHelper.sendClientSound(player, sound, SoundSource.PLAYERS, volume, 1.0f);
            }
        });
}
```

These sound utilities provide helpful shortcuts for common audio operations while maintaining cross-platform compatibility.