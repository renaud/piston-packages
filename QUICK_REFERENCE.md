# Scala 2.13 Piston Package - Quick Reference

## Setup Checklist

- [ ] Create GitHub repo: `steacher-piston-packages`
- [ ] Upload `scala-2.13.16.pkg.tar.gz` to release v1.0.0
- [ ] Enable GitHub Pages
- [ ] Create `index` file with your GitHub username
- [ ] Restart Piston with custom index URL
- [ ] Install Scala 2.13.16 via API
- [ ] Run test suite

## Key Commands

### Start Piston with Custom Index
```bash
docker run --privileged \
  -v $PWD/piston_data:/piston \
  -e PISTON_REPO_URL=https://YOUR_USERNAME.github.io/steacher-piston-packages/index \
  -dit -p 2000:2000 --name piston_api \
  ghcr.io/engineer-man/piston
```

### Install Scala 2.13.16
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"language":"scala","version":"2.13.16"}' \
  http://localhost:2000/api/v2/packages
```

### Check Installed Runtimes
```bash
curl -s http://localhost:2000/api/v2/runtimes | python3 -m json.tool
```

### Run Test Suite
```bash
python3 test_scala_2.13.py
```

## Package Info

- **File**: `scala-2.13.16.pkg.tar.gz`
- **Size**: 22MB
- **SHA256**: `9202d928f30eea25c0ff4c1f3ee11002bc937d605900214948f15ee664441be6`
- **Aliases**: `scala2`, `scala2.13`

## Index File Format

```
scala,2.13.16,9202d928f30eea25c0ff4c1f3ee11002bc937d605900214948f15ee664441be6,https://github.com/YOUR_USERNAME/steacher-piston-packages/releases/download/v1.0.0/scala-2.13.16.pkg.tar.gz
```

## Supported Syntax

### Option 1: Main Method
```scala
object Hello {
  def main(args: Array[String]): Unit = {
    println("Hello!")
  }
}
```

### Option 2: App Trait
```scala
object Hello extends App {
  println("Hello!")
}
```

## API Usage Example

```python
import requests

response = requests.post("http://localhost:2000/api/v2/execute", json={
    "language": "scala",
    "version": "2.13.16",
    "files": [{
        "name": "main.scala",
        "content": 'object Hello { def main(args: Array[String]): Unit = println("Hi!") }'
    }],
    "compile_timeout": 10000,
    "run_timeout": 3000,
})

result = response.json()
print(result["run"]["stdout"])
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Index not found | Wait 2-3 min after enabling GitHub Pages |
| Package won't install | Check release is published, not draft |
| Compilation fails | Verify syntax (main method or App trait) |
| Runtime error | Check Docker logs: `docker logs piston_api` |

## URLs to Replace

Throughout the setup, replace these placeholders:
- `YOUR_USERNAME` → Your GitHub username
- Example: If username is `rsmith`, index URL is:
  `https://rsmith.github.io/steacher-piston-packages/index`

## Next Steps After Setup

1. Test locally with `test_scala_2.13.py`
2. Update your Steacher deployment config with the custom index URL
3. Add Scala 2.13.16 installation to your deployment scripts
4. Update your exercise execution code to use version `2.13.16`

## Production Deployment Notes

- Set `PISTON_REPO_URL` environment variable in docker-compose
- Install Scala 2.13.16 on container startup
- Keep Python 3.10.0 from official index (works automatically)
- Monitor that both runtimes are available before serving traffic

