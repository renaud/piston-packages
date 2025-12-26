# Scala 2.13.16 Custom Piston Package

A fully self-contained Piston package for Scala 2.13.16 with bundled OpenJDK 17. No external dependencies required!

## 🎉 Status: Fully Working

All tests passing:
- ✅ Traditional main method
- ✅ App trait
- ✅ Case classes and pattern matching
- ✅ Higher-order functions

## Package Details

| Property | Value |
|----------|-------|
| **Language** | Scala |
| **Version** | 2.13.16 |
| **Java** | Bundled OpenJDK 17 (no external Java needed) |
| **Size** | 86MB compressed (184MB uncompressed) |
| **Aliases** | `scala2`, `scala2.13` |
| **SHA256** | `ef7d711818f11588bf4d2da1d317e8a35d81d54b5aafe0c7e15172107df5a617` |

## What's Included

```
scala-2.13.16.pkg.tar.gz (86MB)
├── bin/              # Scala binaries (scalac, scala, etc.)
├── lib/              # Scala libraries
├── jdk/              # Bundled OpenJDK 17 (184MB uncompressed)
│   ├── bin/          # Java binaries (java, javac, jar, etc.)
│   ├── conf/         # Java configuration
│   ├── legal/        # License files
│   └── lib/          # Java runtime libraries
├── doc/              # Scala documentation
├── man/              # Man pages
├── compile           # Custom compile script (supports main & App)
├── run               # Run script
├── environment       # Environment setup (sets JAVA_HOME)
└── metadata.json     # Package metadata
```

## Quick Start

### 1. Set Up GitHub Repository

1. **Create a new GitHub repository** (e.g., `steacher-piston-packages`)

2. **Create a release** (e.g., `v1.0.0`)

3. **Upload the package**:
   - Upload `scala-2.13.16.pkg.tar.gz` to the release

4. **Set up GitHub Pages**:
   - Go to Settings → Pages
   - Source: Deploy from a branch
   - Branch: `main` (or `master`)
   - Folder: `/ (root)`

5. **Create index file**:
   - Create a file named `index` in the repository root
   - Copy contents from the `piston-index` file
   - Update `YOUR_USERNAME` with your GitHub username
   - Commit and push

6. **Get your index URL**:
   ```
   https://YOUR_USERNAME.github.io/steacher-piston-packages/index
   ```

### 2. Configure Piston

Restart Piston with your custom index:

```bash
docker stop piston_api
docker rm piston_api

docker run --privileged \
  -v $PWD/piston_data:/piston \
  -e PISTON_REPO_URL=https://YOUR_USERNAME.github.io/steacher-piston-packages/index \
  -dit -p 2000:2000 --name piston_api \
  ghcr.io/engineer-man/piston
```

### 3. Install Scala 2.13.16

```bash
curl -X POST http://localhost:2000/api/v2/packages \
  -H "Content-Type: application/json" \
  -d '{"language":"scala","version":"2.13.16"}'
```

Installation takes ~1-2 minutes due to the 86MB package size.

### 4. Test It

```bash
python3 test_scala_2.13.py
```

Expected output:
```
Total: 4/4 tests passed
🎉 All tests passed! Scala 2.13.16 is working correctly.
```

## Supported Scala Syntax

### Traditional main method
```scala
object Hello {
  def main(args: Array[String]): Unit = {
    println("Hello, World!")
  }
}
```

### App trait
```scala
object HelloApp extends App {
  println("Hello, World!")
}
```

Both styles are fully supported!

## How It Works

### Why Bundle Java?

The Piston container doesn't include Java by default. Rather than requiring users to modify the container, we bundle OpenJDK 17 directly with Scala for a complete, self-contained package.

### Environment Setup

When Piston loads the package, it sources the `environment` file which:
```bash
export JAVA_HOME=$PWD/jdk
export PATH=$PWD/jdk/bin:$PWD/bin:$PATH
```

This makes both Java and Scala available without any external dependencies.

### Compilation Process

1. **Source environment**: Sets up Java and Scala paths
2. **Run scalac**: Compiles Scala code to bytecode
3. **Detect entry point**: Automatically finds `main` method or `App` trait
4. **Create JAR**: Packages with proper manifest and Scala libraries
5. **Execute**: Runs with bundled Java runtime

## API Usage

### Execute Scala Code

```bash
curl -X POST http://localhost:2000/api/v2/execute \
  -H "Content-Type: application/json" \
  -d '{
    "language": "scala",
    "version": "2.13.16",
    "files": [{
      "name": "main.scala",
      "content": "object Hello extends App { println(\"Hello from Scala!\") }"
    }],
    "compile_timeout": 10000,
    "run_timeout": 3000
  }'
```

### Response Format

```json
{
  "compile": {
    "stdout": "",
    "stderr": "",
    "code": 0,
    "signal": null
  },
  "run": {
    "stdout": "Hello from Scala!\n",
    "stderr": "",
    "code": 0,
    "signal": null
  }
}
```

