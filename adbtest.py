import time
from ppadb.client import Client

def sendevent(device, input_device, events):
    """
    Sends raw touch events to the specified input device.
    """
    for event in events:
        cmd = f"sendevent {input_device} {event[0]} {event[1]} {event[2]}"
        print(cmd)  # For debugging
        device.shell(cmd)

def rc2xy(x, y):
    """
    This function converts logical screen coordinates (x, y) to raw touch event coordinates.
    Modify this based on the actual screen resolution and your coordinate system.
    """
    return x, y  # No transformation in this case, adjust as necessary.

def raw_swipe(device, start_x, start_y, end_x, end_y, input_device="/dev/input/event3"):
    """
    Sends raw touch events to simulate a swipe gesture from (start_x, start_y) to (end_x, end_y).
    """
    events = []
    tracking_id = 1

    # Start touch (first point)
    events.append((3, 0x39, tracking_id))  # Tracking ID
    events.append((3, 0x35, start_x))      # X coordinate
    events.append((3, 0x36, start_y))      # Y coordinate
    events.append((0, 0, 0))               # SYN_REPORT

    # Move touch to the end point
    events.append((3, 0x35, end_x))        # Update X coordinate
    events.append((3, 0x36, end_y))        # Update Y coordinate
    events.append((0, 0, 0))               # SYN_REPORT

    # End touch (release the touch)
    events.append((3, 0x39, -1))           # Release touch
    events.append((0, 0, 0))               # SYN_REPORT

    # Send the events to the device
    sendevent(device, input_device, events)

def applySwipe(device):
    """
    Applies a swipe from (500, 1000) to (500, 200).
    """
    start_x, start_y = 500, 1000
    end_x, end_y = 500, 200
    raw_swipe(device, start_x, start_y, end_x, end_y, input_device="/dev/input/event5")

# Connect to the ADB device
adb = Client(host="127.0.0.1", port=5037)
devices = adb.devices()
if not devices:
    print("No device attached.")
    quit()

device = devices[0]  # Use the first connected device

device.shell('input touchscreen swipe 500 1000 500 200')

# Perform the swipe
# applySwipe(device)

# Wait for a bit to observe the swipe
time.sleep(1)



