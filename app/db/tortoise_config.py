from typing import List

from app.config.settings import settings

MODELS_MODULES: List[str] = ["app.db.models"]  # noqa: WPS407

TORTOISE_CONFIG = {
    "connections": {
        "default": settings.get_asyncpg_conn_string,
    },
    "apps": {
        "models": {
            "models": MODELS_MODULES,
            "default_connection": "default",
        },
    },
}
