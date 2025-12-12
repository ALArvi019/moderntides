# Dashboard Examples

A collection of ready-to-use Home Assistant dashboard configurations for the Modern Tides integration.

## 📋 Example Categories

### Basic Setups
- **[01-basic-entity-card](01-basic-entity-card/)** - Simple entity list for beginners
- **[03-glance-card](03-glance-card/)** - Quick overview with status icons

### Visual Dashboards  
- **[02-picture-elements-overlays](02-picture-elements-overlays/)** - Interactive tide plots with overlays
- **[06-dark-mode-visualization](06-dark-mode-visualization/)** - Dark theme optimized displays

### Mobile & Compact
- **[04-mushroom-cards](04-mushroom-cards/)** - Modern card design
- **[07-compact-mobile-friendly](07-compact-mobile-friendly/)** - Mobile-optimized layouts

### Advanced Features
- **[05-preferred-panel-configuration](05-preferred-panel-configuration/)** - Complete dashboard setup
- **[08-multiple-stations](08-multiple-stations/)** - Multi-station monitoring
- **[09-multi-day-plots](09-multi-day-plots/)** ⭐ **NEW** - 1-7 day forecasts with automatic generation
- **[10-custom-colors](10-custom-colors/)** ⭐ **NEW** - Customize text colors and fonts for better readability

### Weather Integration
- **[07-comprehensive-weather-tides](07-comprehensive-weather-tides/)** - Combined weather and tide data

## 🚀 Quick Start

1. **Choose an example** that matches your needs
2. **Copy the YAML code** from the example
3. **Replace `STATION_NAME`** with your configured station name
4. **Add to your dashboard** in Home Assistant

## ⭐ Featured: Multi-Day Plots

The newest addition automatically generates **14 plot files per station**:
- 🌅 **Light mode**: 1-7 day forecasts  
- 🌙 **Dark mode**: 1-7 day forecasts
- 📁 **Auto-generated**: No configuration needed
- 📱 **Responsive**: Perfect for all devices

Example files created:
```
/config/www/moderntides_cadiz_plot.svg        # Today (light)
/config/www/moderntides_cadiz_plot_3d.svg     # 3 days (light)  
/config/www/moderntides_cadiz_plot_7d.svg     # 7 days (light)
/config/www/moderntides_cadiz_plot_dark.svg   # Today (dark)
/config/www/moderntides_cadiz_plot_7d_dark.svg # 7 days (dark)
... and 9 more variations
```

## 🎯 Use Case Guide

| Need | Recommended Examples |
|------|---------------------|
| **First time setup** | [01-basic-entity-card](01-basic-entity-card/) |
| **Mobile use** | [07-compact-mobile-friendly](07-compact-mobile-friendly/), [09-multi-day-plots](09-multi-day-plots/mobile-optimized.yaml) |
| **Multiple locations** | [08-multiple-stations](08-multiple-stations/) |
| **Trip planning** | [09-multi-day-plots](09-multi-day-plots/) |
| **Dark themes** | [06-dark-mode-visualization](06-dark-mode-visualization/) |
| **Weather integration** | [07-comprehensive-weather-tides](07-comprehensive-weather-tides/) |
| **Interactive displays** | [02-picture-elements-overlays](02-picture-elements-overlays/) |
| **Better readability** | [10-custom-colors](10-custom-colors/) |

## 📱 Device Compatibility

- **📱 Mobile**: Responsive layouts in examples 04, 07, 09
- **💻 Desktop**: Grid layouts in examples 05, 08, 09  
- **📺 Tablets**: Picture elements in examples 02, 06, 09
- **🖥️ Kiosks**: Full-screen displays in examples 05, 09

## 🛠️ Technical Requirements

### Minimum Setup
- Modern Tides integration installed
- At least one tide station configured
- Home Assistant with dashboard access

### Optional Enhancements
- **Custom themes**: For enhanced dark mode support
- **Mobile app**: For responsive mobile layouts
- **Picture elements**: For interactive overlays
- **Multiple stations**: For comparison dashboards

## 📖 Configuration Guide

### Step 1: Install Integration
```bash
# Via HACS or manual installation
# Configure your first tide station
```

### Step 2: Choose Example
```bash
# Browse examples directory
# Select based on your use case
```

### Step 3: Customize Code
```yaml
# Replace STATION_NAME with your station
# Example: cadiz, barcelona, valencia
type: entities
entities:
  - sensor.cadiz_current_tide_height  # ← Your station name here
```

### Step 4: Add to Dashboard
```bash
# Copy YAML to Home Assistant
# Add as new dashboard card
# Adjust layout as needed
```

## 🔧 Troubleshooting

### Common Issues
- **Missing entities**: Check integration configuration
- **Empty plots**: Verify API connectivity
- **Mobile layout**: Use mobile-specific examples
- **Dark mode**: Ensure theme support enabled

### File Locations
```bash
/config/www/                    # Plot files location
/config/custom_components/      # Integration files
/config/configuration.yaml     # HA configuration
```

## 🆘 Support

- **Issues**: Report on GitHub repository
- **Questions**: Check README.md documentation
- **Features**: Request via GitHub issues
- **Examples**: Contribute new examples welcome

## 📈 Version Compatibility

| Example | Integration Version | Features |
|---------|-------------------|----------|
| 01-08 | v1.0+ | Basic functionality |
| 09 | v1.1.4+ | Multi-day plots |
| 10 | v1.2.0+ | Custom colors and fonts |

All examples are backwards compatible and regularly updated.
