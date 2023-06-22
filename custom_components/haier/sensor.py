import logging

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import HomeAssistantType

from . import async_register_entity
from .coordinator import DeviceCoordinator
from .entity import HaierAbstractEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistantType, entry: ConfigEntry, async_add_entities) -> None:
    def register(coordinator: DeviceCoordinator, spec: str):
        return HaierSensor(coordinator, spec)

    await async_register_entity(hass, entry, async_add_entities, register, 'sensors')


class HaierSensor(HaierAbstractEntity, SensorEntity):

    def __init__(self, coordinator: DeviceCoordinator, spec: dict):
        super().__init__(coordinator, spec)
        if not spec['value_formatter']:
            self._attr_device_class = SensorDeviceClass.ENUM
            self._attr_options = list(spec['value_formatter'].values())

    def _update_value(self):
        formatter = self._spec['value_formatter']
        value = self.coordinator.data[self._spec['key']]
        self._attr_native_value = formatter[str(value)] if str(value) in formatter.keys() else value


