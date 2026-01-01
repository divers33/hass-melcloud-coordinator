"""Coordinator for MELCloud integration."""

from __future__ import annotations

import asyncio
from datetime import timedelta
import logging
from typing import TYPE_CHECKING

from aiohttp import ClientConnectionError, ClientResponseError
from pymelcloud import get_devices

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_TOKEN
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed, ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL, DOMAIN
from .device import MelCloudDevice

if TYPE_CHECKING:
    from . import MelCloudConfigEntry

_LOGGER = logging.getLogger(__name__)


class MelCloudDataUpdateCoordinator(
    DataUpdateCoordinator[dict[str, list[MelCloudDevice]]]
):
    """Coordinator for MELCloud data updates."""

    config_entry: MelCloudConfigEntry

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        """Initialize the coordinator."""
        # Get scan interval from options, with fallback to default
        scan_interval_minutes = config_entry.options.get(
            CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL
        )

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            config_entry=config_entry,
            update_interval=timedelta(minutes=scan_interval_minutes),
        )

    async def _mel_devices_setup(
        self, token: str
    ) -> dict[str, list[MelCloudDevice]]:
        """Query connected devices from MELCloud."""
        session = async_get_clientsession(self.hass)
        async with asyncio.timeout(10):
            all_devices = await get_devices(
                token=token,
                session=session,
                conf_update_interval=timedelta(minutes=30),
                device_set_debounce=timedelta(seconds=2),
            )
        wrapped_devices: dict[str, list[MelCloudDevice]] = {}
        for device_type, devices in all_devices.items():
            wrapped_devices[device_type] = [
                MelCloudDevice(device) for device in devices
            ]
        return wrapped_devices

    async def _async_setup(self) -> None:
        """Set up the coordinator."""
        try:
            mel_devices = await self._mel_devices_setup(
                self.config_entry.data[CONF_TOKEN]
            )
        except ClientResponseError as ex:
            if ex.status == 401:
                raise ConfigEntryAuthFailed from ex
            raise ConfigEntryNotReady from ex
        except (TimeoutError, ClientConnectionError) as ex:
            raise ConfigEntryNotReady from ex

        _LOGGER.debug("MELCloud devices found: %s", mel_devices)
        self.data = mel_devices

    async def _async_update_data(self) -> dict[str, list[MelCloudDevice]]:
        """Fetch data from MELCloud."""
        _LOGGER.debug("Updating MELCloud devices")

        # On first refresh, data is set by _async_setup
        if self.data is None:
            return {}

        try:
            for device_list in self.data.values():
                for device in device_list:
                    await device.async_update()
        except ClientConnectionError as ex:
            raise UpdateFailed(f"Error communicating with MELCloud: {ex}") from ex

        return self.data
