# Event System

Amber provides a comprehensive event system that works consistently across Fabric, Forge, and NeoForge. The events are designed to be simple to use while providing powerful hooks into Minecraft's game loop.

## Overview

The event system includes:

- **Player Events**: Player interactions, joining/leaving, respawning, shield blocking
- **Block Events**: Block breaking, placing, interaction
- **Item Events**: Item dropping, picking up
- **Entity Events**: Entity spawning, death, damage
- **Animal Events**: Animal taming, breeding
- **Farming Events**: Crop growth, bone meal usage
- **Command Events**: Server command registration
- **Loot Events**: Loot table modification
- **Creative Mode Tab Events**: Adding items to existing creative tabs
- **World Events**: World loading, unloading, saving
- **Weather Events**: Lightning strikes
- **Server Tick Events**: Server tick start/end (server-side only)
- **Client Events**: Rendering, input, HUD, tick events (client-side only)

## Player Events

Player events provide hooks for player-related actions and state changes.

### ENTITY_INTERACT

Fired when a player interacts with (right-clicks) an entity.

```java
PlayerEvents.ENTITY_INTERACT.register((player, level, hand, entity) -> {
    // Check if player is holding a special item
    ItemStack stack = player.getItemInHand(hand);
    if (stack.is(MyItems.MAGIC_WAND.get())) {
        // Cast a spell on the entity
        if (entity instanceof LivingEntity living) {
            living.addEffect(new MobEffectInstance(MobEffects.GLOWING, 200));
        }
        return InteractionResult.SUCCESS; // Cancel default interaction
    }
    return InteractionResult.PASS; // Allow default interaction
});
```

### PLAYER_JOIN

Fired when a player joins the server.

```java
PlayerEvents.PLAYER_JOIN.register((player) -> {
    // Send welcome message
    player.sendSystemMessage(Component.literal("Welcome to the server!"));
    
    // Give new players a starter kit
    if (!player.getInventory().hasAnyOf(Set.of(Items.OAK_LOG))) {
        player.getInventory().add(new ItemStack(Items.OAK_LOG, 16));
        player.getInventory().add(new ItemStack(Items.APPLE, 4));
    }
    
    // Log join event
    Constants.LOG.info("{} joined the server", player.getName().getString());
});
```

### PLAYER_LEAVE

Fired when a player leaves the server.

```java
PlayerEvents.PLAYER_LEAVE.register((player) -> {
    // Save player-specific data
    PlayerData.save(player.getUUID());
    
    // Log leave event
    Constants.LOG.info("{} left the server", player.getName().getString());
});
```

### PLAYER_RESPAWN

Fired after a player respawns (from death or leaving the End).

```java
PlayerEvents.PLAYER_RESPAWN.register((oldPlayer, newPlayer, alive) -> {
    if (!alive) {
        // Player died and respawned
        newPlayer.sendSystemMessage(Component.literal("Don't die again!"));
        
        // Give respawn protection
        newPlayer.addEffect(new MobEffectInstance(
            MobEffects.DAMAGE_RESISTANCE, 100, 4
        ));
    } else {
        // Player respawned from leaving the End
        newPlayer.sendSystemMessage(Component.literal("Welcome back from the End!"));
    }
});
```

### CRAFT_ITEM

Fired when a player crafts an item using a crafting table or other crafting mechanism.

```java
PlayerEvents.CRAFT_ITEM.register((player, craftedItems) -> {
    // Calculate total items crafted
    int totalItems = craftedItems.stream().mapToInt(ItemStack::getCount).sum();

    // Award experience for crafting (example use case)
    if (totalItems > 0) {
        player.giveExperienceLevels(totalItems);
        player.sendSystemMessage(Component.literal("Gained " + totalItems + " levels from crafting!"));
    }

    // Log crafting for analytics
    Constants.LOG.info("{} crafted {} items",
        player.getName().getString(), totalItems);
});
```

### SHIELD_BLOCK

Fired when a player successfully blocks damage with a shield. This event fires on both client and server.

```java
PlayerEvents.SHIELD_BLOCK.register((player, shield, blockedDamage, source) -> {
    // Track shield blocking for leveling systems
    ShieldLeveling.addExperience(player, (int)blockedDamage);

    // Custom shield effects
    if (shield.getItem() == MyItems.MAGIC_SHIELD.get()) {
        // Reflect damage back to attacker
        if (source.getEntity() instanceof LivingEntity attacker) {
            attacker.hurt(player.damageSources().magic(), blockedDamage * 0.5F);
        }
    }

    // Shield durability management
    if (shouldReduceDurability(shield, source)) {
        shield.hurtAndBreak(1, player, (p) -> {
            p.broadcastBreakEvent(net.minecraft.world.InteractionHand.MAIN_HAND);
        });
    }

    // Log shield blocks for analytics
    Constants.LOG.info("{} blocked {} damage from {} using {}",
        player.getName().getString(),
        blockedDamage,
        source.getMsgId(),
        shield.getItem().getDescriptionId());
});
```

## Block Events

Block events provide hooks for block-related interactions and changes.

### BLOCK_BREAK_BEFORE

Fired before a block is broken. Can be cancelled to prevent breaking.

