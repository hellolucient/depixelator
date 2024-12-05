import streamlit as st
from analyzer import analyze_pixel_art
from processor import reconstruct_pixel_art
import os
import json
from PIL import Image

st.title('Pixel Art Analyzer')

# Multiple file uploader
uploaded_files = st.file_uploader("Choose image files", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)

if uploaded_files:
    # Create a selectbox for choosing which image to analyze
    selected_file = st.selectbox(
        "Select image to analyze",
        uploaded_files,
        format_func=lambda x: x.name
    )
    
    # Process the selected file
    try:
        # Create a temporary file to process
        with open('temp_image.jpg', 'wb') as f:
            f.write(selected_file.getvalue())
        
        # Process the image
        result = analyze_pixel_art('temp_image.jpg')
        
        # Display original and reconstructed images
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Original Image")
            st.image(selected_file)
            
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
        reconstructed_filename = f"reconstructed_{selected_file.name}"
        reconstructed.save(reconstructed_filename)
        with open(reconstructed_filename, 'rb') as f:
            st.download_button(
                "Download Reconstructed Image",
                f,
                file_name=reconstructed_filename,
                mime="image/jpeg",
                key=f"download_image_{selected_file.name}"
            )
        
        # Save and offer JSON downloads
        pixel_data = {
            'metadata': result['metadata'],
            'pixels': {coord: list(color) for coord, color in result['pixels'].items()}
        }
        
        st.download_button(
            "Download Pixel Data (JSON)",
            json.dumps(pixel_data, indent=2),
            file_name=f"pixel_data_{selected_file.name}.json",
            mime="application/json",
            key=f"download_pixel_{selected_file.name}"
        )
        
        st.download_button(
            "Download Analysis (JSON)",
            json.dumps(result, indent=2, default=str),
            file_name=f"analysis_{selected_file.name}.json",
            mime="application/json",
            key=f"download_analysis_{selected_file.name}"
        )
        
    except Exception as e:
        st.error(f"Error processing {selected_file.name}: {str(e)}")
    
    finally:
        # Cleanup
        if os.path.exists('temp_image.jpg'):
            os.remove('temp_image.jpg')
        if os.path.exists(reconstructed_filename):
            os.remove(reconstructed_filename)