## Troubleshooting

### Package won't install

**Check Docker logs:**
```bash
docker logs piston_api | tail -50
```

**Verify index URL:**
- Open your index URL in a browser
- Should show: `scala,2.13.16,ef7d711818...`

**Check GitHub release:**
- Release must be published (not draft)
- Package file must be accessible

### Compilation fails

**Check package installation:**
```bash
curl http://localhost:2000/api/v2/runtimes | jq '.[] | select(.language=="scala")'
```

**Verify Java in container:**
```bash
docker exec -it piston_api ls -la /piston/packages/scala/2.13.16/jdk/bin/java
```

**Manual test:**
```bash
docker exec -it piston_api bash
cd /piston/packages/scala/2.13.16
source ./environment
java -version
echo 'object Test extends App { println("Works!") }' > test.scala
./compile test.scala
./run test.scala
```

### Checksum mismatch

This means the file on GitHub doesn't match the index:

1. **Verify local file:**
   ```bash
   shasum -a 256 scala-2.13.16.pkg.tar.gz
   # Should be: ef7d711818f11588bf4d2da1d317e8a35d81d54b5aafe0c7e15172107df5a617
   ```

2. **Re-upload to GitHub:**
   - Delete old package from release
   - Upload the correct package
   - Wait 1-2 minutes for CDN to update

3. **Verify index file:**
   - Check that SHA256 in index matches local file
   - Push updated index to GitHub
   - Wait for GitHub Pages to update

## Updating the Package

If you need to make changes:

### 1. Modify Source Files

Edit files in `scala-2.13-build/`:
- `compile` - Compilation script
- `run` - Execution script
- `environment` - Environment variables

### 2. Rebuild Package

```bash
cd scala-2.13-build
tar -czf ../scala-2.13.16.pkg.tar.gz *
cd ..
shasum -a 256 scala-2.13.16.pkg.tar.gz
```

### 3. Update Index

Copy the new SHA256 and update `piston-index`:
```
scala,2.13.16,NEW_SHA256_HERE,https://github.com/YOUR_USERNAME/...
```

### 4. Deploy

1. Upload new package to GitHub release
2. Commit and push updated index
3. Reinstall in Piston

## Technical Details

### Package Optimization

The bundled JDK has been optimized for size:
- Removed `jmods/` (Java modules, not needed at runtime)
- Removed `include/` (C header files)
- Removed `lib/src.zip` (Java source code)
- Result: 307MB → 184MB (40% reduction)

### Compatibility

- **Scala 2.13.16**: Latest stable release
- **Java 17**: LTS version, excellent Scala support
- **Platform**: Linux x64 (standard Piston platform)
- **Glibc**: Standard Linux C library (included in Piston)

### Performance

- **Package download**: ~30 seconds (86MB)
- **Extraction**: ~10 seconds
- **First compilation**: ~3-5 seconds (JVM warmup)
- **Subsequent compilations**: ~2-3 seconds
- **Execution**: <1 second for simple programs

### Timeouts

Default timeouts (configurable in API calls):
- **Compilation**: 10 seconds
- **Execution**: 3 seconds

For complex programs, increase timeouts:
```json
{
  "compile_timeout": 20000,
  "run_timeout": 10000
}
```

## Files in This Repository

- `scala-2.13.16.pkg.tar.gz` - The complete package (86MB)
- `piston-index` - Template index file for GitHub Pages
- `test_scala_2.13.py` - Test suite to verify the package works
- `scala-2.13-build/` - Source files used to build the package
- `GITHUB_SETUP.md` - Detailed GitHub setup instructions
- `QUICK_REFERENCE.md` - Quick command reference

## Key Features

✅ **Self-contained** - No external dependencies  
✅ **Portable** - Works on any Piston installation  
✅ **Complete** - Includes both Scala and Java  
✅ **Optimized** - Size-optimized JDK (184MB)  
✅ **Compatible** - Supports both main method and App trait  
✅ **Tested** - Full test suite included  
✅ **Documented** - Comprehensive documentation  

## Support

If you encounter issues:

1. **Run the test suite**: `python3 test_scala_2.13.py`
2. **Check Docker logs**: `docker logs piston_api`
3. **Verify installation**: `curl http://localhost:2000/api/v2/runtimes`
4. **Manual testing**: Follow troubleshooting steps above

## License

This package includes:
- **Scala 2.13.16**: Apache License 2.0
- **OpenJDK 17**: GNU General Public License v2 with Classpath Exception

See `scala-2.13-build/LICENSE` and `scala-2.13-build/jdk/legal/` for full license texts.

## Acknowledgments

- Scala team for the excellent language and tooling
- OpenJDK project for the Java runtime
- Piston project for the code execution engine

---

**Package Version**: 1.0.0  
**Last Updated**: December 2024  
**Status**: Production Ready ✅
