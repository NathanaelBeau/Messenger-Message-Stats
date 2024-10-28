import os

def get_html_files(directory):
    all_files = os.listdir(directory)  # List all files in the directory
    html_files = [f for f in all_files if f.endswith('.html')]  # Filter out .html files
    return html_files
