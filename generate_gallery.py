
import os
import argparse
import html  # To escape filenames for attributes


def list_image_files(directory_path):
    """
    Lists image files (jpg, jpeg, png, gif, webp) in a given directory.

    Args:
        directory_path (str): The path to the directory to scan.

    Returns:
        list: A sorted list of image filenames found in the directory.
              Returns an empty list if the directory doesn't exist or
              if no images are found.
    """
    image_files = []
    image_extensions = ('.jpg', '.jpeg', '.png', '.gif',
                        '.webp')  # Common web image extensions

    try:
        if not os.path.isdir(directory_path):
            print(f"Error: Directory not found at '{directory_path}'")
            return []

        print(f"Scanning directory: '{directory_path}'...")
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            if os.path.isfile(file_path) and filename.lower().endswith(image_extensions):
                image_files.append(filename)
                # print(f" Found image: {filename}") # Optional: print found files

        if not image_files:
            print("No image files found in the specified directory.")

    except OSError as e:
        print(f"Error accessing directory '{directory_path}': {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []

    image_files.sort()  # Sort files alphabetically
    print(f"Found {len(image_files)} image file(s).")
    return image_files


def generate_gallery_html(image_filenames, web_image_path):
    """
    Generates HTML code for gallery items based on a list of image filenames.
    Assumes these images are thumbnails for videos and links to them.

    Args:
        image_filenames (list): A list of image filenames.
        web_image_path (str): The relative path to the images directory
                               as it should appear in the HTML src attribute.
                               (e.g., 'assets/gallery/thumbnails')

    Returns:
        str: A string containing the generated HTML for all gallery items.
    """
    html_output = ""
    base_animation_class = "gallery-item rounded-lg overflow-hidden shadow-md hover:shadow-xl transition-shadow duration-300"

    # Ensure trailing slash for web path if needed
    if web_image_path and not web_image_path.endswith('/'):
        web_image_path += '/'

    print("Generating HTML...")
    for index, filename in enumerate(image_filenames):
        # Create safe versions of filename for attributes
        safe_filename = html.escape(filename)
        # Basic alt text from filename (remove extension)
        alt_text = f"Video Thumbnail: {os.path.splitext(safe_filename)[0]}"
        # Construct the source path for the image
        image_src = f"{web_image_path}{safe_filename}"
        # Placeholder link for the video itself (replace # later)
        video_link = "#"
        # Calculate animation delay (simple stagger)
        delay = (index + 1) * 0.05  # Adjust multiplier for speed
        animation_style = f"animation-delay: {delay:.2f}s;"

        html_output += f"""
                <div class="{base_animation_class}" style="{animation_style}">
                    <a href="{video_link}" title="Watch Video: {os.path.splitext(safe_filename)[0]}">
                        <img src="{image_src}"
                             alt="{alt_text}"
                             class="w-full h-auto object-cover aspect-video placeholder-block transform transition-transform duration-300"
                             loading="lazy">
                        <div class="play-overlay"><i class="fas fa-play-circle"></i></div>
                    </a>
                </div>"""

    print("HTML generation complete.")
    return html_output.strip()  # Remove leading/trailing whitespace


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate HTML gallery items from images in a directory.")
    parser.add_argument(
        'scan_directory',
        type=str,
        help="The actual path to the directory containing the image files to scan."
    )
    parser.add_argument(
        'web_path',
        type=str,
        help="The relative web path to use for the 'src' attribute in the generated HTML (e.g., 'images/gallery')."
    )

    args = parser.parse_args()

    # Get the list of image files
    images = list_image_files(args.scan_directory)

    if images:
        # Generate the HTML
        gallery_html = generate_gallery_html(images, args.web_path)

        # Print the generated HTML to the console
        print("\n--- Generated HTML (Copy and paste this into your gallery.html file) ---")
        print(gallery_html)
        print("----------------------------------------------------------------------")
        print(f"\nInstructions: Replace the contents of the <div class=\"gallery-grid ...\"> element in your gallery.html file with the HTML printed above.")
