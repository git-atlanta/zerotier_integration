import logging
import requests
import voluptuous as vol
from homeassistant.components.sensor import PLATFORM_SCHEMA, SensorEntity
from homeassistant.const import CONF_API_KEY, CONF_NAME
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

CONF_NETWORK_ID = 'network_id'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_API_KEY): cv.string,
    vol.Required(CONF_NETWORK_ID): cv.string,
})

async def async_setup_platform(
    hass, config, async_add_entities: AddEntitiesCallback, discovery_info=None
):
    """Set up the ZeroTier sensor platform."""
    api_key = config[CONF_API_KEY]
    network_id = config[CONF_NETWORK_ID]
    session = async_get_clientsession(hass)

    async def async_update_data():
        """Fetch data from ZeroTier API."""
        url = f"https://api.zerotier.com/api/v1/network/{network_id}/member"
        headers = {"Authorization": f"token {api_key}"}
        response = await session.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    async_add_entities([ZeroTierSensor(async_update_data)], True)

class ZeroTierSensor(SensorEntity):
    """Implementation of the ZeroTier sensor."""

    def __init__(self, async_update_data):
        """Initialize the sensor."""
        self._state = None
        self._async_update_data = async_update_data

    @property
    def name(self):
        """Return the name of the sensor."""
        return "ZeroTier Members"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    async def async_update(self):
        """Update the sensor state."""
        data = await self._async_update_data()
        self._state = len(data)  # Example: return the number of members
