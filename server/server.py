from flask import Flask
from flask import jsonify
from flask import Response
from flask import request
import gphoto2 as gp
import time
import io

global CAMERA

PORT = 8080
CAMERA = None

app = Flask(__name__)


@app.after_request
def after_request(response):  # Handle CORS
    headers = response.headers
    headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/set-config-item/<name>', methods=['POST'])
def set_config_item(name):
    # It's not connected
    if CAMERA == None:
        return 'The camera is not connected', 500

    value = request.data.decode('UTF-8')

    # Get the config
    config = CAMERA.get_config()

    # Get the widget
    OK, widget = gp.gp_widget_get_child_by_name(config, name)
    if OK != gp.GP_OK:
        return 'There are no widgets with the name of ' + name, 500

    OK = gp.gp_widget_set_value(widget, value)
    if OK != gp.GP_OK:
        return 'Could not set the value', 500

    OK = gp.gp_camera_set_config(CAMERA, config)
    if OK != gp.GP_OK:
        return 'Could not set the config', 500

    return 'Value updated successfully'


@app.route('/get-config-item/<name>')
def get_config_item(name):
    # It's not connected
    if CAMERA == None:
        return 'The camera is not connected', 500

    # Get the config
    config = CAMERA.get_config()

    # Get the widget
    OK, widget = gp.gp_widget_get_child_by_name(config, name)
    if OK != gp.GP_OK:
        return 'There are no widgets with the name of ' + name, 500

    choices = []

    # Some config may not have choices
    try:
        # Get the value and the choices
        w_val = widget.get_value()
        choices_raw = widget.get_choices()

        # Format choices
        for c in choices_raw:
            choices.append(c)
    except:
        pass

    # Return formatted
    return jsonify(
        value=w_val,
        choices=choices
    )


@app.route('/capture-preview')
def app_capture_preview():
    # It's not connected
    if CAMERA == None:
        return 'The camera is not connected', 500

    # Determine the image format
    config = gp.check_result(gp.gp_camera_get_config(CAMERA))
    OK, image_format = gp.gp_widget_get_child_by_name(config, 'imagequality')
    if OK >= gp.GP_OK:
        value = gp.check_result(gp.gp_widget_get_value(image_format))
        print('The value is ', value)

    # Capture a preview image and grab the file data
    camera_file = CAMERA.capture_preview()
    file_data = gp.check_result(gp.gp_file_get_data_and_size(camera_file))

    # Process the data
    data = memoryview(file_data)
    print(type(data), len(data))

    return Response(data.tobytes(), mimetype='image/x-nikon-nef')


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


# Start the web server
if __name__ == '__main__':
    CAMERA = get_camera()
    app.run(host='0.0.0.0', port=PORT, threaded=False)
