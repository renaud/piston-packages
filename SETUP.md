To run Piston, you can either use the public API for quick testing or set up a self-hosted instance using Docker for production-grade privacy and performance.

### 1. Setup: Start a Local Piston Server

If you have Docker installed, you can launch a Piston instance on your server with a single command. This starts the API on port 2000.

```bash
# Create a dedicated directory for Piston data (only needed once)
mkdir -p piston_data

# Start the container with the dedicated data directory
docker run --privileged -v $PWD/piston_data:/piston -dit -p 2000:2000 --name piston_api ghcr.io/engineer-man/piston
```

*Note: After starting the container, you must install the language runtimes you need (e.g., `python` and `scala`) using the Piston CLI manager inside the container or via the API.*

### 2. Demo Code: Python Client

The following Python code demonstrates how to send arbitrary snippets of Python and Scala to your local Piston engine for execution.

```python
import requests

PISTON_URL = "http://localhost:2000/api/v2/execute"

def run_code(language, version, code_content, file_name="main"):
    payload = {
        "language": language,
        "version": version,
        "files": [
            {
                "name": f"{file_name}.{language}",
                "content": code_content
            }
        ],
        "compile_timeout": 10000, # 10 seconds
        "run_timeout": 3000,      # 3 seconds
    }
    
    try:
        response = requests.post(PISTON_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        
        # Piston returns separate keys for compilation and execution
        if "compile" in result and result["compile"]["stderr"]:
            print(f"Compilation Error:\n{result['compile']['stderr']}")
        
        print(f"--- Output for {language} ---")
        print(result["run"]["stdout"])
        if result["run"]["stderr"]:
            print(f"Errors:\n{result['run']['stderr']}")
            
    except Exception as e:
        print(f"Error connecting to Piston: {e}")

# --- Example 1: Running Python ---
python_snippet = "print('Hello from a Python sandbox!')"
run_code("python", "3.10.0", python_snippet)

# --- Example 2: Running Scala ---
# Scala 3 uses @main annotation for entry points
scala_snippet = """
@main def hello(): Unit = {
  val msg = "Hello from a Scala sandbox!"
  println(msg)
}
"""
run_code("scala", "3.0.0", scala_snippet)

```

To install languages, use the API:

```bash
# List available packages
curl -s http://localhost:2000/api/v2/packages | python3 -m json.tool

# Install Python 3.10.0
curl -X POST -H "Content-Type: application/json" \
  -d '{"language":"python","version":"3.10.0"}' \
  http://localhost:2000/api/v2/packages

# Install Scala 3.0.0
curl -X POST -H "Content-Type: application/json" \
  -d '{"language":"scala","version":"3.0.0"}' \
  http://localhost:2000/api/v2/packages

# Verify installed runtimes
curl -s http://localhost:2000/api/v2/runtimes | python3 -m json.tool
```

### Key Technical Details

* **Execution Workflow:** When the API receives your POST request, it writes the content to a temporary file inside an **Isolate** sandbox (using Linux namespaces and cgroups) and executes it.


* **Response Format:** The response contains a `run` object with `stdout`, `stderr`, and a two-letter `status` code (e.g., `TO` for timeout, `RE` for runtime error).


* **Isolation:** By default, Piston disables outgoing network interaction and caps memory and CPU time to prevent "fork bombs" or resource exhaustion.


* **Language Versions:** You can query `GET /api/v2/runtimes` to see the exact strings required for the `language` and `version` fields for your specific installation.