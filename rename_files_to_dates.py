import os
import shutil
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime

input_folder = r"C:\folder\path"
output_folder = r"C:\folder\path"

def normalize_path(path):
    return path.replace("\\", "/")

def get_image_date(file_path):
    """Pobiera datę z EXIF lub z daty modyfikacji pliku."""
    try:
        with Image.open(file_path) as img:
            exif_data = img._getexif()
            if exif_data:
                for tag_id, value in exif_data.items():
                    tag = TAGS.get(tag_id, tag_id)
                    if tag == 'DateTimeOriginal':
                        return datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
    except Exception:
        pass

    ts = os.path.getmtime(file_path)
    return datetime.fromtimestamp(ts)

def rename_files_to_dates(input_folder, output_folder):
    input_folder = normalize_path(input_folder)
    output_folder = normalize_path(output_folder)
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        src_path = os.path.join(input_folder, filename)
        date_taken = get_image_date(src_path)
        base_name = date_taken.strftime("%Y%m%d")

        name_part, ext = os.path.splitext(filename)
        new_filename = f"{base_name} {name_part}{ext.lower()}"

        dst_path = os.path.join(output_folder, new_filename)
        shutil.copy2(src_path, dst_path)  # zachowuje metadane

rename_files_to_dates(input_folder, output_folder)