```java
BlockEvents.BLOCK_BREAK_BEFORE.register((level, player, pos, state, blockEntity) -> {
    // Prevent breaking certain blocks in protected areas
    if (isProtectedArea(level, pos)) {
        player.sendSystemMessage(Component.literal("This area is protected!"));
        return InteractionResult.FAIL; // Cancel block breaking
    }
    
    // Check for special tool requirements
    if (state.getBlock() == MyBlocks.MAGIC_ORE.get()) {
        ItemStack tool = player.getMainHandItem();
        if (!tool.is(MyItems.MAGIC_PICKAXE.get())) {
            player.sendSystemMessage(Component.literal("You need a magic pickaxe!"));
            return InteractionResult.FAIL; // Cancel block breaking
        }
    }
    
    return InteractionResult.PASS; // Allow breaking
});
```

### BLOCK_BREAK_AFTER

Fired after a block has been broken.

```java
BlockEvents.BLOCK_BREAK_AFTER.register((level, player, pos, state, blockEntity) -> {
    // Handle special block breaking effects
    if (state.getBlock() == MyBlocks.EXPLOSIVE_ORE.get()) {
        // Create explosion after breaking
        level.explode(null, pos.getX(), pos.getY(), pos.getZ(), 3.0F, 
            Level.ExplosionInteraction.BLOCK);
    }
    
    // Track statistics
    if (player instanceof ServerPlayer serverPlayer) {
        MyStats.incrementBlocksMined(serverPlayer, state.getBlock());
    }
    
    // Spawn particles
    level.addParticle(ParticleTypes.CRIT, 
        pos.getX() + 0.5, pos.getY() + 0.5, pos.getZ() + 0.5,
        0, 0, 0);
});
```

### BLOCK_PLACE

Fired when a player places a block. Can be cancelled.

```java
BlockEvents.BLOCK_PLACE.register((level, player, pos, state, context) -> {
    // Prevent placing blocks in protected areas
    if (isProtectedArea(level, pos)) {
        player.sendSystemMessage(Component.literal("Cannot place blocks here!"));
        return InteractionResult.FAIL;
    }
    
    // Check for special placement conditions
    if (state.getBlock() == MyBlocks.MAGIC_PLANT.get()) {
        // Only allow placing on specific blocks
        BlockState below = level.getBlockState(pos.below());
        if (!below.is(BlockTags.DIRT)) {
            player.sendSystemMessage(Component.literal("Magic plants need dirt!"));
            return InteractionResult.FAIL;
        }
    }
    
    return InteractionResult.PASS;
});
```

### BLOCK_INTERACT

Fired when a player right-clicks on a block.

```java
BlockEvents.BLOCK_INTERACT.register((player, level, hand, hitResult) -> {
    BlockPos pos = hitResult.getBlockPos();
    BlockState state = level.getBlockState(pos);
    
    // Custom block interactions
    if (state.is(MyBlocks.MAGIC_BLOCK.get())) {
        if (!level.isClientSide()) {
            // Toggle magic block state
            boolean powered = state.getValue(MagicBlockBlock.POWERED);
            level.setBlock(pos, state.setValue(MagicBlockBlock.POWERED, !powered), 3);
            
            // Play sound
            level.playSound(null, pos, SoundEvents.LEVER_CLICK, 
                SoundSource.BLOCKS, 1.0F, 1.0F);
        }
        return InteractionResult.SUCCESS; // Cancel default interaction
    }
    
    return InteractionResult.PASS;
});
```

### BLOCK_CLICK

Fired when a player left-clicks (attacks/punches) a block.

```java
BlockEvents.BLOCK_CLICK.register((player, level, hand, pos, direction) -> {
    BlockState state = level.getBlockState(pos);

    // Custom block clicking behavior
    if (state.is(MyBlocks.HARD_BLOCK.get())) {
        // Check if player has the right tool
        ItemStack stack = player.getItemInHand(hand);
        if (!stack.is(MyItems.HEAVY_PICKAXE.get())) {
            player.sendSystemMessage(Component.literal("You need a heavy pickaxe!"));
            return InteractionResult.FAIL; // Cancel the click
        }
    }

    // Track mining statistics
    if (player instanceof ServerPlayer serverPlayer) {
        MiningStats.trackBlockClick(serverPlayer, state.getBlock());
    }

    return InteractionResult.PASS;
});
```

## Item Events

Item events provide hooks for item-related actions.

### ITEM_DROP

Fired when a player drops an item (informational only).

```java
ItemEvents.ITEM_DROP.register((player, itemEntity) -> {
    ItemStack stack = itemEntity.getItem();
    
    // Log valuable item drops
    if (stack.getItem() == Items.DIAMOND) {
        Constants.LOG.info("{} dropped {} diamonds at {}", 
            player.getName().getString(), 
            stack.getCount(),
            itemEntity.blockPosition());
    }
    
    // Apply special effects to certain items
    if (stack.is(MyItems.CURSED_ITEM.get())) {
        // Apply curse to player
        player.addEffect(new MobEffectInstance(
            MobEffects.UNLUCK, 6000, 0));
    }
});
```

### ITEM_PICKUP

Fired when a player picks up an item (informational only).

```java
ItemEvents.ITEM_PICKUP.register((player, itemEntity, itemStack) -> {
    // Track item collection achievements
    if (itemStack.getItem() == Items.DIAMOND) {
        PlayerProgress.trackDiamondsCollected(player, itemStack.getCount());
    }
    
    // Special pickup effects
    if (itemStack.is(MyItems.MAGIC_ORB.get())) {
        // Restore mana/energy
        if (player instanceof ServerPlayer serverPlayer) {
            PlayerMana.restore(serverPlayer, 50);
            player.sendSystemMessage(Component.literal("Mana restored!"));
        }
    }
});
```

