from falcon import testing
import pytest

import app


@pytest.fixture()
def client():
    """Create falcon testing client to send requests"""
    return testing.TestClient(app.api)

