document.addEventListener('DOMContentLoaded', function () {     //чекаємо поки вся сторінка завантажиться
    const allImgBlocks = document.querySelectorAll('.hero__img'); //пошук всіх блоків з картинками
    if (allImgBlocks.length > 0) {  //перевіряєм чи є картинки
        const randomIndex = Math.floor(Math.random() * allImgBlocks.length);  //вибираємо рандомний номер для картинки
        allImgBlocks[randomIndex].classList.add('is-visible'); //додаємо клас і робимо картинку видимою
    }

    if (window.location.pathname === '/') { //перевірка чи це головна сторінка
        document.body.style.setProperty('background-color', '#151515'); //змінюємо фон сторінки
    }

    const showcaseButton = document.querySelector('.header__button-btn'); //шукаєм кнопку
    if (showcaseButton) {
        showcaseButton.addEventListener('click', function () { //якщо кнопка є то додаєм подію переходу на сторінку upload по кліку
            window.location.href = '/upload';
        });
    }
});