### MODIFY_DEFAULT_COMPONENTS

Fired when default data components for items are being registered. This event is informational only and cannot be cancelled.

```java
ItemEvents.MODIFY_DEFAULT_COMPONENTS.register((context) -> {
    // Add default enchantment to items
    context.modify(Items.DIAMOND_SWORD, (builder) -> {
        builder.set(DataComponents.ENCHANTMENTS, new ItemEnchantments(
            new EnchantmentInstance(Enchantments.SHARPNESS, 2)
        ));
    });

    // Add custom damage value to items
    context.modify(MyItems.SPECIAL_ITEM.get(), (builder) -> {
        builder.set(MyDataComponents.DAMAGE_VALUE, 10);
    });

    // Add custom color to leather armor
    context.modify(Items.LEATHER_HELMET, (builder) -> {
        builder.set(DataComponents.DYED_COLOR, new DyedItemColor(0xFF0000, false));
    });
});
```

## Entity Events

Entity events provide hooks for entity-related actions.

### ENTITY_SPAWN

Fired when an entity spawns in the world.

```java
EntityEvents.ENTITY_SPAWN.register((entity, level) -> {
    // Modify spawning conditions
    if (entity instanceof Zombie zombie) {
        // Give zombies random armor in hard mode
        if (level.getDifficulty() == Difficulty.HARD && level.random.nextFloat() < 0.3F) {
            zombie.setItemSlot(EquipmentSlot.CHEST, new ItemStack(Items.LEATHER_CHESTPLATE));
        }
    }

    // Track entity spawning for analytics
    if (level instanceof ServerLevel serverLevel) {
        SpawnTracker.recordSpawn(serverLevel, entity.getType(), entity.blockPosition());
    }
});
```

### ENTITY_DEATH

Fired when a living entity dies.

```java
EntityEvents.ENTITY_DEATH.register((entity, source) -> {
    // Log death events
    Constants.LOG.info("{} died from {}", entity.getName().getString(), source.getMsgId());

    // Handle special death effects
    if (entity instanceof WitherBoss wither) {
        // Create explosion when wither dies
        wither.level().explode(null, wither.getX(), wither.getY(), wither.getZ(),
            5.0F, Level.ExplosionInteraction.MOB);
    }

    // Drop custom items on death
    if (entity instanceof Player player && source.getEntity() instanceof Player killer) {
        // Drop player head when killed by another player
        player.spawnAtLocation(new ItemStack(Items.PLAYER_HEAD));
    }

    // Track kills for advancement systems
    if (source.getEntity() instanceof ServerPlayer killer) {
        KillTracker.trackKill(killer, entity.getType());
    }
});
```

### ENTITY_DAMAGE

Fired when an entity takes damage, before damage is applied. Can be cancelled.

```java
EntityEvents.ENTITY_DAMAGE.register((entity, source, amount) -> {
    // Reduce damage from specific sources
    if (source.is(DamageTypes.ON_FIRE) && entity.hasEffect(MobEffects.FIRE_RESISTANCE)) {
        return InteractionResult.FAIL; // Cancel fire damage completely
    }

    // Implement custom damage reduction
    if (entity instanceof Player player) {
        ItemStack helmet = player.getItemBySlot(EquipmentSlot.HEAD);
        if (helmet.is(MyItems.PROTECTION_HELMET.get())) {
            // Reduce damage by 50% when wearing protection helmet
            float newDamage = amount * 0.5F;
            entity.hurt(source, newDamage);
            return InteractionResult.FAIL; // Cancel original damage
        }
    }

    // Prevent friendly fire
    if (entity instanceof Player victim && source.getEntity() instanceof Player attacker) {
        if (areTeammates(victim, attacker)) {
            attacker.sendSystemMessage(Component.literal("You cannot hurt your teammates!"));
            return InteractionResult.FAIL; // Cancel damage
        }
    }

    return InteractionResult.PASS; // Allow damage to proceed
});
```

### AFTER_DAMAGE

Fired after a living entity took damage, unless they were killed. The base damage taken is given as damage taken before armor or enchantments are applied, but after other effects like shields are applied.

```java
EntityEvents.AFTER_DAMAGE.register((entity, source, baseDamageTaken, damageTaken, blocked) -> {
    // Track damage for leveling systems
    if (entity instanceof ServerPlayer player) {
        CombatLeveling.addExperience(player, (int)damageTaken);
    }

    // Handle thorns damage reflection
    if (!blocked && entity instanceof LivingEntity living) {
        ItemStack chestplate = living.getItemBySlot(EquipmentSlot.CHEST);
        if (chestplate.is(Items.DIAMOND_CHESTPLATE) && chestplate.hasEnchantments()) {
            int thornsLevel = EnchantmentHelper.getEnchantmentLevel(
                Enchantments.THORNS, chestplate);
            if (thornsLevel > 0 && source.getEntity() instanceof LivingEntity attacker) {
                // Reflect damage back to attacker
                attacker.hurt(entity.damageSources().thorns(attacker), thornsLevel * 1.5F);
            }
        }
    }

    // Log damage events
    if (entity instanceof Player player) {
        Constants.LOG.info("Player took {} damage (base: {}, blocked: {})",
            damageTaken, baseDamageTaken, blocked);
    }
});
```

## Animal Events

Animal events provide hooks for animal taming and breeding.

### ANIMAL_TAME

Fired when an animal is being tamed. Can be cancelled or used to implement custom taming logic.

