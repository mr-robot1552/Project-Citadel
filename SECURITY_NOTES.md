# Security Notes (Portfolio Repository)

This repository contains an academic capstone implementation that integrates Raspberry Pi GPIO, sensors, and a local visualization interface. To keep the public source code safe and employer-ready, any authentication values and sensitive runtime settings are configured outside the codebase.

## No Hardcoded Secrets
- PINs, passphrases, and similar authorization values are not embedded in source files.
- When authorization is required for a demonstration, values are provided at runtime using environment variables.

## Network Exposure Defaults
- Network services default to safe/local settings where possible.
- Host/port values are configurable to support controlled demonstrations.

## Example Runtime Configuration
The following examples illustrate configuration patterns used across modules:

- Room 2 (authorization PIN):
  - `ROOM2_REQUIRE_PIN`
  - `ROOM2_AUTH_PIN`

- Room 3 (disarm passphrase):
  - `ROOM3_REQUIRE_PASSPHRASE`
  - `ROOM3_DISARM_PASSPHRASE`

- Radar (controller host/port and optional password gate):
  - `RADAR_TCP_HOST`
  - `RADAR_TCP_PORT`
  - `RADAR_REQUIRE_PASSWORD`
  - `RADAR_PASSWORD`

These settings are optional and may be disabled for local-only demonstrations.
