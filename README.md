# Raspberry Pi GPIO Rotary Encoder for Home Assistant
# Home Assistant Raspberry Pi GPIO PWM custom integration

**This code is heavily inspired by https://github.com/RedMeKool/HA-Raspberry-pi-GPIO-PWM**
For controlling the GPIOs, the platform connects to the pigpio-daemon (http://abyz.me.uk/rpi/pigpio/pigpiod.html), which must be running. On Raspbian Jessie 2016-05-10 or newer the pigpio library is already included. On other operating systems it needs to be installed first (see installation instructions: https://github.com/soldag/python-pwmled#installation).

For Home Assistant this daemon can be installed as an add-on (https://github.com/Poeschl/Hassio-Addons/tree/master/pigpio).

# Installation

### HACS

The recommend way to install `ha-rpi-gpio-rotary` is through [HACS](https://hacs.xyz/), by adding the repository url with category `integration`.

### Manual installation

Copy the `ha-rpi-gpio-rotary` folder and all of its contents into your Home Assistant's `custom_components` folder. This folder is usually inside your `/config` folder. If you are running Hass.io, use SAMBA to copy the folder over. You may need to create the `custom_components` folder and then copy the `ha-rpi-gpio-rotary` folder and all of its contents into it.

# Configuration
To enable this platform, add the following lines to your configuration.yaml:

```yaml
# Example configuration.yaml entry
sensor:
  - platform: rpi_gpio_rotary
    encoders:
      - name: Encoder Livingroom
        pinA: 10
        pinB: 9
        pinSW: 11
```
# CONFIGURATION VARIABLES
- **encoders** list *(REQUIRED)*: Can contain multiple encoders.

- **name** string *(REQUIRED)*: The name of the encoder.

- **pinA** integer *(REQUIRED)*: The pin connected to the pin A of the encoder.

- **pinB** integer *(REQUIRED)*: The pin connected to the pin B of the encoder.

- **pinSW** integer *(REQUIRED)*: The pin connected to the switch/push button of the encoder.

- **host** string *(optional, default: localhost)*: The remote host address for the GPIO driver.

- **port** integer *(optional, default: 8888)*: The port on which the GPIO driver is listening.