```java
AnimalEvents.ANIMAL_TAME.register((animal, player) -> {
    // Require special items for taming
    ItemStack stack = player.getMainHandItem();
    if (stack.is(Items.WHEAT)) {
        player.sendSystemMessage(Component.literal("This animal needs something special!"));
        return InteractionResult.FAIL; // Cancel taming
    }

    // Implement custom taming mechanics
    if (stack.is(MyItems.MAGIC_TREAT.get())) {
        animal.tame(player);
        animal.setCustomName(Component.literal("Tamed " + animal.getName().getString()));
        return InteractionResult.SUCCESS; // Cancel vanilla taming (already handled)
    }

    // Bonus: auto-sit after taming
    if (animal instanceof Wolf wolf && !wolf.isTame()) {
        wolf.tame(player);
        wolf.setInSittingPose(true);
        wolf.level().playSound(null, wolf, SoundEvents.WOLF_WHINE,
            SoundSource.NEUTRAL, 1.0F, 1.0F);
        return InteractionResult.SUCCESS;
    }

    return InteractionResult.PASS; // Allow default taming
});
```

### ANIMAL_BREED

Fired when a baby animal is spawned from breeding. This is informational and cannot be cancelled.

```java
AnimalEvents.ANIMAL_BREED.register((parentA, parentB, baby) -> {
    // Track breeding for analytics
    Constants.LOG.info("Baby {} born from {} and {}",
        baby.getType().getDescriptionId(),
        parentA.getUUID(),
        parentB.getUUID());

    // Give baby animals special traits
    if (parentA instanceof Wolf || parentB instanceof Wolf) {
        // Baby wolf gets extra speed
        baby.getAttribute(Attributes.MOVEMENT_SPEED).setBaseValue(
            baby.getAttribute(Attributes.MOVEMENT_SPEED).getBaseValue() * 1.2F
        );
    }

    // Apply genetic traits from parents
    if (parentA instanceof Sheep sheepA && parentB instanceof Sheep) {
        // Baby inherits parent's color or gets a mix
        DyeColor colorA = sheepA.getColor();
        DyeColor colorB = ((Sheep) parentB).getColor();
        DyeColor babyColor = Math.random() < 0.5 ? colorA : colorB;
        ((Sheep) baby).setColor(babyColor);
    }

    // Special effects for rare breeding combinations
    if (parentA.getType() == EntityType.HORSE && parentB.getType() == EntityType.HORSE) {
        // Check for special breeding combinations
        if (hasGoldenApple(parentA) && hasGoldenApple(parentB)) {
            baby.setAttribute(BaseAttributes.GENERIC_FOLLOW_RANGE, 48.0);
        }
    }
});
```

## Farming Events

Farming events provide hooks for agriculture-related actions.

### BONE_MEAL_USE

Fired when bone meal is used on a block.

```java
FarmingEvents.BONE_MEAL_USE.register((level, pos, state, stack, entity) -> {
    // Custom bone meal effects
    if (state.is(MyBlocks.MAGIC_CROP.get())) {
        if (!level.isClientSide()) {
            // Magic crops grow instantly with bone meal
            ((BonemealableBlock) state.getBlock()).performBonemeal(
                (ServerLevel) level, level.random, pos, state);

            // Consume extra bone meal for magic effect
            if (entity instanceof Player player && !player.getAbilities().instabuild) {
                stack.shrink(1);
            }

            // Create particle effect
            for (int i = 0; i < 10; i++) {
                level.addParticle(ParticleTypes.HAPPY_VILLAGER,
                    pos.getX() + level.random.nextDouble(),
                    pos.getY() + level.random.nextDouble(),
                    pos.getZ() + level.random.nextDouble(),
                    0, 0, 0);
            }
        }
        return InteractionResult.SUCCESS; // Cancel default bone meal behavior
    }

    return InteractionResult.PASS;
});
```

### FARMLAND_TRAMPLE

Fired when an entity tramples farmland. Can be cancelled to prevent the farmland from turning to dirt.

```java
FarmingEvents.FARMLAND_TRAMPLE.register((level, pos, state, fallDistance, entity) -> {
    // Prevent farmland trampling by specific entities
    if (entity instanceof Player player) {
        // Check if player has special boots
        ItemStack boots = player.getItemBySlot(EquipmentSlot.FEET);
        if (boots.is(MyItems.FARMER_BOOTS.get())) {
            return InteractionResult.FAIL; // Prevent trampling
        }
    }

    // Prevent farmland trampling for animals in protected areas
    if (entity instanceof Animal && isProtectedArea(level, pos)) {
        return InteractionResult.FAIL; // Prevent trampling
    }

    // Allow trampling for heavy entities (like iron golems)
    if (fallDistance > 2.0F) {
        return InteractionResult.PASS; // Allow trampling
    }

    return InteractionResult.PASS;
});
```

### CROP_GROW

Fired when a crop attempts to grow. Can be cancelled to prevent growth.

```java
FarmingEvents.CROP_GROW.register((level, pos, state) -> {
    // Accelerate crop growth in specific biomes
    if (level.getBiome(pos).is(MyBiomes.FERTILE_LANDS)) {
        // Apply growth boost logic
        if (level.random.nextFloat() < 0.3F) {
            // Trigger additional growth tick
            level.scheduleTick(pos, state.getBlock(), 1);
        }
    }

    // Prevent crop growth in cursed areas
    if (isCursedArea(level, pos)) {
        return InteractionResult.FAIL; // Cancel growth
    }

    // Modify growth based on nearby blocks
    if (hasGrowthAccelerator(level, pos)) {
        // Force immediate growth
        state.randomTick((ServerLevel) level, pos, level.random);
        return InteractionResult.SUCCESS; // Cancel vanilla growth (custom applied)
    }

    return InteractionResult.PASS;
});
```

