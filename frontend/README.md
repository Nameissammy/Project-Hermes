# Project Hermes Frontend

A simple Streamlit-based web interface for the Project Hermes travel planning system.

## Features

- User-friendly interface for travel planning
- Example queries for quick testing
- Detailed display of travel plans with tabs for different sections
- Real-time feedback on query confidence

## Prerequisites

- Python 3.10+
- Streamlit
- Requests

## Installation

1. Create a virtual environment and install dependencies using uv:

   ```bash
   cd frontend

   # Install uv if you don't have it
   pip install uv

   # Create and activate a virtual environment
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate

   # Install dependencies using pyproject.toml
   uv pip install -e .
   ```

   Alternatively, using pip:

   ```bash
   pip install streamlit requests python-dotenv
   ```

2. Set up environment variables:

   ```bash
   # Copy the example environment file
   cp .env.example .env

   # Edit .env if your API is not running on localhost:8001
   # API_HOST=http://localhost:8001
   ```

## Running the Frontend

1. Start the backend API server first (from the backend directory):

   ```
   cd ../backend
   python run_server.py
   ```

2. Start the Streamlit app:
   ```
   cd frontend
   streamlit run app.py
   ```

The app will be available at http://localhost:8501

## Usage

1. Select a pre-defined example query or enter your own travel query
2. Click "Generate Travel Plan"
3. View the detailed travel plan with tabs for:
   - Overview
   - Itinerary
   - Safety information
   - Budget breakdown
   - Raw JSON data
