@echo off
echo 🚀 Setting up MCP Server for Hackathons...

REM Check if we're preparing for GitHub upload
if "%1"=="github" (
    echo 🧹 Cleaning up for GitHub upload...
    
    REM Remove virtual environment
    if exist myenv (
        echo 🗑️ Removing virtual environment myenv\...
        rmdir /s /q myenv
    )
    
    REM Remove database file
    if exist mcp.db (
        echo 🗑️ Removing database file mcp.db...
        del mcp.db
    )
    
    REM Remove __pycache__ directories
    echo 🗑️ Removing Python cache files...
    for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
    for /r . %%f in (*.pyc) do @if exist "%%f" del "%%f"
    
    REM Remove .env file
    if exist .env (
        echo 🗑️ Removing .env file contains API keys...
        del .env
    )
    
    REM Create .env.example if it doesn't exist
    if not exist .env.example (
        echo � Creating .env.example template...
        echo # MCP Server Environment Variables > .env.example
        echo # Copy this file to .env and add your actual API keys >> .env.example
        echo. >> .env.example
        echo GEMINI_API_KEY=your_gemini_api_key_here >> .env.example
        echo OPENWEATHER_API_KEY=your_openweather_api_key_here >> .env.example
    )
    
    REM Create .gitignore if it doesn't exist
    if not exist .gitignore (
        echo 📝 Creating .gitignore...
        echo # Environment variables > .gitignore
        echo .env >> .gitignore
        echo. >> .gitignore
        echo # Virtual environment >> .gitignore
        echo myenv/ >> .gitignore
        echo venv/ >> .gitignore
        echo env/ >> .gitignore
        echo. >> .gitignore
        echo # Python cache >> .gitignore
        echo __pycache__/ >> .gitignore
        echo *.pyc >> .gitignore
        echo *.pyo >> .gitignore
        echo *.pyd >> .gitignore
        echo. >> .gitignore
        echo # Database files >> .gitignore
        echo *.db >> .gitignore
        echo *.sqlite >> .gitignore
        echo *.sqlite3 >> .gitignore
        echo. >> .gitignore
        echo # IDE files >> .gitignore
        echo .vscode/ >> .gitignore
        echo .idea/ >> .gitignore
        echo *.swp >> .gitignore
        echo *.swo >> .gitignore
        echo. >> .gitignore
        echo # OS files >> .gitignore
        echo .DS_Store >> .gitignore
        echo Thumbs.db >> .gitignore
        echo. >> .gitignore
        echo # Logs >> .gitignore
        echo *.log >> .gitignore
        echo logs/ >> .gitignore
        echo. >> .gitignore
        echo # Temporary files >> .gitignore
        echo temp/ >> .gitignore
        echo tmp/ >> .gitignore
        echo *.tmp >> .gitignore
    )
    
    echo ✅ Repository cleaned for GitHub upload!
    echo.
    echo 📋 Files ready for GitHub:
    echo   ✓ Source code files
    echo   ✓ Configuration templates
    echo   ✓ Documentation
    echo   ✓ Setup scripts
    echo.
    echo 🚫 Excluded from GitHub:
    echo   ✗ Virtual environment myenv\
    echo   ✗ API keys .env
    echo   ✗ Database files *.db
    echo   ✗ Cache files __pycache__\
    echo.
    echo 📤 Ready to commit and push to GitHub!
    pause
    exit /b 0
)

REM Regular setup process
echo 📦 Creating virtual environment...
if not exist myenv (
    python -m venv myenv
)

echo �📦 Activating virtual environment...
call myenv\Scripts\activate.bat

echo 📦 Installing dependencies...
pip install -r requirements.txt

if not exist .env (
    echo 📝 Creating .env file...
    if exist .env.example (
        copy .env.example .env
    ) else (
        echo # MCP Server Environment Variables > .env
        echo GEMINI_API_KEY=your_gemini_api_key_here >> .env
        echo OPENWEATHER_API_KEY=your_openweather_api_key_here >> .env
    )
    echo Please edit .env file and add your API keys:
    echo   - GEMINI_API_KEY=your_gemini_api_key_here
    echo   - OPENWEATHER_API_KEY=your_openweather_api_key_here
)

echo ✅ Setup complete!
echo.
echo Next steps:
echo 1. Edit .env file with your API keys
echo 2. Test the server: python test_mcp.py
echo 3. Run the MCP server: python mcp_server.py
echo 4. Or run the Flask server: python app.py
echo.
echo For Claude Desktop integration:
echo 1. Copy claude_desktop_config.json content to your Claude Desktop config
echo 2. Update the paths and API keys in the config
echo.
echo 📤 To prepare for GitHub upload:
echo    setup.bat github

pause
