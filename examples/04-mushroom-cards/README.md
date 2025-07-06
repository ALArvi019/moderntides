# Mushroom Cards

Modern, beautiful cards using the popular Mushroom custom component for a clean, Material Design look.

## Features

- Dynamic title with station name from entity attributes
- Current tide height card with blue wave icon
- Chip-style next tide indicators with colored icons
- Clean tide chart display
- Material Design aesthetic
- Responsive layout

## Screenshot

![Mushroom Cards](preview.png)

## Code

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

## Usage Instructions

1. **Install Mushroom Cards**: Follow the [installation guide](https://github.com/piitaya/lovelace-mushroom)
2. Replace `STATION_NAME` with your actual station name
3. Copy the YAML code above
4. Add it to your Home Assistant dashboard

## Customization Tips

- Change `icon_color` values for different color schemes
- Modify `subtitle` text in the title card
- Adjust `content_info` in chips (state, name, last-changed, etc.)
- Add more chips or entity cards as needed

## Requirements

- **Mushroom Cards** custom component installed via HACS
- Modern Tides integration installed and configured
- At least one tide station configured

## Difficulty Level

⭐⭐ **Intermediate** - Requires custom component installation