## Loot Events

Loot events provide hooks for modifying loot tables when they are loaded.

### MODIFY

Fired when a loot table is loaded, allowing you to add additional loot pools to it.

```java
LootEvents.MODIFY.register((lootTable, addPool) -> {
    // Add items to vanilla chest loot tables
    if (lootTable.equals(ResourceLocation.fromNamespaceAndPath("minecraft", "chests/simple_dungeon"))) {
        addPool.accept(LootPool.lootPool()
            .setRolls(UniformGenerator.between(1, 3))
            .add(LootItem.lootTableItem(MyItems.RARE_SWORD.get())
                .setWeight(1))
            .add(LootItem.lootTableItem(MyItems.MAGIC_COIN.get())
                .setWeight(5)
                .apply(SetItemCountFunction.setCount(UniformGenerator.between(2, 6))))
        );
    }

    // Add bonus drops to entity loot
    if (lootTable.equals(ResourceLocation.fromNamespaceAndPath("minecraft", "entities/zombie"))) {
        addPool.accept(LootPool.lootPool()
            .setRolls(UniformGenerator.between(0, 1))
            .add(LootItem.lootTableItem(MyItems.ZOMBIE_ESSENCE.get())
                .setWeight(10))
        );
    }

    // Add rare loot to fishing
    if (lootTable.equals(ResourceLocation.fromNamespaceAndPath("minecraft", "gameplay/fishing"))) {
        addPool.accept(LootPool.lootPool()
            .setRolls(UniformGenerator.between(0, 1))
            .add(LootItem.lootTableItem(MyItems.MAGIC_FISHING_ROD.get())
                .setWeight(1)
                .apply(EnchantRandomlyFunction.randomEnchantment()))
        );
    }
});
```

Common loot table identifiers you might want to modify:

```java
// Chest loot tables
ResourceLocation.fromNamespaceAndPath("minecraft", "chests/simple_dungeon")
ResourceLocation.fromNamespaceAndPath("minecraft", "chests/village/village_weaponsmith")
ResourceLocation.fromNamespaceAndPath("minecraft", "chests/village/village_armorer")
ResourceLocation.fromNamespaceAndPath("minecraft", "chests/desert_pyramid")
ResourceLocation.fromNamespaceAndPath("minecraft", "chests/stronghold_corridor")

// Entity loot tables
ResourceLocation.fromNamespaceAndPath("minecraft", "entities/zombie")
ResourceLocation.fromNamespaceAndPath("minecraft", "entities/skeleton")
ResourceLocation.fromNamespaceAndPath("minecraft", "entities/creeper")
ResourceLocation.fromNamespaceAndPath("minecraft", "entities/ender_dragon")

// Gameplay loot tables
ResourceLocation.fromNamespaceAndPath("minecraft", "gameplay/fishing")
```

## Command Events

Command events allow you to register custom commands during server initialization.

### REGISTER

Fired when the server is registering commands. This is where you should register your mod's custom commands.

```java
CommandEvents.EVENT.register((dispatcher, registryAccess, environment) -> {
    // Register a simple command
    dispatcher.register(Commands.literal("hello")
        .executes(context -> {
            context.getSource().sendSuccess(() -> Component.literal("Hello, world!"), true);
            return 1;
        })
    );

    // Register a command with arguments
    dispatcher.register(Commands.literal("giveitem")
        .then(Commands.argument("item", ItemArgument.item(context))
            .executes(context -> {
                ServerPlayer player = context.getSource().getPlayerOrException();
                ItemStack stack = ItemArgument.getItem(context, "item").createItemStack(1, false);
                player.getInventory().add(stack);
                context.getSource().sendSuccess(() -> Component.literal("Gave " + stack), true);
                return 1;
            })
        )
    );

    // Register commands only for dedicated server
    if (environment == Commands.CommandSelection.DEDICATED) {
        dispatcher.register(Commands.literal("admin-only")
            .requires(source -> source.hasPermission(2))
            .executes(context -> {
                context.getSource().sendSuccess(() -> Component.literal("Admin command!"), true);
                return 1;
            })
        );
    }

    // Register commands only for integrated server
    if (environment == Commands.CommandSelection.INTEGRATED) {
        dispatcher.register(Commands.literal("singleplayer")
            .executes(context -> {
                context.getSource().sendSuccess(() -> Component.literal("Singleplayer command!"), true);
                return 1;
            })
        );
    }
});
```

## Creative Mode Tab Events

Creative mode tab events allow mods to add items to existing creative tabs (vanilla or from other mods) in a unified way.

### MODIFY_ENTRIES

Fired when items are being added to a creative mode tab.

