"""Device tracker platform for WiFi Presence."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components import mqtt
from homeassistant.components.device_tracker import SourceType, TrackerEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect, async_dispatcher_send
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    DOMAIN,
    CONF_TOPIC_PREFIX,
    DEFAULT_TOPIC_PREFIX,
    PAYLOAD_CONNECTED,
    PAYLOAD_NOT_CONNECTED,
)

_LOGGER = logging.getLogger(__name__)

SIGNAL_NEW_DEVICE = f"{DOMAIN}_new_device"


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up WiFi Presence device tracker from a config entry."""
    topic_prefix = entry.data.get(CONF_TOPIC_PREFIX, DEFAULT_TOPIC_PREFIX)
    entry_data = hass.data[DOMAIN][entry.entry_id]
    known_devices = entry_data["devices"]

    @callback
    def async_add_device_tracker(device: WifiPresenceTracker) -> None:
        async_add_entities([device])

    unsub_dispatcher = async_dispatcher_connect(
        hass, f"{SIGNAL_NEW_DEVICE}_{entry.entry_id}", async_add_device_tracker
    )
    entry_data["unsub_listeners"].append(unsub_dispatcher)

    @callback
    def message_received(msg: mqtt.ReceiveMessage) -> None:
        """Handle incoming MQTT event for WiFi client presence."""
        # Format: <prefix>/<ap_name>/<mac>
        parts = msg.topic.split("/")
        if len(parts) < 3:
            return

        mac = parts[-1].upper()
        ap_name = parts[-2]
        payload = msg.payload.strip()

        if mac not in known_devices:
            tracker = WifiPresenceTracker(entry, mac, ap_name)
            known_devices[mac] = tracker
            async_dispatcher_send(hass, f"{SIGNAL_NEW_DEVICE}_{entry.entry_id}", tracker)

        tracker = known_devices[mac]
        tracker.async_update_state(ap_name, payload)

    sub_topic = f"{topic_prefix}/+/+"
    unsub_mqtt = await mqtt.async_subscribe(hass, sub_topic, message_received, qos=0)
    entry_data["unsub_listeners"].append(unsub_mqtt)


class WifiPresenceTracker(TrackerEntity):
    """Representing a WiFi client tracked by wifi-presence."""

    _attr_has_entity_name = True

    def __init__(self, entry: ConfigEntry, mac: str, ap_name: str) -> None:
        """Initialize the device tracker."""
        self._entry = entry
        self._mac = mac
        self._ap_name = ap_name
        self._is_connected = False
        self._attr_unique_id = f"wifi_presence_{mac.replace(':', '').lower()}"
        self._attr_name = f"WiFi Client {mac}"

    @property
    def source_type(self) -> SourceType:
        """Return the source type of the device tracker."""
        return SourceType.ROUTER

    @property
    def is_connected(self) -> bool:
        """Return true if the device is connected to the network."""
        return self._is_connected

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return device tracker attributes."""
        return {
            "mac": self._mac,
            "access_point": self._ap_name,
        }

    @callback
    def async_update_state(self, ap_name: str, payload: str) -> None:
        """Update tracker connection state."""
        self._ap_name = ap_name
        if payload == PAYLOAD_CONNECTED:
            self._is_connected = True
        elif payload == PAYLOAD_NOT_CONNECTED:
            self._is_connected = False
        if self.hass:
            self.async_write_ha_state()
