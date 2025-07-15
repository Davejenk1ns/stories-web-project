# Stories Web Project

A web project that displays stories and photos, with both a simple web interface and a Django CMS backend.

## Project Overview

This project consists of two main components:
1. A simple web interface for viewing stories and photos
2. A Django CMS for managing stories and photos content

## Running the Web Interface

### Option 1: Using the Shell Script (Recommended)

The easiest way to run the web interface is using the provided shell script:

```bash
# Make sure the script is executable (only needed once)
chmod +x run.sh

# Run the server
./run.sh
```

### Option 2: Using Python Directly

You can also run the server directly with Python:

```bash
python3 -m http.server 8000
```

### Option 3: Using npm (if installed)

If you have Node.js and npm installed:

```bash
npm run start
# OR
npm run dev
```

After starting the server with any of these methods:
1. Open your browser to http://localhost:8000
2. You should see the web project running

## Running the Django CMS

To run the Django CMS:

```bash
# Navigate to the stories_cms directory
cd stories_cms

# Run the Django development server
python manage.py runserver
```

Then open your browser to http://localhost:8000/admin to access the admin interface.

## Project Structure

### Web Interface
- `index.html` - Main HTML file
- `css/styles.css` - CSS styles for the project
- `package.json` - Project configuration and scripts
- `run.sh` - Shell script to easily start the server
- `stories/` - Directory containing HTML files for individual stories
- `img/` - Directory containing images for the project

### Django CMS
- `stories_cms/` - Django project directory
  - `stories/` - Django app for managing stories
  - `photos/` - Django app for managing photos
  - `templates/` - HTML templates for the CMS
  - `import_stories.py` - Script for importing stories into the CMS
  - `import_photos.py` - Script for importing photos into the CMS

### Utility Scripts
- `download_stories.py` - Script for downloading stories
- `download_remaining_stories.py` - Script for downloading additional stories
- `clean_stories.py` - Script for cleaning up story data

## Contributing

Feel free to submit issues or pull requests if you have suggestions for improvements or find any bugs.
