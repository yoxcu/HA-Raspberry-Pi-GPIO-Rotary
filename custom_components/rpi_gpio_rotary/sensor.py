"""Support for Rotary Ecoders with Push Button."""
from __future__ import annotations

import logging
import time
from gpiozero import Button, RotaryEncoder
from gpiozero.pins.pigpio import PiGPIOFactory

import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA

from homeassistant.const import CONF_HOST, CONF_PORT, CONF_NAME
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .const import ATTR_Test, ATTR_VALUE

_LOGGER = logging.getLogger(__name__)

CONF_ENCODERS = "encoders"
CONF_PINA = "pinA"
CONF_PINB = "pinB"
CONF_PINSW = "pinSW"


DEFAULT_HOST = "localhost"
DEFAULT_PORT = 8888


PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_ENCODERS): vol.All(
            cv.ensure_list,
            [
                {
                    vol.Required(CONF_NAME): cv.string,
                    vol.Required(CONF_PINA): cv.positive_int,
                    vol.Required(CONF_PINB): cv.positive_int,
                    vol.Required(CONF_PINSW): cv.positive_int,
                    vol.Optional(CONF_HOST, default=DEFAULT_HOST): cv.string,
                    vol.Optional(CONF_PORT, default=DEFAULT_PORT): cv.port,
                }
            ],
        )
    }
)

def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: Callable,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the Rotary Encoder and Push Button."""
    entities = []
    for encoder_conf in config[CONF_ENCODERS]:
        pinA = encoder_conf[CONF_PINA]
        pinB = encoder_conf[CONF_PINB]
        opt_args = {}
        opt_args["pin_factory"] = PiGPIOFactory(host=encoder_conf[CONF_HOST], port=encoder_conf[CONF_PORT])
        encoder = RotaryEncoderSensor(RotaryEncoder(pinA,pinB,**opt_args), "{}_encoder".format(encoder_conf[CONF_NAME]))
        entities.append(encoder)

        pinSW = encoder_conf[CONF_PINSW]
        opt_args = {}
        opt_args["pin_factory"] = PiGPIOFactory(host=encoder_conf[CONF_HOST], port=encoder_conf[CONF_PORT])
        button = ButtonSensor(Button(pinSW,**opt_args), "{}_button".format(encoder_conf[CONF_NAME]))
        entities.append(button)


    add_entities(entities)

class RotaryEncoderSensor(Entity):
    def __init__(self, encoder, name):
        super().__init__()
        """Initialize the Rotary Encoder"""
        self._name = name
        self._state = 0
        self._available = True
        self.encoder = encoder
        self.attrs: Dict[str, Any] = {ATTR_Test: "Test", ATTR_VALUE: 0}
        self.encoder.when_rotated = self.update_Home_Assistant


    @property
    def name(self) -> str:
        """Return the name of the entity."""
        return self._name

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._available

    @property
    def state(self) -> Optional[str]:
        return self._state

    @property
    def device_state_attributes(self) -> Dict[str, Any]:
        return self.attrs

    @property
    def should_poll(self):
        return False
    
    def update_Home_Assistant(self):
        self.attrs[ATTR_VALUE]=self.encoder.value
        self._state = int((self.encoder.value+1)*50)
        self.async_write_ha_state()

class ButtonSensor(Entity):
    def __init__(self, button, name):
        super().__init__()
        """Initialize the Push Button."""
        self._name = name
        self._state = "off"
        self._available = True
        self.button = button
        self.attrs: Dict[str, Any] = {ATTR_Test: "Test", ATTR_VALUE: 0}
        self.button.when_pressed = self.update_Home_Assistant
        self.button.when_released = self.update_Home_Assistant


    @property
    def name(self) -> str:
        """Return the name of the entity."""
        return self._name

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._available

    @property
    def state(self) -> Optional[str]:
        return self._state

    @property
    def device_state_attributes(self) -> Dict[str, Any]:
        return self.attrs

    @property
    def should_poll(self):
        return False
    
    def update_Home_Assistant(self):
        if self.button.is_pressed:
            self.attrs[ATTR_VALUE]="on"
            self._state = "on"
        else:
            self.attrs[ATTR_VALUE]="off"
            self._state = "off"

        self.async_write_ha_state()

