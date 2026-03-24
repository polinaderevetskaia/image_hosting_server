ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'} #перелік дозволених розширень файлів для завантаження
MAX_FILE_SIZE = 5 * 1024 * 1024 #визначення максимального розміру файлу 5 МБ


def validate_file_extension(filename): #функція перевіряє чи має файл допустиме розширення
    if not filename or '.' not in filename: #перевіряє ім'я файлу і чи має він розширення
        return False, "File has no extension" #якщо ні то виводить відповідне повідомлення
    extension = filename.lower().split('.')[-1] #виокремлює розширення файлу
    if extension not in ALLOWED_EXTENSIONS: #перевіряє чи розширення відповідає вимогам
        allowed = ', '.join(ALLOWED_EXTENSIONS) #формування і подальший вивід дозволених розширень
        return False, f"Unsupported file format: .{extension}. Allowed: {allowed}"
    return True, "File extension is supported"


def validate_file_size(file_size): #функція перевіряє чи не перевищує файл заданий ліміт розміру
    if file_size > MAX_FILE_SIZE: #порівняння розміру файлу з максимально дозволеним
        size_mb = file_size / (1024 * 1024) #розмір файлу в МБ для повідомлення юзеру
        max_mb = MAX_FILE_SIZE / (1024 * 1024) #максимальний дозволений розмір у МБ
        return False, f"File too large: {size_mb:.2f} MB (max {max_mb} MB)" #вивід відповідних повідомлень
    return True, "File size is acceptable"


def validate_image_file(file, filename): #функція перевіряю повну валідацію файлу і за розширенням і за розміром
    is_valid, message = validate_file_extension(filename)
    if not is_valid:
        return False, f"Format error: {message}" #повідомлення про помилку валідації

    current_position = file.tell() #зберігаємо поточну позицію в файлі
    file.seek(0, 2) #переходимо у кінець файлe
    file_size = file.tell() #отримуємо позицію курсора
    file.seek(current_position) #повертаємо курсор на початкову позицію

    is_valid, message = validate_file_size(file_size) #виклик функції перевірки розміру файлу
    if not is_valid:
        return False, f"Size error: {message}" #повідомлення про помилку валідації

    return True, "File passed validation successfully" #повідомлення про успішну валідацію