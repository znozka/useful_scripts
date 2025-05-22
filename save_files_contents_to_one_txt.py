"""
Skrypt kopiujący zawartość wielu plików i zapisujący je do jednego pliku .txt w formacie:

    nazwa/ze/ścieżką/względną:
    zawartość pliku

"""

import os

# === TUTAJ WPISZ ŚCIEŻKI DO SWOICH PLIKÓW (w systemie windowsowym, tzn. z "\") ===
file_paths = [
    r"sciezka\do\pliku",
    r"sciezka\do\pliku"
]

# === TUTAJ WPISZ ŚCIEŻKĘ DO FOLDERU BAZOWEGO (tzn. odkąd chcesz odciąć ścieżkę) ===
base_path = r"sciezka\do\folderu"

output_file = "output.txt"

def normalize_path(path):
    """Zamienia backslash (\) na slash (/), aby ścieżki były kompatybilne."""
    return path.replace("\\", "/")

def save_files_to_txt(file_paths, base_path, output_file="output.txt"):
    base_path = normalize_path(base_path)

    with open(output_file, 'w', encoding='utf-8') as out_f:
        for raw_path in file_paths:
            path = normalize_path(raw_path)
            if not os.path.isfile(path):
                print(f"Plik nie istnieje: {path}")
                continue
            try:
                relative_path = os.path.relpath(path, base_path).replace("/", "\\")
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                out_f.write(f"{relative_path}:\n")
                out_f.write(content + "==================================================================================\n")
            except Exception as e:
                print(f"Błąd podczas przetwarzania pliku {path}: {e}")

save_files_to_txt(file_paths, base_path, output_file)
