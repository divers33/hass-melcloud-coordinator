"""Base entity for MELCloud integration."""

from __future__ import annotations

import logging

from homeassistant.core import callback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .coordinator import MelCloudDevice, MelCloudDeviceUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


class MelCloudEntity(CoordinatorEntity[MelCloudDeviceUpdateCoordinator]):
    """Base class for MELCloud entities."""

    _attr_has_entity_name = True

    def __init__(
        self,
        api: MelCloudDevice,
    ) -> None:
        """Initialize the entity."""
        super().__init__(api.coordinator)
        self._api = api

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return super().available and self._api.available

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        _LOGGER.debug(
            "Entity %s received coordinator update, writing state",
            self.entity_id,
        )
        super()._handle_coordinator_update()
