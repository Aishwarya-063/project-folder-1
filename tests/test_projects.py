from urllib.parse import urlparse

import pytest

import DAL


def test_projects_page_shows_seeded_projects(client_seeded):
    resp = client_seeded.get("/projects")
    assert resp.status_code == 200
    html = resp.get_data(as_text=True)

    # Seeded titles present
    assert "Real-Time Geofencing System for Airport Ground Vehicle Safety" in html
    assert "Analysis of Skin Diseases using Transform-based Techniques" in html


def test_projects_page_empty_state(client_empty):
    resp = client_empty.get("/projects")
    assert resp.status_code == 200
    html = resp.get_data(as_text=True)
    assert "No projects yet." in html


def test_add_project_flow(client_empty):
    # Add a project
    form = {
        "title": "Test Project",
        "description": "A sample project for testing.",
        "image_file_name": "test.png",
    }
    post = client_empty.post("/projects/new", data=form, follow_redirects=False)
    assert post.status_code in (301, 302)

    # Redirect target should be /projects
    loc = post.headers.get("Location", "")
    assert "/projects" in urlparse(loc).path

    # Follow and verify it renders the new project
    page = client_empty.get("/projects")
    assert page.status_code == 200
    html = page.get_data(as_text=True)
    assert "Test Project" in html
    assert "A sample project for testing." in html

    # DB should contain exactly 1 project
    assert DAL.count_projects() == 1


@pytest.mark.parametrize(
    "page,endpoint_path",
    [
        ("projects.html", "/projects"),
        ("index.html", "/"),
    ],
)
def test_legacy_redirects(client_seeded, page, endpoint_path):
    r = client_seeded.get(f"/templates/{page}")
    assert r.status_code in (301, 302)
    loc = r.headers.get("Location", "")
    # Ensure redirect points to the correct endpoint
    assert urlparse(loc).path == endpoint_path

