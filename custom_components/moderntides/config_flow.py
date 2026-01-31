"""Config flow for Modern Tides integration."""
import logging
from typing import Any, Dict, Optional

try:
    import voluptuous as vol
except ImportError:
    # Handle import failure
    vol = None

try:
    from homeassistant import config_entries
    from homeassistant.core import callback
    from homeassistant.data_entry_flow import FlowResult
    import homeassistant.helpers.config_validation as cv
except ImportError:
    # Fallback definitions in case of import failure
    callback = lambda func: func
    FlowResult = Dict[str, Any]
    cv = None
    config_entries = None

from .const import (
    CONF_STATION_ID,
    CONF_STATION_NAME,
    CONF_STATIONS,
    CONF_UPDATE_INTERVAL,
    CONF_CUSTOM_COLORS_LIGHT,
    CONF_CUSTOM_COLORS_DARK,
    CONF_FONT_SIZE_TITLE,
    CONF_FONT_SIZE_LABELS,
    CONF_FONT_SIZE_AXIS,
    DEFAULT_UPDATE_INTERVAL,
    DEFAULT_COLORS_LIGHT,
    DEFAULT_COLORS_DARK,
    DEFAULT_FONT_SIZE_TITLE,
    DEFAULT_FONT_SIZE_LABELS,
    DEFAULT_FONT_SIZE_AXIS,
    DOMAIN,
    INTERVALS,
)
from .tide_api import TideApiClient

# Color validation regex
COLOR_REGEX = r'^#[0-9A-Fa-f]{6}$'

_LOGGER = logging.getLogger(__name__)

class ModernTidesConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Modern Tides."""

    VERSION = 1

    def __init__(self):
        """Initialize the config flow."""
        self._entry_data = {CONF_STATIONS: []}
        self._current_stations = []

    async def async_step_user(
        self, user_input: Optional[Dict[str, Any]] = None
    ):
        """Handle the initial step - go directly to station setup."""
        return await self.async_step_station()

    async def async_step_station(
        self, user_input: Optional[Dict[str, Any]] = None
    ):
        """Handle adding a tide station."""
        errors = {}

        if user_input is not None:
            # Get the list of stations
            api_client = TideApiClient()
            stations = await self.hass.async_add_executor_job(api_client.get_stations)

            # Check if the station ID exists
            station_id = user_input[CONF_STATION_ID]
            valid_station_ids = [str(station["id"]) for station in stations]
            
            if station_id not in valid_station_ids:
                errors[CONF_STATION_ID] = "invalid_station"
            else:
                # Find the station name
                station_name = None
                for station in stations:
                    if str(station["id"]) == station_id:
                        # Use puerto or name field depending on what's available
                        station_name = station.get("puerto", station.get("name", f"Station {station_id}"))
                        break
                
                if not station_name:
                    station_name = f"Station {station_id}"
                
                # Check if station already exists in current config
                if any(station[CONF_STATION_ID] == station_id for station in self._entry_data[CONF_STATIONS]):
                    errors[CONF_STATION_ID] = "station_exists"
                else:
                    # Add the new station
                    self._entry_data[CONF_STATIONS].append({
                        CONF_STATION_ID: station_id,
                        CONF_STATION_NAME: user_input.get(CONF_STATION_NAME, station_name),
                        CONF_UPDATE_INTERVAL: user_input.get(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL),
                    })
                    
                    # Create the final configuration entry and finish
                    return self.async_create_entry(
                        title="Modern Tides", 
                        data=self._entry_data
                    )

        # Get available stations for dropdown
        stations_list = {}
        try:
            api_client = TideApiClient()
            stations = await self.hass.async_add_executor_job(api_client.get_stations)
            
            # Process each station safely
            for station in stations:
                try:
                    station_id = str(station["id"])
                    # Use puerto or name field depending on what's available
                    station_name = station.get("puerto", station.get("name", f"Station {station_id}"))
                    stations_list[station_id] = f"{station_name} ({station_id})"
                except Exception as e:
                    _LOGGER.error("Error processing station: %s - %s", station, e)
        except Exception as e:
            _LOGGER.error("Error fetching stations: %s", e)
            import traceback
            _LOGGER.error("Traceback: %s", traceback.format_exc())
            errors["base"] = "cannot_connect"

        # Prepare the schema for the form
        schema = vol.Schema({
            vol.Required(CONF_STATION_ID): vol.In(stations_list) if stations_list else str,
            vol.Optional(CONF_STATION_NAME, description={"suffix": " (optional)"}): cv.string,
            vol.Optional(CONF_UPDATE_INTERVAL, default=DEFAULT_UPDATE_INTERVAL): vol.In(
                {k: f"{k} ({v} min)" for k, v in INTERVALS.items()}
            ),
        })

        return self.async_show_form(
            step_id="station",
            data_schema=schema,
            errors=errors,
        )
    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return ModernTidesOptionsFlow()


class ModernTidesOptionsFlow(config_entries.OptionsFlow):
    """Handle options for the Modern Tides integration."""

    def __init__(self):
        """Initialize options flow."""
        self._current_station_id = None

    @property
    def _options(self):
        """Get current options."""
        return dict(self.config_entry.options)

    @property
    def _data(self):
        """Get current data."""
        return dict(self.config_entry.data)

    async def async_step_init(self, user_input=None):
        """Manage basic options - show menu."""
        if user_input is not None:
            action = user_input.get("action")
            if action == "modify_station":
                return await self.async_step_select_station()
            elif action == "customize_visuals":
                return await self.async_step_customize_visuals()
            return self.async_create_entry(title="", data=self._options)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required("action", default="customize_visuals"): vol.In({
                    "customize_visuals": "Customize colors and fonts",
                    "modify_station": "Modify station settings",
                }),
            }),
        )

    async def async_step_select_station(self, user_input=None):
        """Select station to modify."""
        if user_input is not None:
            station_to_modify = user_input.get("station_to_modify")
            if station_to_modify:
                self._current_station_id = station_to_modify
                return await self.async_step_modify_station()
            return self.async_create_entry(title="", data=self._options)

        current_stations = self._data.get(CONF_STATIONS, [])

        if not current_stations:
            return self.async_abort(reason="no_stations_configured")

        station_options = {}
        for station in current_stations:
            station_id = station[CONF_STATION_ID]
            station_name = station[CONF_STATION_NAME]
            station_options[station_id] = f"{station_name} ({station_id})"

        return self.async_show_form(
            step_id="select_station",
            data_schema=vol.Schema({
                vol.Required("station_to_modify"): vol.In(station_options),
            }),
        )

    async def async_step_modify_station(self, user_input=None):
        """Modify an existing station."""
        station_id = self._current_station_id

        if user_input is not None:
            current_data = dict(self.config_entry.data)
            stations = list(current_data.get(CONF_STATIONS, []))

            # Find and update the selected station
            for i, station in enumerate(stations):
                if station[CONF_STATION_ID] == station_id:
                    stations[i] = {
                        CONF_STATION_ID: station_id,
                        CONF_STATION_NAME: user_input.get(CONF_STATION_NAME),
                        CONF_UPDATE_INTERVAL: user_input.get(CONF_UPDATE_INTERVAL),
                    }
                    break

            current_data[CONF_STATIONS] = stations
            self.hass.config_entries.async_update_entry(
                self.config_entry, data=current_data
            )
            return self.async_abort(reason="station_modified")

        # Get current station settings
        current_stations = self._data.get(CONF_STATIONS, [])
        station = next((s for s in current_stations if s[CONF_STATION_ID] == station_id), None)
        
        if not station:
            return self.async_abort(reason="station_not_found")

        return self.async_show_form(
            step_id="modify_station",
            data_schema=vol.Schema({
                vol.Required(CONF_STATION_NAME, default=station[CONF_STATION_NAME]): cv.string,
                vol.Required(CONF_UPDATE_INTERVAL, default=station[CONF_UPDATE_INTERVAL]): vol.In(
                    {k: f"{k} ({v} min)" for k, v in INTERVALS.items()}
                ),
            }),
        )

    async def async_step_customize_visuals(self, user_input=None):
        """Customize colors and fonts for tide plots."""
        if user_input is not None:
            # Save color and font settings to options
            new_options = dict(self._options)
            new_options[CONF_CUSTOM_COLORS_LIGHT] = {
                "high_tide": user_input.get("light_high_tide"),
                "low_tide": user_input.get("light_low_tide"),
                "tide_line": user_input.get("light_tide_line"),
                "text": user_input.get("light_text"),
            }
            new_options[CONF_CUSTOM_COLORS_DARK] = {
                "high_tide": user_input.get("dark_high_tide"),
                "low_tide": user_input.get("dark_low_tide"),
                "tide_line": user_input.get("dark_tide_line"),
                "text": user_input.get("dark_text"),
            }
            new_options[CONF_FONT_SIZE_TITLE] = user_input.get(CONF_FONT_SIZE_TITLE)
            new_options[CONF_FONT_SIZE_LABELS] = user_input.get(CONF_FONT_SIZE_LABELS)
            new_options[CONF_FONT_SIZE_AXIS] = user_input.get(CONF_FONT_SIZE_AXIS)

            return self.async_create_entry(title="", data=new_options)

        # Get current values from options or defaults
        current_options = self._options
        light_colors = current_options.get(CONF_CUSTOM_COLORS_LIGHT, {})
        dark_colors = current_options.get(CONF_CUSTOM_COLORS_DARK, {})

        # Color selector using Home Assistant's color picker
        from homeassistant.helpers.selector import (
            ColorRGBSelector,
            NumberSelector,
            NumberSelectorConfig,
            NumberSelectorMode,
        )

        def hex_to_rgb(hex_color: str) -> list:
            """Convert hex color to RGB list."""
            hex_color = hex_color.lstrip('#')
            return [int(hex_color[i:i+2], 16) for i in (0, 2, 4)]

        def get_color_default(colors_dict: dict, key: str, defaults: dict) -> list:
            """Get color as RGB list from dict or defaults."""
            color = colors_dict.get(key, defaults.get(key, "#000000"))
            # If already a list (RGB), return as-is
            if isinstance(color, list):
                return color
            # Otherwise convert from hex string
            return hex_to_rgb(color)

        return self.async_show_form(
            step_id="customize_visuals",
            data_schema=vol.Schema({
                # Light mode colors
                vol.Required(
                    "light_high_tide",
                    default=get_color_default(light_colors, "high_tide", DEFAULT_COLORS_LIGHT)
                ): ColorRGBSelector(),
                vol.Required(
                    "light_low_tide",
                    default=get_color_default(light_colors, "low_tide", DEFAULT_COLORS_LIGHT)
                ): ColorRGBSelector(),
                vol.Required(
                    "light_tide_line",
                    default=get_color_default(light_colors, "tide_line", DEFAULT_COLORS_LIGHT)
                ): ColorRGBSelector(),
                vol.Required(
                    "light_text",
                    default=get_color_default(light_colors, "text", DEFAULT_COLORS_LIGHT)
                ): ColorRGBSelector(),
                # Dark mode colors
                vol.Required(
                    "dark_high_tide",
                    default=get_color_default(dark_colors, "high_tide", DEFAULT_COLORS_DARK)
                ): ColorRGBSelector(),
                vol.Required(
                    "dark_low_tide",
                    default=get_color_default(dark_colors, "low_tide", DEFAULT_COLORS_DARK)
                ): ColorRGBSelector(),
                vol.Required(
                    "dark_tide_line",
                    default=get_color_default(dark_colors, "tide_line", DEFAULT_COLORS_DARK)
                ): ColorRGBSelector(),
                vol.Required(
                    "dark_text",
                    default=get_color_default(dark_colors, "text", DEFAULT_COLORS_DARK)
                ): ColorRGBSelector(),
                # Font sizes
                vol.Required(
                    CONF_FONT_SIZE_TITLE,
                    default=current_options.get(CONF_FONT_SIZE_TITLE, DEFAULT_FONT_SIZE_TITLE)
                ): NumberSelector(NumberSelectorConfig(
                    min=10, max=32, step=1, mode=NumberSelectorMode.SLIDER, unit_of_measurement="px"
                )),
                vol.Required(
                    CONF_FONT_SIZE_LABELS,
                    default=current_options.get(CONF_FONT_SIZE_LABELS, DEFAULT_FONT_SIZE_LABELS)
                ): NumberSelector(NumberSelectorConfig(
                    min=8, max=24, step=1, mode=NumberSelectorMode.SLIDER, unit_of_measurement="px"
                )),
                vol.Required(
                    CONF_FONT_SIZE_AXIS,
                    default=current_options.get(CONF_FONT_SIZE_AXIS, DEFAULT_FONT_SIZE_AXIS)
                ): NumberSelector(NumberSelectorConfig(
                    min=6, max=18, step=1, mode=NumberSelectorMode.SLIDER, unit_of_measurement="px"
                )),
            }),
        )
