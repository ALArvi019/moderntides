"""
Custom component for Modern Tides integration with Home Assistant.
For more details about this component, please refer to the documentation at
https://github.com/ALArvi019/moderntides
"""
import logging
from datetime import timedelta
import os
import sys
import async_timeout
import datetime
import traceback

from homeassistant.util import dt as dt_util

try:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.typing import ConfigType
    from homeassistant.helpers.update_coordinator import (
        DataUpdateCoordinator,
        UpdateFailed,
    )
    from homeassistant.util import dt as dt_util
except ImportError:
    ConfigEntry = object
    HomeAssistant = object
    ConfigType = dict
    DataUpdateCoordinator = object
    UpdateFailed = Exception
    dt_util = None

from .const import (
    DOMAIN,
    PLATFORMS,
    CONF_STATION_ID,
    CONF_STATION_NAME,
    CONF_STATIONS,
    CONF_UPDATE_INTERVAL,
    INTERVALS
)
from .tide_api import TideApiClient
from .plot_manager import TidePlotManager

_LOGGER = logging.getLogger(__name__)

def _install_dependencies():
    try:
        import requests
    except ImportError:
        _LOGGER.warning("Installing missing dependency: requests")
        os.system(f"{sys.executable} -m pip install requests")

_install_dependencies()

