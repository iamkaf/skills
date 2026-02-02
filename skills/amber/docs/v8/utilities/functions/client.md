# ClientFunctions

Client-side operations including HUD rendering, tooltips, and text writing.

**Package**: `com.iamkaf.amber.api.functions.v1`

## HUD Rendering

### shouldRenderHud()

Checks if HUDs should be rendered based on the current game state (debug screen, GUI hidden, player null).

```java
boolean shouldRender = ClientFunctions.shouldRenderHud();
```

### renderText()

Renders text at the specified coordinates with the given color.

```java
ClientFunctions.renderText(
    GuiGraphics context,
    Font font,
    Component message,
    int x, int y,
    int color
);
```

**Color Constants**:
- `ClientFunctions.WHITE` - Default white (0xFFFFFFFF)
- `ClientFunctions.BLACK` - Black (0x000000FF)
- `ClientFunctions.TRANSPARENT` - Transparent (0x00000000)
- `ClientFunctions.PACKED_LIGHT` - Packed light value (15728880)

### renderTooltip()

Renders an item tooltip at the specified coordinates.

```java
ClientFunctions.renderTooltip(
    GuiGraphics guiGraphics,
    ItemStack stack,
    int x, int y
);
```

## SmartTooltip

Builder for conditional tooltips based on key presses.

```java
new ClientFunctions.SmartTooltip()
    .add(Component.literal("Always shown"))
    .shift(Component.literal("Shown when holding Shift"))
    .keybind(myKeybind, Component.literal("Shown when key pressed"))
    .shiftKeybind(myKeybind, Component.literal("Shift + key"))
    .into(tooltipAdder);
```

### Methods

- `add(Component)` - Add unconditionally
- `shift(Component)` - Add when Shift is held
- `keybind(KeyMapping, Component)` - Add when keybind is pressed
- `shiftKeybind(KeyMapping, Component)` - Add when both Shift and keybind are pressed
- `into(Consumer<Component>)` - Output to tooltip consumer

## TextWriter

Helper for writing text with a cursor position.

```java
ClientFunctions.TextWriter writer = new ClientFunctions.TextWriter(graphics, font, 20, 40);

writer.writeLine(Component.literal("First line"), ClientFunctions.WHITE);
writer.writeLine(Component.literal("Second line"));
writer.write(Component.literal("At cursor"));

// Reposition cursor
writer.write(Component.literal("At 100,100"), 100, 100);
```

### Methods

- `write(Component, int x, int y, int color)` - Write at position with color
- `write(Component, int x, int y)` - Write at position with default color
- `write(Component)` - Write at cursor position
- `writeLine(Component, int color)` - Write line with color, advance cursor
- `writeLine(Component)` - Write line with default color, advance cursor

## Migration

Replaces `CommonClientUtils` and `SmartTooltip`:

| Old | New |
|-----|-----|
| `CommonClientUtils.shouldRender()` | `ClientFunctions.shouldRenderHud()` |
| `CommonClientUtils.text()` | `ClientFunctions.renderText()` |
| `CommonClientUtils.renderTooltip()` | `ClientFunctions.renderTooltip()` |
| `CommonClientUtils.TextWriter` | `ClientFunctions.TextWriter` |
| `SmartTooltip` | `ClientFunctions.SmartTooltip` |
