# Pixel Art Analyzer

A tool for analyzing and reconstructing pixel art images. Upload an image to get detailed color analysis, grid information, and a reconstructed version of the image.

## Features
- Image analysis showing dimensions and color usage
- Side-by-side comparison of original and reconstructed images
- Color palette visualization
- Downloadable results (reconstructed image, analysis data, pixel data)

## Setup and Running

1. Clone the repository:   ```bash
   git clone https://github.com/hellolucient/depixelator.git
   cd depixelator   ```

2. Create and activate virtual environment:   ```bash
   python3 -m venv venv
   source venv/bin/activate   ```

3. Install requirements:   ```bash
   pip install -r requirements.txt   ```

## Running the App

1. Open terminal
2. Navigate to project directory:   ```bash
   cd /Users/trentmunday/depixelator   ```

3. Activate virtual environment:   ```bash
   source venv/bin/activate   ```

4. Run the Streamlit app:   ```bash
   streamlit run src/streamlit_app.py   ```

The app will automatically open in your default web browser.

To stop the app, press Ctrl+C in the terminal.