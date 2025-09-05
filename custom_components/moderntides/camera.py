"""Camera platform for Modern Tides integration."""
import aiofiles
import aiofiles.os
import logging
import os
import time
from typing import Optional

from homeassistant.components.camera import Camera
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.entity_registry import async_get
from homeassistant.helpers.event import async_track_state_change_event

from .const import CONF_STATION_ID, CONF_STATION_NAME, CONF_STATIONS, DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up Modern Tides camera based on a config entry."""
    stations = entry.data.get(CONF_STATIONS, [])
    
    if not stations:
        return

    entities = []
    
    # Get coordinators from the hass.data structure
    entry_data = hass.data[DOMAIN][entry.entry_id]
    coordinators = entry_data["coordinators"]
    
    _LOGGER.debug("Setting up cameras for %d stations", len(stations))
    
    # Create camera entities for each station
    for station in stations:
        station_id = station[CONF_STATION_ID]
        station_name = station[CONF_STATION_NAME]
        
        if station_id in coordinators:
            coordinator = coordinators[station_id]
            
            # Create light mode tide plot camera
            camera_light = ModernTidesCamera(
                coordinator,
                station_name,
                entry.entry_id,
                dark_mode=False
            )
            entities.append(camera_light)
            
            # Create dark mode tide plot camera
            camera_dark = ModernTidesCamera(
                coordinator,
                station_name,
                entry.entry_id,
                dark_mode=True
            )
            entities.append(camera_dark)
            
            _LOGGER.debug("Added cameras (light and dark) for station: %s", station_name)

    if entities:
        async_add_entities(entities)


class ModernTidesCamera(Camera):
    """Modern Tides camera that displays tide plots."""

    def __init__(self, coordinator, station_name: str, entry_id: str, dark_mode: bool = False):
        """Initialize the camera."""
        super().__init__()
        self.coordinator = coordinator
        self._station_name = station_name
        self._entry_id = entry_id
        self._dark_mode = dark_mode
        
        # Set name and unique_id based on mode
        mode_suffix = " Dark" if dark_mode else ""
        self._attr_name = f"{station_name} Tide Plot{mode_suffix}"
        mode_id_suffix = "_dark" if dark_mode else ""
        self._attr_unique_id = f"{DOMAIN}_{coordinator.station_id}_{entry_id}_camera{mode_id_suffix}"
        
        # Generate safe name for filename (will be used in async_added_to_hass)
        self._safe_name = station_name.lower().replace(" ", "_").replace("-", "_")
        self._image_filename = None  # Will be set in async_added_to_hass
        
        # Image data
        self._last_image = None
        self._last_updated = None

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, f"{self.coordinator.station_id}_{self._entry_id}")},
            name=f"Modern Tides {self._station_name}",
            manufacturer="Modern Tides",
            model="Tide Station",
            entry_type=DeviceEntryType.SERVICE,
        )

    @property
    def available(self) -> bool:
        """Return if camera is available."""
        return (self.coordinator.last_update_success and 
                self._image_filename is not None and 
                os.path.exists(self._image_filename))

    async def async_added_to_hass(self) -> None:
        """Handle entity added to hass."""
        await super().async_added_to_hass()
        
        # Generate image filename now that we have access to hass
        mode_suffix = "_dark" if self._dark_mode else ""
        self._image_filename = self.hass.config.path("www", f"{DOMAIN}_{self._safe_name}_plot{mode_suffix}.svg")
        
        # Set content type for SVG images
        self.content_type = "image/svg+xml"
        
        # Listen for coordinator updates
        self.async_on_remove(
            self.coordinator.async_add_listener(self._handle_coordinator_update)
        )
        
        # Listen for sensor state changes (optional, for more responsive updates)
        registry = async_get(self.hass)
        sensor_entity_id = registry.async_get_entity_id(
            "sensor", DOMAIN, f"{DOMAIN}_{self.coordinator.station_id}_{self._entry_id}"
        )
        
        if sensor_entity_id:
            self.async_on_remove(
                async_track_state_change_event(
                    self.hass, [sensor_entity_id], self._async_sensor_state_listener
                )
            )

        # Initial image load
        await self.async_update()

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self.async_write_ha_state()

    async def _async_sensor_state_listener(self, event) -> None:
        """Handle sensor state changes."""
        self.async_write_ha_state()

    def camera_image(
        self, width: Optional[int] = None, height: Optional[int] = None
    ) -> Optional[bytes]:
        """Return bytes of camera image."""
        return self._last_image

    async def async_camera_image(
        self, width: Optional[int] = None, height: Optional[int] = None
    ) -> Optional[bytes]:
        """Return bytes of camera image."""
        await self.async_update()
        return self._last_image

    async def async_update(self) -> None:
        """Update the camera image."""
        try:
            if self._image_filename is not None:
                # Read the SVG file directly (filename already includes the correct mode suffix)
                if await aiofiles.os.path.exists(self._image_filename):
                    # Check if SVG file has been updated
                    file_mtime = await aiofiles.os.path.getmtime(self._image_filename)
                    
                    if self._last_updated is None or file_mtime > self._last_updated:
                        # Read SVG content and convert to bytes (non-blocking)
                        async with aiofiles.open(self._image_filename, "r", encoding='utf-8') as svg_file:
                            svg_content = await svg_file.read()
                        
                        # For SVG content, we need to return it as bytes
                        # Home Assistant can handle SVG content type
                        self._last_image = svg_content.encode('utf-8')
                        self._last_updated = file_mtime
                        mode_info = " (Dark Mode)" if self._dark_mode else " (Light Mode)"
                        _LOGGER.debug("Updated camera image (SVG)%s for %s", mode_info, self._station_name)
                else:
                    _LOGGER.debug("Image file not found: %s", self._image_filename)
                    self._last_image = None
            else:
                _LOGGER.debug("Image filename not set yet")
                self._last_image = None
                
        except Exception as e:
            _LOGGER.error("Error reading camera image for %s: %s", self._station_name, e)
            self._last_image = None

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        attrs = {}
        
        if self._last_updated:
            attrs["last_updated"] = time.ctime(self._last_updated)
            
        if self._image_filename and os.path.exists(self._image_filename):
            attrs["image_path"] = self._image_filename
            
        return attrs
