# MultiBrowser - Qt6 Tabbed Web Browser

A lightweight tabbed web browser built with PyQt6 and QtWebEngine, designed for use with window managers like Hyprland.

## Features

- **Tabbed Interface**: Multiple web pages in separate tabs (fixed configuration)
- **JSON Configuration**: Load tabs from a JSON configuration file
- **Window Class Support**: Command line option for window class (useful for Hyprland scratchpads)
- **Persistent Cookies**: Logins and sessions persist across browser restarts
- **CSS Theming**: Beautiful themes with FiraCode Nerd Font support
- **Keyboard Shortcuts**:
  - `Alt+1` to `Alt+0`: Switch to tabs 1-10
  - `Ctrl++`: Zoom in
  - `Ctrl+-`: Zoom out
  - `Ctrl+0`: Reset zoom
- **Google.com Token Support**: Full web engine compatibility for modern websites
- **Fixed Tab Configuration**: No add/close tab functionality (as requested)

## Installation

### Prerequisites
- Python 3.7+
- pip
- Qt6 development libraries (on Linux)

### Setup

1. **Clone the repository or create the project structure:**
   ```bash
   git clone https://github.com/yourusername/multibrowser.git
   cd multibrowser
   ```

2. **Create and activate virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install PyQt6 PyQt6-WebEngine
   ```

## Usage

### Basic Usage
```bash
# Start with default configuration
python3 main.py

# Start with custom config file
python3 main.py --config my_tabs.json

# Start with custom window class (for Hyprland scratchpads)
python3 main.py --window-class "my-browser-class"
```

### Using the Startup Script
```bash
# Make the script executable (if not already)
chmod +x start_multibrowser.sh

# Launch the browser
./start_multibrowser.sh

# Launch with custom window class
./start_multibrowser.sh --window-class "custom-class"
```

### Hyprland Scratchpad Configuration

Add this to your Hyprland configuration (`~/.config/hypr/hyprland.conf`):

```ini
windowrule = float,class:^(multibrowser)$
windowrule = size 80% 80%,class:^(multibrowser)$
windowrule = center,class:^(multibrowser)$

bind = SUPER, B, exec, /path/to/multibrowser/start_multibrowser.sh --window-class "multibrowser"
```

## Configuration

The browser loads tabs from a JSON configuration file. By default, it looks for `tabs.json` in the same directory.

### Example `tabs.json`

```json
[
    {
        "title": "Google",
        "url": "https://www.google.com"
    },
    {
        "title": "GitHub",
        "url": "https://github.com"
    },
    {
        "title": "DuckDuckGo",
        "url": "https://duckduckgo.com"
    }
]
```

### Configuration Options

- `title`: The display name for the tab
- `url`: The URL to load in the tab

## Command Line Options

```
usage: main.py [-h] [--config CONFIG] [--window-class WINDOW_CLASS]
               [--theme {dark,tokyo-night}]

MultiBrowser - Tabbed Web Browser

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG       Path to JSON config file with tabs
  --window-class WINDOW_CLASS
                        Window class for window manager identification
  --theme {dark,tokyo-night}
                        Theme for the browser (dark, tokyo-night)
```

## Persistent Cookies and Sessions

The browser now features **persistent cookie storage** to maintain logins and sessions across browser restarts:

- **Persistent Profile**: All tabs share a common profile with persistent storage
- **Cookie Storage**: Cookies are saved to disk and persist between sessions
- **HTTP Cache**: Web content is cached for better performance
- **Session Management**: Login sessions (including Google tokens) are preserved

### Cookie Storage Location

Cookies and session data are stored in:
- **Linux**: `~/.local/share/MultiBrowser/`
- **Windows**: `%APPDATA%\MultiBrowser\`
- **macOS**: `~/Library/Application Support/MultiBrowser/`

### CSS Theming

The browser supports beautiful CSS themes with custom styling:

**Available Themes:**
- `dark` - Professional dark theme with blue accents (default)
- `tokyo-night` - Tokyo Night inspired theme with purple/blue accents

**Features:**
- FiraCode Nerd Font support (24px) for tabs
- Custom color schemes
- Hover and selection effects
- Professional styling

### Keyboard Shortcut Indicators

The first 10 tabs display keyboard shortcut indicators in their titles:
- Tab 1: `(Alt+1) Title`
- Tab 2: `(Alt+2) Title`
- ...
- Tab 10: `(Alt+0) Title`

This uses the standard `Alt+n` notation which is widely recognized across platforms.

### Testing Keyboard Shortcuts

You can test the keyboard shortcut functionality using the provided test script:

```bash
python3 test_keyboard_shortcuts.py
```

Then press:
- `Alt+1` to switch to tab 1
- `Alt+5` to switch to tab 5
- `Alt+0` to switch to tab 10

### Testing CSS Styling

You can test the styling functionality using the provided test script:

```bash
# Test dark theme
python3 test_styling.py --theme dark

