# Networking System

Amber provides a unified networking system that works across all mod loaders, allowing you to send and receive packets between client and server with a type-safe API. The system handles platform differences automatically while providing a clean, modern interface.

## Overview

The networking system consists of:

- **NetworkChannel**: Main interface for packet communication
- **Packet**: Base interface for all packet types
- **PacketEncoder/Decoder**: Handle packet serialization
- **PacketHandler**: Process received packets
- **Cross-platform compatibility**: Works identically on all platforms

## Basic Usage

### Creating a Network Channel

First, create a network channel for your mod:

```java
import com.iamkaf.amber.api.networking.v1.NetworkChannel;
import net.minecraft.resources.ResourceLocation;

public class MyNetworking {
    public static final NetworkChannel CHANNEL = NetworkChannel.create(
        ResourceLocation.fromNamespaceAndPath("mymod", "main")
    );
    
    public static void init() {
        // Register all packet types
        registerPackets();
    }
    
    private static void registerPackets() {
        // Packet registration will be shown below
    }
}
```

### Creating a Packet

Create a packet class that implements the `Packet<T>` interface:

```java
import com.iamkaf.amber.api.networking.v1.Packet;

public class SyncEnergyPacket implements Packet<SyncEnergyPacket> {
    private final int energy;
    private final BlockPos pos;
    
    public SyncEnergyPacket(int energy, BlockPos pos) {
        this.energy = energy;
        this.pos = pos;
    }
    
    public int getEnergy() {
        return energy;
    }
    
    public BlockPos getPos() {
        return pos;
    }
    
    // Encoding and decoding will be shown below
}
```

### Registering a Packet

Register your packet with the network channel:

```java
private static void registerPackets() {
    // Register the SyncEnergyPacket
    CHANNEL.register(
        SyncEnergyPacket.class,                    // Packet class
        SyncEnergyPacket::encode,                  // Encoder
        SyncEnergyPacket::decode,                  // Decoder
        SyncEnergyPacket::handle                   // Handler
    );
    
    // Register other packets
    CHANNEL.register(
        OpenGuiPacket.class,
        OpenGuiPacket::encode,
        OpenGuiPacket::decode,
        OpenGuiPacket::handle
    );
}
```

### Implementing Packet Methods

Each packet needs to implement encoding, decoding, and handling:

```java
public class SyncEnergyPacket implements Packet<SyncEnergyPacket> {
    private final int energy;
    private final BlockPos pos;
    
    // Constructor and getters...
    
    // Encode the packet to a FriendlyByteBuf
    public static void encode(SyncEnergyPacket packet, FriendlyByteBuf buf) {
        buf.writeInt(packet.energy);
        buf.writeBlockPos(packet.pos);
    }
    
    // Decode the packet from a FriendlyByteBuf
    public static SyncEnergyPacket decode(FriendlyByteBuf buf) {
        int energy = buf.readInt();
        BlockPos pos = buf.readBlockPos();
        return new SyncEnergyPacket(energy, pos);
    }
    
    // Handle the received packet
    public static void handle(SyncEnergyPacket packet, PacketContext context) {
        // Always execute on the main thread
        context.queue(() -> {
            // Get the player who received the packet
            ServerPlayer player = context.player();
            
            // Handle the packet logic
            if (player != null && player.level().isClientSide()) {
                // Client-side handling
                ClientEnergyData.setEnergy(packet.getPos(), packet.getEnergy());
            }
        });
    }
}
```

## Sending Packets

### Client to Server

Send packets from client to server:

```java
public class ClientPacketSender {
    public static void sendEnergyRequest(BlockPos pos) {
        // Send a packet to request energy data
        CHANNEL.sendToServer(new RequestEnergyPacket(pos));
    }
    
    public static void sendButtonClick(int buttonId) {
        // Send a button click packet
        CHANNEL.sendToServer(new ButtonClickPacket(buttonId));
    }
}
```

### Server to Client

Send packets from server to specific players:

