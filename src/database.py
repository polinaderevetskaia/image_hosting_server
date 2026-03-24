import psycopg2 #імпорт основного драйвера для PostgreSQL
from psycopg2.extras import RealDictCursor #додатковий курсор який повертає результати у вигляді словників
import os #імпорт модуля для роботи з системними змінними середовища
from dotenv import load_dotenv #імпорт функції для завантаження .env файлів з конфіденційними даними

load_dotenv() #завантажуємо змінні середовища з файлу .env


class DatabaseManager: #клас для роботи з базою даних PostgreSQL
    def __init__(self): #ініціалізація змінної для з'єднання з базою даних
        self.connection = None

    def connect(self): #підключення до PostgreSQL з використанням змінних середовища
        try:
            self.connection = psycopg2.connect(
                host=os.getenv('DB_HOST'), #хост бази даних
                database=os.getenv('DB_NAME'), #назва бази даних
                user=os.getenv('DB_USER'), #юзер
                password=os.getenv('DB_PASSWORD'), #пароль
                port=os.getenv('DB_PORT') #порт
            )
            print("✅ Connected to PostgreSQL") #повідомлення про успішне підключення
        except Exception as e:
            print(f"❌ Connection error: {e}") #повідомлення про те що підключення не вдалося

    def disconnect(self): #закриття підключення до бази даних
        if self.connection:
            self.connection.close() #закриваємо з'єднання
            print("🛑 Disconnected from PostgreSQL") #відповідне повідомлення

    def save_metadata(self, filename, original_name, size, file_type): #збереження даних про картинки в таблицю images
        try:
            with self.connection.cursor() as cursor: #використовуємо курсор для виконання запиту
                cursor.execute("""
                    INSERT INTO images (filename, original_name, size, file_type)
                    VALUES (%s, %s, %s, %s)
                """, (filename, original_name, size, file_type)) #виконуємо sql запит
                self.connection.commit() #підтверджуємо зміни в БД
                return True #успішне збереження
        except Exception as e:
            print(f"❌ Save error: {e}") #вивід помилки при збереженні
            return False

    def get_all_images(self, page=1, per_page=10): #отримання всіх зображень з пагінацією
        try:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor: #використовуємо словниковий курсор
                offset = (page - 1) * per_page #вираховуємо зміщення для пагінації
                cursor.execute("""
                    SELECT * FROM images
                    ORDER BY upload_time DESC
                    LIMIT %s OFFSET %s
                """, (per_page, offset)) #виконуємо sql запит для сторінки
                images = cursor.fetchall() #отримуємо результати

                cursor.execute("SELECT COUNT(*) FROM images") #отримуємо загальну кількість зображень
                total = cursor.fetchone()['count']

                return images, total #повертаємо список зображень і загальну кількість
        except Exception as e:
            print(f"❌ Retrieval error: {e}") #повідомлення про помилки при отриманні даних
            return [], 0 #повертаємо порожні значення при помилці

    def delete_image(self, image_id): #видалення картинки з бази даних за його ID
        try:
            with self.connection.cursor() as cursor: #отримуємо ім'я файлу для видалення з файлової системи
                cursor.execute("SELECT filename FROM images WHERE id = %s", (image_id,)) #виконуємо sql запит
                result = cursor.fetchone() #отримуємо перший рядок результату запиту
                if not result:
                    return False #повертаємо False якщо картинки не знайдено

                filename = result[0] #беремо ім'я файлу
                cursor.execute("DELETE FROM images WHERE id = %s", (image_id,)) #видаляємо запис з таблиці images
                self.connection.commit() #підтверджуємо зміни
                return filename #повертаємо ім'я видаленого файлу
        except Exception as e:
            print(f"❌ Delete error: {e}") #вивід помилки при видаленні
            return False