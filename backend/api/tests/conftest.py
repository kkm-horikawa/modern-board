"""pytest configuration and global fixtures."""

import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    """DRF API client fixture."""
    return APIClient()
