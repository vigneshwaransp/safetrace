from app.core.config import Settings


def test_settings_initialization():
    settings = Settings()
    assert settings.PROJECT_NAME == "SafeTrace"
    assert settings.API_V1_STR == "/api/v1"
    assert settings.PDQ_THRESHOLD_HIGH == 20
    assert settings.PDQ_THRESHOLD_MEDIUM == 31
    assert settings.storage_path.exists()


def test_cors_origins_parsing():
    settings = Settings(BACKEND_CORS_ORIGINS=["http://localhost:3000"])
    assert "http://localhost:3000" in settings.BACKEND_CORS_ORIGINS
