# Installation Guide

This guide covers how to add Amber to your Minecraft mod project, whether you're starting from scratch or adding it to an existing project.

## Supported Versions

- **Minecraft**: 1.21.10
- **Java**: 21 or higher
- **Platforms**: Fabric, Forge, NeoForge

## Adding Amber to Your Project

### 1. Repository Configuration

Add the Amber Maven repository to your `build.gradle` file:

```gradle
repositories {
    // Add other repositories as needed
    mavenCentral()
    
    // Amber Maven Repository
    maven {
        name = 'Amber Maven'
        url = 'https://raw.githubusercontent.com/iamkaf/modresources/main/maven/'
    }
}
```

### 2. Dependency Configuration

#### For Multiloader Projects

If you're using a multiloader setup with separate modules for each platform:

**Common Module (`common/build.gradle`)**:
```gradle
dependencies {
    // Amber Common - contains all shared APIs
    implementation "com.iamkaf:amber-common:8.3.2+1.21.10"
}
```

**Fabric Module (`fabric/build.gradle`)**:
```gradle
dependencies {
    // Include common module
    implementation project(':common')
    
    // Amber Fabric implementation
    implementation "com.iamkaf:amber-fabric:8.3.2+1.21.10"
}
```

**Forge Module (`forge/build.gradle`)**:
```gradle
dependencies {
    // Include common module
    implementation project(':common')
    
    // Amber Forge implementation
    implementation "com.iamkaf:amber-forge:8.3.2+1.21.10"
}
```

**NeoForge Module (`neoforge/build.gradle`)**:
```gradle
dependencies {
    // Include common module
    implementation project(':common')
    
    // Amber NeoForge implementation
    implementation "com.iamkaf:amber-neoforge:8.3.2+1.21.10"
}
```

#### For Single-Platform Projects

If you're targeting only one platform:

**Fabric Only**:
```gradle
dependencies {
    implementation "com.iamkaf:amber-fabric:8.3.2+1.21.10"
}
```

**Forge Only**:
```gradle
dependencies {
    implementation "com.iamkaf:amber-forge:8.3.2+1.21.10"
}
```

**NeoForge Only**:
```gradle
dependencies {
    implementation "com.iamkaf:amber-neoforge:8.3.2+1.21.10"
}
```

## Project Setup Examples

### New Multiloader Project

Here's a complete example for setting up a new multiloader project:

**Root `build.gradle`**:
```gradle
plugins {
    id 'fabric-loom' version '1.11-SNAPSHOT' apply false
    id 'net.neoforged.moddev' version '2.0.110' apply false
}
```

**`gradle.properties`**:
```properties
# Project Info
mod_version=1.0.0
mod_id=mymod
mod_name=My Mod
mod_author=YourName

# Minecraft
minecraft_version=1.21.10

# Amber Version
amber_version=8.3.2+1.21.10

# Platform-specific versions
fabric_version=0.135.0+1.21.10
fabric_loader_version=0.17.2
forge_version=60.0.0
neoforge_version=21.10.2-beta

# Java
java_version=21
```

**`common/build.gradle`**:
```gradle
plugins {
    id 'multiloader-common'
}

dependencies {
    implementation "com.iamkaf:amber-common:${amber_version}"
}
```

**`fabric/build.gradle`**:
```gradle
plugins {
    id 'fabric-loom'
}

dependencies {
    implementation project(':common')
    implementation "com.iamkaf:amber-fabric:${amber_version}"
}
```

### Existing Project Integration

If you're adding Amber to an existing project:

1. **Add the repository** (as shown above)
2. **Add the appropriate dependencies**
3. **Update your mod initialization**:

**Before (Fabric example)**:
```java
public class MyMod implements ModInitializer {
    @Override
    public void onInitialize() {
        // Your existing initialization code
    }
}
```

**After (with Amber)**:
```java
public class MyMod implements ModInitializer {
    @Override
    public void onInitialize() {
        // Initialize Amber first
        AmberInitializer.initialize("mymod");
        
        // Your existing initialization code
    }
}
```

## Version Management

### Using Variables

It's recommended to use variables for version management:

**`gradle.properties`**:
```properties
amber_version=8.3.2+1.21.10
minecraft_version=1.21.10
```

**`build.gradle`**:
```gradle
dependencies {
    implementation "com.iamkaf:amber-common:${amber_version}"
    implementation "com.iamkaf:amber-fabric:${amber_version}"
}
```

### Version Compatibility

Amber follows semantic versioning. When updating:

- **Patch versions** (X.Y.Z): Safe to update, contains bug fixes
- **Minor versions** (X.Y.Z): May contain new features, generally safe
- **Major versions** (X.Y.Z): May contain breaking changes

Check the [changelog](https://github.com/iamkaf/amber/blob/main/CHANGELOG.md) for breaking changes when updating major versions.

## IDE Configuration

### IntelliJ IDEA

1. **Import the project** as a Gradle project
2. **Ensure JDK 21** is selected (File → Project Structure → Project SDK)
3. **Refresh Gradle** if dependencies don't appear (Click the elephant icon)

### VS Code

1. **Install the Extension Pack for Java**
2. **Open the folder** as a workspace
3. **Trust the Gradle project** when prompted
4. **Run "Java: Import Project"** from the command palette

## Common Issues

### Dependency Resolution Errors

**Problem**: `Could not find com.iamkaf:amber-common:8.3.2+1.21.10`

**Solution**:
1. Verify the repository URL is correct
2. Check your internet connection
3. Try refreshing Gradle dependencies:
   ```bash
   ./gradlew --refresh-dependencies
   ```

### Version Conflicts

**Problem**: Conflicts between different mod loader versions

**Solution**:
1. Ensure all platform versions match your Minecraft version
2. Check for transitive dependency conflicts:
   ```bash
   ./gradlew dependencies
   ```

### Build Failures

**Problem**: Compilation errors after adding Amber

**Solution**:
1. Clean and rebuild:
   ```bash
   ./gradlew clean build
   ```
2. Check that you're using the correct Java version
3. Verify all dependencies are properly resolved

## Verification

To verify Amber is properly installed:

1. **Add test code** to your main mod class:
   ```java
   public class MyMod {
       public static void init() {
           AmberModInfo info = AmberInitializer.initialize("mymod");
           System.out.println("Amber initialized: " + info.name() + " v" + info.version());
       }
   }
   ```

2. **Run the game** and check the logs for the initialization message

3. **Test basic functionality**:
   ```java
   // Test platform detection
   System.out.println("Platform: " + Platform.getPlatformName());
   
   // Test registry system
   DeferredRegister<Item> items = DeferredRegister.create("mymod", Registries.ITEM);
   System.out.println("Registry system working");
   ```

## Next Steps

After installation:

1. Read the [Getting Started Guide](getting-started.md)
2. Explore the [API Documentation](../api/core.md)
3. Check out the [Examples](../systems/events.md)

If you encounter any issues during installation, please:

1. Check the [Common Issues](#common-issues) section above
2. Look at existing [GitHub Issues](https://github.com/iamkaf/amber/issues)
3. Create a new issue with details about your setup and the error you're encountering