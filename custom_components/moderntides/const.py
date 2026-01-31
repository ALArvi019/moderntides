"""Constants for the Modern Tides integration."""

DOMAIN = "moderntides"
PLATFORMS = ["sensor", "camera"]

# Metadata to ensure Home Assistant finds the integration
INTEGRATION_TITLE = "Modern Tides"
INTEGRATION_DOMAIN = DOMAIN

# Configuration options
CONF_STATIONS = "stations"
CONF_STATION_ID = "station_id"
CONF_STATION_NAME = "station_name"
CONF_UPDATE_INTERVAL = "update_interval"

# Visual customization options
CONF_CUSTOM_COLORS_LIGHT = "custom_colors_light"
CONF_CUSTOM_COLORS_DARK = "custom_colors_dark"
CONF_FONT_SIZE_TITLE = "font_size_title"
CONF_FONT_SIZE_LABELS = "font_size_labels"
CONF_FONT_SIZE_AXIS = "font_size_axis"

# Color keys for customization
COLOR_KEYS = [
    "high_tide",
    "low_tide",
    "tide_line",
    "text",
]

# Plot generation settings
PLOT_DAYS_TO_GENERATE = [1, 2, 3, 4, 5, 6, 7]  # Generate plots for these day ranges

# Update intervals in minutes
DEFAULT_UPDATE_INTERVAL = 360
INTERVALS = {
    "30min": 30,
    "1h": 60,
    "3h": 180,
    "6h": 360,
    "12h": 720,
    "24h": 1440
}

# API endpoints
API_BASE_URL = "https://ideihm.covam.es/api-ihm/getmarea"
API_STATION_LIST = f"{API_BASE_URL}?request=getlist&format=json"
API_DAY_TIDES = f"{API_BASE_URL}?request=gettide&format=json&id={{station_id}}&date={{date}}"
API_MONTH_TIDES = f"{API_BASE_URL}?request=gettide&format=json&id={{station_id}}&month={{month}}"

# Default color schemes for tide plots
# Light mode colors - using high contrast black text for better readability
DEFAULT_COLORS_LIGHT = {
    'background': '#FFFFFF',  # White
    'grid': '#D3D3D3',
    'tide_line': '#6495ED',  # Cornflower blue
    'tide_fill': '#ADD8E6',  # Light blue
    'tide_fill_opacity': '0.3',
    'current_marker': '#000000',
    'current_text': '#000000',  # Black text for better contrast
    'high_tide': '#CC0000',  # Darker red for better contrast
    'low_tide': '#0000CC',  # Darker blue for better contrast
    'text': '#000000',  # Black text
    'title': '#000000',  # Black title
    'axis_text': '#000000',  # Black axis text
    'error_text': '#CC0000',  # Error message text color
}

# Dark mode colors - optimized for dark interfaces
DEFAULT_COLORS_DARK = {
    'background': '#1E1E1E',
    'grid': '#404040',
    'tide_line': '#4CAF50',  # Green
    'tide_fill': '#4CAF50',  # Green fill
    'tide_fill_opacity': '0.2',
    'current_marker': '#FFFFFF',
    'current_text': '#FFFFFF',  # White text
    'high_tide': '#FF5722',  # Orange
    'low_tide': '#2196F3',  # Light blue
    'text': '#FFFFFF',  # White text
    'title': '#FFFFFF',  # White title
    'axis_text': '#CCCCCC',  # Light gray axis text
    'error_text': '#FF5722',  # Error message text color (orange)
}

# Default font settings
DEFAULT_FONT_FAMILY = "Arial"
DEFAULT_FONT_SIZE_TITLE = 16
DEFAULT_FONT_SIZE_LABELS = 12
DEFAULT_FONT_SIZE_AXIS = 10
