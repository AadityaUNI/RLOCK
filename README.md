# RLOCK

A streaming service info-provider web application built with Flask.  RLOCK helps you discover which streaming platforms offer your favorite movies and TV shows, and in which countries they're available! 

![Demo](https://github.com/user-attachments/assets/9d55077a-8dab-4884-864b-773802346214)

## Features

- **Auto-detect Location** - Automatically detects your country to show relevant streaming options
- **Search by Title** - Find streaming availability for any movie or TV show
- **Regional Search** - Search for content availability in specific countries
- **Multiple Streaming Types** - View subscription, rental, and purchase options
- **Direct Links** - Get direct links to watch content on streaming platforms
- **Feedback System** - Submit feedback and improvement suggestions

## Prerequisites

Make sure you have **Python 3.x** installed on your system. 

### Required Python Packages

```bash
pip install flask
pip install flask-session
pip install python-Levenshtein
pip install requests
```

Or install all dependencies at once:

```bash
pip install flask flask-session python-Levenshtein requests
```

## Getting Started

1. **Clone the repository:**
   ```bash
   git clone https://github.com/AadityaUNI/RLOCK.git
   cd RLOCK
   ```

2. **Install dependencies:**
   ```bash
   pip install flask flask-session python-Levenshtein requests
   ```

3. **Navigate to the project directory:**
   ```bash
   cd project
   ```

4. **Run the application:**
   ```bash
   flask run
   ```
   
   Or alternatively: 
   ```bash
   python app.py
   ```

5. **Open your browser** and navigate to: 
   ```
   http://127.0.0.1:5000
   ```

## Project Structure

```
RLOCK/
├── README.md
└── project/
    ├── app.py              # Main Flask application
    ├── Feedback.txt        # User feedback storage
    ├── static/
    │   └── styles.css      # Custom CSS styles
    ├── templates/
    │   ├── layout.html     # Base template
    │   ├── index.html      # Home page
    │   ├── about.html      # About & feedback page
    │   ├── search.html     # Search results
    │   ├── searchadv.html  # Advanced search form
    │   ├── searched.html   # Advanced search results
    │   ├── searchp.html    # Regional search form
    │   ├── searchedp.html  # Regional search results
    │   ├── error.html      # Error page
    │   └── thanks.html     # Feedback confirmation
    └── flask_session/      # Session storage
```

## Dependencies

| Package | Description |
|---------|-------------|
| `flask` | Web framework |
| `flask-session` | Server-side session management |
| `python-Levenshtein` | Fuzzy string matching for title search |
| `requests` | HTTP library for API calls |

## APIs Used

- **IMDB API** - For movie/show search and metadata
- **Streaming Availability API** - For streaming platform information

## Requirements

- **Python 3.x**
- **pip** (Python package manager)
- Internet connection (for API calls)
