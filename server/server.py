from flask import Flask
from flask import jsonify
from flask import Response
import gphoto2 as gp
import time
import io

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


@app.after_request
def after_request(response):  # Handle CORS
    headers = response.headers
    headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/set-config-item')
def set_config_item(request):
    # Get the camera
    camera = get_camera()
    if (camera == None):
        return 'The camera is not connected', 500

    # Get the config
    config = camera.get_config()

    widget = gp.gp_widget_get_child_by_name(config, 'iso')


@app.route('/get-config-item/<name>')
def get_config_item(name):
    # Get the camera
    camera = get_camera()
    if (camera == None):
        return 'The camera is not connected', 500

    # Get the config
    config = camera.get_config()

    # Get the widget
    OK, widget = gp.gp_widget_get_child_by_name(config, name)
    w_val = widget.get_value()
    w_type = widget.get_type()
    OK, choices = gp.gp_widget_get_choices(widget)

    return jsonify(
        value=w_val,
        choices=choices,
        type=w_type,
    )


@app.route('/capture-preview')
def app_capture_preview():
    # Get the camera
    camera = get_camera()
    if (camera == None):
        return 'The camera is not connected', 500

    # Determine the image format
    config = gp.check_result(gp.gp_camera_get_config(camera))
    OK, image_format = gp.gp_widget_get_child_by_name(config, 'imagequality')
    if OK >= gp.GP_OK:
        value = gp.check_result(gp.gp_widget_get_value(image_format))
        print('The value is ', value)

    # Capture a preview image and grab the file data
    camera_file = camera.capture_preview()
    file_data = gp.check_result(gp.gp_file_get_data_and_size(camera_file))

    # Process the data
    data = memoryview(file_data)
    print(type(data), len(data))

    # Done with the camera
    camera.exit()

    return Response(data.tobytes(), mimetype='image/x-nikon-nef')
    # return make_response(True)


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
