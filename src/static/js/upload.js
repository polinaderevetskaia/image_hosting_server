document.addEventListener('DOMContentLoaded', function () { //подія виконується після повного завантаження html сторінки
    document.addEventListener('keydown', function (event) { //обробка натискання клавіш
        if (event.key === 'Escape' || event.key === 'F5') {
            event.preventDefault(); //не дозволяєм стандартну подію клавіші оновлення сторінки або вихід
            window.location.href = '/'; //переміщуємо користувача на головну сторінку
        }
    });

    const fileUpload = document.getElementById('file-upload'); //input для вибору файлу
    const imagesButton = document.getElementById('images-tab-btn'); //кнопка переходу до списку картинок
    const dropzone = document.querySelector('.upload__dropzone'); //зона для загрузки файлів
    const currentUploadInput = document.querySelector('.upload__input'); //поле для відображення url завантаженого файлу
    const copyButton = document.querySelector('.upload__copy'); //кнопка для копіювання url

    if (imagesButton) {
        imagesButton.addEventListener('click', () => window.location.href = '/images-list');
        //обробник кліку кнопки перехід на сторінку зі списком картинок
    }

    const showMessage = (message, isError = false) => { //функція для відображення повідомлення користувачу
        let msgEl = document.querySelector('.upload__message'); //пошук на сторінці елементу для відображення повідомлення
        if (!msgEl) {
            msgEl = document.createElement('p'); //якщо такого нема то створюємо новий
            msgEl.className = 'upload__message'; //задаємо css клас для стилів
            dropzone?.parentNode?.insertBefore(msgEl, dropzone.nextSibling);
            //створюємо елемент повідомлення якщо його ще нема
        }
        msgEl.textContent = message;
        msgEl.style.color = isError ? '#e53e3e' : '#38a169'; //встановлюємо текст і колір червоний — помилка а зелений — успіх
    };

    const uploadFile = async (file) => { //функція для відправки файлу на сервер
        const formData = new FormData();
        formData.append('file', file); //створюєм запит

        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData //пробуємо відправити POST-запит на сервер
            });

            const data = await response.json(); //отримуємо відповідь у форматі json

            if (data.success) {
                const storedFiles = JSON.parse(localStorage.getItem('uploadedImages')) || []; //отримуєм збережені файли з localStorage

                const getNextImageNumber = () =>
                    storedFiles.filter(f => f.displayName && f.displayName.startsWith('image')).length + 1;
                //функція вираховує номер наступного зображення підраховуючи їх загальну кількість і збільшуючи на 1

                const ext = file.name.substring(file.name.lastIndexOf('.')); //отримуємо розширення файлу
                const displayName = `image${String(getNextImageNumber()).padStart(2, '0')}${ext}`; //створюємо нове ім'я

                const reader = new FileReader(); //створюємо об'єкт для зчитування файлу у браузері
                reader.onload = (event) => { //коли файл буде зчитано, виконається ця функція
                    storedFiles.push({
                        name: data.filename, //ім'я файлу на сервері
                        displayName: displayName, //створене ім'я
                        originalName: file.name, //оригінальне ім'я файлу з комп’ютера юзера
                        url: event.target.result
                    }); //додаємо об’єкт файлу до масиву uploadedImages
                    localStorage.setItem('uploadedImages', JSON.stringify(storedFiles)); //зберігаємо оновлений список файлів у localStorage
                };
                reader.readAsDataURL(file); //зчитуємо файл як DataURL щоб його можна було одразу показати на сторінці

                if (currentUploadInput) {
                    currentUploadInput.value = `https://group6-image-hosting-server.com/${data.filename}`;
                } // виводимо url завантаженого файлу
                showMessage('File uploaded successfully!'); //повідомлення про успішне завантаження
            } else {
                showMessage(data.message || 'Upload failed.', true); //повідомлення про помилку
            }
        } catch (err) {
            showMessage('Something went wrong. Please try again.', true); //обробка помилки запиту
        }
    };

    const handleAndStoreFiles = (files) => { //функція для обробки декількох файлів
        if (!files || files.length === 0) return; //перевірка наявності файлів для обробки
        for (const file of files) {
            uploadFile(file); //завантажуємо кожен файл окремо
        }
    };

    if (copyButton && currentUploadInput) { //перевірка існування кнопки копіювання та поле для url файлу
        copyButton.addEventListener('click', () => { // обробник кліку на кнопку копіювання
            const textToCopy = currentUploadInput.value; //беремо текст з input
            if (textToCopy && textToCopy !== 'https://') { //перевірка наповненості поля
                navigator.clipboard.writeText(textToCopy).then(() => { //копіюємо текст у буфер обміну
                    copyButton.textContent = 'COPIED!'; //змінюємо текст кнопки для підтвердження юзеру
                    setTimeout(() => copyButton.textContent = 'COPY', 2000); //через 2 секунди повертаємо текст кнопки назад
                }).catch(err => console.error('Failed to copy text: ', err)); //обробка помилки якщо не вдалось скопіювати
            }
        });
    }

    if (fileUpload) { //перевіряємо, чи існує input для завантаження файлу
        fileUpload.addEventListener('change', (event) => {
            handleAndStoreFiles(event.target.files); //викликаємо функцію для обробки вибраних файлів
            event.target.value = ''; //очищаємо поле input для того щоб можна було вибрати той самий файл ще раз
    });
        });
    }

    if (dropzone) { //перевірка наявності зони для перетягування файлів
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropzone.addEventListener(eventName, (e) => {
                e.preventDefault();
                e.stopPropagation(); //вимикаємо стандартну поведінку браузера для цих подій щоб при перетягуванні файл не відкривався
            });
        });

        dropzone.addEventListener('dragover', () => dropzone.classList.add('dragover')); //додаємо css клас при наведенні файлу на зону для завантаження
        dropzone.addEventListener('dragleave', () => dropzone.classList.remove('dragover')); //прибираємо підсвічування коли файл покидає зону
        dropzone.addEventListener('drop', (event) => {
            dropzone.classList.remove('dragover'); //прибираємо підсвічування при відпусканні файлу
            handleAndStoreFiles(event.dataTransfer.files); //обробляємо файли перетягнуті у зону
        });
    }
});