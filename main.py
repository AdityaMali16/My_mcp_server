import platform
import subprocess
from pathlib import Path
import os
import psutil
from fastmcp import FastMCP

mcp = FastMCP("Personal AI Command Center")


@mcp.tool()
def get_system_info():
    """Get CPU, RAM and disk information."""
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    return {
        "os": platform.system(),
        "processor": platform.processor(),
        "cpu_usage": f"{psutil.cpu_percent()}%",
        "ram_usage": f"{ram.percent}%",
        "ram_free_gb": round(ram.available / 1024**3, 2),
        "disk_free_gb": round(disk.free / 1024**3, 2),
    }


@mcp.tool()
def list_directory(path: str):
    """List files and folders."""
    folder = Path(path)

    if not folder.exists():
        return "Path does not exist."

    return [item.name for item in folder.iterdir()]


@mcp.tool()
def read_file(path: str):
    """Read a text file."""
    try:
        return Path(path).read_text(
            encoding="utf-8",
            errors="ignore"
        )[:20000]
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
def git_status(path: str):
    """Check Git status."""
    try:
        result = subprocess.run(
            ["git", "-C", path, "status", "--short"],
            capture_output=True,
            text=True
        )

        return result.stdout or "Working tree clean."

    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
def get_processes():
    """Show top processes using RAM."""
    processes = []

    for p in psutil.process_iter(["pid", "name", "memory_percent"]):
        try:
            processes.append(p.info)
        except:
            pass

    processes.sort(
        key=lambda x: x["memory_percent"] or 0,
        reverse=True
    )

    return processes[:10]


if __name__ == "__main__":
 

    mcp.run(
        transport="streamable_http",
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000))
    )
