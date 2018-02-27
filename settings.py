# The message sent when up is pressed on the joystick
email_message = 'A simple test of the email protocol'

# The Sense Hat is accurate but normally a few degrees off, put a int here to compensate for that
temprature_offset = 0

# The temperature that the system sends an alert e-mail
alert_temprature = 80

# these are the two display colors, highlight is the highlighted area and background is the background
primary = (0, 0, 255)
secondary = (0, 0, 0)

# This is the gateway to be pinged so that the internal IP can be discovered
default_gateway = '127.0.0.1'

all_settings = {
    'email_message': email_message,
    'offset': temprature_offset,
    'alert_temprature': alert_temprature,
    'primary': primary,
    'secondary': secondary,
    'default_gateway': default_gateway,
}
