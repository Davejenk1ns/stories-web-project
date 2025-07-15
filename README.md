# Web Project

A simple web project that can be run on localhost.

## Running the Project

### Option 1: Using the Shell Script (Recommended)

The easiest way to run the project is using the provided shell script:

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

## Project Structure

- `index.html` - Main HTML file
- `css/styles.css` - CSS styles for the project
- `package.json` - Project configuration and scripts
- `run.sh` - Shell script to easily start the server
