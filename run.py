from appointment_app import create_app
from appointment_app.config import ConfigProd


if __name__ == "__main__":
    app = create_app(ConfigProd())
    app.run(port=5009, debug=True)
else:
    gunicorn_app = create_app(config=ConfigProd())
