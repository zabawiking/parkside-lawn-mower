import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.entity import EntityCategory
from .pymoebot2 import MoeBot

from . import BaseMoeBotEntity
from .const import DOMAIN

_log = logging.getLogger(__package__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Add sensors for passed config_entry in HA."""
    moebot = hass.data[DOMAIN][config_entry.entry_id]

    async_add_entities([ParkWhenRainingSwitch(moebot), HedgehogProtectionSwitch(moebot), 
        RainCompentastionSwitch(moebot)])


class ParkWhenRainingSwitch(BaseMoeBotEntity, SwitchEntity):

    def __init__(self, moebot: MoeBot):
        super().__init__(moebot)

        # A unique_id for this entity within this domain.
        # Note: This is NOT used to generate the user visible Entity ID used in automations.
        self._attr_unique_id = f"{self._moebot.id}_park_if_raining"
        self._attr_entity_category = EntityCategory.CONFIG

        self._attr_has_entity_name = True
        self._attr_translation_key = "park_if_raining"

    @property
    def is_on(self) -> bool:
        return self._moebot.mow_in_rain

    def turn_on(self, **kwargs: Any) -> None:
        self._moebot.mow_in_rain = True

    def turn_off(self, **kwargs: Any) -> None:
        self._moebot.mow_in_rain = False

class HedgehogProtectionSwitch(BaseMoeBotEntity, SwitchEntity):

    def __init__(self, moebot: MoeBot):
        super().__init__(moebot)

        # A unique_id for this entity within this domain.
        # Note: This is NOT used to generate the user visible Entity ID used in automations.
        self._attr_unique_id = f"{self._moebot.id}_hedgehog_protection"
        self._attr_entity_category = EntityCategory.CONFIG

        self._attr_has_entity_name = True
        self._attr_translation_key = "hedgehog_protection"

    @property
    def is_on(self) -> bool:
        return self._moebot.hedgehog_protection

    def turn_on(self, **kwargs: Any) -> None:
        self._moebot.hedgehog_protection = True

    def turn_off(self, **kwargs: Any) -> None:
        self._moebot.hedgehog_protection = False

class RainCompentastionSwitch(BaseMoeBotEntity, SwitchEntity):
    def __init__(self, moebot):
        super().__init__(moebot)

        # A unique_id for this entity within this domain.
        # Note: This is NOT used to generate the user visible Entity ID used in automations.
        self._attr_unique_id = f"{self._moebot.id}_rain_compensation"
        self._attr_entity_category = EntityCategory.CONFIG

        # The name of the entity
        self._attr_has_entity_name = True
        self._attr_translation_key = "rain_compensation"

    @property
    def is_on(self) -> bool:
        return self._moebot.rain_compensation

    def turn_on(self, **kwargs: Any) -> None:
        self._moebot.rain_compensation = True

    def turn_off(self, **kwargs: Any) -> None:
        self._moebot.rain_compensation = False