class TideDataCoordinator(DataUpdateCoordinator):
    """Class to manage fetching tide data."""

    def __init__(
        self,
        hass: HomeAssistant,
        station: dict,
    ):
        """Initialize coordinator."""
        self.station_id = station[CONF_STATION_ID]
        self.station_name = station[CONF_STATION_NAME]
        self.api_client = TideApiClient()
        
        # Convert update interval string to minutes
        update_interval_str = station.get(CONF_UPDATE_INTERVAL, "1h")
        update_interval_min = INTERVALS.get(update_interval_str, 60)
        update_interval = datetime.timedelta(minutes=update_interval_min)

        _LOGGER.debug("Creating coordinator for station %s (%s) with update interval %s",
                      self.station_name, self.station_id, update_interval)

        # Initialize plot manager for tide charts
        safe_name = self.station_name.lower().replace(" ", "_").replace("-", "_")
        plot_filename = hass.config.path("www", f"{DOMAIN}_{safe_name}_plot.svg")
        self.plot_manager = TidePlotManager(
            name=self.station_name,
            filename=plot_filename,
            transparent_background=False
        )

        super().__init__(
            hass,
            _LOGGER,
            name=f"Modern Tides {self.station_name}",
            update_interval=update_interval,
        )

    async def _async_update_data(self):
        """Fetch data from API endpoint."""
        try:
            async with async_timeout.timeout(10):
                # Get current day data
                today = datetime.datetime.now().strftime("%Y%m%d")
                daily_data = await self.hass.async_add_executor_job(
                    self.api_client.get_daily_tides, self.station_id, today
                )
                
                # Log the data structure for debugging
                _LOGGER.debug("Daily data for station %s: %s", self.station_id, daily_data)
                
                # Get current month data for trend analysis
                current_month = datetime.datetime.now().strftime("%Y%m")
                monthly_data = await self.hass.async_add_executor_job(
                    self.api_client.get_monthly_tides, self.station_id, current_month
                )
                
                # Combine data
                data = {
                    "daily": daily_data,
                    "monthly": monthly_data,
                    "station_id": self.station_id,
                    "station_name": self.station_name
                }
                
                # Process data to extract current tide height and next events
                if daily_data and "mareas" in daily_data and "datos" in daily_data["mareas"]:
                    if "marea" in daily_data["mareas"]["datos"]:
                        # Current API format has data in 'datos.marea'
                        data.update(self._process_tide_data(daily_data["mareas"]["datos"]["marea"]))
                    else:
                        _LOGGER.error("Unexpected data format: 'marea' key not found in 'datos'")
                else:
                    _LOGGER.error("No valid tide data found for station %s", self.station_id)
                
                # Generate tide plot
                try:
                    if daily_data:
                        await self.hass.async_add_executor_job(
                            self.plot_manager.generate_tide_plot, data
                        )
                        _LOGGER.debug("Tide plot generated for station %s", self.station_id)
                except Exception as plot_err:
                    _LOGGER.warning("Failed to generate tide plot for station %s: %s", 
                                   self.station_id, plot_err)
                
                return data
        except Exception as err:
            _LOGGER.error("Error updating data for station %s: %s", self.station_id, err)
            import traceback
            _LOGGER.error("Traceback: %s", traceback.format_exc())
            raise UpdateFailed(f"Error communicating with API: {err}") from err

    def _process_tide_data(self, tide_data):
        """Process tide data to extract current and next tide information."""
        now = dt_util.now()  # Use Home Assistant's dt_util for timezone-aware datetime
        today = now.strftime("%Y-%m-%d")
        current_height = None
        next_high = None
        next_low = None
        
        # Log the tide data for debugging
        _LOGGER.debug("Processing tide data for station %s: %s", self.station_id, tide_data)
        
        # Find current tide height (interpolate between points if needed)
        tide_points = []
        processed_tide_points = []  # For plot manager
        for point in tide_data:
            # Log each point for debugging
            _LOGGER.debug("Processing tide point: %s", point)
            
            if "hora" in point and "altura" in point:
                time_str = point["hora"]  # Format is "HH:MM"
                height = float(point["altura"])
                
                try:
                    # Parse the time (format: "HH:MM")
                    # Combine with today's date
                    time_parts = time_str.split(":")
                    hours = int(time_parts[0])
                    minutes = int(time_parts[1])
                    
                    # Create a UTC datetime first (API times are in UTC)
                    utc_time = datetime.datetime(
                        year=now.year,
                        month=now.month,
                        day=now.day,
                        hour=hours,
                        minute=minutes,
                        tzinfo=datetime.timezone.utc
                    )
                    
                    # Convert UTC to local timezone
                    tide_time = dt_util.as_local(utc_time)
                    
                    # Handle case when tide time is past midnight but still part of today's data
                    if tide_time > now + datetime.timedelta(hours=12):
                        utc_time_prev_day = utc_time - datetime.timedelta(days=1)
                        tide_time = dt_util.as_local(utc_time_prev_day)
                    elif tide_time < now - datetime.timedelta(hours=12):
                        utc_time_next_day = utc_time + datetime.timedelta(days=1)
                        tide_time = dt_util.as_local(utc_time_next_day)
                        
                    tide_points.append((tide_time, height))
                    processed_tide_points.append({
                        'time': tide_time,
                        'height': height
                    })
                    _LOGGER.debug("Added tide point for station %s: time=%s, height=%s", 
                                 self.station_id, tide_time, height)
                except ValueError as e:
                    _LOGGER.error("Error parsing tide time: %s - %s", time_str, e)
                    continue
        
        # Sort by time
        tide_points.sort(key=lambda x: x[0])
        
        # Find current height through linear interpolation
        for i in range(len(tide_points) - 1):
            if tide_points[i][0] <= now <= tide_points[i+1][0]:
                t1, h1 = tide_points[i]
                t2, h2 = tide_points[i+1]
                
                # Linear interpolation
                time_diff = (t2 - t1).total_seconds()
                height_diff = h2 - h1
                now_diff = (now - t1).total_seconds()
                
                if time_diff > 0:
                    current_height = h1 + (height_diff * now_diff / time_diff)
                else:
                    current_height = h1
                break
        
        # If we couldn't interpolate, use the closest data point
        if current_height is None and tide_points:
            tide_points.sort(key=lambda x: abs((x[0] - now).total_seconds()))
            current_height = tide_points[0][1]
        
        # Identify tide type points (high/low)
        high_tides = []
        low_tides = []
        
        for point in tide_data:
            if "hora" in point and "altura" in point and "tipo" in point:
                time_str = point["hora"]  # Format is "HH:MM"
                height = float(point["altura"])
                tide_type = point["tipo"]
                
                try:
                    # Parse the time (format: "HH:MM")
                    # Combine with today's date
                    time_parts = time_str.split(":")
                    hours = int(time_parts[0])
                    minutes = int(time_parts[1])
                    
                    # Create a UTC datetime first (API times are in UTC)
                    utc_time = datetime.datetime(
                        year=now.year,
                        month=now.month,
                        day=now.day,
                        hour=hours,
                        minute=minutes,
                        tzinfo=datetime.timezone.utc
                    )
                    
                    # Convert UTC to local timezone
                    tide_time = dt_util.as_local(utc_time)
                    
                    # Handle case when tide time is past midnight but still part of today's data
                    if tide_time > now + datetime.timedelta(hours=12):
                        utc_time_prev_day = utc_time - datetime.timedelta(days=1)
                        tide_time = dt_util.as_local(utc_time_prev_day)
                    elif tide_time < now - datetime.timedelta(hours=12):
                        utc_time_next_day = utc_time + datetime.timedelta(days=1)
                        tide_time = dt_util.as_local(utc_time_next_day)
                    
                    if tide_type == "pleamar" and tide_time >= now:
                        high_tides.append((tide_time, height))
                        _LOGGER.debug("Added high tide for station %s: time=%s, height=%s", 
                                     self.station_id, tide_time, height)
                    elif tide_type == "bajamar" and tide_time >= now:
                        low_tides.append((tide_time, height))
                        _LOGGER.debug("Added low tide for station %s: time=%s, height=%s", 
                                     self.station_id, tide_time, height)
                except ValueError as e:
                    _LOGGER.error("Error parsing tide type time: %s - %s", time_str, e)
                    continue
        
        # Sort by time to get next events
        high_tides.sort(key=lambda x: x[0])
        low_tides.sort(key=lambda x: x[0])
        
        # Extract next high and low tide info
        if high_tides:
            next_high = {
                "time": high_tides[0][0],
                "height": high_tides[0][1]
            }
            
        if low_tides:
            next_low = {
                "time": low_tides[0][0],
                "height": low_tides[0][1]
            }
            
        return {
            "current_height": current_height,
            "next_high_tide": next_high,
            "next_low_tide": next_low,
            "tide_points": processed_tide_points
        }

