import os
import csv
from PIL import Image, ExifTags
import pathlib
from datetime import datetime
import requests

def generate_google_maps_url(latitude, longitude):
    if latitude is not None and longitude is not None:
        latitude = str(latitude)
        longitude = str(longitude)
        base_url = "https://www.google.com/maps"
        location_url = f"?q={latitude},{longitude}"
        google_maps_url = base_url + location_url
        return google_maps_url
    else:
        return "GPS coordinates not found"


def extract_the_data(image_folder):
    metadata_list = []

    image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.HEIC'))]
    # Extract metadata
    
    for image_file in image_files:
        image_path = os.path.join(image_folder, image_file)
        img = Image.open(image_path)

        img_size = img.size
        img_height = img.height
        img_width = img.width
        img_format = img.format
        img_is_animated = getattr(img, "is_animated", False)
        frames_count = getattr(img, "n_frames", 1)

        # gps extraction

        gps_info = None
        exif_data = img._getexif()
        if exif_data:
            for tag, value in exif_data.items():
                tag_name = ExifTags.TAGS.get(tag, tag)
                if tag_name == "GPSInfo":
                    gps_info = value
                    break

        gps_latitude = None
        gps_longitude = None
        if gps_info:
            gps_latitude = gps_info.get(2)  # usb transfer se longitude latitude arhe h but download krne se nhi arhe
            gps_longitude = gps_info.get(4)
            gps_latitude = str(gps_latitude)
            gps_longitude = str(gps_longitude)
            # Format gps_latitude and gps_longitude
            if gps_latitude and gps_longitude:
                # Remove brackets
                gps_latitude = gps_latitude.replace("(", "").replace(")", "")
                gps_longitude = gps_longitude.replace("(", "").replace(")", "")

                # Split into degrees, minutes, and seconds
                parts_latitude = gps_latitude.split(",")
                parts_longitude = gps_longitude.split(",")

                if len(parts_latitude) == 3 and len(parts_longitude) == 3:
                    # Format degrees, minutes, and seconds
                    degrees_latitude = parts_latitude[0]
                    minutes_latitude = parts_latitude[1]
                    seconds_latitude = parts_latitude[2]

                    degrees_longitude = parts_longitude[0]
                    minutes_longitude = parts_longitude[1]
                    seconds_longitude = parts_longitude[2]

                    # Construct the formatted strings
                    formatted_latitude = f"{degrees_latitude}{minutes_latitude}{seconds_latitude}"
                    formatted_longitude = f"{degrees_longitude}{minutes_longitude}{seconds_longitude}"
                    # Split into degrees, minutes, and seconds
                    parts_latitude = [float(part.strip()) for part in gps_latitude.replace(',', '').split()]
                    parts_longitude = [float(part.strip()) for part in gps_longitude.replace(',', '').split()]


                    # Format degrees, minutes, and seconds
                    degrees_latitude = parts_latitude[0]
                    minutes_latitude = parts_latitude[1]
                    seconds_latitude = parts_latitude[2]

                    degrees_longitude = parts_longitude[0]
                    minutes_longitude = parts_longitude[1]
                    seconds_longitude = parts_longitude[2]

                    # Construct the formatted strings
                    formatted_latitude = f"{degrees_latitude + minutes_latitude/60 + seconds_latitude/3600:.7f}"
                    formatted_longitude = f"{degrees_longitude + minutes_longitude/60 + seconds_longitude/3600:.7f}"
                    google_maps_url= ""
                    # Generate Google Maps URL
                    google_maps_url = generate_google_maps_url(formatted_latitude, formatted_longitude)

                else:
                    # Handle invalid GPS values
                    google_maps_url = "No GPS Data"
        
        # Extract the date and time of image captured
        camera_model = "Unknown"  # Initialize with a default value
        capture_date = "Unknown"

        if exif_data:
            camera_model = exif_data.get(272, "Unknown")  # 272 model number k liye use hota h
            capture_date = exif_data.get(306, "Unknown")  # 306 date k liye

            if isinstance(capture_date, bytes):
                capture_date = capture_date.decode()

            try:
                capture_date = datetime.strptime(capture_date, "%Y:%m:%d %H:%M:%S")
            except:
                capture_date = "Unknown"

        img_metadata = {
            "file_name": pathlib.Path(image_path).name,
            "size": img_size,
            "height": img_height,
            "width": img_width,
            "format": img_format,
            "is_animated": img_is_animated,
            "frames": frames_count,
            "camera model": camera_model,
            "date and time": capture_date,
            "gps latitude": gps_latitude,
            "gps longitude": gps_longitude,
            "google_maps_url": google_maps_url,
        }

        metadata_list.append(img_metadata)
        img.close()

    # csv for metadata
    csv_file_name = "image_metadata.csv"
    with open(csv_file_name, "w", newline="") as csv_file:
        field_names = metadata_list[0].keys()
        writer = csv.DictWriter(csv_file, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(metadata_list)

    print("Metadata extraction complete. CSV file saved as", csv_file_name, "hehehehehehehe")

# main function 
if __name__ == "__main__":
    image_folder_path = "D:\\Cyber Security\\PGDCD\\projects\\Image forensics\\uploads"
    extract_the_data(image_folder_path)
