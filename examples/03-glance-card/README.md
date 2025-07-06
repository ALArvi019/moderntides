# Glance Card

A compact overview card showing the most important tide information at a glance.

## Features

- Current tide height with wave icon
- Next high tide time with up arrow
- Next low tide time with down arrow
- Compact horizontal layout
- Perfect for dashboards with limited space

## Screenshot

![Glance Card](preview.png)

## Code

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

## Usage Instructions

1. Replace `STATION_NAME` with your actual station name
2. Copy the YAML code above
3. Add it to your Home Assistant dashboard
4. The card will show a compact overview of tide information

## Customization Tips

- Change the `title` to customize the card header
- Modify `name` fields to change the labels under each entity
- Add more entities if needed
- Use different icons by changing the `mdi:` values

## Requirements

- Modern Tides integration installed and configured
- At least one tide station configured

## Difficulty Level

⭐ **Beginner** - Simple configuration, no custom components required
