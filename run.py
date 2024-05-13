from appointment_app import create_app
from appointment_app.config import ConfigDev


if __name__ == "__main__":
    app = create_app(ConfigDev())
    app.run(port=5009, debug=True)
