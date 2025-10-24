# app.py
from flask import Flask, render_template, request, redirect, url_for
from pathlib import Path
import re
import DAL  # local data access layer


def _find_image_filename(keyword: str) -> str | None:
    """
    Look inside static/images for the first file whose name contains the keyword.
    Returns the file name (not full path) or None.
    """
    images_dir = Path("static") / "images"
    if not images_dir.exists():
        return None
    pattern = re.compile(re.escape(keyword), re.IGNORECASE)
    for p in images_dir.iterdir():
        if p.is_file() and pattern.search(p.name):
            return p.name
    return None


def _seed_initial_projects_if_needed():
    """
    Ensure Airport (Project 1) and Skin Diseases (Project 2) exist in DB.
    Only runs if the table is empty.
    """
    if DAL.count_projects() > 0:
        return

    # Try to auto-detect image filenames from static/images
    airport_img = _find_image_filename("Project_1_image1.png") or "Project_1_image1.png"
    skin_img = _find_image_filename("Project_2_image2.png") or "Project_2_image2.png"

    DAL.insert_project(
        title="Real-Time Geofencing System for Airport Ground Vehicle Safety",
        description=(
         "Developed and published a real-time ground vehicle monitoring system using GPS and geofencing technology, enabling location tracking and automated alerts to prevent collisions between support vehicles and aircraft in airport environments."
        ),
        image_file_name="Project_1_image2.png",
    )

    DAL.insert_project(
        title="Analysis of Skin Diseases using Transform-based Techniques",
        description=(
            "Utilized MATLAB, Image Processing methods and Transform methods like FFT and DCT for classification of diseases detected in skin images. Developed algorithms for automated detection and analysis of dermatological conditions."
        ),
        image_file_name="Project_2_image2.png",
    )


def create_app():
    app = Flask(__name__)

    # --- DB bootstrap + seed (NEW)
    DAL.init_db()
    Path("static/images").mkdir(parents=True, exist_ok=True)  # ensure images dir exists
    _seed_initial_projects_if_needed()

    # --- Main pages (existing)
    @app.route("/")
    def home():
        return render_template("index.html")

    @app.route("/about")
    def about():
        return render_template("about.html")

    @app.route("/resume")
    def resume():
        return render_template("resume.html")

    # --- Projects (already DB-backed)
    @app.route("/projects")
    def projects():
        projects_list = DAL.get_all_projects()
        return render_template("projects.html", projects=projects_list)

    # --- Add Project form (POST inserts → redirect to /projects)
    @app.route("/projects/new", methods=["GET", "POST"])
    def add_project():
        if request.method == "POST":
            title = request.form.get("title", "")
            description = request.form.get("description", "")
            image_file_name = request.form.get("image_file_name", "")
            DAL.insert_project(title, description, image_file_name)
            return redirect(url_for("projects"))
        return render_template("add_project.html")
    
    @app.route("/add_project")
    def add_project_form():
        return render_template("add_project.html")

    # --- Contact + thank-you (existing)
    @app.route("/contact")
    def contact():
        return render_template("contact.html")

    @app.route("/thankyou")
    def thankyou():
        return render_template("thankyou.html")

    # --- Legacy redirects (optional)
    @app.route("/templates/<page>")
    def legacy(page):
        mapping = {
            "index.html": "home",
            "about.html": "about",
            "resume.html": "resume",
            "projects.html": "projects",
            "add_project.html": "add_project_form",
            "contact.html": "contact",
            "thankyou.html": "thankyou",
        }
        endpoint = mapping.get(page, "home")
        return redirect(url_for(endpoint), code=302)

    return app


if __name__ == "__main__":
    import os

    app = create_app()
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug)