# Test Tokyo Night theme
python3 test_styling.py --theme tokyo-night
```

### Testing Persistent Cookie Functionality

You can test the persistent cookie functionality using the provided test script:

```bash
python3 test_persistent_cookies_simple.py
```

This script will:
1. Set up a persistent profile
2. Configure cookie storage
3. Verify all persistent features are working
4. Provide a summary of cookie persistence functionality

The test will automatically close after completing all checks.

## Google.com Token Support

The browser is configured with full QtWebEngine settings to ensure compatibility with modern websites including:

- JavaScript enabled
- Local storage support
- WebGL and accelerated canvas
- Cookies and session storage
- Modern web APIs

This ensures that Google.com tokens and other authentication mechanisms work properly.

## Development

### Running in Development Mode

```bash
source venv/bin/activate
python3 main.py --config dev_tabs.json
```

### Debugging

```bash
# Run with debug output
python3 -v main.py

# Check Qt debug messages
QT_DEBUG_PLUGINS=1 python3 main.py
```

## Troubleshooting

### Missing Qt Dependencies

On some Linux distributions, you may need to install Qt6 development packages:

**Debian/Ubuntu:**
```bash
sudo apt-get install qt6-base-dev qt6-webengine-dev
```

**Arch Linux:**
```bash
sudo pacman -S qt6-base qt6-webengine
```

**Fedora:**
```bash
sudo dnf install qt6-qtbase-devel qt6-qtwebengine-devel
```

### Window Class Not Working

If the window class doesn't work with your window manager:

1. Check that you're using the `--window-class` parameter
2. Verify the window class with `xprop | grep WM_CLASS` (for X11) or equivalent Wayland tools
3. Try different window manager rules

### Web Content Not Loading

Ensure you have proper internet connectivity and that your system has the required QtWebEngine dependencies installed.

## Chezmoi Setup

### Files to Add to `.chezmoiignore`

Add these files to your `.chezmoiignore` to exclude them from chezmoi management:

```
# Virtual environment
venv/

# Python cache
__pycache__/
*.pyc

# Test files (optional - include if you want to manage tests)
test_*.py

# Debug files
debug_*.py

# Cache and data directories
.themes/
```

### Initial Setup Script

Add this to your chezmoi template script for initial setup:

```bash
#!/bin/bash

# MultiBrowser setup script for chezmoi

echo "🚀 Setting up MultiBrowser..."

# Create virtual environment
python3 -m venv venv

# Activate and install dependencies
source venv/bin/activate
pip install PyQt6 PyQt6-WebEngine

# Set up initial tabs configuration
if [ ! -f tabs.json ]; then
    cat > tabs.json << 'EOF'
[
    {
        "title": "Google",
        "url": "https://www.google.com"
    },
    {
        "title": "GitHub",
        "url": "https://github.com"
    },
    {
        "title": "DuckDuckGo",
        "url": "https://duckduckgo.com"
    }
]
EOF
    echo "✓ Created initial tabs.json"
fi

# Make scripts executable
chmod +x start_multibrowser.sh
chmod +x test_*.py
chmod +x debug_keyboard.py
chmod +x test_keyboard_manual.py

# Install FiraCode Nerd Font (optional but recommended)
if ! fc-list | grep -q "FiraCode"; then
    echo "💡 Installing FiraCode Nerd Font..."
    mkdir -p ~/.local/share/fonts
    cd ~/.local/share/fonts
    wget https://github.com/ryanoasis/nerd-fonts/releases/download/v3.2.1/FiraCode.zip
    unzip FiraCode.zip
    rm FiraCode.zip
    fc-cache -fv
    echo "✓ FiraCode Nerd Font installed"
else
    echo "✓ FiraCode Nerd Font already installed"
fi

echo "🎉 MultiBrowser setup complete!"
echo ""
echo "Usage:"
echo "  ./start_multibrowser.sh        # Launch with default settings"
echo "  ./start_multibrowser.sh --help # Show all options"
```

### Chezmoi Template File Structure

```
multibrowser/
├── main.py                  # Main application (managed)
├── tabs.json                # Tab configuration (managed)
├── start_multibrowser.sh    # Startup script (managed)
├── themes/                  # Theme CSS files (managed)
│   ├── dark.css
│   └── tokyo-night.css
├── README.md                # Documentation (managed)
├── FONTS.md                 # Font info (managed)
├── .chezmoiignore           # Chezmoi ignore file
└── setup.sh                 # Setup script (managed)
```

### Deployment Steps

1. **Add to chezmoi:**
   ```bash
   chezmoi add multibrowser/
   ```

2. **Apply to new machine:**
   ```bash
   chezmoi apply
   cd multibrowser
   ./setup.sh
   ```

3. **Update existing installation:**
   ```bash
   cd multibrowser
   git pull
   source venv/bin/activate
   pip install -r requirements.txt  # If requirements change
   ```

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please open issues or pull requests on GitHub.