# Scala 2.13.16 Custom Piston Package

This directory contains a custom Piston package for Scala 2.13.16 with Java 17 support.

## What's Included

- `scala-2.13.16.pkg.tar.gz` - The complete package (22MB)
- `piston-index` - Template index file for GitHub Pages
- `GITHUB_SETUP.md` - Step-by-step setup instructions
- `test_scala_2.13.py` - Test suite to verify the package works
- `scala-2.13-build/` - Source files used to build the package

## Quick Start

### 1. Set Up GitHub Repository

Follow the detailed instructions in `GITHUB_SETUP.md` to:
1. Create a new GitHub repository
2. Upload the package as a release
3. Set up GitHub Pages for the index file
4. Get your custom index URL

### 2. Configure Piston

Once your GitHub repo is set up, restart Piston with your custom index:

```bash
docker stop piston_api
docker rm piston_api

docker run --privileged \
  -v $PWD/piston_data:/piston \
  -e PISTON_REPO_URL=https://renaud.github.io/steacher-piston-packages/index \
  -dit -p 2000:2000 --name piston_api \
  ghcr.io/engineer-man/piston
```

### 3. Install Scala 2.13.16

```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"language":"scala","version":"2.13.16"}' \
  http://localhost:2000/api/v2/packages
```

### 4. Test It

```bash
python3 test_scala_2.13.py
```

## Supported Scala Syntax

The package supports both Scala 2.13 entry point styles:

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

## Package Details

- **Language**: Scala
- **Version**: 2.13.16
- **Java Version**: Uses container's Java (compatible with Java 8+)
- **Aliases**: `scala2`, `scala2.13`
- **SHA256**: `9202d928f30eea25c0ff4c1f3ee11002bc937d605900214948f15ee664441be6`

## How It Works

1. **Custom Index**: Piston checks your custom index first for packages
2. **Fallback**: If a package isn't in your index, Piston falls back to the official index
3. **This means**: You get Scala 2.13.16 from your index, Python/etc from official index

## Files in the Package

```
scala-2.13.16.pkg.tar.gz contains:
├── bin/              # Scala binaries (scalac, scala, etc.)
├── lib/              # Scala libraries
├── doc/              # Documentation
├── man/              # Man pages
├── compile           # Custom compile script (supports main & App)
├── run               # Run script
├── environment       # Environment variables
├── metadata.json     # Package metadata
├── pkg-info.json     # Build info
├── .ppman-installed  # Marker file
└── test.scala        # Sample test file
```

## Troubleshooting

### Package won't install
- Check Docker logs: `docker logs piston_api`
- Verify your index URL is accessible in a browser
- Ensure the GitHub release is published (not draft)

### Compilation fails
- Check that both syntax styles are in your code
- Verify the object name matches the file structure
- Look at compile errors in the response

### Runtime errors
- Check that Java is available in the container
- Verify the manifest was created correctly
- Check the run script has correct permissions

## Updating the Package

If you need to make changes:

1. Modify files in `scala-2.13-build/`
2. Rebuild the archive:
   ```bash
   cd scala-2.13-build
   tar -czf ../scala-2.13.16.pkg.tar.gz *
   cd ..
   shasum -a 256 scala-2.13.16.pkg.tar.gz
   ```
3. Update the SHA256 in your `piston-index` file
4. Upload the new package to GitHub releases
5. Update the index file in your repository


## Notes

- The package is ~22MB (smaller than Scala 3 which is 128MB)
- Compilation timeout: 10 seconds (configurable in API calls)
- Run timeout: 3 seconds (configurable in API calls)
- The compile script prioritizes explicit `main` method over `App` trait
- Error messages are clear if neither entry point is found

## Support

If you encounter issues:
1. Check `docker logs piston_api`
2. Verify the package is installed: `curl http://localhost:2000/api/v2/runtimes`
3. Test with the provided test suite: `python3 test_scala_2.13.py`
4. Check the compile script in the package has execute permissions