async def async_setup(hass, config):
    """Set up the Modern Tides component."""
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass, entry):
    """Set up Modern Tides from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    
    # Initialize entry data structure
    hass.data[DOMAIN][entry.entry_id] = {
        "entry": entry,
        "coordinators": {}
    }
    
    # Create a coordinator for each station
    stations = entry.data.get(CONF_STATIONS, [])
    _LOGGER.debug("Setting up %d stations: %s", len(stations), stations)
    
    for station in stations:
        station_id = station[CONF_STATION_ID]
        station_name = station[CONF_STATION_NAME]
        _LOGGER.debug("Creating coordinator for station %s (%s)", station_id, station_name)
        
        coordinator = TideDataCoordinator(hass, station)
        
        # Do initial data update
        try:
            await coordinator.async_config_entry_first_refresh()
            _LOGGER.debug("Initial data update successful for station %s", station_id)
        except Exception as err:
            _LOGGER.error("Error during initial data update for station %s: %s", station_id, err)
            import traceback
            _LOGGER.error("Traceback: %s", traceback.format_exc())
        
        # Store the coordinator
        hass.data[DOMAIN][entry.entry_id]["coordinators"][station_id] = coordinator
        _LOGGER.debug("Added coordinator for station %s to data structure", station_id)

    # Set up all platforms for this device/entry.
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Register update listener for config entry changes
    entry.async_on_unload(entry.add_update_listener(async_update_options))

    return True

async def async_update_options(hass, entry):
    """Update options for the entry."""
    await hass.config_entries.async_reload(entry.entry_id)

async def async_unload_entry(hass, entry):
    """Unload a config entry."""
    # Unload entities for this entry/device
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    # Remove entry from data
    if unload_ok and entry.entry_id in hass.data[DOMAIN]:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
