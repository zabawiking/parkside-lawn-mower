import logging

from homeassistant.components.binary_sensor import BinarySensorDeviceClass, BinarySensorEntity
from homeassistant.helpers.entity import EntityCategory

from . import BaseMoeBotEntity
from .const import DOMAIN

_log = logging.getLogger()


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Add binary ensors for passed config_entry in HA."""
    moebot = hass.data[DOMAIN][config_entry.entry_id]

    async_add_entities([CoverOpenSensor(moebot)])

class CoverOpenSensor(BaseMoeBotEntity, BinarySensorEntity):
    def __init__(self, moebot):
        super().__init__(moebot)

        # A unique_id for this entity within this domain.
        # Note: This is NOT used to generate the user visible Entity ID used in automations.
        self._attr_unique_id = f"{self._moebot.id}_cover_open"

        # The name of the entity
        self._attr_has_entity_name = True
        self._attr_translation_key = "cover_open"

        self._attr_device_class = BinarySensorDeviceClass.DOOR

    # The value of this sensor.
    @property
    def is_on(self) -> bool:
        """Return the state of the sensor."""
        return bool(self._moebot.cover_open)