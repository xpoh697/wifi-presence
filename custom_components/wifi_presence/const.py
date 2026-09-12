"""Constants for the WiFi Presence integration."""

DOMAIN = "wifi_presence"

CONF_TOPIC_PREFIX = "topic_prefix"
DEFAULT_TOPIC_PREFIX = "wifi-presence"

CONF_DISCOVERY_PREFIX = "discovery_prefix"
DEFAULT_DISCOVERY_PREFIX = "homeassistant"

# MQTT payloads
STATUS_ONLINE = "online"
STATUS_OFFLINE = "offline"
PAYLOAD_CONNECTED = "connected"
PAYLOAD_NOT_CONNECTED = "not_connected"

# Platforms
PLATFORMS = ["device_tracker"]