```java
CreativeModeTabEvents.MODIFY_ENTRIES.register((tabKey, output) -> {
    // Add items to the vanilla building blocks tab
    if (tabKey.equals(CreativeModeTabs.BUILDING_BLOCKS)) {
        output.accept(MyItems.CUSTOM_BRICK.get());
        output.accept(MyItems.DECORATIVE_BLOCK.get());
        output.accept(MyItems.MAGIC_BRICK.get(), 64); // Specify stack size
    }

    // Add items to the redstone tab
    if (tabKey.equals(CreativeModeTabs.REDSTONE_BLOCKS)) {
        output.accept(MyBlocks.POWERED_BLOCK.get());
        output.accept(MyItems.REDSTONE_COMPONENT.get());
    }

    // Add items to combat tab
    if (tabKey.equals(CreativeModeTabs.COMBAT)) {
        output.accept(MyItems.ENHANCED_SWORD.get());
        output.accept(MyItems.PROTECTION_HELMET.get());
        output.accept(MyItems.MAGIC_SHIELD.get());
    }

    // Add to all tabs (useful for debug/dev items)
    if (tabKey.equals(CreativeModeTabs.OPERATOR) || isDevMode()) {
        output.accept(MyItems.DEBUG_ITEM.get());
    }
});
```

This event is particularly useful for:
- Adding your mod's items to appropriate vanilla tabs
- Organizing items by functionality instead of just having a separate tab
- Adding items to other mods' tabs for better integration
- Conditional display based on feature flags or mod configuration

## Server Tick Events

Server tick events only fire on the server side and are useful for game logic that needs to run consistently on each server tick.

### START_SERVER_TICK

Fired at the start of each server tick.

```java
ServerTickEvents.START_SERVER_TICK.register(() -> {
    // Logic that runs at the start of each server tick
    tickCounter++;
    
    // Process queued actions
    processQueuedActions();
    
    // Update world data
    updateWorldData();
});
```

### END_SERVER_TICK

Fired at the end of each server tick.

```java
ServerTickEvents.END_SERVER_TICK.register(() -> {
    // Logic that runs at the end of each server tick
    
    // Clean up temporary data
    cleanupTempData();
    
    // Send updates to clients if needed
    if (shouldSendUpdate()) {
        sendClientUpdates();
    }
    
    // Log every 1000 ticks to avoid spam
    if (tickCounter % 1000 == 0) {
        Constants.LOG.info("Server has been running for {} ticks", tickCounter);
    }
});
```

## World Events

World events provide hooks for world/level lifecycle operations. These events fire on the server side.

### WORLD_LOAD

Fired when a world/level is loaded (works on both client and server).

```java
WorldEvents.WORLD_LOAD.register((server, level) -> {
    // Run logic on world load...
});
```

### WORLD_UNLOAD

Fired when a world/level is unloaded.

```java
WorldEvents.WORLD_UNLOAD.register((server, level) -> {
    // Run logic on world unload...
});
```

### WORLD_SAVE

Fired when a world/level is saved to disk, server-side only.

```java
WorldEvents.WORLD_SAVE.register((server, level) -> {
    // This event only fires on the server side
    String dimensionKey = ((ServerLevel)level).dimension().location().toString();
    
    // Update world statistics
    WorldStats.update(dimensionKey);
    
    // Save custom data structures
    CustomDataManager.save(dimensionKey);
});
```

## Weather Events

Weather events provide hooks for weather-related phenomena.

### LIGHTNING_STRIKE

Fired when an entity is struck by lightning. Can be cancelled.

```java
WeatherEvents.LIGHTNING_STRIKE.register((entity, lightning) -> {
    // This event works consistently across all platforms and can be cancelled on all platforms
    
    // Convert items struck by lightning into their smelted variants
    if (entity instanceof ItemEntity itemEntity) {
        ItemStack item = itemEntity.getItem();
        ItemStack result = getSmeltedResult(item);
        if (!result.isEmpty()) {
            itemEntity.setItem(result);
            // Return SUCCESS to prevent default damage but still allow the transformation
            if (!entity.level().isClientSide()) {
                entity.level().playSound(null, entity.blockPosition(),
                    SoundEvents.FIRE_EXTINGUISH, SoundSource.BLOCKS, 0.5F, 2.6F);
            }
            return InteractionResult.SUCCESS;
        }
    }
    
    // Track lightning strikes
    LightningTracker.recordStrike(entity);
    
    // Prevent lightning from striking certain entities
    if (entity instanceof Player player) {
        ItemStack mainHandItem = player.getMainHandItem();
        if (mainHandItem.is(Items.TRIDENT)) {
            player.sendSystemMessage(Component.literal("Your trident glows as it absorbs the lightning!"));
            return InteractionResult.FAIL; // Cancel the lightning strike completely
        }
    }
    
    return InteractionResult.PASS; // Allow the lightning strike to proceed
});

private static ItemStack getSmeltedResult(ItemStack item) {
    if (item.is(Items.RAW_IRON)) {
        return new ItemStack(Items.IRON_INGOT, item.getCount());
    } else if (item.is(Items.RAW_GOLD)) {
        return new ItemStack(Items.GOLD_INGOT, item.getCount());
    } else if (item.is(Items.PORKCHOP)) {
        return new ItemStack(Items.COOKED_PORKCHOP, item.getCount());
    }
    return ItemStack.EMPTY;
}
```

## Client Events

Client events only fire on the client side and are useful for rendering and input handling.

### RENDER_HUD

Fired after the HUD is being rendered. This allows you to render custom elements on the HUD.

```java
// This would typically be registered through a client-specific entry point
HudEvents.RENDER_HUD.register((guiGraphics, tickCounter) -> {
    Minecraft minecraft = Minecraft.getInstance();

    // Render custom HUD element
    if (shouldShowHUD()) {
        guiGraphics.drawString(minecraft.font,
            "Energy: " + getCurrentEnergy(),
            10, 10, 0xFFFFFF);
    }
});
```

