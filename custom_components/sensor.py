import logging
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(hass: HomeAssistant, config, async_add_entities, discovery_info=None):
    """Set up the sensor platform."""
    api_key = config.get("api_key")
    network_id = config.get("network_id")

    # 创建一个DataUpdateCoordinator来处理数据更新
    coordinator = ZeroTierDataUpdateCoordinator(hass, api_key, network_id)

    # 等待数据更新完成
    await coordinator.async_refresh()

    # 创建传感器实体
    async_add_entities([ZeroTierSensor(coordinator)], True)

class ZeroTierDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching ZeroTier data."""

    def __init__(self, hass, api_key, network_id):
        """Initialize the data updater."""
        self.api_key = api_key
        self.network_id = network_id
        update_interval = datetime.timedelta(minutes=5)  # 您可以根据需要调整更新间隔
        super().__init__(hass, _LOGGER, name='ZeroTier Data', update_interval=update_interval)

    async def _async_update_data(self):
        """Fetch data from ZeroTier API."""
        session = async_get_clientsession(self.hass)
        url = f"https://api.zerotier.com/api/v1/network/{self.network_id}/member"
        headers = {"Authorization": f"token {self.api_key}"}
        async with session.get(url, headers=headers) as resp:
            if resp.status == 200:
                return await resp.json()
            else:
                raise UpdateFailed(f"Error fetching data: {resp.status}")

class ZeroTierSensor:
    """Implementation of a ZeroTier sensor."""

    def __init__(self, coordinator):
        """Initialize the sensor."""
        self.coordinator = coordinator

    @property
    def name(self):
        """Return the name of the sensor."""
        return "ZeroTier Members"

    @property
    def state(self):
        """Return the state of the sensor."""
        # 这里我们返回成员数量作为示例，您可以根据需要调整
        return len(self.coordinator.data)

    @property
    def device_info(self):
        """Return device information."""
        # 返回设备信息，您可以根据需要调整
        return {
            "identifiers": {(DOMAIN, self.coordinator.data[0]["id"])} if self.coordinator.data else None,
            "name": "ZeroTier",
            "manufacturer": "ZeroTier, Inc.",
            "model": "Virtual Network",
        }

    async def async_update(self):
        """Update the sensor."""
        await self.coordinator.async_request_refresh()

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        # 这里我们返回设备名称、最后可见时间和IP地址
        attributes = {}
        for member in self.coordinator.data or []:
            name = member.get("name")
            last_seen = member.get("lastSeen")
            ip_address = member.get("ipAssignments", [None])[0]
            if name and last_seen and ip_address:
                attributes[name] = {
                    "Last Seen": last_seen,
                    "IP Address": ip_address,
                }
        return attributes
