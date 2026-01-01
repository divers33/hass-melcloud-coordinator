# MELCloud Integration with Coordinator

[![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg)](https://github.com/hacs/integration)
[![Validate with hassfest and HACS](https://github.com/divers33/hass-melcloud-coordinator/actions/workflows/hacs.yml/badge.svg)](https://github.com/divers33/hass-melcloud-coordinator/actions/workflows/hacs.yml)

Custom Home Assistant integration for MELCloud (Mitsubishi Electric) with improved architecture using a DataUpdateCoordinator pattern.

## Features

- **Coordinator-based updates**: Uses Home Assistant's DataUpdateCoordinator for efficient, centralized data polling
- **Configurable polling interval**: Adjust the update frequency (1-60 minutes) via options flow
- **Multi-device support**: Supports both Air-to-Air (ATA) and Air-to-Water (ATW) devices
- **Zone support**: Full support for ATW zone devices
- **Climate control**: Temperature, HVAC mode, fan speed, and vane position control
- **Sensors**: Room temperature, outside temperature, tank temperature, energy consumption
- **Water heater**: Control for ATW water heating functionality
- **Diagnostics**: Built-in diagnostics support for troubleshooting

## Installation

### HACS (Recommended)

1. Open HACS in your Home Assistant instance
2. Click on "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add the URL: `https://github.com/divers33/hass-melcloud-coordinator`
6. Select category: "Integration"
7. Click "Add"
8. Search for "MELCloud" and install

### Manual Installation

1. Download the latest release zip file
2. Extract the `custom_components/melcloud` folder to your Home Assistant `custom_components` directory
3. Restart Home Assistant

## Configuration

1. Go to Settings > Devices & Services
2. Click "Add Integration"
3. Search for "MELCloud"
4. Enter your MELCloud credentials (email and password)

### Options

After setup, you can configure:
- **Update interval**: How often to poll MELCloud for updates (1-60 minutes, default: 15)

## Supported Devices

- **Air-to-Air (ATA)**: Heat pumps, air conditioners
- **Air-to-Water (ATW)**: Heat pumps with water heating and zone control

## Platforms

| Platform | Description |
|----------|-------------|
| Climate | HVAC control (temperature, mode, fan, vanes) |
| Sensor | Temperature sensors, energy consumption |
| Water Heater | ATW water heating control |

## Services

### `melcloud.set_vane_horizontal`
Set horizontal vane position for ATA devices.

### `melcloud.set_vane_vertical`
Set vertical vane position for ATA devices.

## Requirements

- Home Assistant 2024.1.0 or newer
- pymelcloud library (automatically installed)

## Credits

This integration is based on the official Home Assistant MELCloud integration with improvements for better performance and reliability using the coordinator pattern.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
