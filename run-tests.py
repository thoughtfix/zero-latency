#!/usr/bin/env python3
import argparse
import csv
import os
import time
from datetime import datetime
from gpiozero import LED, InputDevice

# Setup argparse
parser = argparse.ArgumentParser(description="Measure game latency in Cyberpunk 2077.")
parser.add_argument("--tests", type=int, default=10, help="Number of tests to run (default: %(default)s)")
parser.add_argument("--weapon", type=int, choices=[1, 2, 3], default=1, help="Which weapon slot to use for testing. (default: %(default)s)")
parser.add_argument("--mag-size", type=int, default=10, help="Number of shots before needing to reload (default: %(default)s)")
parser.add_argument("--reload-speed", type=float, default=2.5, help="Amount of time needed for reload (default: %(default)s)")
parser.add_argument("--shot-delay", type=float, default=1.5, help="Delay in seconds after each shot (default: %(default)s)")
parser.add_argument("--too-slow", type=float, default=1000, help="Threshold in ms above which response is considered too slow (default: %(default)s)")
parser.add_argument("--too-fast", type=float, default=20, help="Threshold in ms below which response is considered too fast (default: %(default)s)")
parser.add_argument("--log", nargs='?', const=datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".csv", default=None, help="Enable logging of results to a CSV file. Optional value to specify log name. Without value, uses current timestamp.")
parser.add_argument("--mock", action="store_true", help="Run the program in mock mode without sending actual keyboard or mouse events.")
args = parser.parse_args()

# Define paths for HID devices
keyboard_hid_path = '/dev/hidg0'
mouse_hid_path = '/dev/hidg1'

# Initialize LED and sensor
led = LED(3)
sensor = InputDevice(17, pull_up=True)

# Helper functions for HID reports
def send_keyboard_command(report, mock):
    if not mock:
        with open(keyboard_hid_path, 'wb') as fd:
            fd.write(report)
    time.sleep(0.05)  # Short delay for key press
    if not mock:
        with open(keyboard_hid_path, 'wb') as fd:
            fd.write(b'\x00' * 8)  # Release key

def send_mouse_command(report, mock):
    if not mock:
        with open(mouse_hid_path, 'wb') as fd:
            fd.write(report)

# Key press simulation using specific key codes
def press_key(key_char, mock):
    key_press_map = {
        '1': b'\x00\x00\x1e\x00\x00\x00\x00\x00',  # Usage ID for '1'
        '2': b'\x00\x00\x1f\x00\x00\x00\x00\x00',  # Usage ID for '2'
        '3': b'\x00\x00\x20\x00\x00\x00\x00\x00',  # Usage ID for '3'
        'r': b'\x00\x00\x15\x00\x00\x00\x00\x00',  # Usage ID for 'r'
    }
    key_press = key_press_map.get(key_char, b'\x00' * 8)
    if args.mock:
        print("Mock mode: Simulating key press for", key_char)
    else:
        send_keyboard_command(key_press, args.mock)
    
# Simulate a left mouse click
def fire_weapon(mock):
    if args.mock:
        print("Mock mode: Simulating left mouse click")
    else:
        with open(mouse_hid_path, 'wb') as fd:
            send_mouse_command(b'\x10\x01\x00\x01\x00\x00', mock)  # Left button press
            time.sleep(0.05)
            send_mouse_command(b'\00\x00\x00\x00\x00\x00', mock)  # Release all buttons

# Implement weapon selection, reloading, firing, and logging
def select_weapon(weapon_slot, mock):
    press_key(str(weapon_slot), mock)
    time.sleep(args.reload_speed)

def reload_weapon(mock):
    press_key('r', mock)
    time.sleep(args.reload_speed)

