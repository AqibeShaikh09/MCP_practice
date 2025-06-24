#!/bin/bash

echo "🚀 Setting up MCP Server for Hackathons..."

# Check if we're preparing for GitHub upload
if [ "$1" == "github" ]; then
    echo "🧹 Cleaning up for GitHub upload..."
    
    # Remove virtual environment (too large for GitHub)
    if [ -d "myenv" ]; then
        echo "🗑️ Removing virtual environment (myenv/)..."
        rm -rf myenv/
    fi
    
    # Remove database file (user-specific data)
    if [ -f "mcp.db" ]; then
        echo "🗑️ Removing database file (mcp.db)..."
        rm -f mcp.db
    fi
    
    # Remove __pycache__ directories
    echo "🗑️ Removing Python cache files..."
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -name "*.pyc" -delete 2>/dev/null || true
    
    # Remove .env file (contains sensitive API keys)
    if [ -f ".env" ]; then
        echo "🗑️ Removing .env file (contains API keys)..."
        rm -f .env
    fi
    
    # Create .env.example if it doesn't exist
    if [ ! -f ".env.example" ]; then
        echo "📝 Creating .env.example template..."
        cat > .env.example << EOF
# MCP Server Environment Variables
# Copy this file to .env and add your actual API keys

GEMINI_API_KEY=your_gemini_api_key_here
OPENWEATHER_API_KEY=your_openweather_api_key_here
EOF
    fi
    
    # Create .gitignore if it doesn't exist
    if [ ! -f ".gitignore" ]; then
        echo "📝 Creating .gitignore..."
        cat > .gitignore << EOF
# Environment variables
.env

# Virtual environment
myenv/
venv/
env/

# Python cache
__pycache__/
*.pyc
*.pyo
*.pyd

# Database files
*.db
*.sqlite
*.sqlite3

# IDE files
.vscode/
.idea/
*.swp
*.swo

# OS files
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Temporary files
temp/
tmp/
*.tmp
EOF
    fi
    
    echo "✅ Repository cleaned for GitHub upload!"
    echo ""
    echo "📋 Files ready for GitHub:"
    echo "  ✓ Source code files"
    echo "  ✓ Configuration templates"
    echo "  ✓ Documentation"
    echo "  ✓ Setup scripts"
    echo ""
    echo "🚫 Excluded from GitHub:"
    echo "  ✗ Virtual environment (myenv/)"
    echo "  ✗ API keys (.env)"
    echo "  ✗ Database files (*.db)"
    echo "  ✗ Cache files (__pycache__/)"
    echo ""
    echo "📤 Ready to commit and push to GitHub!"
    exit 0
fi

# Regular setup process
echo "📦 Creating virtual environment..."
if [ ! -d "myenv" ]; then
    python -m venv myenv
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source myenv/Scripts/activate
else
    source myenv/bin/activate
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
    else
        cat > .env << EOF
# MCP Server Environment Variables
GEMINI_API_KEY=your_gemini_api_key_here
OPENWEATHER_API_KEY=your_openweather_api_key_here
EOF
    fi
    echo "Please edit .env file and add your API keys:"
    echo "  - GEMINI_API_KEY=your_gemini_api_key_here"
    echo "  - OPENWEATHER_API_KEY=your_openweather_api_key_here"
fi

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your API keys"
echo "2. Test the server: python test_mcp.py"
echo "3. Run the MCP server: python mcp_server.py"
echo "4. Or run the Flask server: python app.py"
echo ""
echo "For Claude Desktop integration:"
echo "1. Copy claude_desktop_config.json content to your Claude Desktop config"
echo "2. Update the paths and API keys in the config"
echo ""
echo "📤 To prepare for GitHub upload:"
echo "   ./setup.sh github"
