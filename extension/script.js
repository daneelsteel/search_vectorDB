// Файл script.js

// Отправка POST-запроса на Flask-сервер в Docker-контейнере
fetch('/search', {
    method: 'POST',
    body: JSON.stringify({'search_interview': searchTerm}),
    headers: {
        'Content-Type': 'application/json'
    }
})
.then(response => response.json())
.then(data => {
    // Обработка результатов поиска
    console.log(data);
})
.catch(error => console.error('Error:', error));