def log_result(log_file, data_point):
    if log_file:
        with open(log_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([data_point])

# Function to check for existing log file and create a unique name if necessary
def get_unique_log_filename(base_name):
    if base_name:
        if os.path.exists(base_name):
            base_name = f"{base_name}_{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.csv"
        elif not base_name.endswith('.csv'):
            base_name += ".csv"
    return base_name

# Function to perform the preparation cycle
def prep_cycle(mock):
    print("Starting prep cycle...")
    # Select the weapon based on the user's choice
    select_weapon(args.weapon, mock)
    time.sleep(0.5)  # Wait a bit after selecting the weapon
    
    # Fire a few shots to ensure everything is set up correctly
    for _ in range(3):
        fire_weapon(mock)
        time.sleep(0.25)  # Wait between shots
    
    # Reload the weapon to start the tests with a full magazine
    reload_weapon(mock)
    time.sleep(0.5)
    print("Prep cycle complete.")


# Main testing logic
def run_latency_tests():
    start_time = time.time()  # Record the start time of the test session
    log_file = get_unique_log_filename(args.log)
    shots_available = args.mag_size
    successful_tests = 0
    consecutive_errors = 0
    total_tests_attempted = 0
    light_calibration_errors = 0
    discarded_too_fast = 0
    discarded_too_slow = 0
    timeout_errors = 0
    total_latency = 0  # Accumulator for calculating average latency

    print("Running prep cycle...")
    prep_cycle(args.mock)
    print("Prep cycle complete.")

    while successful_tests < args.tests and consecutive_errors < 5:
        total_tests_attempted += 1
        print(f"Attempt {total_tests_attempted} of {args.tests} (success {successful_tests}): ", end="")

        if sensor.is_active:
            print("Light already detected. Calibrate sensor.")
            light_calibration_errors += 1
            consecutive_errors += 1
            time.sleep(5)
            continue

        led.on()
        test_start_time = time.time()
        fire_weapon(args.mock)
        shots_available -= 1

        while not sensor.is_active and time.time() < test_start_time + 3:
            pass

        if time.time() >= test_start_time + 3:
            print("Time out waiting for light. Discarding result.")
            led.off()
            timeout_errors += 1
            consecutive_errors += 1
            continue

        led.off()
        test_end_time = time.time()

        latency_ms = (test_end_time - test_start_time) * 1000
        if args.too_fast <= latency_ms <= args.too_slow:
            print(f"Latency: {latency_ms:.2f} ms")
            log_result(log_file, latency_ms)
            total_latency += latency_ms
            successful_tests += 1
            consecutive_errors = 0
        else:
            if latency_ms > args.too_slow:
                print(f"{latency_ms:.2f} ms. Unrealistically slow. Discarding result.")
                discarded_too_slow += 1
            elif latency_ms < args.too_fast:
                print(f"{latency_ms:.2f} ms. Unrealistically fast. Discarding result.")
                discarded_too_fast += 1
            consecutive_errors += 1

        if shots_available <= 1:
            print("Reloading...")
            reload_weapon(args.mock)
            shots_available = args.mag_size

        time.sleep(args.shot_delay)

    total_time_taken = time.time() - start_time
    average_latency = total_latency / successful_tests if successful_tests else 0

    # Final report
    if successful_tests >= args.tests:
        print("\nReport Summary:")
        print(f"Completed {successful_tests} shots in {total_tests_attempted} attempted tests.")
        print(f"Light calibration errors: {light_calibration_errors} ({light_calibration_errors / total_tests_attempted * 100:.2f}%)")
        print(f"Discarded (too fast): {discarded_too_fast} ({discarded_too_fast / total_tests_attempted * 100:.2f}%)")
        print(f"Discarded (too slow): {discarded_too_slow} ({discarded_too_slow / total_tests_attempted * 100:.2f}%)")
        print(f"Timeout errors: {timeout_errors} ({timeout_errors / total_tests_attempted * 100:.2f}%)")
        print(f"Total time taken: {total_time_taken:.2f} seconds")
        print(f"Average latency: {average_latency:.2f} ms.")
    elif consecutive_errors >= 5:
        print("Test stopped due to consecutive errors.")

if __name__ == "__main__":
    run_latency_tests()
