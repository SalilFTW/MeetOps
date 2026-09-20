from app.config import (
    APP_NAME,
    APP_ENV,
    GROQ_MODEL,
)


def test_app_configuration():

    assert APP_NAME == "MeetOps"
    assert APP_ENV == "development"


def test_groq_model_configuration():

    assert GROQ_MODEL
    assert isinstance(GROQ_MODEL, str)