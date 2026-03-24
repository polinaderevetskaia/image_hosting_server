document.addEventListener('DOMContentLoaded', function () { //подія виконується після повного завантаження html сторінки
    document.addEventListener('keydown', function (event) { //обробка натискання клавіш F5 та Escape
        if (event.key === 'F5' || event.key === 'Escape') {
            event.preventDefault();
            window.location.href = '/upload'; //перенаправляємо юзера на сторінку завантаження файлів
        }
    });

    const fileListWrapper = document.getElementById('file-list-wrapper'); //контейнер для відображення списку файлів
    const uploadRedirectButton = document.getElementById('upload-tab-btn'); //кнопка для переходу на сторінку завантаження

    if (uploadRedirectButton) {
        uploadRedirectButton.addEventListener('click', () => window.location.href = '/upload');
        //обробка кліку тобто перенаправлення юзера на сторінку завантаження
    }

    const displayFiles = () => { //функція для відображення списку завантажених файлів
        const storedFiles = JSON.parse(localStorage.getItem('uploadedImages')) || []; //отримуємо список файлів з localStorage або порожній масив
        fileListWrapper.innerHTML = ''; //очищаємо контейнер перед відображенням

        if (storedFiles.length === 0) {
            fileListWrapper.innerHTML = '<p class="upload__promt" style="text-align: center; margin-top: 50px;">No images uploaded yet.</p>';
            return; //якщо файлів немає то показуємо повідомлення
        }

        const container = document.createElement('div');
        container.className = 'file-list-container';
        //створюємо контейнер для списку файлів

        const header = document.createElement('div'); //створюємо новий блок для шапки списку файлів
        header.className = 'file-list-header'; //додаємо css клас для стилів шапки
        header.innerHTML = `
            <div class="file-col file-col-name">Name</div> //назва
            <div class="file-col file-col-url">Url</div> //url
            <div class="file-col file-col-delete">Delete</div> //видалення
        `;
        container.appendChild(header); //додаємо шапку таблиці у контейнер списку файлів

        const list = document.createElement('div');
        list.id = 'file-list'; //контейнер для елементів файлів

        storedFiles.forEach((fileData, index) => { //перебираємо кожен файл і створюємо елемент списку
            const fileItem = document.createElement('div'); //створюємо контейнер для одного файлу у списку
            fileItem.className = 'file-list-item'; //додаємо css клас для стилізації рядка файлу
            fileItem.innerHTML = `
                <div class="file-col file-col-name">
                    <span class="file-icon"><img src="/static/img/group.png" alt="file icon"></span>
                    ${fileData.url ? `<img src="${fileData.url}" alt="thumbnail">` : ''}
                    <span class="file-name" title="${fileData.originalName || fileData.displayName || fileData.name}">${fileData.displayName || fileData.name}</span>
                </div>
                <div class="file-col file-col-url">https://group6-image-hosting-server.com/${fileData.name}</div>
                <div class="file-col file-col-delete">
                    <button class="delete-btn" data-index="${index}"><img src="/static/img/delete.png" alt="delete icon"></button>
                </div> //цей блок коду формує html для одного рядка списку файлів а саме: в першому стовпці - іконка і мініатюра картинки а також її назва
                //в другому - стовпці url файлу для копіювання
                //в третьому - кнопка для видалення файлу і відповідна іконка
            `;
            list.appendChild(fileItem); //додаємо кожен файл до списку з кнопкою видалення
        });

        container.appendChild(list);
        fileListWrapper.appendChild(container); //додаємо контейнер із файлами до сторінки
        addDeleteListeners(); //додаємо обробники для кнопок видалення
    };

    const addDeleteListeners = () => { //функція для додавання обробки видалення файлів
        document.querySelectorAll('.delete-btn').forEach(button => { //знаходимо всі кнопки видалення на сторінці і додаємо хм обробник подій
            button.addEventListener('click', async (event) => {
                const indexToDelete = parseInt(event.currentTarget.dataset.index); //отримуємо індекс файлу для видалення із data-атрибуту кнопки
                let storedFiles = JSON.parse(localStorage.getItem('uploadedImages')) || [];
                const fileToDelete = storedFiles[indexToDelete]; //отримуємо дані файлу із localStorage за індексом

                if (fileToDelete && fileToDelete.name) {
                    try {
                        const imagesResponse = await fetch('/api/images');
                        const imagesResult = await imagesResponse.json(); //отримуємо список файлів, що збережені на сервері

                        if (imagesResult.success) {
                            const imageRecord = imagesResult.images.find(img => img.filename === fileToDelete.name); //шукаємо запис файлу на сервері за його ім’ям

                            if (imageRecord) {
                                const deleteResponse = await fetch(`/api/images/${imageRecord.id}`, {
                                    method: 'DELETE' //відправляємо запит на сервер для видалення файлу
                                });

                                const deleteResult = await deleteResponse.json(); //отримуємо відповідь від сервера у форматі json

                                if (deleteResult.success) {
                                    console.log('File deleted from server:', fileToDelete.name); //повідомлення про успішне видалення файла на сервері
                                } else {
                                    console.error('Failed to delete file from server:', deleteResult.message); //повідомлення про невдачу при видалення файла на сервері
                                }
                            }
                        }
                    } catch (error) {
                        console.error('Error deleting file:', error); //обробка помилок при зверненні до сервера
                    }
                }

                storedFiles.splice(indexToDelete, 1);
                localStorage.setItem('uploadedImages', JSON.stringify(storedFiles)); //видаляємо файл із localStorage
                displayFiles(); //оновлюємо список файлів на сторінці
            });
        });
    };

    displayFiles(); //викликаємо функцію для початкового відображення списку файлів
});