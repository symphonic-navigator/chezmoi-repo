#!/usr/bin/env python3

import sys
import json
import argparse
import os
import threading
import time
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget, QTabBar, QLabel, QHBoxLayout, QToolButton, QMenu
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineSettings, QWebEngineProfile
from PyQt6.QtCore import Qt, QStandardPaths, QFile, QTextStream, QIODevice, QSize
from PyQt6.QtGui import QFontDatabase, QFont, QColor, QShortcut, QKeySequence, QAction

# Configuration constants
DEFAULT_CONFIG_DIR = os.path.expanduser("~/.config/multibrowser")
DEFAULT_CONFIG_FILE = os.path.join(DEFAULT_CONFIG_DIR, "multibrowser.json")
DEFAULT_THEME = "tokyo-night"  # Default to tokyo-night theme
DEFAULT_DARK_MODE = True  # Default to dark mode

class CustomTabBar(QTabBar):
    """Custom tab bar with rich text formatting for keyboard shortcuts"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.shortcut_color = QColor("#ffffff")  # Default shortcut color
        self.title_color = QColor("#ffffff")    # Default title color
        self.font = QFont("Monospace", 24)     # Default font


def load_config():
    """Load configuration from persistent config file"""
    try:
        # Create config directory if it doesn't exist
        os.makedirs(DEFAULT_CONFIG_DIR, exist_ok=True)
        
        if os.path.exists(DEFAULT_CONFIG_FILE):
            with open(DEFAULT_CONFIG_FILE, 'r') as f:
                config = json.load(f)
                print(f"✓ Loaded config from {DEFAULT_CONFIG_FILE}")
                return config
        else:
            # Return default config if file doesn't exist
            default_config = {
                'theme': DEFAULT_THEME,
                'dark_mode': DEFAULT_DARK_MODE,
                'zoom_factors': {}
            }
            save_config(default_config)
            return default_config
    except Exception as e:
        print(f"⚠️  Error loading config: {e}")
        # Return default config on error
        return {
            'theme': DEFAULT_THEME,
            'dark_mode': DEFAULT_DARK_MODE,
            'zoom_factors': {}
        }


def save_config(config):
    """Save configuration to persistent config file"""
    try:
        # Create config directory if it doesn't exist
        os.makedirs(DEFAULT_CONFIG_DIR, exist_ok=True)
        
        with open(DEFAULT_CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"✓ Saved config to {DEFAULT_CONFIG_FILE}")
    except Exception as e:
        print(f"⚠️  Error saving config: {e}")


def update_config_from_args(args, config):
    """Update configuration based on command line arguments and save as new defaults"""
    updated = False
    
    if args.theme and args.theme != config.get('theme'):
        config['theme'] = args.theme
        updated = True
        print(f"📝 Updated default theme to: {args.theme}")
    
    # Handle dark/light mode flags
    if args.light_mode and config.get('dark_mode', DEFAULT_DARK_MODE) != False:
        config['dark_mode'] = False
        updated = True
        print(f"📝 Updated default dark mode to: False (light mode)")
    elif args.dark_mode and config.get('dark_mode', DEFAULT_DARK_MODE) != True:
        config['dark_mode'] = True
        updated = True
        print(f"📝 Updated default dark mode to: True (dark mode)")
    
    if updated:
        save_config(config)
    
    def set_styles(self, shortcut_color, title_color, font):
        """Set the styling for shortcut and title"""
        self.shortcut_color = shortcut_color
        self.title_color = title_color
        self.font = font
        self.update()  # Refresh the display
    
    def paintEvent(self, event):
        """Custom painting to handle rich text formatting"""
        painter = self.painter() if hasattr(self, 'painter') else None
        if not painter:
            return super().paintEvent(event)
        
        # For now, use the default painting but we'll enhance this
        super().paintEvent(event)

class BrowserTab(QWebEngineView):
    def __init__(self, url=None, profile=None):
        if profile:
            super().__init__(profile)
        else:
            super().__init__()
        if url:
            from PyQt6.QtCore import QUrl
            self.setUrl(QUrl(url))
        
        # Enable settings for better compatibility with modern websites
        settings = self.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.XSSAuditingEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.SpatialNavigationEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.HyperlinkAuditingEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.ScrollAnimatorEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.ErrorPageEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.FullScreenSupportEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.ScreenCaptureEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.Accelerated2dCanvasEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.AutoLoadImages, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanOpenWindows, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanAccessClipboard, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.AllowRunningInsecureContent, False)
        settings.setAttribute(QWebEngineSettings.WebAttribute.AllowGeolocationOnInsecureOrigins, False)
        settings.setAttribute(QWebEngineSettings.WebAttribute.PrintElementBackgrounds, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.PdfViewerEnabled, True)

class MultiBrowser(QMainWindow):
    def __init__(self, config_file="tabs.json", window_class=None, theme=None, dark_mode=None, config=None):
        super().__init__()
        
        # Store configuration
        self.config = config or {}
        self.config_file = config_file
        
        # Set up persistent profile for cookies
        self.setup_persistent_profile()
        
        # Set window class if provided
        if window_class:
            self.setWindowTitle(window_class)
            # For X11/Wayland window managers
            self.setProperty("windowClass", window_class)
            
        self.setWindowTitle("MultiBrowser")
        self.setGeometry(100, 100, 1200, 800)
        
        # Main layout
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Tab widget - removed closable and movable features
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(False)  # Disable close buttons
        self.tab_widget.setMovable(False)  # Disable tab reordering
        
        # Apply styling - use theme from config if available, otherwise use provided theme
        effective_theme = theme or self.config.get('theme', DEFAULT_THEME)
        self.apply_theme(effective_theme)
        
        # Add hamburger menu to tab bar
        self.setup_hamburger_menu()
        
        layout.addWidget(self.tab_widget)
        self.setCentralWidget(central_widget)
        
        # Set up keyboard shortcuts using QShortcut
        self.setup_keyboard_shortcuts()
        
        # Load tabs from config
        self.load_tabs_from_config(config_file)
        
        # Connect tab change signal to restore zoom
        self.tab_widget.currentChanged.connect(self.restore_tab_zoom)
        
        # Restore zoom for all tabs after a small delay to ensure pages are loaded
        def delayed_zoom_restore():
            time.sleep(2)  # Wait 2 seconds for pages to start loading
            for i in range(self.tab_widget.count()):
                self.restore_tab_zoom(i)
        
        # Start the delayed zoom restore in a separate thread
        threading.Thread(target=delayed_zoom_restore, daemon=True).start()
    
    def setup_persistent_profile(self):
        """Set up persistent profile for cookies and session data in portable .profile directory"""
        # Use application directory for portable profile
        app_dir = os.path.dirname(os.path.abspath(__file__))
        profile_dir = os.path.join(app_dir, ".profile")
        
        # Create profile directory if it doesn't exist
        os.makedirs(profile_dir, exist_ok=True)
        
        # Set up persistent profile
        self.profile = QWebEngineProfile("MultiBrowser", self)
        self.profile.setPersistentStoragePath(profile_dir)
        self.profile.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.AllowPersistentCookies)
        
        # Configure HTTP cache
        cache_path = os.path.join(profile_dir, "cache")
        self.profile.setHttpCacheType(QWebEngineProfile.HttpCacheType.DiskHttpCache)
        self.profile.setHttpCacheMaximumSize(100 * 1024 * 1024)  # 100MB cache
        self.profile.setCachePath(cache_path)
        
        print(f"Persistent profile set up at: {profile_dir}")
        print("✓ Cookies and session data will persist across sessions")
        print("✓ Profile is portable (stored in application directory)")
    
    def apply_theme(self, theme_name):
        """Apply CSS theme to the application"""
        # Load FiraCode Nerd Font
        self.load_nerd_font()
        
        # Apply theme-specific styling
        if theme_name == "dark":
            self.apply_dark_theme()
        elif theme_name == "tokyo-night":
            self.apply_tokyo_night_theme()
        else:
            # Default to dark theme
            self.apply_dark_theme()
    
    def load_nerd_font(self):
        """Load FiraCode Nerd Font for tabs"""
        try:
            # Try to load FiraCode Nerd Font
            font_id = QFontDatabase.addApplicationFont("FiraCode Nerd Font Complete.ttf")
            if font_id != -1:
                font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
                font = QFont(font_family, 24)
                
                # Apply to tab bar
                tab_bar = self.tab_widget.tabBar()
                tab_bar.setFont(font)
                tab_bar.setStyleSheet("""
                    QTabBar {
                        font-family: '" + font_family + "';
                        font-size: 24px;
                    }
                """)
                print(f"✓ FiraCode Nerd Font loaded: {font_family}")
            else:
                print("⚠️  FiraCode Nerd Font not found, using fallback")
                self.apply_fallback_font()
        except Exception as e:
            print(f"⚠️  Error loading FiraCode Nerd Font: {e}")
            self.apply_fallback_font()
    
    def apply_fallback_font(self):
        """Apply fallback font styling"""
        tab_bar = self.tab_widget.tabBar()
        font = QFont("Monospace", 24)
        tab_bar.setFont(font)
        tab_bar.setStyleSheet("""
            QTabBar {
                font-family: 'Monospace';
                font-size: 24px;
            }
        """)
    
    def apply_dark_theme(self):
        """Apply dark theme styling with separate styles for shortcut and title"""
        # Define common base style
        base_font_family = "'FiraCode Nerd Font', monospace"
        base_font_size = "24px"
        
        # Apply theme with separate colors for shortcut and title
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: #1e1e1e;
                color: #ffffff;
            }}
            
            QTabWidget::pane {{
                border: 1px solid #333333;
                background-color: #252526;
            }}
            
            QTabBar::tab {{
                background-color: #252526;
                color: #ffffff;
                padding: 8px 16px;
                border: 1px solid #333333;
                border-bottom: none;
                min-width: 120px;
                font-family: {base_font_family};
                font-size: {base_font_size};
            }}
            
            QTabBar::tab:selected {{
                background-color: #0078d7;
                color: #ffffff;
                border-color: #0078d7;
            }}
            
            QTabBar::tab:hover {{
                background-color: #2d2d30;
            }}
            
            /* Style for keyboard shortcut part - lighter color for contrast */
            .shortcut {{
                color: #a8a8a8;  /* Lighter gray for shortcut */
            }}
            
            /* Style for title part - brighter color for emphasis */
            .title {{
                color: #ffffff;  /* White for title */
            }}
            
            /* Style for hamburger menu button - visible and aligned */
            QToolButton {{
                font-size: 24px;
                padding: 0px 10px;
                border: none;
                background-color: transparent;
                color: #ffffff;  /* White for visibility */
            }}
            
            QToolButton:hover {{
                background-color: rgba(255, 255, 255, 0.1);
            }}
        """)
        
        print("✓ Dark theme applied with separate shortcut/title styling")
    
    def apply_tokyo_night_theme(self):
        """Apply Tokyo Night theme styling with separate styles for shortcut and title"""
        # Define common base style
        base_font_family = "'FiraCode Nerd Font', monospace"
        base_font_size = "24px"
        
        # Apply theme with separate colors for shortcut and title
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: #1a1b26;
                color: #c0caf5;
            }}
            
            QTabWidget::pane {{
                border: 1px solid #16161e;
                background-color: #16161e;
            }}
            
            QTabBar::tab {{
                background-color: #16161e;
                color: #7aa2f7;
                padding: 8px 16px;
                border: 1px solid #16161e;
                border-bottom: none;
                min-width: 120px;
                font-family: {base_font_family};
                font-size: {base_font_size};
            }}
            
            QTabBar::tab:selected {{
                background-color: #7aa2f7;
                color: #16161e;
                border-color: #7aa2f7;
            }}
            
            QTabBar::tab:hover {{
                background-color: #1e1e2e;
                color: #7aa2f7;
            }}
            
            /* Style for keyboard shortcut part - lighter blue for contrast */
            .shortcut {{
                color: #9aa5ff;  /* Lighter blue for shortcut */
            }}
            
            /* Style for title part - brighter blue for emphasis */
            .title {{
                color: #7aa2f7;  /* Bright blue for title */
            }}
            
            /* Style for hamburger menu button - visible and aligned */
            QToolButton {{
                font-size: 24px;
                padding: 0px 10px;
                border: none;
                background-color: transparent;
                color: #7aa2f7;  /* Bright blue for visibility */
            }}
            
            QToolButton:hover {{
                background-color: rgba(7aa2f7, 0.1);
            }}
        """)
        
        print("✓ Tokyo Night theme applied with separate shortcut/title styling")
    
    def load_tabs_from_config(self, config_file):
        try:
            with open(config_file, 'r') as f:
                self.tabs_config = json.load(f)
                
            for tab_config in self.tabs_config:
                title = tab_config.get('title', 'New Tab')
                url = tab_config.get('url', 'about:blank')
                self.add_tab_with_url(title, url)
                
        except FileNotFoundError:
            print(f"Config file {config_file} not found, starting with default tab")
            self.tabs_config = [{'title': 'Home', 'url': 'about:blank'}]
            self.add_tab_with_url("Home", "about:blank")
        except json.JSONDecodeError:
            print(f"Error parsing {config_file}, starting with default tab")
            self.tabs_config = [{'title': 'Home', 'url': 'about:blank'}]
            self.add_tab_with_url("Home", "about:blank")
        except Exception as e:
            print(f"Error loading config: {e}, starting with default tab")
            self.tabs_config = [{'title': 'Home', 'url': 'about:blank'}]
            self.add_tab_with_url("Home", "about:blank")
    
    def add_tab_with_url(self, title, url):
        # Use persistent profile for all tabs
        tab = BrowserTab(url, profile=self.profile)
        index = self.tab_widget.addTab(tab, title)
        
        # Add keyboard shortcut indicator for first 10 tabs
        self.update_tab_title_with_shortcut(index, title)
        
        # Connect signals for URL and title changes
        tab.urlChanged.connect(lambda url, i=index: self.update_tab_title(i, url))
        if hasattr(tab, 'titleChanged'):
            tab.titleChanged.connect(lambda title, i=index: self.update_tab_title_from_title(i, title))
        elif hasattr(tab, 'page') and hasattr(tab.page(), 'titleChanged'):
            tab.page().titleChanged.connect(lambda title, i=index: self.update_tab_title_from_title(i, title))
        
        # Also connect loadFinished signal to restore zoom after page loads
        if hasattr(tab, 'loadFinished'):
            tab.loadFinished.connect(lambda success, i=index: self.restore_tab_zoom_after_load(i))
        elif hasattr(tab, 'page') and hasattr(tab.page(), 'loadFinished'):
            tab.page().loadFinished.connect(lambda success, i=index: self.restore_tab_zoom_after_load(i))
    
    def update_tab_title_with_shortcut(self, index, title):
        """Update tab title with keyboard shortcut indicator for first 10 tabs"""
        if index < 10:
            # Use standard Alt+n notation with styling
            shortcut_text = f"(Alt+{index + 1}) {title}"
            self.tab_widget.setTabText(index, shortcut_text)
        else:
            self.tab_widget.setTabText(index, title)
    
    def update_tab_title_from_title(self, index, title):
        """Update tab title when page title changes - but always use original title from tabs.json"""
        if index >= 0 and index < self.tab_widget.count():
            # Always use the original title from tabs.json, never let website override it
            if index < len(self.tabs_config):
                original_title = self.tabs_config[index].get('title', 'Untitled')
            else:
                original_title = 'Untitled'
            
            # Truncate if too long
            if len(original_title) > 25:  # Reduced to make room for shortcut
                original_title = original_title[:22] + "..."
            
            # Re-add shortcut indicator if it's one of the first 10 tabs
            if index < 10:
                original_title = f"(Alt+{index + 1}) {original_title}"
            
            self.tab_widget.setTabText(index, original_title)
    
    def setup_keyboard_shortcuts(self):
        """Set up keyboard shortcuts using QShortcut"""
        
        # Create shortcuts for first 10 tabs
        for i in range(10):
            if i == 9:
                key = Qt.Key.Key_0
                shortcut_text = f"Alt+0"
            else:
                key = Qt.Key.Key_1 + i
                shortcut_text = f"Alt+{i+1}"
            
            # Create shortcut
            shortcut = QShortcut(QKeySequence(f"Alt+{i+1}"), self)
            shortcut.activated.connect(lambda tab_index=i: self.switch_to_tab(tab_index))
            
            print(f"✓ Keyboard shortcut {shortcut_text} registered for tab {i+1}")
        
        # Alt+Left for previous tab (with cycling)
        shortcut_left = QShortcut(QKeySequence("Alt+Left"), self)
        shortcut_left.activated.connect(self.previous_tab)
        print("✓ Keyboard shortcut Alt+Left registered for previous tab")
        
        # Alt+Right for next tab (with cycling)
        shortcut_right = QShortcut(QKeySequence("Alt+Right"), self)
        shortcut_right.activated.connect(self.next_tab)
        print("✓ Keyboard shortcut Alt+Right registered for next tab")
        
        # F5 for refresh current tab
        shortcut_refresh = QShortcut(QKeySequence("F5"), self)
        shortcut_refresh.activated.connect(self.refresh_current_tab)
        print("✓ Keyboard shortcut F5 registered for refresh")
    
    def setup_hamburger_menu(self):
        """Set up hamburger menu with options"""
        # Create hamburger button
        menu_button = QToolButton()
        menu_button.setText("☰")  # Hamburger icon
        
        # Create menu
        menu = QMenu(menu_button)
        
        # Add "Clear Cookies" action
        clear_cookies_action = QAction("Clear Cookies", menu_button)
        clear_cookies_action.triggered.connect(self.clear_cookies_and_reload)
        menu.addAction(clear_cookies_action)
        
        # Add separator
        menu.addSeparator()
        
        # Add "Close" action
        close_action = QAction("Close", menu_button)
        close_action.triggered.connect(self.close)
        menu.addAction(close_action)
        
        # Set menu on button
        menu_button.setMenu(menu)
        menu_button.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        
        # Add to tab bar corner widget
        self.tab_widget.setCornerWidget(menu_button, Qt.Corner.TopRightCorner)
        
        print("✓ Hamburger menu set up with Clear Cookies and Close options")
    
    def switch_to_tab(self, tab_index):
        """Switch to the specified tab"""
        if 0 <= tab_index < self.tab_widget.count():
            self.tab_widget.setCurrentIndex(tab_index)
            print(f"✓ Switched to tab {tab_index + 1} via keyboard shortcut")
    
    def previous_tab(self):
        """Switch to previous tab with cycling"""
        current_index = self.tab_widget.currentIndex()
        new_index = (current_index - 1) % self.tab_widget.count()
        self.tab_widget.setCurrentIndex(new_index)
        print(f"✓ Switched to previous tab {new_index + 1} (with cycling)")
    
    def next_tab(self):
        """Switch to next tab with cycling"""
        current_index = self.tab_widget.currentIndex()
        new_index = (current_index + 1) % self.tab_widget.count()
        self.tab_widget.setCurrentIndex(new_index)
        print(f"✓ Switched to next tab {new_index + 1} (with cycling)")
    
    def refresh_current_tab(self):
        """Refresh the current tab"""
        current_widget = self.tab_widget.currentWidget()
        if hasattr(current_widget, 'reload'):
            current_widget.reload()
            print("✓ Current tab refreshed")
        else:
            print("⚠️  Current widget doesn't support refresh")
    
    def clear_cookies_and_reload(self):
        """Clear cookies and reload all tabs"""
        print("🔒 Clearing cookies and session data...")
        
        # Clear cookies
        self.profile.cookieStore().deleteAllCookies()
        
        # Clear HTTP cache
        self.profile.clearHttpCache()
        
        print("🔄 Reloading all tabs...")
        
        # Reload all tabs
        for i in range(self.tab_widget.count()):
            widget = self.tab_widget.widget(i)
            if hasattr(widget, 'reload'):
                widget.reload()
                print(f"✓ Reloaded tab {i+1}")
        
        print("🎉 Cookies cleared and all tabs reloaded - ready for new session!")
    
    def update_tab_title(self, index, url):
        if index >= 0 and index < self.tab_widget.count():
            # Use the title from config for initial setup
            if index < len(self.tabs_config):
                tab_text = self.tabs_config[index].get('title', url.toString())
            else:
                tab_text = url.toString()
            
            # Truncate if too long
            if len(tab_text) > 25:  # Reduced to make room for shortcut
                tab_text = tab_text[:22] + "..."
            
            # Re-add shortcut indicator if it's one of the first 10 tabs
            if index < 10:
                tab_text = f"(Alt+{index + 1}) {tab_text}"
            
            self.tab_widget.setTabText(index, tab_text)
    
    def restore_tab_zoom_after_load(self, index):
        """Restore zoom factor for the tab after page load completes"""
        if index >= 0 and index < self.tab_widget.count():
            # Get the tab URL as a unique identifier
            tab_widget = self.tab_widget.widget(index)
            if hasattr(tab_widget, 'url'):
                tab_url = tab_widget.url().toString()
                
                # Get saved zoom factor for this URL
                zoom_factors = self.config.get('zoom_factors', {})
                saved_zoom = zoom_factors.get(tab_url)
                
                if saved_zoom is not None and hasattr(tab_widget, 'setZoomFactor'):
                    tab_widget.setZoomFactor(saved_zoom)
                    print(f"🔍 Restored zoom factor {saved_zoom} for tab after load: {tab_url}")
                else:
                    # If no saved zoom, set default zoom factor
                    if hasattr(tab_widget, 'setZoomFactor'):
                        tab_widget.setZoomFactor(1.0)
                        print(f"🔍 Set default zoom factor 1.0 for tab after load: {tab_url}")

    def restore_tab_zoom(self, index):
        """Restore zoom factor for the current tab"""
        if index >= 0 and index < self.tab_widget.count():
            # Get the tab URL as a unique identifier
            tab_widget = self.tab_widget.widget(index)
            if hasattr(tab_widget, 'url'):
                tab_url = tab_widget.url().toString()
                
                # Get saved zoom factor for this URL
                zoom_factors = self.config.get('zoom_factors', {})
                saved_zoom = zoom_factors.get(tab_url)
                
                if saved_zoom is not None and hasattr(tab_widget, 'setZoomFactor'):
                    tab_widget.setZoomFactor(saved_zoom)
                    print(f"🔍 Restored zoom factor {saved_zoom} for tab: {tab_url}")
                else:
                    # If no saved zoom, set default zoom factor
                    if hasattr(tab_widget, 'setZoomFactor'):
                        tab_widget.setZoomFactor(1.0)
                        print(f"🔍 Set default zoom factor 1.0 for tab: {tab_url}")
    
    def save_current_tab_zoom(self):
        """Save zoom factor for the current tab"""
        current_index = self.tab_widget.currentIndex()
        if current_index >= 0:
            tab_widget = self.tab_widget.widget(current_index)
            if hasattr(tab_widget, 'url') and hasattr(tab_widget, 'zoomFactor'):
                tab_url = tab_widget.url().toString()
                current_zoom = tab_widget.zoomFactor()
                
                # Update config
                if 'zoom_factors' not in self.config:
                    self.config['zoom_factors'] = {}
                
                self.config['zoom_factors'][tab_url] = current_zoom
                save_config(self.config)
                print(f"💾 Saved zoom factor {current_zoom} for tab: {tab_url}")
    
    def keyPressEvent(self, event):
        # Handle Alt+n keyboard shortcuts for tab switching (first 10 tabs)
        if event.modifiers() & Qt.KeyboardModifier.AltModifier:
            # Check for number keys 1-9 and 0
            if (Qt.Key.Key_1 <= event.key() <= Qt.Key.Key_9) or (event.key() == Qt.Key.Key_0):
                # Map key to tab index (Key_1 = 0, Key_2 = 1, ..., Key_0 = 9)
                if event.key() == Qt.Key.Key_0:
                    tab_index = 9
                else:
                    tab_index = event.key() - Qt.Key.Key_1
                
                # Switch to the corresponding tab if it exists
                if 0 <= tab_index < self.tab_widget.count():
                    self.tab_widget.setCurrentIndex(tab_index)
                    event.accept()
                    return
        
        # Keep only zoom keyboard shortcuts
        elif event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            if event.key() == Qt.Key.Key_Plus or event.key() == Qt.Key.Key_Equal:
                self.zoom_in()
            elif event.key() == Qt.Key.Key_Minus:
                self.zoom_out()
            elif event.key() == Qt.Key.Key_0:
                self.reset_zoom()
        
        super().keyPressEvent(event)
    
    def zoom_in(self):
        current_widget = self.tab_widget.currentWidget()
        if hasattr(current_widget, 'setZoomFactor'):
            current_widget.setZoomFactor(current_widget.zoomFactor() + 0.1)
            self.save_current_tab_zoom()
    
    def zoom_out(self):
        current_widget = self.tab_widget.currentWidget()
        if hasattr(current_widget, 'setZoomFactor'):
            current_widget.setZoomFactor(current_widget.zoomFactor() - 0.1)
            self.save_current_tab_zoom()
    
    def reset_zoom(self):
        current_widget = self.tab_widget.currentWidget()
        if hasattr(current_widget, 'setZoomFactor'):
            current_widget.setZoomFactor(1.0)
            self.save_current_tab_zoom()

def main():
    parser = argparse.ArgumentParser(description='MultiBrowser - Tabbed Web Browser')
    parser.add_argument('--config', default='tabs.json', help='Path to JSON config file with tabs')
    parser.add_argument('--window-class', help='Window class for window manager identification')
    parser.add_argument('--theme', choices=['dark', 'tokyo-night'], 
                       help='Theme for the browser (dark, tokyo-night)')
    parser.add_argument('--dark-mode', action='store_true', 
                       help='Enable dark mode (default is enabled)')
    parser.add_argument('--light-mode', action='store_true', 
                       help='Disable dark mode (enable light mode)')
    
    args = parser.parse_args()
    
    # Enable high DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    
    app = QApplication(sys.argv)
    
    # Set application attributes for better compatibility
    app.setApplicationName("MultiBrowser")
    app.setOrganizationName("MultiBrowser")
    app.setOrganizationDomain("multibrowser.local")
    
    # Set window class if provided
    if args.window_class:
        app.setProperty("windowClass", args.window_class)
        # For X11 window managers
        app.setDesktopFileName(args.window_class)
    
    # Load persistent configuration
    config = load_config()
    
    # Handle dark/light mode flags
    if args.light_mode:
        dark_mode = False
    elif args.dark_mode:
        dark_mode = True
    else:
        # Use saved preference or default
        dark_mode = config.get('dark_mode', DEFAULT_DARK_MODE)
    
    # Update config from command line arguments (save as new defaults)
    update_config_from_args(args, config)
    
    # Determine effective theme - use command line theme if provided, otherwise use config
    effective_theme = args.theme if args.theme else config.get('theme', DEFAULT_THEME)
    
    print(f"🌓 Starting MultiBrowser with theme: {effective_theme}, dark_mode: {dark_mode}")
    
    browser = MultiBrowser(
        config_file=args.config, 
        window_class=args.window_class, 
        theme=effective_theme,
        dark_mode=dark_mode,
        config=config
    )
    browser.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()