import asyncio
import json
import os
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import importlib

# Initialize MCP server
app = Server("hackathon-mcp-server")

PLUGINS_DIR = "plugins"

def get_available_tools():
    """Get list of available plugin tools"""
    return [f.replace(".py", "") for f in os.listdir(PLUGINS_DIR) 
            if f.endswith(".py") and f != "__init__.py" and not f.startswith("__")]

async def run_plugin_tool(tool_name: str, arguments: dict):
    """Execute a plugin tool with given arguments"""
    try:
        module = importlib.import_module(f"{PLUGINS_DIR}.{tool_name}")
        result = module.run(arguments)
        return result
    except ModuleNotFoundError:
        return {"error": f"Tool '{tool_name}' not found."}
    except Exception as e:
        return {"error": str(e)}

@app.list_tools()
async def list_tools() -> list[Tool]:
    """List all available tools from plugins directory"""
    tools = []
    available_tools = get_available_tools()
    
    for tool_name in available_tools:
        try:
            # Try to get tool description from plugin
            module = importlib.import_module(f"{PLUGINS_DIR}.{tool_name}")
            description = getattr(module, 'DESCRIPTION', f"Execute {tool_name} tool")
            schema = getattr(module, 'SCHEMA', {
                "type": "object",
                "properties": {
                    "params": {"type": "object", "description": "Tool parameters"}
                }
            })
            
            tools.append(Tool(
                name=tool_name,
                description=description,
                inputSchema=schema
            ))
        except Exception as e:
            # Fallback tool definition
            tools.append(Tool(
                name=tool_name,
                description=f"Execute {tool_name} tool",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "params": {"type": "object", "description": "Tool parameters"}
                    }
                }
            ))
    
    return tools

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Execute a tool and return results"""
    result = await run_plugin_tool(name, arguments)
    
    return [TextContent(
        type="text",
        text=json.dumps(result, indent=2)
    )]

async def main():
    """Run the MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
