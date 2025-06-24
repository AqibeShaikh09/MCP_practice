# MCP Server for Hackathons 🚀

A Model Context Protocol (MCP) server with plugin-based tools for hackathon development. This server provides AI models with access to various tools including Gemini AI, weather data, shell commands, and database operations.

## Features

- **🤖 Gemini AI Integration**: Generate text using Google's Gemini models
- **🌤️ Weather Service**: Get real-time weather data for any location
- **💻 Shell Commands**: Execute safe shell commands
- **🗄️ Database Operations**: Store and retrieve key-value records
- **� Simple Text Generator**: Fallback text generation when AI APIs are unavailable
- **�🔌 Plugin System**: Easy to extend with new tools
- **🌐 Dual Interface**: Both MCP protocol and web interface

## Quick Setup

### 1. Clone and Install Dependencies
```bash
# Clone the repository
git clone <your-repo-url>
cd MCP_practice

# Windows
setup.bat

# Linux/Mac
chmod +x setup.sh
./setup.sh
```

### 2. Configure API Keys
Copy the example environment file and add your API keys:
```bash
# Copy template
cp .env.example .env

# Edit with your actual API keys
GEMINI_API_KEY=your_gemini_api_key_here
OPENWEATHER_API_KEY=your_openweather_api_key_here
```

### 3. Test the Server
```bash
python test_mcp.py
```

### 4. Run the Server
```bash
# MCP Protocol Server (for Claude Desktop)
python mcp_server.py

# Web Interface Server (for browser testing)
python app.py
```

## Available Tools

### 🤖 Gemini AI Tool
Generate text using Google's Gemini models.

**Parameters:**
- `prompt` (required): Text prompt for generation
- `model`: Gemini model to use (gemini-1.5-pro, gemini-1.5-flash, gemini-pro)
- `max_tokens`: Maximum tokens to generate (default: 1000)

**Example:**
```json
{
  "prompt": "Write a Python function to calculate fibonacci numbers",
  "model": "gemini-1.5-pro",
  "max_tokens": 500
}
```

### 🌤️ Weather Tool
Get current weather information for any location.

**Parameters:**
- `city` (required): City name
- `units`: Temperature units (metric, imperial, kelvin)

**Example:**
```json
{
  "city": "London",
  "units": "metric"
}
```

### 💻 Shell Tool
Execute shell commands safely with security restrictions.

**Parameters:**
- `command` (required): Shell command to execute
- `timeout`: Command timeout in seconds (default: 30)

**Example:**
```json
{
  "command": "echo Hello World",
  "timeout": 10
}
```

### 🗄️ Database Tool
Perform CRUD operations on key-value records.

**Parameters:**
- `action` (required): Database action (insert, query, delete, list_all)
- `key`: Record key (required for insert/query)
- `value`: Record value (required for insert)
- `id`: Record ID (required for delete)

**Examples:**
```json
// Insert
{
  "action": "insert",
  "key": "user_preference",
  "value": "dark_theme"
}

// Query
{
  "action": "query",
  "key": "user_preference"
}

// Delete
{
  "action": "delete",
  "id": 1
}

// List all
{
  "action": "list_all"
}
```

### 📝 Simple Text Tool
Fallback text generator when AI APIs are unavailable.

**Parameters:**
- `prompt` (required): Text prompt for generation
- `style`: Generation style (creative, technical, simple)

**Example:**
```json
{
  "prompt": "Explain machine learning",
  "style": "technical"
}
```

## Claude Desktop Integration

1. Copy the content from `claude_desktop_config.json`
2. Add it to your Claude Desktop configuration file
3. Update the paths and API keys
4. Restart Claude Desktop

The configuration file location:
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

## Adding New Tools

Create a new Python file in the `plugins/` directory:

```python
# plugins/my_tool.py

# MCP metadata
DESCRIPTION = "Description of what your tool does"
SCHEMA = {
    "type": "object",
    "properties": {
        "parameter_name": {
            "type": "string",
            "description": "Parameter description"
        }
    },
    "required": ["parameter_name"]
}

def run(params):
    # Your tool logic here
    return {
        "tool": "my_tool",
        "result": "Tool output"
    }
```

The tool will be automatically discovered and made available.

## Project Structure

```
├── app.py                      # Flask web server
├── mcp_server.py              # MCP protocol server
├── database.py                # Database configuration
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables
├── plugins/                   # Tool plugins
│   ├── gemini.py             # Gemini AI tool
│   ├── weather.py            # Weather tool
│   ├── shell.py              # Shell command tool
│   └── db.py                 # Database tool
├── templates/
│   └── index.html            # Web interface
└── myenv/                    # Virtual environment
```

## Security Notes

- Shell commands have security restrictions to prevent dangerous operations
- API keys are loaded from environment variables only
- Database operations are isolated to the local SQLite database
- Command timeouts prevent hanging processes

## Troubleshooting

### "Module not found" errors
```bash
pip install -r requirements.txt
```

### "API key not found" errors
Make sure your `.env` file contains the correct API keys.

### Gemini API quota exceeded errors
The free tier has strict limits:
- **gemini-1.5-pro**: 15 requests/minute, 1,500 requests/day
- **gemini-1.5-flash**: 15 requests/minute, 1,500 requests/day
- **gemini-pro**: 60 requests/minute, 1,500 requests/day

**Solutions:**
1. Wait a few minutes and try again
2. Use `gemini-1.5-flash` (often has better availability)
3. Reduce `max_tokens` in your requests
4. Upgrade to a paid plan for higher quotas
5. The plugin automatically tries fallback models

### "Permission denied" on shell commands
Some commands may be blocked for security reasons.

### Database connection issues
The SQLite database file (`mcp.db`) will be created automatically.

## Contributing

1. Add new tools to the `plugins/` directory
2. Include proper MCP metadata (DESCRIPTION and SCHEMA)
3. Handle errors gracefully
4. Test with both MCP and web interfaces

## Development

### Preparing for GitHub Upload
To clean the repository for GitHub upload (removes sensitive files):

```bash
# Windows
setup.bat github

# Linux/Mac
./setup.sh github
```

This will:
- Remove virtual environment (`myenv/`)
- Remove database files (`*.db`)
- Remove API keys (`.env`)
- Remove Python cache files (`__pycache__/`)
- Create `.gitignore` and `.env.example`

### Setting up from GitHub
After cloning from GitHub:

1. Run setup script to create virtual environment
2. Copy `.env.example` to `.env`
3. Add your actual API keys
4. Test the server

## License

MIT License - feel free to use in your hackathon projects!

---

Happy hacking! 🎉
