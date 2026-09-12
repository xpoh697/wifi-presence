"""The WiFi Presence integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.components import mqtt

from .const import DOMAIN, PLATFORMS

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up WiFi Presence from a config entry."""
    if not await mqtt.async_wait_for_mqtt_client(hass):
        raise ConfigEntryNotReady("MQTT integration is not available")

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "devices": {},
        "unsub_listeners": [],
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    entry_data = hass.data[DOMAIN].get(entry.entry_id, {})
    for unsub in entry_data.get("unsub_listeners", []):
        unsub()

    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)

    return unload_ok
