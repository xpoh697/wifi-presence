# Technical Specification (ТЗ): HACS Compatibility for WiFi Presence

## 1. Goal and Overview
Adapt the `wifi-presence` repository (forked at `https://github.com/xpoh697/wifi-presence`) to be fully compatible with HACS (Home Assistant Community Store) as an Integration (`custom_components`), while preserving the existing OpenWrt Go daemon functionality.

## 2. Target Directory Structure
The repository must conform to HACS integration requirements:
- `hacs.json` in the root of the repository.
- `custom_components/wifi_presence/` directory containing the Home Assistant custom integration:
  - `manifest.json`: Integration metadata complying with Home Assistant and HACS standards.
  - `__init__.py`: Async setup, integration entry lifecycle, and MQTT coordination.
  - `const.py`: Domain, configuration constants, default values, and MQTT topic definitions.
  - `config_flow.py`: UI configuration flow for setting up MQTT topic prefix and tracking options.
  - `device_tracker.py`: Entities representing WiFi clients tracked by wifi-presence.
  - `strings.json`: Translatable strings for UI / config flow.
  - `translations/en.json`: English localization.
  - `translations/ru.json`: Russian localization.
- `.github/workflows/hacs.yml`: CI workflow running HACS action validation and Hassfest.

## 3. Integration Requirements
- **Domain**: `wifi_presence`
- **Name**: `WiFi Presence`
- **IoT Class**: `local_push`
- **Dependencies**: `["mqtt"]` (uses Home Assistant's built-in MQTT client, zero external pip dependencies).
- **Architecture**: Fully asynchronous (`async_setup_entry`, `async_unload_entry`), no blocking calls in the event loop.
- **HACS Compliance**: Pass standard HACS repository checks (`hacs/action`).
