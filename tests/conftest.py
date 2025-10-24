import importlib
import sys
from pathlib import Path

import pytest

# Ensure repository root is importable in all environments (CI, IDEs)
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


@pytest.fixture()
def app_seeded(tmp_path, monkeypatch):
    """Create the Flask app with a fresh, seeded temp DB."""
    # Ensure DAL uses a temp DB file per-test
    import DAL as dal
    monkeypatch.setattr(dal, "_DB_PATH", Path(tmp_path) / "projects_test.db", raising=False)

    # Create app (this will call DAL.init_db and seed initial projects)
    import app as app_mod
    application = app_mod.create_app()
    yield application


@pytest.fixture()
def app_empty(tmp_path, monkeypatch):
    """Create the Flask app with a fresh temp DB and no seed data."""
    import DAL as dal
    monkeypatch.setattr(dal, "_DB_PATH", Path(tmp_path) / "projects_test.db", raising=False)

    import app as app_mod
    # Prevent seeding for this app instance
    monkeypatch.setattr(app_mod, "_seed_initial_projects_if_needed", lambda: None, raising=True)
    application = app_mod.create_app()
    yield application


@pytest.fixture()
def client_seeded(app_seeded):
    with app_seeded.test_client() as c:
        yield c


@pytest.fixture()
def client_empty(app_empty):
    with app_empty.test_client() as c:
        yield c
