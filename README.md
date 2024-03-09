# Zero-Latency - Game Latency Testing with Raspberry Pi Zero

## Overview

This tool is designed to measure the relative latency of specific actions within the game Cyberpunk 2077, focusing on the delay between initiating an action (such as shooting a weapon) and observing the result on-screen. It utilizes a Raspberry Pi Zero 2W, configured as a USB Human Interface Device (HID), to simulate keyboard and mouse inputs. An external light sensor connected to the Raspberry Pi detects changes in screen brightness as an indicator of action completion.

This tool is intended for testing RELATIVE latency. Its purpose is to compare one software configuration to another on the same hardware or to test network streaming across multiple hardware configurations. It is not designed for comparing the physical configurations of different setups or for benchmarking against a standard. Variations in hardware response time, screen response time, light sensor sensitivity, and even screen brightness can affect testing results, so it's recommended to conduct all tests on the same monitor without moving the sensor.

This guide assumes the user knows how to set up a Raspberry Pi, connect digital light sensors, set up LEDs with resistors, and can read a Python script and install appropriate Python libraries.

## Requirements

- Raspberry Pi Zero 2W set up with Raspberry Pi OS available over SSH and configured as a USB HID device.
- Digital light sensor and optional LED connected to the Raspberry Pi.
- `gpiozero` library installed on the Raspberry Pi. `/dev/hidg0` configured as keyboard and `/dev/hidg0` configured as mouse, with both writeable by the user.

## Setup

1. **Connect Hardware**: Connect your LED to GPIO 3 and your digital light sensor to GPIO 17 on your Raspberry Pi Zero 2W.
2. **Prepare Raspberry Pi**: Ensure your Raspberry Pi Zero 2W is configured to act as a USB HID device.
3. **Game Setup**: Open Cyberpunk 2077 and navigate to the scene or action you wish to measure latency for.

## Calibration and Troubleshooting

- **Light Sensor Calibration**: Position the light sensor to accurately detect changes in screen brightness. Adjust its sensitivity or positioning based on your monitor and ambient light conditions. For Cyberpunk 2077, configure it to detect a muzzle flash in-game.
- **USB HID Configuration**: Confirm that the Raspberry Pi Zero 2W is properly set up as a USB HID device and recognized by the PC running Cyberpunk 2077. Various guides and projects like PiKVM and BADUSB offer extensive information on using a Pi Zero as a USB HID device.
- **Mock Mode**: Test script behavior without actual typing or clicking. In mock mode, the LED on GPIO3 illuminates upon sending the fire command and turns off when light is detected. You may use an LED flashlight to trigger the LED detection manually.
- **Internal Latency Testing**: Directly pointing the light detector at the LED in mock mode allows for measuring the latency of the light sensor function alone.

## Features

- **Behavior and Error Trapping**: Defaults are set for Cyberpunk 2077 controls, with shot delays and reload behavior tailored for a revolver-type weapon. Revolvers were chosen for its bright muzzle flash and absence of full-auto firing. Upon execution, the script runs a prep function to ready the weapon for measurement—loading the weapon in Slot 1, firing a few rounds, and reloading. Weapon behavior, magazine size, and reloading times are configurable.

- **Data Collection**: Data points that are unrealistically slow or fast are configurable and can be disregarded. The script times out if no light is detected for several seconds, indicating a missed "fire" command or missed light detection by the sensor. See `make-graphs.py` for an example of parsing the graph data.

## Usage

1. **Starting the Tool**:
   - Configure the Raspberry Pi for WiFi and SSH access, install Python3 and required libraries, and upload this script. Some Python libraries work better when installed with `apt` from the Raspberry Pi OS repositories. SSH is necessary because the Pi Zero's USB data port is also the USB HID port. This tool is best used when connected via SSH from another machine.
   - Open a terminal and navigate to the directory containing the script.
   - Execute the script with the command:
     ```
     python3 run-tests.py
     ```

2. **Command-line Arguments**:
   - `--tests` (int): Number of tests to run (default: 10).
   - `--weapon` (int): Which weapon slot to use for testing (1, 2, or 3; default: 1).
   - `--mag-size` (int): Number of shots before needing to reload (default: 10).
   - `--reload-speed` (float): Amount of time needed for reload in seconds (default: 2.5).
   - `--shot-delay` (float): Delay in seconds after each shot (default: 1.5).
   - `--too-slow` (float): Threshold in ms above which response is considered too slow (default: 1000).
   - `--too-fast` (float): Threshold in ms below which response is considered too fast (default: 20).
   - `--log` (string): Enable logging of results to a CSV file. Optionally specify the log name. Without value, uses current timestamp.
   - `--mock`: Run the program in mock mode without sending actual keyboard or mouse events.

3. **Operation**:
   - The tool will automatically select the weapon, perform the prep cycle, and begin the latency measurement tests.
   - Visual and textual feedback will be provided in the console for each test attempt.

4. **Reviewing Results**:
   - Upon completion, the tool generates a report summarizing the tests, including average latency, number of tests completed, and any errors encountered.
   - If logging was enabled, detailed results for each test are saved to the specified CSV file.