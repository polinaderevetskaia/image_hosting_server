import uuid #імпорт модуля для генерації унікальних ідентифікаторів
from pathlib import Path #імпорт Path для зручної роботи з файловими шляхами

IMAGES_DIR = Path(__file__).parent.parent / 'images' #визначаємо місце для збереження зображень - піднімаємось на два рівні вище та додаємо папку images


def generate_unique_filename(original_name): #функція для генерації унікального ім'я
    ext = original_name.lower().split('.')[-1] #переводимо розширення у нижній регістр
    unique_name = f"{uuid.uuid4()}.{ext}" #генеруємо унікальне ім'я файлу за допомогою модолю і додаємо розширення
    return unique_name #повертаємо унікальне ім'я файлу


def save_file(file_data, filename): #функція для збереження картинок у папці
    IMAGES_DIR.mkdir(exist_ok=True) #створення папки для зображень якщо її ще нема
    unique_name = generate_unique_filename(filename) #генеруємо унікальне ім'я файлу
    filepath = IMAGES_DIR / unique_name #створюємо повний шлях до файлу для збереження

    with open(filepath, 'wb') as f: #відкриваємо файл у бінарному режимі для запису
        f.write(file_data) #записуємо бінарні дані у файл

    print(f"✅ File saved successfully: {unique_name}") #повідомлення про успішне збереження файлу
    return unique_name #повертаємо унікальне ім'я файлу


def delete_file(filename): #функція для видалення файлу
    filepath = IMAGES_DIR / filename #створюємо повний шлях до файлу який потрібно видалити
    if filepath.exists(): #перевірка наявності файлу
        filepath.unlink() #видаляємо файл
        return True #файл успішно видалено
    return False #файл не існує