### MOUSE_SCROLL_PRE

Fired before the mouse wheel is scrolled. Can be cancelled to prevent the scroll action.

```java
InputEvents.MOUSE_SCROLL_PRE.register((mouseX, mouseY, scrollX, scrollY) -> {
    // Prevent scrolling in specific UI contexts
    if (isInCustomUI()) {
        return InteractionResult.FAIL; // Cancel scroll
    }

    // Handle custom scroll behavior
    if (shouldZoom()) {
        handleZoom(scrollY);
        return InteractionResult.SUCCESS; // Cancel default scroll
    }

    return InteractionResult.PASS; // Allow default scroll
});
```

### MOUSE_SCROLL_POST

Fired after the mouse wheel has been scrolled. This event cannot be cancelled.

```java
InputEvents.MOUSE_SCROLL_POST.register((mouseX, mouseY, scrollX, scrollY) -> {
    // Track scroll distance for statistics
    ScrollTracker.recordScrollDistance(Math.abs(scrollY));

    // Trigger custom effects based on scroll
    if (scrollY > 0) {
        onScrollUp();
    } else if (scrollY < 0) {
        onScrollDown();
    }
});
```

### START_CLIENT_TICK

Fired at the start of each client tick.

```java
// This would typically be registered through a client-specific entry point
ClientTickEvents.START_CLIENT_TICK.register(() -> {
    Minecraft minecraft = Minecraft.getInstance();

    // Logic that runs at the start of each client tick
    tickCounter++;

    // Update animations
    updateAnimations();

    // Handle particle effects
    updateParticles();
});
```

### END_CLIENT_TICK

Fired at the end of each client tick.

```java
// This would typically be registered through a client-specific entry point
ClientTickEvents.END_CLIENT_TICK.register(() -> {
    Minecraft minecraft = Minecraft.getInstance();

    // Logic that runs at the end of each client tick

    // Update custom HUD data
    updateHUDData();

    // Log every 1000 ticks to avoid spam
    if (tickCounter % 1000 == 0) {
        Constants.LOG.info("Client has been running for {} ticks", tickCounter);
    }
});
```

### BLOCK_OUTLINE_RENDER

Fired when a block outline is about to be rendered. Can be cancelled or used to customize the outline rendering.

```java
// This would typically be registered through a client-specific entry point
RenderEvents.BLOCK_OUTLINE_RENDER.register((camera, bufferSource, poseStack, hitResult, pos, state) -> {
    Minecraft minecraft = Minecraft.getInstance();

    // Custom block outline rendering
    if (state.is(MyBlocks.MAGIC_BLOCK.get())) {
        // Render glowing outline for magic blocks
        renderGlowingOutline(bufferSource, poseStack, pos, 0x00FFFF);
        return InteractionResult.SUCCESS; // Cancel default outline
    }

    // Hide outline for specific blocks
    if (state.is(MyBlocks.INVISIBLE_BLOCK.get())) {
        return InteractionResult.FAIL; // Don't render outline
    }

    // Color-code outline based on block properties
    if (state.getBlock() instanceof MyCustomBlock customBlock) {
        int outlineColor = customBlock.getOutlineColor(state);
        renderCustomOutline(bufferSource, poseStack, pos, outlineColor);
        return InteractionResult.SUCCESS; // Cancel default outline
    }

    return InteractionResult.PASS; // Allow default outline rendering
});
```

## Event Best Practices

### 1. Return Values

Most events return an `InteractionResult`:

- `PASS` - Allow default behavior to continue
- `SUCCESS` - Cancel default behavior, indicate success
- `FAIL` - Cancel default behavior, indicate failure
- `CONSUME` - Cancel default behavior, without specific result

### 2. Side Checks

Always check which side you're on before accessing side-specific code:

```java
PlayerEvents.ENTITY_INTERACT.register((player, level, hand, entity) -> {
    // Server-only logic
    if (!level.isClientSide()) {
        // Only run on server
        processInteraction(player, entity);
    }
    
    // Client-only effects
    if (level.isClientSide()) {
        // Only run on client
        spawnParticles(entity);
    }
    
    return InteractionResult.PASS;
});
```

### 3. Performance Considerations

- Keep event handlers fast, especially for frequently fired events
- Avoid expensive operations in client events
- Use caching for expensive calculations

### 4. Event Registration

Register events during mod initialization:

```java
public class MyMod {
    public static void init() {
        AmberInitializer.initialize(MOD_ID);
        
        // Register events
        registerEvents();
        
        // Other initialization
    }
    
    private static void registerEvents() {
        // Register all event handlers
        PlayerEvents.ENTITY_INTERACT.register(MyEventHandlers::handleEntityInteract);
        BlockEvents.BLOCK_BREAK_AFTER.register(MyEventHandlers::handleBlockBreak);
        ItemEvents.ITEM_PICKUP.register(MyEventHandlers::handleItemPickup);
    }
}
```

## Event Reference

### Player Events

| Event | When Fired | Cancellable | Parameters |
|-------|------------|--------------|------------|
| `ENTITY_INTERACT` | Player right-clicks entity | Yes | `(Player, Level, InteractionHand, Entity)` |
| `PLAYER_JOIN` | Player joins server | No | `(ServerPlayer)` |
| `PLAYER_LEAVE` | Player leaves server | No | `(ServerPlayer)` |
| `PLAYER_RESPAWN` | Player respawns | No | `(ServerPlayer, ServerPlayer, boolean)` |
| `CRAFT_ITEM` | Player crafts item | No | `(ServerPlayer, List<ItemStack>)` |
| `SHIELD_BLOCK` | Player blocks with shield | No | `(Player, ItemStack, float, DamageSource)` |

