"""Pytest configuration and fixtures for FastAPI tests."""

import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add src directory to Python path so we can import app
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from app import app


@pytest.fixture
def client():
    """
    Fixture that provides a TestClient for making requests to the FastAPI app.
    
    This fixture creates a fresh test client for each test, allowing
    tests to be isolated and independent.
    """
    return TestClient(app)
