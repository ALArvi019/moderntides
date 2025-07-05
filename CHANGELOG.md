# Changelog

## 1.1.0 (2025-07-05)

### Major Improvements
- **TRANSLATION**: Complete translation of all Spanish text to English
  - Updated README dashboard examples from Spanish to English
  - Translated GitHub issue templates
  - Translated CHANGELOG entries
  - Updated plot manager UI text
- **CONFIG FLOW**: Streamlined configuration process
  - Removed unnecessary initial modal step
  - Direct access to station configuration form
  - Simplified options flow with dropdown station selection
  - Added "(optional)" indicator for station name field
- **UI/UX**: Enhanced user experience
  - Better configuration flow navigation
  - Improved options management interface
  - Cleaner GitHub Actions workflow validation
- **DOCS**: Updated README with preferred dashboard configuration
  - Added new modern Mushroom card layouts
  - Improved CSS styling examples
  - Better organized dashboard examples

## 1.0.2 (2025-07-05)

### Improvements
- **NEW**: Added moderntides domain to Home Assistant brands repository
- **IMPROVED**: Integration now appears with proper branding in HACS and Home Assistant
- **DOCS**: Updated repository structure for better organization

## 1.0.1 (2025-07-05)

### Bug Fixes
- **FIXED**: Timezone handling for tide times - now correctly converts UTC API times to local timezone
- **FIXED**: Proper creation of UTC datetime objects instead of naive datetime objects
- **IMPROVED**: Better handling of tide times across midnight boundaries
- **IMPROVED**: Enhanced timezone conversion logic for accurate local time display

## 1.0.0 (2025-07-04)

### Major Release
- **NEW**: Beautiful SVG tide chart visualization with camera entity
- **NEW**: Modern tide plots with smooth curves and professional styling
- **NEW**: Complete English translation of all components
- **IMPROVED**: Enhanced error handling and timezone management
- **IMPROVED**: Optimized data processing and rendering
- **REMOVED**: Cleaned up unused files and dependencies
- **DOCS**: Comprehensive dashboard examples and usage guides

### Features
- Real-time tide data visualization through camera entity
- SVG-based charts with smooth interpolated curves
- Professional styling with grid lines and color coding
- Multiple dashboard examples for various use cases
- Support for multiple stations simultaneously
- Efficient data updates and caching

## 0.1.9 (2025-07-03)

### Bug Fixes
- Removed external cairosvg dependencies that caused installation issues
- Reverted to SVG format for image visualization for compatibility
- Improved component robustness for systems without graphics libraries

## 0.1.8 (2025-07-03)

### Improvements
- Added SVG to PNG conversion to improve image compatibility
- Added cairosvg dependency for image conversion
- Improved camera visualization with PNG format

## 0.1.7 (2025-07-03)

### Bug Fixes
- Fixed issue with Curve Picture image visualization
- Correctly set content type for SVG camera

## 0.1.6 (2025-07-03)

### Bug Fixes
- Fixed issue with timestamp sensors (high/low tide) using timezone-aware datetime objects
- Improved tide data processing for better accuracy

## 0.1.5 (2025-07-03)

### Improvements
- Added more debug logging to facilitate troubleshooting
- Improved error handling during coordinator initialization
- Better detection and notification when coordinators are not found for stations

## 0.1.4 (2025-07-03)

### Improvements
- Fixes in multiple station identification
- Improved error messages for configuration issues

## 0.1.3 (2025-07-03)

### Improvements
- Centralization of data coordinators: single coordinator per station for all related sensors
- Improved data update management for multiple stations
- Increased logging for better tracking and debugging
- Fixed issue where not all stations were updated correctly

## 0.1.2 (2023-07-06)

### Improvements
- Removal of unnecessary dependencies (matplotlib, numpy, Pillow)
- SVG implementation to display tide information instead of generated charts
- Adaptation to support changes in API response format (tides/stations)

## 0.1.1 (2023-07-05)

### Improvements
- Support for multiple stations
- Update interval configuration per station
- Enhanced configuration flow to add/modify/remove stations

## 0.1.0 (2023-07-04)

### Initial Features
- Integration with IHM API for tide data
- Sensors for current height, next high and low tide
- Configuration through user interface
