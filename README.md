# Personal Portfolio Website

A Flask-based personal portfolio website for Aishwarya Kondaparthi featuring dynamic project management with SQLite database integration.

## Features

- **Multi-page Portfolio**: Home, About, Resume, Projects, and Contact pages
- **Dynamic Project Management**: Database-backed projects with image support
- **Responsive Design**: Mobile-friendly interface with modern CSS
- **Form Validation**: Contact form with comprehensive client-side validation
- **Database Integration**: SQLite with custom Data Access Layer (DAL)
- **Image Management**: Automatic image detection and fallback handling


## Project Structure
portfolio-website/
├── app.py # Main Flask application
├── DAL.py # Data Access Layer for database operations
├── projects.db # SQLite database (auto-generated)
├── requirements.txt # Python dependencies
├── static/
│ ├── styles.css # Main stylesheet
│ └── images/ # Project images and assets
├── templates/ # Jinja2 HTML templates
│ ├── index.html # Home page
│ ├── about.html # About Me page
│ ├── resume.html # Resume page
│ ├── projects.html # Projects listing (database-backed)
│ ├── add_project.html # Add project form
│ ├── contact.html # Contact form
│ └── thankyou.html # Thank you page
└── README.md # Project documentation


## Database Schema

The `projects` table contains:
- `id` (INTEGER, Primary Key, Auto-increment)
- `Title` (TEXT, NOT NULL)
- `Description` (TEXT, NOT NULL)
- `ImageFileName` (TEXT, NOT NULL)
- `CreatedAt` (DATETIME, DEFAULT CURRENT_TIMESTAMP)

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step-by-Step Installation

1. **Clone or download the project files**

2. **Create and activate a virtual environment** (recommended):
   
   # Windows
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1

   # macOS/Linux
   python3 -m venv .venv
   source .venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Run the application:
python app.py

Access the website:
Open your browser and navigate to http://127.0.0.1:5000/

Usage
Viewing Projects:
Navigate to the "Projects" page to see all projects from the database

Projects are displayed in a table with titles, descriptions, and images

Adding New Projects:
Go to "Add Projects" from the navigation menu

Fill in the project details:

Title: Project name

Description: Detailed project description

Image File Name: Name of the image file (must be in static/images/)

Click "Save Project" to add to the database

The new project will immediately appear on the Projects page

Managing Images:
Place project images in the static/images/ folder

Reference images by filename in the add project form

Supported formats: PNG, JPG, JPEG, GIF

The system includes fallback handling for missing images

Dependencies:
Flask: Web framework

SQLite3: Database (included with Python)

See requirements.txt for complete dependency list.

Development Notes:
This project was developed with AI assistance using Cursor, with significant customization and enhancement. Key development insights:

AI excelled at generating boilerplate code and basic structures

Human oversight was crucial for database design and business logic

The Data Access Layer pattern improved code maintainability

Template inheritance simplified consistent UI across pages

File Descriptions:
app.py: Main Flask application with routes and database initialization

DAL.py: Data Access Layer handling all database operations

templates/: HTML templates with Jinja2 syntax for dynamic content

static/styles.css: Comprehensive styling with responsive design

projects.db: SQLite database (created automatically on first run)

Troubleshooting:
Common Issues
Database not initializing:

Delete projects.db and restart the application

Check file permissions in the project directory

Images not displaying:

Verify images are in static/images/ folder

Check filename spelling in the database

Ensure image file extensions are correct

Import errors:

Verify virtual environment is activated

Run pip install -r requirements.txt again

Reset Database
To start with a fresh database:

# Delete existing database
rm projects.db  # Linux/macOS
del projects.db  # Windows

# Restart application:
python app.py