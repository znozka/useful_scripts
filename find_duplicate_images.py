import os
from PIL import Image
import imagehash

def find_similar_images(folder_path, hash_size=16, threshold=5):
    """
    Wyszukuje podobne zdjęcia w folderze na podstawie perceptual hash (pHash).
    hash_size – większa wartość = większa dokładność (koszt wydajności)
    threshold – maksymalna różnica bitów między hashami uznana za duplikat
    """

    folder_path = folder_path.replace("\\", "/")

    # słownik: hash -> lista plików
    hashes = {}
    images = [f for f in os.listdir(folder_path) if f.lower().endswith((".jpg", ".jpeg", ".png"))]

    for img_name in images:
        img_path = os.path.join(folder_path, img_name)
        try:
            with Image.open(img_path) as img:
                img_hash = imagehash.phash(img, hash_size=hash_size)

            # sprawdź, czy pasuje do istniejących hashy w granicy threshold
            found = False
            for existing_hash in hashes:
                if abs(img_hash - existing_hash) <= threshold:
                    hashes[existing_hash].append(img_name)
                    found = True
                    break

            if not found:
                hashes[img_hash] = [img_name]

        except Exception as e:
            print(f"Błąd przy {img_name}: {e}")

    # wypisz tylko grupy z więcej niż jednym elementem
    duplicates_found = False
    for files in hashes.values():
        if len(files) > 1:
            duplicates_found = True
            print("Prawdopodobne duplikaty:")
            for f in files:
                print("  ", f)
            print()

    if not duplicates_found:
        print("Brak znalezionych podobnych zdjęć.")

folder = r"C:\folder\path"
find_similar_images(folder, hash_size=16, threshold=50)
