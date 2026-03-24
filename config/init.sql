CREATE TABLE IF NOT EXISTS images ( --створення нової таблиці в базі даних якщо її ще не існує
    id SERIAL PRIMARY KEY, --унікальний ідентифікатор
    filename TEXT NOT NULL, --ім'я файлу на сервері
    original_name TEXT NOT NULL, --оригінальне ім'я файлу
    size INTEGER NOT NULL, --розмір файлу в байтах
    file_type TEXT NOT NULL, --тип файлу
    upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP --час завантаження
);