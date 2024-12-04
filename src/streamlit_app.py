import streamlit as st
from analyzer import analyze_pixel_art
from processor import reconstruct_pixel_art
import os
import json
from PIL import Image

st.title('Pixel Art Analyzer')

# File uploader
uploaded_file = st.file_uploader("Choose an image file", type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    # Create a temporary file to process
    with open('temp_image.jpg', 'wb') as f:
        f.write(uploaded_file.getvalue())
    
    # Process the image
    try:
        result = analyze_pixel_art('temp_image.jpg')
        
        # Display original and reconstructed images
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Original Image")
            st.image(uploaded_file)
            
        with col2:
            st.subheader("Reconstructed Image")
            reconstructed = reconstruct_pixel_art(result)
            st.image(reconstructed)
        
        # Display analysis results
        st.subheader("Analysis Results")
        st.write(f"Original dimensions: {result['analysis']['original_dimensions']}")
        st.write(f"Grid dimensions: {result['analysis']['grid_dimensions']}")
        st.write(f"Total blocks: {result['analysis']['total_blocks']}")
        st.write(f"Unique colors: {result['analysis']['unique_colors']}")
        
        # Display color usage
        st.subheader("Color Usage")
        for color_str, count in result['analysis']['color_usage'].items():
            color = eval(color_str)  # Convert string tuple to actual tuple
            st.markdown(
                f'<div style="background-color: rgb{color}; width: 20px; height: 20px; display: inline-block; margin-right: 10px;"></div>'
                f'RGB{color}: {count} blocks',
                unsafe_allow_html=True
            )
        
        # Download buttons
        st.subheader("Download Results")
        
        # Save reconstructed image
        reconstructed.save('reconstructed.jpg')
        with open('reconstructed.jpg', 'rb') as f:
            st.download_button(
                "Download Reconstructed Image",
                f,
                file_name="reconstructed.jpg",
                mime="image/jpeg"
            )
        
        # Save and offer JSON downloads
        pixel_data = {
            'metadata': result['metadata'],
            'pixels': {coord: list(color) for coord, color in result['pixels'].items()}
        }
        
        st.download_button(
            "Download Pixel Data (JSON)",
            json.dumps(pixel_data, indent=2),
            file_name="pixel_data.json",
            mime="application/json"
        )
        
        st.download_button(
            "Download Analysis (JSON)",
            json.dumps(result, indent=2, default=str),
            file_name="analysis.json",
            mime="application/json"
        )
        
    except Exception as e:
        st.error(f"Error processing image: {str(e)}")
    
    # Cleanup
    if os.path.exists('temp_image.jpg'):
        os.remove('temp_image.jpg')
    if os.path.exists('reconstructed.jpg'):
        os.remove('reconstructed.jpg') 