"""The MELCloud Climate integration."""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .coordinator import MelCloudDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.CLIMATE, Platform.SENSOR, Platform.WATER_HEATER]

type MelCloudConfigEntry = ConfigEntry[MelCloudDataUpdateCoordinator]


async def async_setup_entry(hass: HomeAssistant, entry: MelCloudConfigEntry) -> bool:
    """Establish connection with MELCloud."""
    coordinator = MelCloudDataUpdateCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: MelCloudConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
