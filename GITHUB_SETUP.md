# GitHub Setup for Custom Piston Packages

## Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `piston-packages`
3. Description: "Custom Piston packages for Steacher (Scala 2.13)"
4. Make it **Public** (required for GitHub Pages)
5. Click "Create repository"

## Step 2: Upload Package to GitHub Release

1. In your new repository, click "Releases" (right sidebar)
2. Click "Create a new release"
3. Tag version: `v1.0.0`
4. Release title: `Scala 2.13.16 Package`
5. Description: 
   ```
   Custom Piston package for Scala 2.13.16 with Java 17 support.
   
   Features:
   - Scala 2.13.16
   - Support for both `object X { def main(...) }` and `object X extends App`
   - SHA256: 9202d928f30eea25c0ff4c1f3ee11002bc937d605900214948f15ee664441be6
   ```
6. Attach the file: `scala-2.13.16.pkg.tar.gz` (drag and drop or click to upload)
7. Click "Publish release"

## Step 3: Set Up GitHub Pages for Index File

1. In your repository, click "Settings"
2. Scroll down to "Pages" section (left sidebar under "Code and automation")
3. Under "Source", select:
   - Source: "Deploy from a branch"
   - Branch: `main` (or `master`)
   - Folder: `/ (root)`
4. Click "Save"

## Step 4: Create Index File in Repository

1. In your repository main page, click "Add file" → "Create new file"
2. Name the file: `index` (no extension)
3. Paste this content:
   ```
   scala,2.13.16,9202d928f30eea25c0ff4c1f3ee11002bc937d605900214948f15ee664441be6,https://github.com/renaud/piston-packages/releases/download/v1.0.0/scala-2.13.16.pkg.tar.gz
   ```
5. Commit the file (click "Commit new file")

## Step 5: Get Your Index URL

After GitHub Pages is enabled (takes 1-2 minutes), your index will be available at:

```
https://renaud.github.io/piston-packages/index
```



## Step 6: Configure Piston to Use Your Custom Index

Stop and remove the existing Piston container:
```bash
docker stop piston_api
docker rm piston_api
```

Start Piston with your custom index:
```bash
cd sandbox_executor

docker run --privileged \
  -v $PWD/piston_data:/piston \
  -e PISTON_REPO_URL=https://renaud.github.io/piston-packages/index \
  -dit -p 2000:2000 --name piston_api \
  ghcr.io/engineer-man/piston
```

## Step 7: Install Scala 2.13.16

```bash
# Install Scala 2.13.16
curl -X POST -H "Content-Type: application/json" \
  -d '{"language":"scala","version":"2.13.16"}' \
  http://localhost:2000/api/v2/packages

# Verify it's installed
curl -s http://localhost:2000/api/v2/runtimes | python3 -m json.tool
```

## Step 8: Test Scala 2.13.16

Test with both syntax styles:

```python
import requests

PISTON_URL = "http://localhost:2000/api/v2/execute"

# Test 1: Traditional main method
scala_main = """
object Hello {
  def main(args: Array[String]): Unit = {
    println("Hello from Scala 2.13 with main method!")
  }
}
"""

# Test 2: App trait
scala_app = """
object HelloApp extends App {
  println("Hello from Scala 2.13 with App trait!")
}
"""

for name, code in [("main method", scala_main), ("App trait", scala_app)]:
    payload = {
        "language": "scala",
        "version": "2.13.16",
        "files": [{"name": "main.scala", "content": code}],
        "compile_timeout": 10000,
        "run_timeout": 3000,
    }
    
    response = requests.post(PISTON_URL, json=payload)
    result = response.json()
    
    print(f"\n--- Test: {name} ---")
    if "compile" in result and result["compile"]["stderr"]:
        print(f"Compilation Error:\n{result['compile']['stderr']}")
    print(result["run"]["stdout"])
    if result["run"]["stderr"]:
        print(f"Errors:\n{result['run']['stderr']}")
```

## Troubleshooting

### Index file not found
- Wait 2-3 minutes after enabling GitHub Pages
- Check that the file is named exactly `index` (no extension)
- Verify GitHub Pages is enabled in Settings → Pages
- Try accessing the URL directly in your browser

### Package download fails
- Verify the release is published (not draft)
- Check the URL in the index file matches your actual release URL
- Ensure the repository is public

### Scala compilation fails
- Check Docker logs: `docker logs piston_api`
- Verify the package installed: `curl -s http://localhost:2000/api/v2/runtimes`
- Check the compile script has execute permissions in the package

## Notes

- The custom index ONLY contains Scala 2.13.16
- Piston will fall back to the official index for other languages (Python, etc.)
- You can add more packages to your index file (one per line, same format)
- Keep the `scala-2.13.16.pkg.tar.gz` file - you'll need it for the release

