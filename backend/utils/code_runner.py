import subprocess
import sys
import tempfile
import os
import shutil


def run_python_code(code: str, stdin: str = "", timeout: int = 10) -> tuple:
    """Run Python code in a subprocess and return (stdout, stderr)."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".py", delete=False, encoding="utf-8"
    ) as f:
        f.write(code)
        fname = f.name

    try:
        result = subprocess.run(
            [sys.executable, fname],
            input=stdin,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return "", "⏱️  Execution timed out (10 s limit)"
    except Exception as e:
        return "", f"❌  Runtime error: {str(e)}"
    finally:
        try:
            os.unlink(fname)
        except Exception:
            pass


def run_javascript_code(code: str, stdin: str = "", timeout: int = 10) -> tuple:
    """Run JavaScript with Node.js if available."""
    node_exe = shutil.which("node")
    if not node_exe:
        return (
            "",
            "⚠️  Node.js not found. Install Node.js to run JavaScript code.",
        )

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".js", delete=False, encoding="utf-8"
    ) as f:
        f.write(code)
        fname = f.name

    try:
        result = subprocess.run(
            [node_exe, fname],
            input=stdin,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return "", "⏱️  Execution timed out (10 s limit)"
    except Exception as e:
        return "", f"❌  Runtime error: {str(e)}"
    finally:
        try:
            os.unlink(fname)
        except Exception:
            pass


# Map language names → runner functions
_RUNNERS = {
    "python": run_python_code,
    "javascript": run_javascript_code,
    "js": run_javascript_code,
}

_COMPILER_HINTS = {
    "java":       "☕  Java: install JDK and run `javac + java` locally.",
    "cpp":        "⚙️  C++: install g++ / MSVC and compile locally.",
    "c":          "⚙️  C: install gcc / MSVC and compile locally.",
    "go":         "🐹  Go: install the Go toolchain and run `go run` locally.",
    "rust":       "🦀  Rust: install Rust and run `cargo run` locally.",
    "typescript": "🔷  TypeScript: install ts-node (`npm i -g ts-node`) to run .ts files.",
    "bash":       "🐚  Bash: only available on Unix/Mac environments.",
}


def run_code(code: str, language: str, stdin: str = "") -> tuple:
    """
    Execute code for the given language.
    Returns (stdout, stderr) strings.
    """
    lang = language.lower().strip()
    runner = _RUNNERS.get(lang)

    if runner:
        return runner(code, stdin=stdin)

    hint = _COMPILER_HINTS.get(lang, f"Running {language} is not yet supported here.")
    return "", hint
