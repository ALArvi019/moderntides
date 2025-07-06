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

## Requirements

- Modern Tides integration installed and configured
- At least one tide station configured

## Difficulty Level

⭐ **Beginner** - No custom components required
