# Multi-Day Tide Plot Camera Entities

A comprehensive guide to using the automatic multi-day camera entities for tide predictions from single-day views to full week forecasts.

## Features

- **Flexible time ranges**: 1 day to 7 days of tide predictions
- **14 camera entities per station**: Light and dark modes for each time range
- **Easy integration**: Just use camera entities like any other HA entity
- **Automatic updates**: All plots refresh automatically
- **No configuration needed**: All cameras created automatically

## Screenshot

![Multi-Day Camera Entities Dashboard](preview.png)

## Available Camera Entities

### Light Mode Cameras
- `camera.moderntides_STATION_ID_camera` - 1 day (default)
- `camera.moderntides_STATION_ID_camera_2d` - 2 days
- `camera.moderntides_STATION_ID_camera_3d` - 3 days
- `camera.moderntides_STATION_ID_camera_4d` - 4 days
- `camera.moderntides_STATION_ID_camera_5d` - 5 days
- `camera.moderntides_STATION_ID_camera_6d` - 6 days
- `camera.moderntides_STATION_ID_camera_7d` - 7 days

### Dark Mode Cameras
- `camera.moderntides_STATION_ID_camera_dark` - 1 day
- `camera.moderntides_STATION_ID_camera_2d_dark` - 2 days
- `camera.moderntides_STATION_ID_camera_3d_dark` - 3 days
- `camera.moderntides_STATION_ID_camera_4d_dark` - 4 days
- `camera.moderntides_STATION_ID_camera_5d_dark` - 5 days
- `camera.moderntides_STATION_ID_camera_6d_dark` - 6 days
- `camera.moderntides_STATION_ID_camera_7d_dark` - 7 days

## Basic Dashboard Example

```yaml
type: grid
title: Tide Camera Comparison Dashboard
columns: 2
cards:
  # Time Range Comparison
  - type: vertical-stack
    cards:
      - type: heading
        heading: 📅 Time Range Comparison
        heading_style: title
      - type: grid
        columns: 2
        cards:
          - type: picture-entity
            entity: camera.STATION_NAME_tide_plot
            name: Today (1 Day)
          - type: picture-entity
            entity: camera.STATION_NAME_tide_plot_3d
            name: Weekend (3 Days)
          - type: picture-entity
            entity: camera.STATION_NAME_tide_plot_5d
            name: Work Week (5 Days)
          - type: picture-entity
            entity: camera.STATION_NAME_tide_plot_7d
            name: Full Week (7 Days)

  # Theme Comparison
  - type: vertical-stack
    cards:
      - type: heading
        heading: 🌓 Light vs Dark Themes
        heading_style: title
      - type: grid
        columns: 2
        cards:
          - type: picture-entity
            entity: camera.STATION_NAME_tide_plot_2d
            name: Light Theme (2 Days)
          - type: picture-entity
            entity: camera.STATION_NAME_tide_plot_2d_dark
            name: Dark Theme (2 Days)
          - type: picture-entity
            entity: camera.STATION_NAME_tide_plot_4d
            name: Light Theme (4 Days)
          - type: picture-entity
            entity: camera.STATION_NAME_tide_plot_4d_dark
            name: Dark Theme (4 Days)

  # All Time Ranges Grid
  - type: vertical-stack
    cards:
      - type: heading
        heading: 📊 Complete Forecast Grid (Light Mode)
        heading_style: title
      - type: grid
        columns: 3
        cards:
          - type: picture-entity
            entity: camera.STATION_NAME_tide_plot
            name: "1D"
          - type: picture-entity
            entity: camera.STATION_NAME_tide_plot_2d
            name: "2D"
          - type: picture-entity
            entity: camera.STATION_NAME_tide_plot_3d
            name: "3D"
          - type: picture-entity
            entity: camera.STATION_NAME_tide_plot_4d
            name: "4D"
          - type: picture-entity
            entity: camera.STATION_NAME_tide_plot_5d
            name: "5D"
          - type: picture-entity
            entity: camera.STATION_NAME_tide_plot_6d
            name: "6D"
          - type: picture-entity
            entity: camera.STATION_NAME_tide_plot_7d
            name: "7D"

  # Dark Mode Grid
  - type: vertical-stack
    cards:
      - type: heading
        heading: 🌙 Dark Mode Collection
        heading_style: title
      - type: grid
        columns: 3
        cards:
          - type: picture-entity
            entity: camera.STATION_NAME_tide_plot_dark
            name: "1D Dark"
          - type: picture-entity
            entity: camera.STATION_NAME_tide_plot_2d_dark
            name: "2D Dark"
          - type: picture-entity
            entity: camera.STATION_NAME_tide_plot_3d_dark
            name: "3D Dark"
          - type: picture-entity
            entity: camera.STATION_NAME_tide_plot_4d_dark
            name: "4D Dark"
          - entity: camera.STATION_NAME_tide_plot_5d_dark
            name: "5D Dark"
          - entity: camera.STATION_NAME_tide_plot_6d_dark
            name: "6D Dark"
          - entity: camera.STATION_NAME_tide_plot_7d_dark
            name: "7D Dark"

```

## Perfect Use Cases

### Marine Activities
- **Sailing**: Plan departure and return times
- **Fishing**: Identify optimal tide windows
- **Diving**: Plan multi-dive trip schedules
- **Surfing**: Track swell and tide combinations

### Commercial Operations
- **Ports**: Vessel scheduling optimization
- **Marinas**: Docking availability planning
- **Shipping**: Multi-day route planning
- **Coastal construction**: Work window identification

### Research & Analysis
- **Pattern recognition**: Tidal cycle analysis
- **Weather correlation**: Compare with forecasts
- **Historical comparison**: Trend identification
- **Environmental monitoring**: Ecosystem impact studies

## Requirements

- Modern Tides integration installed and configured
- At least one tide station configured
- Home Assistant with dashboard access

## Difficulty Level

⭐ **Beginner** - No configuration needed, plots auto-generated

## Performance Notes

- All 14 plots generated automatically every update
- SVG format ensures small file sizes
- No impact on camera entity performance
- Files stored in `/config/www/` for direct access

## Tips & Tricks

1. **File Access**: All plots are available at `http://YOUR_HA_IP:8123/local/moderntides_STATION_NAME_plot_Xd.svg`
2. **External Use**: SVG files can be embedded in external websites
3. **Backup**: Multi-day plots provide forecast backup if API fails
4. **Comparison**: Use side-by-side views to compare different time ranges
5. **Mobile Friendly**: SVG format scales perfectly on all devices
