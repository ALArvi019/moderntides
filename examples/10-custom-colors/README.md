# Custom Colors Configuration

Customize text colors and fonts for tide plots to improve readability and match your Home Assistant theme.

## Features

- **Custom text colors**: Override default colors for better contrast
- **Customizable fonts**: Change font family and sizes
- **Light and dark mode support**: Different color schemes for each mode
- **High contrast defaults**: Updated default colors for improved readability

## Default Color Schemes

### Light Mode (Improved Contrast)

| Element | Default Color | Description |
|---------|--------------|-------------|
| Background | `#FFFFFF` (White) | Plot background |
| Grid | `#D3D3D3` | Grid lines |
| Tide curve | `#6495ED` (Cornflower blue) | Main tide line |
| Tide fill | `#ADD8E6` (Light blue) | Area under curve |
| High tide markers | `#CC0000` (Dark red) | High tide points |
| Low tide markers | `#0000CC` (Dark blue) | Low tide points |
| Text/Title/Axis | `#000000` (Black) | All text elements |

### Dark Mode

| Element | Default Color | Description |
|---------|--------------|-------------|
| Background | `#1E1E1E` | Dark background |
| Grid | `#404040` | Grid lines |
| Tide curve | `#4CAF50` (Green) | Main tide line |
| Tide fill | `#4CAF50` (Green) | Area under curve |
| High tide markers | `#FF5722` (Orange) | High tide points |
| Low tide markers | `#2196F3` (Light blue) | Low tide points |
| Text/Title | `#FFFFFF` (White) | Primary text |
| Axis text | `#CCCCCC` (Light gray) | Axis labels |

## Customization Options

The following color keys can be customized:

```python
custom_colors = {
    'background': '#FFFFFF',      # Plot background color
    'grid': '#D3D3D3',            # Grid line color
    'tide_line': '#6495ED',       # Main tide curve color
    'tide_fill': '#ADD8E6',       # Fill color under curve
    'tide_fill_opacity': '0.3',   # Fill opacity (0.0 to 1.0)
    'current_marker': '#000000',  # Current time marker color
    'current_text': '#000000',    # Current time label color
    'high_tide': '#CC0000',       # High tide marker and label color
    'low_tide': '#0000CC',        # Low tide marker and label color
    'text': '#000000',            # General text color
    'title': '#000000',           # Title text color
    'axis_text': '#000000',       # Axis label color
    'error_text': '#CC0000',      # Error message text color
}
```

## Font Settings

The following font settings can be customized:

```python
font_family = "Arial"       # Font family (e.g., "Arial", "Helvetica", "sans-serif")
font_size_title = 16        # Title font size in pixels
font_size_labels = 12       # Label font size in pixels
font_size_axis = 10         # Axis label font size in pixels
```

## Usage Examples

### High Contrast Light Mode

For users who find the default colors hard to read, use these high-contrast settings:

```python
# In custom_components/moderntides/plot_manager.py
# These are now the default colors for light mode

high_contrast_light = {
    'background': '#FFFFFF',
    'grid': '#D3D3D3',
    'tide_line': '#2E5CB8',       # Darker blue
    'tide_fill': '#87CEEB',       # Sky blue
    'tide_fill_opacity': '0.4',
    'current_marker': '#000000',
    'current_text': '#000000',
    'high_tide': '#8B0000',       # Dark red
    'low_tide': '#00008B',        # Dark blue
    'text': '#000000',
    'title': '#000000',
    'axis_text': '#333333',
}
```

### Larger Fonts for Better Readability

For users who prefer larger text:

```python
font_family = "Arial"
font_size_title = 20        # Larger title
font_size_labels = 14       # Larger labels
font_size_axis = 12         # Larger axis text
```

### Custom Theme Example (Ocean Theme)

```python
ocean_theme = {
    'background': '#F0F8FF',      # Alice blue
    'grid': '#B0C4DE',            # Light steel blue
    'tide_line': '#006994',       # Sea blue
    'tide_fill': '#87CEEB',       # Sky blue
    'tide_fill_opacity': '0.35',
    'current_marker': '#004080',
    'current_text': '#004080',
    'high_tide': '#FF6347',       # Tomato red
    'low_tide': '#4169E1',        # Royal blue
    'text': '#2F4F4F',            # Dark slate gray
    'title': '#006994',
    'axis_text': '#2F4F4F',
}
```

## Dashboard YAML Examples

### Using Default High Contrast Colors

```yaml
type: picture-entity
entity: camera.STATION_NAME_tide_plot
name: "Tide Chart (High Contrast)"
show_name: true
show_state: false
```

### Side-by-Side Light and Dark Mode

```yaml
type: horizontal-stack
cards:
  - type: picture-entity
    entity: camera.STATION_NAME_tide_plot
    name: "Light Mode"
    show_name: true
  - type: picture-entity
    entity: camera.STATION_NAME_tide_plot_dark
    name: "Dark Mode"
    show_name: true
```

### With Overlays for Better Visibility

```yaml
type: picture-elements
camera_image: camera.STATION_NAME_tide_plot
elements:
  - entity: sensor.STATION_NAME_tide_station_info
    style:
      background-color: rgba(0, 0, 0, 0.8)
      color: white
      font-size: 14px
      padding: 4px 8px
      border-radius: 4px
      left: 50px
      top: 15px
    type: state-label
  - entity: sensor.STATION_NAME_current_tide_height
    style:
      background-color: rgba(0, 100, 148, 0.9)
      color: white
      font-size: 14px
      font-weight: bold
      padding: 4px 8px
      border-radius: 4px
      right: 50px
      top: 15px
    prefix: "Current: "
    suffix: " m"
    type: state-label
```

## Requirements

- Modern Tides integration (with color customization support - version 1.1.6+)
- At least one tide station configured

## Difficulty Level

⭐ **Beginner** - Use default high-contrast colors (no changes needed)  
⭐⭐ **Intermediate** - Customize colors via dashboard YAML overlays  
⭐⭐⭐ **Advanced** - Modify source code for custom color schemes
