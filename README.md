# Modern Tides - Home Assistant Integration

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)
[![hacs][hacsbadge]][hacs]

[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[hacs]: https://github.com/hacs/integration

A modern Home Assistant custom integration that provides real-time tide information and beautiful visualizations from Spanish tide stations. This integration fetches data from the Instituto Hidrográfico de la Marina (IHM) and provides sensors for current tide height, next high/low tide times, and a visual camera entity showing tide charts.

![Modern Tides Logo](images/logo.png)

## Features

- **Real-time tide data** from official Spanish maritime institute
- **Beautiful tide charts** as camera entities (SVG format)
- **Multiple sensors** for current height and next tide times
- **Easy configuration** through the UI
- **Automatic updates** every 30 minutes
- **Support for multiple stations** simultaneously

## Installation

### HACS (Recommended)

1. Make sure you have [HACS](https://hacs.xyz/) installed
2. Go to HACS → Integrations
3. Click the three dots in the top right corner and select "Custom repositories"
4. Add this repository URL: `https://github.com/ALArvi019/moderntides`
5. Select "Integration" as the category
6. Click "Add"
7. Search for "Modern Tides" and install it
8. Restart Home Assistant

### Manual Installation

1. Download the latest release from the [releases page](https://github.com/ALArvi019/moderntides/releases)
2. Extract the contents to your `custom_components` directory:
   ```
   custom_components/
   └── moderntides/
       ├── __init__.py
       ├── manifest.json
       ├── config_flow.py
       ├── const.py
       ├── sensor.py
       ├── camera.py
       ├── tide_api.py
       ├── plot_manager.py
       └── strings.json
   ```
3. Restart Home Assistant

## Configuration

1. Go to **Settings** → **Devices & Services**
2. Click **Add Integration**
3. Search for "Modern Tides"
4. Select your desired tide station from the dropdown list
5. Click **Submit**

The integration will automatically create all necessary entities for your selected station.

For each configured tide station, the following entities will be created:

- **Station information sensor**: General information about the tide station
- **Current height sensor**: Current tide height in meters
- **Next high tide sensor**: Time and height of the next high tide
- **Next low tide sensor**: Time and height of the next low tide
- **Tide plot camera**: Beautiful graphical visualization of the day's tide curve

## Available Entities

After adding a station, you'll have access to these entities (replace `STATION_NAME` with your station's name):

- `sensor.STATION_NAME_tide_station_info` - Station information
- `sensor.STATION_NAME_current_tide_height` - Current tide height in meters
- `sensor.STATION_NAME_next_high_tide_time` - Next high tide time
- `sensor.STATION_NAME_next_low_tide_time` - Next low tide time
- `camera.STATION_NAME_tide_plot` - Tide chart visualization

## Dashboard Examples

Here are several examples of how to display tide information in your Home Assistant dashboards:

### 1. Basic Entity Card

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

### 2. Picture Elements Card with Overlays

```yaml
type: picture-elements
camera_image: camera.STATION_NAME_tide_plot
elements:
  - entity: sensor.STATION_NAME_tide_station_info
    style:
      background-color: rgba(0, 0, 0, 0.8)
      color: white
      font-size: 13px
      line-height: 0px
      padding: 1px 5px
      border-radius: 10px
      pointer-events: none
      font-weight: bold
      left: 40px
      top: 10px
    type: state-label
  - entity: sensor.STATION_NAME_current_tide_height
    style:
      background-color: rgba(0, 100, 200, 0.8)
      color: white
      font-size: 13px
      line-height: 0px
      padding: 1px 5px
      border-radius: 10px
      pointer-events: none
      font-weight: bold
      right: "-70px"
      top: 10px
    prefix: "Current: "
    suffix: " m"
    type: state-label
  - entity: sensor.STATION_NAME_next_high_tide_time
    style:
      background-color: rgba(0, 150, 0, 0.8)
      color: white
      font-size: 13px
      line-height: 0px
      padding: 1px 5px
      border-radius: 10px
      pointer-events: none
      font-weight: bold
      right: "-97px"
      top: 30px
    prefix: "↑ "
    type: state-label
  - entity: sensor.STATION_NAME_next_low_tide_time
    style:
      background-color: rgba(200, 0, 0, 0.8)
      color: white
      font-size: 13px
      line-height: 0px
      padding: 1px 5px
      border-radius: 10px
      pointer-events: none
      font-weight: bold
      right: "-97px"
      top: 50px
    prefix: "↓ "
    type: state-label
```

### 3. Glance Card

```yaml
type: glance
title: Tides Overview
entities:
  - entity: sensor.STATION_NAME_current_tide_height
    name: Current
    icon: mdi:waves
  - entity: sensor.STATION_NAME_next_high_tide_time
    name: Next High
    icon: mdi:arrow-up-bold
  - entity: sensor.STATION_NAME_next_low_tide_time
    name: Next Low
    icon: mdi:arrow-down-bold
```

### 4. Panel con configuración preferida

Configuración recomendada para un panel moderno y funcional:

```yaml
type: vertical-stack
title: Tides at STATION_NAME
cards:
  - type: horizontal-stack
    cards:
      - type: custom:mushroom-template-card
        primary: Current Tide
        secondary: "{{ states('sensor.STATION_NAME_current_tide_height') }} m"
        icon: mdi:waves
        icon_color: blue
        layout: vertical
        fill_container: true
        tap_action:
          action: more-info
          entity: sensor.STATION_NAME_current_tide_height
      - type: custom:mushroom-template-card
        primary: Next High Tide
        secondary: >-
          {{ states('sensor.STATION_NAME_next_high_tide_time') | as_timestamp |
          timestamp_custom('%H:%M') }}
        icon: mdi:arrow-up-bold
        icon_color: green
        layout: vertical
        fill_container: true
        tap_action:
          action: more-info
          entity: sensor.STATION_NAME_next_high_tide_time
      - type: custom:mushroom-template-card
        primary: Next Low Tide
        secondary: >-
          {{ states('sensor.STATION_NAME_next_low_tide_time') | as_timestamp |
          timestamp_custom('%H:%M') }}
        icon: mdi:arrow-down-bold
        icon_color: red
        layout: vertical
        fill_container: true
        tap_action:
          action: more-info
          entity: sensor.STATION_NAME_next_low_tide_time
  - type: picture-elements
    camera_image: camera.STATION_NAME_tide_plot
    style: |
      ha-card {
        border-radius: 16px;
        overflow: hidden;
        margin-top: 16px;
      }
    elements:
      - entity: sensor.STATION_NAME_tide_station_info
        style:
          background-color: rgba(0, 0, 0, 0.8)
          color: white
          font-size: 13px
          line-height: 0px
          padding: 1px 5px
          border-radius: 10px
          pointer-events: none
          font-weight: bold
          left: 40px
          top: 10px
        type: state-label
      - entity: sensor.STATION_NAME_current_tide_height
        style:
          background-color: rgba(0, 100, 200, 0.8)
          color: white
          font-size: 13px
          line-height: 0px
          padding: 1px 5px
          border-radius: 10px
          pointer-events: none
          font-weight: bold
          right: "-70px"
          top: 10px
        prefix: "Current: "
        suffix: " m"
        type: state-label
      - entity: sensor.STATION_NAME_next_high_tide_time
        style:
          background-color: rgba(0, 150, 0, 0.8)
          color: white
          font-size: 13px
          line-height: 0px
          padding: 1px 5px
          border-radius: 10px
          pointer-events: none
          font-weight: bold
          right: "-97px"
          top: 30px
        prefix: "↑ "
        type: state-label
      - entity: sensor.STATION_NAME_next_low_tide_time
        style:
          background-color: rgba(200, 0, 0, 0.8)
          color: white
          font-size: 13px
          line-height: 0px
          padding: 1px 5px
          border-radius: 10px
          pointer-events: none
          font-weight: bold
          right: "-97px"
          top: 50px
        prefix: "↓ "
        type: state-label
  - type: custom:mushroom-chips-card
    style: |
      ha-card {
        margin-top: 16px;
      }
    chips:
      - type: entity
        entity: sensor.STATION_NAME_next_high_tide_time
        icon: mdi:arrow-up-bold
        icon_color: green
        content_info: state
        tap_action:
          action: more-info
      - type: entity
        entity: sensor.STATION_NAME_next_low_tide_time
        icon: mdi:arrow-down-bold
        icon_color: red
        content_info: state
        tap_action:
          action: more-info
```

### 5. Mushroom Cards (Custom Component)

If you have the [Mushroom Cards](https://github.com/piitaya/lovelace-mushroom) custom component installed, you can create beautiful modern cards:

```yaml
type: vertical-stack
cards:
  - type: custom:mushroom-title-card
    title: Tides - STATION_NAME
    subtitle: Instituto Hidrográfico de la Marina
  
  - type: custom:mushroom-template-card
    primary: Current tide height
    secondary: "{{ states('sensor.STATION_NAME_current_tide_height') }} m"
    icon: mdi:waves
    icon_color: blue
    tap_action:
      action: more-info
      entity: sensor.STATION_NAME_current_tide_height
  
  - type: horizontal-stack
    cards:
      - type: custom:mushroom-template-card
        primary: Next high tide
        secondary: >-
          {{ states('sensor.STATION_NAME_next_high_tide_time') | as_timestamp | timestamp_custom('%H:%M') }}
        icon: mdi:arrow-up-bold
        icon_color: green
        tap_action:
          action: more-info
          entity: sensor.STATION_NAME_next_high_tide_time
      
      - type: custom:mushroom-template-card
        primary: Next low tide
        secondary: >-
          {{ states('sensor.STATION_NAME_next_low_tide_time') | as_timestamp | timestamp_custom('%H:%M') }}
        icon: mdi:arrow-down-bold
        icon_color: red
        tap_action:
          action: more-info
          entity: sensor.STATION_NAME_next_low_tide_time
  
  - type: picture-entity
    entity: camera.STATION_NAME_tide_plot
    camera_view: auto
```

### 6. Advanced Mushroom Dashboard

For a more sophisticated Mushroom layout:

```yaml
type: vertical-stack
cards:
  - type: custom:mushroom-title-card
    title: "{{ state_attr('sensor.STATION_NAME_tide_station_info', 'friendly_name') }}"
    subtitle: Real-time tide monitoring
    title_tap_action:
      action: none
    
  - type: custom:mushroom-entity-card
    entity: sensor.STATION_NAME_current_tide_height
    name: Current Tide Height
    icon: mdi:waves
    icon_color: blue
    primary_info: name
    secondary_info: state
    tap_action:
      action: more-info
    
  - type: custom:mushroom-chips-card
    chips:
      - type: entity
        entity: sensor.STATION_NAME_next_high_tide_time
        icon: mdi:arrow-up-bold
        icon_color: green
        content_info: state
        tap_action:
          action: more-info
      - type: entity
        entity: sensor.STATION_NAME_next_low_tide_time
        icon: mdi:arrow-down-bold
        icon_color: red
        content_info: state
        tap_action:
          action: more-info
    
  - type: picture-entity
    entity: camera.STATION_NAME_tide_plot
    camera_view: auto
    show_state: false
    show_name: false
```

### 7. Vertical Stack with Chart

```yaml
type: vertical-stack
cards:
  - type: markdown
    content: |
      # Tide Information - STATION_NAME
      Real-time tide data and predictions
  
  - type: picture-entity
    entity: camera.STATION_NAME_tide_plot
    camera_view: auto
  
  - type: horizontal-stack
    cards:
      - type: gauge
        entity: sensor.STATION_NAME_current_tide_height
        min: 0
        max: 4
        name: Current Height
        unit: m
        severity:
          green: 1.5
          yellow: 0.5
          red: 0
      
      - type: entities
        entities:
          - entity: sensor.STATION_NAME_next_high_tide_time
            name: Next High Tide
            icon: mdi:arrow-up-bold
          - entity: sensor.STATION_NAME_next_low_tide_time
            name: Next Low Tide
            icon: mdi:arrow-down-bold
```

### 8. Compact Mobile-Friendly Card

```yaml
type: picture-elements
camera_image: camera.STATION_NAME_tide_plot
elements:
  - entity: sensor.STATION_NAME_current_tide_height
    style:
      top: 5px
      right: 5px
      background-color: rgba(0, 0, 0, 0.8)
      color: white
      padding: 5px 10px
      border-radius: 20px
      font-size: 12px
      font-weight: bold
    prefix: "Now: "
    suffix: "m"
    type: state-label
  
  - entity: sensor.STATION_NAME_next_high_tide_time
    style:
      top: 35px
      right: 5px
      background-color: rgba(0, 150, 0, 0.8)
      color: white
      padding: 3px 8px
      border-radius: 15px
      font-size: 10px
    prefix: "↑ "
    type: state-label
  
  - entity: sensor.STATION_NAME_next_low_tide_time
    style:
      top: 55px
      right: 5px
      background-color: rgba(200, 0, 0, 0.8)
      color: white
      padding: 3px 8px
      border-radius: 15px
      font-size: 10px
    prefix: "↓ "
    type: state-label
```

### 9. Multiple Stations Dashboard

```yaml
type: grid
title: Spanish Ports Tides
columns: 2
cards:
  - type: picture-elements
    camera_image: camera.cadiz_tide_plot
    elements:
      - entity: sensor.cadiz_tide_station_info
        style:
          bottom: 0
          left: 0
          background-color: rgba(0, 0, 0, 0.7)
          color: white
          font-size: 14px
          padding: 10px
          width: 100%
        type: state-label
  
  - type: picture-elements
    camera_image: camera.barcelona_tide_plot
    elements:
      - entity: sensor.barcelona_tide_station_info
        style:
          bottom: 0
          left: 0
          background-color: rgba(0, 0, 0, 0.7)
          color: white
          font-size: 14px
          padding: 10px
          width: 100%
        type: state-label
```

## Example Automation

You can create automations based on tide data:

```yaml
automation:
  - alias: "High tide warning"
    trigger:
      - platform: template
        value_template: >
          {% set high_tide = states('sensor.STATION_NAME_next_high_tide_time') %}
          {% set time_diff = (as_timestamp(high_tide) - as_timestamp(now())) / 60 %}
          {{ time_diff > 59 and time_diff < 61 }}
    action:
      - service: notify.mobile_app
        data:
          title: "Tide Alert"
          message: "Approximately one hour until the next high tide at STATION_NAME"
```

## Data Source

This component uses the public API of the Instituto Hidrográfico de la Marina (IHM):

- Stations API: `https://ideihm.covam.es/api-ihm/getmarea?request=getlist&format=json`
- Daily tides API: `https://ideihm.covam.es/api-ihm/getmarea?request=gettide&id=STATION_ID&format=json&date=YYYYMMDD`
- Monthly tides API: `https://ideihm.covam.es/api-ihm/getmarea?request=gettide&id=STATION_ID&format=json&month=YYYYMM`

## Troubleshooting

If you encounter any issues with the integration:

1. Check Home Assistant logs for specific error messages
2. Make sure your Home Assistant instance has an Internet connection
3. Verify that the integration is properly installed
4. If the problem persists, open an issue in the [GitHub repository](https://github.com/ALArvi019/moderntides/issues)

## Contributing

Contributions are welcome! If you want to improve this component:

1. Fork the repository
2. Create a branch for your feature (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push the changes to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Developed by [ALArvi019](https://github.com/ALArvi019) - 2025

[commits-shield]: https://img.shields.io/github/commit-activity/y/ALArvi019/moderntides.svg?style=for-the-badge
[commits]: https://github.com/ALArvi019/moderntides/commits/main
[license-shield]: https://img.shields.io/github/license/ALArvi019/moderntides.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/ALArvi019/moderntides.svg?style=for-the-badge
[releases]: https://github.com/ALArvi019/moderntides/releases
