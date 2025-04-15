from dotenv import load_dotenv

import os


load_dotenv()



TORTOISE_ORM = {
    "connections": {
         "default": "mysql://monitoring:SI17j7MfziA9YHh@192.168.130.29:3306/monitoring"
    },
    "apps": {
        "models": {
            "models": ["app.models", "aerich.models"],
            "default_connection": "default",
        },
    },
    "use_tz": False,
    "timezone": "UTC"
}