### Block Events

| Event | When Fired | Cancellable | Parameters |
|-------|------------|--------------|------------|
| `BLOCK_BREAK_BEFORE` | Before block broken | Yes | `(Level, Player, BlockPos, BlockState, BlockEntity)` |
| `BLOCK_BREAK_AFTER` | After block broken | No | `(Level, Player, BlockPos, BlockState, BlockEntity)` |
| `BLOCK_PLACE` | Block placed | Yes | `(Level, Player, BlockPos, BlockState, ItemStack)` |
| `BLOCK_INTERACT` | Block right-clicked | Yes | `(Player, Level, InteractionHand, BlockHitResult)` |
| `BLOCK_CLICK` | Block left-clicked (attacked) | Yes | `(Player, Level, InteractionHand, BlockPos, Direction)` |

### Item Events

| Event | When Fired | Cancellable | Parameters |
|-------|------------|--------------|------------|
| `ITEM_DROP` | Item dropped | No | `(Player, ItemEntity)` |
| `ITEM_PICKUP` | Item picked up | No | `(Player, ItemEntity, ItemStack)` |
| `MODIFY_DEFAULT_COMPONENTS` | Item components being registered | No | `(ComponentModificationContext)` |

### Entity Events

| Event | When Fired | Cancellable | Parameters |
|-------|------------|--------------|------------|
| `ENTITY_SPAWN` | Entity spawns in world | No | `(Entity, Level)` |
| `ENTITY_DEATH` | Living entity dies | No | `(LivingEntity, DamageSource)` |
| `ENTITY_DAMAGE` | Entity takes damage (before applied) | Yes | `(LivingEntity, DamageSource, float)` |
| `AFTER_DAMAGE` | After damage taken (not if killed) | No | `(LivingEntity, DamageSource, float, float, boolean)` |

### Animal Events

| Event | When Fired | Cancellable | Parameters |
|-------|------------|--------------|------------|
| `ANIMAL_TAME` | Animal is being tamed | Yes | `(LivingEntity, Player)` |
| `ANIMAL_BREED` | Baby animal spawned from breeding | No | `(Animal, Animal, AgeableMob)` |

### Farming Events

| Event | When Fired | Cancellable | Parameters |
|-------|------------|--------------|------------|
| `BONEMEAL_USE` | Bonemeal applied to block | Yes | `(Level, BlockPos, BlockState, ItemStack, Entity)` |
| `FARMLAND_TRAMPLE` | Entity tramples farmland | Yes | `(Level, BlockPos, BlockState, float, Entity)` |
| `CROP_GROW` | Crop attempts to grow | Yes | `(Level, BlockPos, BlockState)` |

### Loot Events

| Event | When Fired | Cancellable | Parameters |
|-------|------------|--------------|------------|
| `MODIFY` | Loot table loaded | No | `(ResourceLocation, Consumer<LootPool.Builder>)` |

### Command Events

| Event | When Fired | Cancellable | Parameters |
|-------|------------|--------------|------------|
| `EVENT` | Server registers commands | No | `(CommandDispatcher, CommandBuildContext, CommandSelection)` |

### Creative Mode Tab Events

| Event | When Fired | Cancellable | Parameters |
|-------|------------|--------------|------------|
| `MODIFY_ENTRIES` | Items added to creative tab | No | `(ResourceKey<CreativeModeTab>, CreativeModeTab.Output)` |

### World Events

| Event | When Fired | Cancellable | Parameters |
|-------|------------|--------------|------------|
| `WORLD_LOAD` | World is loaded | No | `(MinecraftServer, LevelAccessor)` |
| `WORLD_UNLOAD` | World is unloaded | No | `(MinecraftServer, LevelAccessor)` |
| `WORLD_SAVE` | World is saved | No | `(MinecraftServer, LevelAccessor)` |

### Weather Events

| Event | When Fired | Cancellable | Parameters |
|-------|------------|--------------|------------|
| `LIGHTNING_STRIKE` | Entity struck by lightning | Yes | `(Entity, LightningBolt)` |

### Server Tick Events

| Event | When Fired | Cancellable | Parameters |
|-------|------------|--------------|------------|
| `START_SERVER_TICK` | Start of server tick | No | `()` |
| `END_SERVER_TICK` | End of server tick | No | `()` |

### Client Events

| Event | When Fired | Cancellable | Parameters |
|-------|------------|--------------|------------|
| `RENDER_HUD` | HUD is being rendered | No | `(GuiGraphics, DeltaTracker)` |
| `MOUSE_SCROLL_PRE` | Mouse wheel scrolled (before) | Yes | `(double, double, double, double)` |
| `MOUSE_SCROLL_POST` | Mouse wheel scrolled (after) | No | `(double, double, double, double)` |
| `START_CLIENT_TICK` | Start of client tick | No | `()` |
| `END_CLIENT_TICK` | End of client tick | No | `()` |
| `BLOCK_OUTLINE_RENDER` | Block outline being rendered | Yes | `(Camera, MultiBufferSource, PoseStack, BlockHitResult, BlockPos, BlockState)` |

The event system provides a clean, consistent API across all platforms, making it easy to handle game events without worrying about platform-specific differences.