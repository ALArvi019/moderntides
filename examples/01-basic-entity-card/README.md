# Basic Entity Card

A simple entity card that displays all tide information in a clean, organized list format.

## Features

- Station information
- Current tide height with wave icon
- Next high and low tide times with directional arrows
- Tide chart camera entity
- Clean dividers for visual organization

## Screenshot

![Basic Entity Card](preview.png)

## Code

```yaml
type: entities
title: Tide Information - STATION_NAME
entities:
  - entity: sensor.STATION_NAME_tide_station_info
    name: Station
  - entity: sensor.STATION_NAME_current_tide_height
    name: Current Height
    icon: mdi:waves
  - type: divider
  - entity: sensor.STATION_NAME_next_high_tide_time
    name: Next High Tide
    icon: mdi:arrow-up-bold
  - entity: sensor.STATION_NAME_next_low_tide_time
    name: Next Low Tide
    icon: mdi:arrow-down-bold
  - type: divider
  - entity: camera.STATION_NAME_tide_plot
    name: Tide Chart
```

## Usage Instructions

1. Replace `STATION_NAME` with your actual station name (e.g., `cadiz`, `barcelona`)
2. Copy the YAML code above
3. Add it to your Home Assistant dashboard
4. The card will automatically display your tide data

## Camera Options

### Available Camera Entities

The integration automatically creates **14 camera entities** per station for maximum flexibility:

**Light Mode (7 cameras):**
- `camera.STATION_NAME_tide_plot` - 1 day (default)
- `camera.STATION_NAME_tide_plot_2d` - 2 days
- `camera.STATION_NAME_tide_plot_3d` - 3 days
- `camera.STATION_NAME_tide_plot_4d` - 4 days
- `camera.STATION_NAME_tide_plot_5d` - 5 days
- `camera.STATION_NAME_tide_plot_6d` - 6 days
- `camera.STATION_NAME_tide_plot_7d` - 7 days

**Dark Mode (7 cameras):**
- `camera.STATION_NAME_tide_plot_dark` - 1 day (default)
- `camera.STATION_NAME_tide_plot_2d_dark` - 2 days
- `camera.STATION_NAME_tide_plot_3d_dark` - 3 days
- `camera.STATION_NAME_tide_plot_4d_dark` - 4 days
- `camera.STATION_NAME_tide_plot_5d_dark` - 5 days
- `camera.STATION_NAME_tide_plot_6d_dark` - 6 days
- `camera.STATION_NAME_tide_plot_7d_dark` - 7 days

### Example: Different Time Ranges

```yaml
# Today's forecast (same as above)
- entity: camera.STATION_NAME_tide_plot
  name: Today's Chart

# Weekend forecast (3 days)
- entity: camera.STATION_NAME_tide_plot_3d
  name: Weekend Chart

# Weekly forecast (7 days) 
- entity: camera.STATION_NAME_tide_plot_7d
  name: Weekly Chart

# Dark mode weekly forecast
- entity: camera.STATION_NAME_tide_plot_7d_dark
  name: Weekly Chart (Dark)
```

Check out the [Multi-Day Plots example](../09-multi-day-plots/) for complete dashboard examples.

## Requirements

- Modern Tides integration installed and configured
- At least one tide station configured

## Difficulty Level

⭐ **Beginner** - No custom components required