```java
public class ServerPacketSender {
    public static void syncEnergyToPlayer(ServerPlayer player, BlockPos pos, int energy) {
        // Send energy data to a specific player
        CHANNEL.sendToPlayer(new SyncEnergyPacket(energy, pos), player);
    }
    
    public static void syncEnergyToAllPlayers(BlockPos pos, int energy) {
        // Send energy data to all players
        CHANNEL.sendToAllPlayers(new SyncEnergyPacket(energy, pos));
    }
    
    public static void syncEnergyToAllExcept(ServerPlayer except, BlockPos pos, int energy) {
        // Send energy data to all players except one
        CHANNEL.sendToAllPlayersExcept(new SyncEnergyPacket(energy, pos), except);
    }
}
```

## Complete Examples

### Energy System Networking

Here's a complete example of a networking system for syncing energy between client and server:

```java
// Packet Classes
public class SyncEnergyPacket implements Packet<SyncEnergyPacket> {
    private final int energy;
    private final BlockPos pos;
    
    public SyncEnergyPacket(int energy, BlockPos pos) {
        this.energy = energy;
        this.pos = pos;
    }
    
    public int getEnergy() { return energy; }
    public BlockPos getPos() { return pos; }
    
    public static void encode(SyncEnergyPacket packet, FriendlyByteBuf buf) {
        buf.writeInt(packet.energy);
        buf.writeBlockPos(packet.pos);
    }
    
    public static SyncEnergyPacket decode(FriendlyByteBuf buf) {
        return new SyncEnergyPacket(buf.readInt(), buf.readBlockPos());
    }
    
    public static void handle(SyncEnergyPacket packet, PacketContext context) {
        context.queue(() -> {
            // Update client-side energy data
            ClientEnergyData.setEnergy(packet.getPos(), packet.getEnergy());
        });
    }
}

public class RequestEnergyPacket implements Packet<RequestEnergyPacket> {
    private final BlockPos pos;
    
    public RequestEnergyPacket(BlockPos pos) {
        this.pos = pos;
    }
    
    public BlockPos getPos() { return pos; }
    
    public static void encode(RequestEnergyPacket packet, FriendlyByteBuf buf) {
        buf.writeBlockPos(packet.pos);
    }
    
    public static RequestEnergyPacket decode(FriendlyByteBuf buf) {
        return new RequestEnergyPacket(buf.readBlockPos());
    }
    
    public static void handle(RequestEnergyPacket packet, PacketContext context) {
        context.queue(() -> {
            ServerPlayer player = context.player();
            if (player != null) {
                // Get energy from server-side block
                BlockEntity be = player.level().getBlockEntity(packet.getPos());
                if (be instanceof EnergyBlockEntity energyBE) {
                    // Send energy data back to player
                    CHANNEL.sendToPlayer(
                        new SyncEnergyPacket(energyBE.getEnergy(), packet.getPos()),
                        player
                    );
                }
            }
        });
    }
}

// Networking Manager
public class MyNetworking {
    public static final NetworkChannel CHANNEL = NetworkChannel.create(
        ResourceLocation.fromNamespaceAndPath("mymod", "main")
    );
    
    public static void init() {
        // Register packets
        CHANNEL.register(SyncEnergyPacket.class, SyncEnergyPacket::encode, 
            SyncEnergyPacket::decode, SyncEnergyPacket::handle);
        CHANNEL.register(RequestEnergyPacket.class, RequestEnergyPacket::encode, 
            RequestEnergyPacket::decode, RequestEnergyPacket::handle);
    }
    
    public static void syncEnergyToNearbyPlayers(BlockPos pos, int energy, ServerLevel level) {
        // Send to all players tracking the chunk
        level.getChunkSource().chunkMap.getPlayers(pos, false).forEach(player -> {
            CHANNEL.sendToPlayer(new SyncEnergyPacket(energy, pos), player);
        });
    }
}

// Client-side Energy Data
public class ClientEnergyData {
    private static final Map<BlockPos, Integer> ENERGY_DATA = new HashMap<>();
    
    public static void setEnergy(BlockPos pos, int energy) {
        ENERGY_DATA.put(pos, energy);
    }
    
    public static int getEnergy(BlockPos pos) {
        return ENERGY_DATA.getOrDefault(pos, 0);
    }
    
    public static void clear() {
        ENERGY_DATA.clear();
    }
}
```

### GUI Open Packet

Example of opening a GUI via networking:

