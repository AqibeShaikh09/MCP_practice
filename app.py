from flask import Flask, request, jsonify, render_template
import importlib
import os

app = Flask(__name__)

PLUGINS_DIR = "plugins"

def get_available_tools():
    return [f.replace(".py", "") for f in os.listdir(PLUGINS_DIR) if f.endswith(".py") and f != "__init__.py"]

def run_tool(tool_name, params):
    try:
        module = importlib.import_module(f"{PLUGINS_DIR}.{tool_name}")
        return module.run(params)
    except ModuleNotFoundError:
        return {"error": f"Tool '{tool_name}' not found."}
    except Exception as e:
        return {"error": str(e)}

@app.route("/")
def index():
    if "text/html" in request.headers.get("Accept", ""):
        return render_template("index.html")
    return jsonify({
        "message": "MCP Server is running",
        "available_tools": get_available_tools()
    })

@app.route("/run/<tool_name>", methods=["POST"])
def run(tool_name):
    params = request.get_json(force=True)
    result = run_tool(tool_name, params)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
