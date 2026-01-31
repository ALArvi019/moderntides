# Custom Colors & Fonts

Starting from version 1.1.6, Modern Tides allows you to customize colors and font sizes directly from the Home Assistant UI.

## How to Customize

1. Go to **Settings** → **Devices & Services**
2. Find **Modern Tides** and click **Configure**
3. Select **Customize colors and fonts**
4. Adjust the colors and font sizes to your preference
5. Click **Submit**

The changes will apply after the next data refresh.

## Available Options

### Light Mode Colors
- **High tide color**: Color for high tide markers and labels
- **Low tide color**: Color for low tide markers and labels
- **Tide curve color**: Color of the main tide line
- **Text color**: Color for all text elements

### Dark Mode Colors
- **High tide color**: Color for high tide markers and labels
- **Low tide color**: Color for low tide markers and labels
- **Tide curve color**: Color of the main tide line
- **Text color**: Color for all text elements

### Font Sizes
- **Title font size**: 10-32px (default: 16px)
- **Labels font size**: 8-24px (default: 12px)
- **Axis font size**: 6-18px (default: 10px)

## Default Color Schemes

### Light Mode

| Element | Default Color |
|---------|---------------|
| High tide markers | Dark red (#CC0000) |
| Low tide markers | Dark blue (#0000CC) |
| Tide curve | Cornflower blue (#6495ED) |
| Text | Black (#000000) |

### Dark Mode

| Element | Default Color |
|---------|---------------|
| High tide markers | Orange (#FF5722) |
| Low tide markers | Light blue (#2196F3) |
| Tide curve | Green (#4CAF50) |
| Text | White (#FFFFFF) |

## Tips

- For **better readability** on light backgrounds, use darker colors for tide markers
- For **high contrast**, use black text (#000000) on light mode
- The color picker supports any RGB color

## Dashboard Examples

### Basic Usage

```yaml
type: picture-entity
entity: camera.STATION_NAME_tide_plot
name: "Tide Chart"
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

## Requirements

- Modern Tides v1.1.6+
