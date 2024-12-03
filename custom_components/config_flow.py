import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN  # Assuming you have a const.py file with DOMAIN defined

# Define the configuration schema
STEP_USER_DATA_SCHEMA = vol.Schema({
    vol.Required("api_key"): str,
    vol.Required("network_id"): str,
})


class ZeroTierConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for ZeroTier."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD

    async def async_step_user(self, user_input: dict = None) -> FlowResult:
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            # You would normally validate the input and create an entry here
            # For this example, we'll just pass
            return self.async_create_entry(title="ZeroTier", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )
