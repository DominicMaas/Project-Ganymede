# Application to run on raspberry pi, the following are requried to be installed:
# libgphoto2-dev

# Phython Setup
# 1. sudo apt-get install python3-pip
# 2. sudo pip3 install pipenv

import gphoto2 as gp
import time


def detect_camera():
    # Setup the context
    context = gp.Context()

    # Run in a loop until we have a camera
    while True:
        try:
            # Attempt to get the camera
            camera = gp.Camera()
            camera.init(context)

            # Return the camera
            print("Camera connected!")
            return camera
        except:
            # If there was an error, wait 10 seconds and try again
            print("Camera not connected to device, trying again in 10 seconds...")
            time.sleep(10)


# Try get the camera
camera = detect_camera()
text = camera.get_summary()
print('Summary')
print('=======')
print(str(text))
camera.exit()
