import logging
from typing import Any, Dict

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN
from .haier import HaierClient, HaierClientException

_LOGGER = logging.getLogger(__name__)


class HaierConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(
            self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle a flow initiated by the user."""
        errors: Dict[str, str] = {}

        if user_input is not None:
            try:
                # 校验账号密码是否正确
                await HaierClient.get_session(user_input[CONF_USERNAME], user_input[CONF_PASSWORD])

                return self.async_create_entry(title="haier", data=user_input)
            except HaierClientException as e:
                _LOGGER.warning(str(e))
                errors['base'] = 'auth_error'

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_USERNAME): str,
                    vol.Required(CONF_PASSWORD): str,
                }
            ),
            errors=errors
        )

    # @staticmethod
    # @callback
    # def async_get_options_flow(
    #         config_entry: config_entries.ConfigEntry,
    # ) -> config_entries.OptionsFlow:
    #     """Create the options flow."""
    #     return OptionsFlowHandler(config_entry)


class OptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="haier", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_USERNAME, default=self.config_entry.data[CONF_USERNAME]): str,
                    vol.Required(CONF_PASSWORD, default=self.config_entry.data[CONF_PASSWORD]): str,
                }
            )
        )