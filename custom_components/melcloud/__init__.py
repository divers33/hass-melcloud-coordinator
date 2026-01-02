"""The MELCloud Climate integration."""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .coordinator import MelCloudConfigEntry, mel_devices_setup

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.CLIMATE, Platform.SENSOR, Platform.WATER_HEATER]


async def async_setup_entry(hass: HomeAssistant, entry: MelCloudConfigEntry) -> bool:
    """Establish connection with MELCloud."""
    _LOGGER.info(
        "MELCloud integration starting with token: %s... (first 8 chars)",
        entry.data.get("token", "")[:8]
    )
    entry.runtime_data = await mel_devices_setup(hass, entry)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(config_entry, PLATFORMS)
