"""Config flow for WiFi Presence integration."""
from __future__ import annotations

from typing import Any
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from homeassistant.components import mqtt

from .const import (
    DOMAIN,
    CONF_TOPIC_PREFIX,
    DEFAULT_TOPIC_PREFIX,
)


class WifiPresenceConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for WiFi Presence."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if not await mqtt.async_wait_for_mqtt_client(self.hass):
            return self.async_abort(reason="mqtt_required")

        if user_input is not None:
            await self.async_set_unique_id(user_input[CONF_TOPIC_PREFIX])
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=f"WiFi Presence ({user_input[CONF_TOPIC_PREFIX]})",
                data=user_input,
            )

        data_schema = vol.Schema(
            {
                vol.Required(CONF_TOPIC_PREFIX, default=DEFAULT_TOPIC_PREFIX): str,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )
