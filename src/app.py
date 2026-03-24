import http.server #підключення модуля сервера для обробки http запитів
import socketserver #підключення модуля для роботи з серверами і портами
import os #підключення модуля для роботи с файлами
import json #підключення модуля для роботи з json
import io #підключення модуля для роботи з потоками даних
import re #підключення модуля для пошуку тексту
from validators import validate_image_file #з модуля імпортувати функцію для валідації картинки
from file_handler import save_file, delete_file #з модуля імпортувати функції для збереження і видалення файлів
from database import DatabaseManager #з модуля імпортувати клас для роботи з базою даних

db = DatabaseManager() #створюємо об'єкт бази даних


class ImageServerHandler(http.server.BaseHTTPRequestHandler): #створення класу який оброблятиме запити від браузера
    def do_GET(self): #виклик методу відбувається коли юзер заходить на сайт
        routes = {  #список сторінок
            '/': 'index.html',
            '/upload': 'upload.html',
            '/images-list': 'images.html'
        }

        if self.path in routes:
            self.serve_template(routes[self.path]) #якщо сторінка є тоді показуємо відповідний html
        elif self.path.startswith('/static/'):
            self.serve_static(self.path) #якщо це css, js, img надсилається відповідний файл
        elif self.path.startswith('/api/images'):
            self.handle_get_images() #якщо API тоді повертаємо список картинок
        else:
            self.send_response(404) #якщо нічого нема тоді показується код 404
            self.end_headers()

    def do_POST(self): #функція відправки даних
        if self.path == '/upload':
            self.handle_upload() #якщо завантажується тоді обробляємо файл
        else:
            self.send_response(404) #інакше код 404
            self.end_headers()

    def do_DELETE(self): #обробка запиту на видалення
        if self.path.startswith('/api/images/'):
            self.handle_delete_image() #видаляємо картинку
        else:
            self.send_response(404) #інакше код 404
            self.end_headers()

    def handle_upload(self): #функція для завантаження картинок
        try:
            content_type = self.headers.get('Content-Type', '') #беремо тип запиту
            if not content_type.startswith('multipart/form-data'): #перевіряємо чи це файл і якшо ні
                self.send_error(400, "Expected multipart/form-data") #помилка 400
                return

            form_data = self.rfile.read(int(self.headers['Content-Length'])) #прочитуємо весь файл
            filename = self._extract_filename(form_data) #витягуєм ім'я файлу
            file_like = io.BytesIO(form_data) #перетворюємо файл на об'єкт

            is_valid, message = validate_image_file(file_like, filename) #перевіряємо чи відповідає файл умовам

            if not is_valid: #якщо не валідний то повернеться json файл з описом помилки
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'success': False,
                    'message': message
                }).encode('utf-8'))
                return

            file_bytes = self._extract_file_bytes(form_data) #витягуєм байти картинки
            saved_name = save_file(file_bytes, filename) #зберігаємо файл на диск

            ext = filename.lower().split('.')[-1] #форматує назву картинки
            db.save_metadata( #записуємо дані в базу назву, розмір, тип
                filename=saved_name,
                original_name=filename,
                size=len(file_bytes),
                file_type=ext
            )

            self.send_response(200) #код 200 значить що все добре працює
            self.send_header('Content-type', 'application/json')  #відповідь зберігається у json
            self.end_headers()
            self.wfile.write(json.dumps({
                'success': True,
                'message': 'File uploaded successfully',
                'filename': saved_name,
                'url': f'https://group6-image-hosting-server.com/{saved_name}'
            }).encode('utf-8')) #перетворюємо словник у json і кодуємо у байти

        except Exception as e: #обробка помилки під кодом 500
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'success': False, 'error': str(e)}).encode('utf-8'))

    def handle_get_images(self): #функція повертає список картинок
        try:
            from urllib.parse import urlparse, parse_qs #імпорт фукнцій для розбору url та параметрів запиту
            parsed = urlparse(self.path) #розбираємо url
            params = parse_qs(parsed.query) #отримуємо параметри у вигляді словника
            page = int(params.get('page', [1])[0]) #отримуємо в якості параметру номер сторінки а якщо його не буде то отримаємо значення за замовчуванням 1

            images, total = db.get_all_images(page=page) #отримуєм список зображень і їх кількість для вказаної сторінки

            self.send_response(200) #код 200 значить все ок
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                'success': True,
                'images': [dict(img) for img in images],
                'total': total,
                'page': page
            }, default=str).encode('utf-8'))

        except Exception as e: #обробка помилок
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'success': False, 'error': str(e)}).encode('utf-8'))

    def handle_delete_image(self): #фунція для видалення картинки
        try:
            image_id = int(self.path.split('/')[-1]) #отримуємо ID зображення з url за допомогою роздільника
            filename = db.delete_image(image_id) #видаляємо запис з бази даних
            if filename:
                delete_file(filename) #видаляємо файл з файлової системи
                self.send_response(200) #код 200 успіх
                self.send_header('Content-type', 'application/json') #позначаєм що відповідь у форматі json
                self.end_headers()
                self.wfile.write(json.dumps({
                    'success': True,
                    'message': f'Image {filename} deleted successfully'
                }).encode('utf-8')) #відправляємо готову відповідь у форматі json
            else:
                self.send_response(404) #в іншому випадку код 404
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    'success': False,
                    'message': 'Image not found'
                }).encode('utf-8')) #відповідне повідомлення про відсутність картинки

        except Exception as e:
            self.send_response(500) #обробка помилок код 500
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'success': False, 'error': str(e)}).encode('utf-8')) #повертаємо текст помилки у форматі json

    def _extract_filename(self, form_data): #функція для отримання імені файлу із запиту
        try:
            decoded = form_data.decode('utf-8', errors='ignore') #перетворюємо байти у рядок при цбому ігноруємо помилки
            match = re.search(r'filename="([^"]+)"', decoded)  #пошук імені файлу у заголовках
            if match:
                return match.group(1) #повертаємо знайдене ім'я файлу
        except Exception:
            pass #у разі помилки просто ігноруємо
        return "unknown" #якщо не знайшлося тоді буде значення за замовчуванням

    def _extract_file_bytes(self, form_data): #функція для отримання байтів файлу із запиту
        boundary = form_data.split(b'\r\n')[0] # отримуємо розділювач частин запиту
        parts = form_data.split(boundary) #розбиваємо весь запит на окремі частини

        for part in parts:
            if b'Content-Type:' in part or b'filename=' in part: #пошук частини яка містить файл
                header_end = part.find(b'\r\n\r\n') #шукаєм кінець заголовків
                if header_end != -1:
                    file_content = part[header_end + 4:] #вирізаємо тільки байти файлу без урахування заголовків
                    if file_content.endswith(b'\r\n'):
                        file_content = file_content[:-2] #видаляємо зайвий перенос рядка в кінці
                    return file_content #повертаємо вміст файлу у вигляді байтів
        return b'' #якщо ж файл не знайшовся то повертаємо пусті байти

    def serve_template(self, filename): #функція для відправки html шаблону клієнту
        try:
            template_path = os.path.join(os.path.dirname(__file__), 'templates', filename) #створюємо повний шлях до файлу шаблону
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read() #читаємо вміст html файлу
            self.send_response(200) #код 200 це успіх
            self.send_header('Content-type', 'text/html') #вказуємо тип контенту
            self.end_headers()
            self.wfile.write(content.encode('utf-8')) # відправляємо html код клієнту
        except FileNotFoundError: #обробка помилок
            self.send_response(404) #якщо файла нема код 404
            self.end_headers()

    def serve_static(self, path): #функція для відправки статичних файлів css, js, img
        try:
            file_path = path[len('/static/'):] #отримуємо шлях до файлу
            static_path = os.path.join(os.path.dirname(__file__), 'static', file_path) #формуємо повний шлях до файлу
            with open(static_path, 'rb') as f:
                content = f.read() #зчитуємо файл у байтах
            self.send_response(200) #код 200 це успіх
            self.send_header('Content-type', self.get_content_type(file_path)) #визначаємо тип файлу
            self.end_headers()
            self.wfile.write(content) #відправляємо файл клієнту
        except FileNotFoundError: #обробка помилок
            self.send_response(404) #якщо файла нема код 404
            self.end_headers()

    def get_content_type(self, file_path): #функція визначає тип файлу за його розширенням
        if file_path.endswith('.css'):
            return 'text/css' #стилі css
        elif file_path.endswith('.js'):
            return 'application/javascript' #js файли
        elif file_path.endswith('.png'):
            return 'image/png' #картинки png формату
        elif file_path.endswith('.jpg') or file_path.endswith('.jpeg'):
            return 'image/jpeg' #картинки jpg/jpeg формату
        else:
            return 'application/octet-stream' #тип за замовчуванням


def run_server(port=8000): #функція для запуску http сервера
    port = int(os.environ.get('PORT', port)) #отримуємо порт із змінної середовища або використовуємо значення за замовчуванням
    db.connect() #підключення до бази даних
    try:
        with socketserver.TCPServer(("", port), ImageServerHandler) as httpd: # створюємо TCP сервер на даному порту
            print(f"🚀 Server running on port {port} ...") #повідомлення про запуск сервера
            try:
                httpd.serve_forever() #сервер працюватиме доти поки його особисто не зупиниш
            except KeyboardInterrupt: #при натисканні комбінації клавіш сервер зупиниться
                print("🛑 Server stopped by user") #вивід відповідного повідомлення
    except OSError as e: #обробка помилок
        if e.errno == 48: #якщо помилка 48 то це означає що порт зайнятий
            print(f"❌ Port {port} is already in use. Please stop the server | lsof -ti :{port} | xargs kill -9") #повідомлення яке сповіщає по це
        else:
            print(f"❌ Error starting server: {e}") #в іншому випадку виводить повідомлення про іншу помилку
    finally:
        db.disconnect() #закриваємо з'єднання з базою даних при завершенні


if __name__ == "__main__": #перевірка чи файл запущений напряму а не імпортований звідкись
    run_server() #виклик команди запуск сервера