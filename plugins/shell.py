import subprocess
import platform

# MCP metadata
DESCRIPTION = "Execute shell commands safely"
SCHEMA = {
    "type": "object",
    "properties": {
        "command": {
            "type": "string",
            "description": "The shell command to execute"
        },
        "timeout": {
            "type": "integer",
            "description": "Command timeout in seconds",
            "default": 30
        }
    },
    "required": ["command"]
}

def run(params):
    command = params.get("command", "")
    if not command:
        return {
            "tool": "shell",
            "error": "Missing 'command' parameter"
        }
    
    timeout = params.get("timeout", 30)
    
    # Basic security check - block dangerous commands
    dangerous_commands = ["rm -rf", "del /f", "format", "shutdown", "reboot"]
    if any(dangerous in command.lower() for dangerous in dangerous_commands):
        return {
            "tool": "shell",
            "error": "Command blocked for security reasons"
        }
    
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True,
            timeout=timeout
        )
        
        return {
            "tool": "shell",
            "command": command,
            "return_code": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "platform": platform.system(),
            "result": result.stdout.strip() if result.returncode == 0 else f"Error: {result.stderr.strip()}"
        }
        
    except subprocess.TimeoutExpired:
        return {
            "tool": "shell",
            "error": f"Command timed out after {timeout} seconds"
        }
    except Exception as e:
        return {
            "tool": "shell",
            "error": f"Shell execution error: {str(e)}"
        }