```java
public class OpenGuiPacket implements Packet<OpenGuiPacket> {
    private final int guiId;
    private final BlockPos pos;
    
    public OpenGuiPacket(int guiId, BlockPos pos) {
        this.guiId = guiId;
        this.pos = pos;
    }
    
    public int getGuiId() { return guiId; }
    public BlockPos getPos() { return pos; }
    
    public static void encode(OpenGuiPacket packet, FriendlyByteBuf buf) {
        buf.writeInt(packet.guiId);
        buf.writeBlockPos(packet.pos);
    }
    
    public static OpenGuiPacket decode(FriendlyByteBuf buf) {
        return new OpenGuiPacket(buf.readInt(), buf.readBlockPos());
    }
    
    public static void handle(OpenGuiPacket packet, PacketContext context) {
        context.queue(() -> {
            ServerPlayer player = context.player();
            if (player != null) {
                // Open GUI on client
                player.openMenu(new SimpleMenuProvider(
                    (containerId, playerInv, player) -> new MyMenu(
                        containerId, playerInv, packet.getPos()
                    ),
                    Component.literal("My GUI")
                ), buf -> buf.writeBlockPos(packet.getPos()));
            }
        });
    }
}
```

## Advanced Features

### Custom Packet Types

You can create more complex packet types with custom data:

```java
public class CustomDataPacket implements Packet<CustomDataPacket> {
    private final Map<String, String> data;
    private final List<ItemStack> items;
    private final CompoundTag tag;
    
    public CustomDataPacket(Map<String, String> data, List<ItemStack> items, CompoundTag tag) {
        this.data = data;
        this.items = items;
        this.tag = tag;
    }
    
    public static void encode(CustomDataPacket packet, FriendlyByteBuf buf) {
        // Write map
        buf.writeVarInt(packet.data.size());
        packet.data.forEach((key, value) -> {
            buf.writeUtf(key);
            buf.writeUtf(value);
        });
        
        // Write item list
        buf.writeVarInt(packet.items.size());
        for (ItemStack stack : packet.items) {
            buf.writeItemStack(stack);
        }
        
        // Write NBT
        buf.writeNbt(packet.tag);
    }
    
    public static CustomDataPacket decode(FriendlyByteBuf buf) {
        // Read map
        int mapSize = buf.readVarInt();
        Map<String, String> data = new HashMap<>();
        for (int i = 0; i < mapSize; i++) {
            data.put(buf.readUtf(), buf.readUtf());
        }
        
        // Read item list
        int listSize = buf.readVarInt();
        List<ItemStack> items = new ArrayList<>();
        for (int i = 0; i < listSize; i++) {
            items.add(buf.readItem());
        }
        
        // Read NBT
        CompoundTag tag = buf.readNbt();
        
        return new CustomDataPacket(data, items, tag);
    }
    
    public static void handle(CustomDataPacket packet, PacketContext context) {
        context.queue(() -> {
            // Handle complex data
            processCustomData(packet.data, packet.items, packet.tag);
        });
    }
}
```

### Packet Validation

Add validation to ensure packets are valid:

```java
public class ValidatedPacket implements Packet<ValidatedPacket> {
    private final String data;
    private final int value;
    
    public ValidatedPacket(String data, int value) {
        this.data = data;
        this.value = value;
    }
    
    public static ValidatedPacket decode(FriendlyByteBuf buf) {
        String data = buf.readUtf(256); // Limit string length
        int value = buf.readInt();
        
        // Validate during decoding
        if (data.length() > 100) {
            throw new IllegalArgumentException("Data too long");
        }
        if (value < 0 || value > 1000) {
            throw new IllegalArgumentException("Value out of range");
        }
        
        return new ValidatedPacket(data, value);
    }
    
    // Other methods...
}
```

## Best Practices

### 1. Thread Safety

Always use `context.queue()` to ensure packet handling runs on the main thread:

```java
public static void handle(MyPacket packet, PacketContext context) {
    // WRONG - Can cause concurrency issues
    // Minecraft.getInstance().player.sendSystemMessage(...);
    
    // RIGHT - Runs on main thread
    context.queue(() -> {
        Minecraft.getInstance().player.sendSystemMessage(
            Component.literal("Packet received!")
        );
    });
}
```

### 2. Packet Size

Keep packets small and efficient:

```java
// Good - Compact data
buf.writeVarInt(value);           // Variable-length integer
buf.writeByte(enumValue.ordinal()); // Small enum
buf.writeBoolean(flag);           // Single bit

// Avoid - Large data
buf.writeUtf(longString);         // Limit string length
buf.writeItemStack(largeStack);   // Be careful with complex items
```

