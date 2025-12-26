# Scala 2.13 Build Directory

This directory contains the source files used to build the Piston package.

## What's Included in Git

Only the small, essential files are committed to Git:
- ✅ `compile` - Compilation script
- ✅ `run` - Execution script
- ✅ `environment` - Environment setup
- ✅ `build.sh` - Build script
- ✅ `metadata.json` - Package metadata
- ✅ `pkg-info.json` - Build info
- ✅ `LICENSE`, `NOTICE` - License files
- ✅ This README

## What's Excluded from Git (Large Files)

The following large binary files are **not** in Git (see `.gitignore`):
- ❌ `jdk/` (184MB) - Bundled OpenJDK 17
- ❌ `lib/` (23MB) - Scala libraries
- ❌ `bin/` (80KB) - Scala binaries
- ❌ `doc/` (120KB) - Documentation
- ❌ `man/` (48KB) - Man pages

**Total excluded**: ~207MB

## How to Rebuild the Package

### 1. Download Required Components

**Scala 2.13.16:**
```bash
wget https://downloads.lightbend.com/scala/2.13.16/scala-2.13.16.tgz
tar -xzf scala-2.13.16.tgz
cp -r scala-2.13.16/{bin,lib,doc,man} .
rm -rf scala-2.13.16 scala-2.13.16.tgz
```

**OpenJDK 17:**
```bash
wget https://download.java.net/java/GA/jdk17.0.2/dfd4a8d0985749f896bed50d7138ee7f/8/GPL/openjdk-17.0.2_linux-x64_bin.tar.gz
tar -xzf openjdk-17.0.2_linux-x64_bin.tar.gz
mv jdk-17.0.2 jdk

# Optimize size (remove unnecessary components)
rm -rf jdk/jmods jdk/include
rm -f jdk/lib/src.zip
```

### 2. Build the Package

```bash
tar -czf ../scala-2.13.16.pkg.tar.gz *
cd ..
shasum -a 256 scala-2.13.16.pkg.tar.gz
```

### 3. Update the Index

Copy the new SHA256 to `piston-index`:
```
scala,2.13.16,NEW_SHA256_HERE,https://github.com/...
```

## Directory Structure (Complete)

```
scala-2.13-build/
├── README.md           # This file (in Git)
├── compile             # Compile script (in Git)
├── run                 # Run script (in Git)
├── environment         # Environment setup (in Git)
├── build.sh            # Build script (in Git)
├── metadata.json       # Package metadata (in Git)
├── pkg-info.json       # Build info (in Git)
├── LICENSE             # License (in Git)
├── NOTICE              # Notice (in Git)
├── bin/                # Scala binaries (NOT in Git - 80KB)
├── lib/                # Scala libraries (NOT in Git - 23MB)
├── jdk/                # OpenJDK 17 (NOT in Git - 184MB)
├── doc/                # Documentation (NOT in Git - 120KB)
└── man/                # Man pages (NOT in Git - 48KB)
```

## Why Exclude Large Files?

1. **Git performance**: Large binary files slow down Git operations
2. **Repository size**: Keeps the repo small and fast to clone
3. **Official sources**: Users can download from official Scala/OpenJDK sources
4. **Package distribution**: The complete package is distributed via GitHub Releases

## For Users

If you just want to **use** the package, you don't need this directory at all. Just:

1. Download `scala-2.13.16.pkg.tar.gz` from GitHub Releases
2. Install via Piston API
3. Start coding!

This directory is only needed if you want to **rebuild** or **modify** the package.

