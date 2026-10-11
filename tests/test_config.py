import os

import pytest

from src.config import load_env


@pytest.fixture
def env_files(tmp_path, monkeypatch):
    (tmp_path / ".env.local").write_text("DynamoDbUrl=http://localhost:8000\n")
    (tmp_path / ".env.dev").write_text("AWS_PROFILE=dev\n")
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("DynamoDbUrl", raising=False)
    monkeypatch.delenv("AWS_PROFILE", raising=False)
    yield
    os.environ.pop("DynamoDbUrl", None)
    os.environ.pop("AWS_PROFILE", None)


def test_load_env_defaults_to_local(env_files, monkeypatch):
    monkeypatch.delenv("APP_ENV", raising=False)
    load_env()
    assert os.environ["DynamoDbUrl"] == "http://localhost:8000"
    assert "AWS_PROFILE" not in os.environ


def test_load_env_uses_app_env(env_files, monkeypatch):
    monkeypatch.setenv("APP_ENV", "dev")
    load_env()
    assert os.environ["AWS_PROFILE"] == "dev"
    assert "DynamoDbUrl" not in os.environ