### 3. Security

Always validate packet data on the server:

```java
public static void handle(PlayerActionPacket packet, PacketContext context) {
    ServerPlayer player = context.player();
    
    // Validate player can perform action
    if (player == null || !player.hasPermissions(2)) {
        return; // Ignore packet from unauthorized player
    }
    
    // Validate action is allowed
    if (!isValidAction(packet.getAction(), player)) {
        return; // Ignore invalid action
    }
    
    // Process valid packet
    processAction(packet.getAction(), player);
}
```

### 4. Performance

Consider performance for frequently sent packets:

```java
// For high-frequency packets like position updates
public class PositionUpdatePacket implements Packet<PositionUpdatePacket> {
    private final double x, y, z;
    private final float yaw, pitch;
    
    // Use floats instead of doubles when precision isn't critical
    public static void encode(PositionUpdatePacket packet, FriendlyByteBuf buf) {
        buf.writeFloat((float) packet.x);
        buf.writeFloat((float) packet.y);
        buf.writeFloat((float) packet.z);
        buf.writeFloat(packet.yaw);
        buf.writeFloat(packet.pitch);
    }
}
```

## Platform-Specific Implementation Details

### Forge Implementation

Amber's Forge implementation uses Forge's ChannelBuilder and SimpleChannel for networking. The implementation handles the complexities of Forge 60.0.0's networking API:

```java
// Forge-specific implementation (handled automatically by Amber)
public class ForgeNetworkChannelImpl implements PlatformNetworkChannel {
    private final SimpleChannel channel;
    
    public ForgeNetworkChannelImpl(ResourceLocation channelId) {
        this.channel = ChannelBuilder.named(channelId)
            .networkProtocolVersion(PROTOCOL_VERSION)
            .clientAcceptedVersions(Channel.VersionTest.exact(PROTOCOL_VERSION))
            .serverAcceptedVersions(Channel.VersionTest.exact(PROTOCOL_VERSION))
            .simpleChannel();
    }
    
    @Override
    public <T extends Packet<T>> void register(Class<T> packetClass,
                                            PacketEncoder<T> encoder,
                                            PacketDecoder<T> decoder,
                                            PacketHandler<T> handler) {
        // Uses MessageBuilder API for packet registration
        channel.messageBuilder(packetClass)
            .decoder(buffer -> decoder.decode(buffer))
            .encoder((packet, buffer) -> encoder.encode(packet, buffer))
            .consumerMainThread((packet, context) -> {
                // Handles thread-safe packet execution
            })
            .add();
    }
}
```

### Thread Safety

All implementations ensure thread-safe packet handling:

- **Forge**: Uses `consumerMainThread()` to ensure packet handling runs on the main thread
- **Fabric**: Uses built-in thread-safe execution
- **NeoForge**: Uses proper context handling

## Migration from Platform-Specific Networking

### From Fabric

```java
// Old Fabric way
public static final PacketIdentifier SYNC_ENERGY =
    new PacketIdentifier("mymod", "sync_energy");

PacketByteBuf buf = PacketByteBufs.create();
buf.writeInt(energy);
buf.writeBlockPos(pos);
ServerPlayNetworking.send(player, SYNC_ENERGY, buf);

// New Amber way
CHANNEL.sendToPlayer(new SyncEnergyPacket(energy, pos), player);
```

### From Forge

```java
// Old Forge way
private static final int SYNC_ENERGY_ID = 0;

@SubscribeEvent
public void onRegisterPackets(RegisterPacketHandlerEvent event) {
    event.register(SyncEnergyPacket.class, SYNC_ENERGY_ID);
}

// New Amber way
CHANNEL.register(SyncEnergyPacket.class, SyncEnergyPacket::encode,
    SyncEnergyPacket::decode, SyncEnergyPacket::handle);
```

### Version Compatibility

Amber's networking system handles version differences automatically:

- **Forge 60.0.0+**: Uses the new ChannelBuilder API
- **Forge 47.x-59.x**: Uses the traditional SimpleChannel API
- **Fabric**: Uses Fabric's networking API
- **NeoForge**: Uses NeoForge's payload system

The Amber networking system provides a cleaner, type-safe API that works across all platforms without the boilerplate of platform-specific code.