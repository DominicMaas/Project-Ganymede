from flask import Flask
from flask import jsonify
import gphoto2 as gp
import time

PORT = 8080


def get_camera():  # Function that attempts to get the camera
    # Setup the context
    context = gp.Context()

    try:
        # Attempt to get the camera
        camera = gp.Camera()
        camera.init(context)

        # Return the camera
        print("Camera connected!")
        return camera
    except:
        print('The camera is not connected')
        return None


def make_response(isError, response=''):  # Wrapper around generating responses
    return jsonify(
        error=isError,
        response=response,
    )



# ENTER PROGRAM
app = Flask(__name__)

@blueprint.after_request
def after_request(response): # Handle CORS
    headers = response.headers
    headers['Access-Control-Origin'] = '*'
    return response


@app.route('/capture-preview')
def app_capture_preview():
    # Get the camera
    camera = get_camera()
    if (camera == None):
        return make_response(False, 'The camera is not connected')

    camera.capture_preview()
    return make_response(True)


def build_config(child):
    config = {}

    label = '{}'.format(child.get_name())

    if child.get_type() == gp.GP_WIDGET_SECTION:
        res = []

        for c_inner in child.get_children():
            res.append(build_config(c_inner))

        config[label] = res
    else:
        config[label] = '{}'.format(child.get_value())

    return config


@app.route('/get-config')
def app_get_config():
    # Get the camera
    camera = get_camera()
    if (camera == None):
        return make_response(False, 'The camera is not connected')

    config = camera.get_config()

    res = []  # The response

    # Build the config
    for child in config.get_children():
        res.append(build_config(child))

    return make_response(False, res)


# Start the web server
app.run(host='0.0.0.0', port=PORT)
