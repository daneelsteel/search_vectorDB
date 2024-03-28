// Файл content.js

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('search-form').addEventListener('submit', function(event) {
        event.preventDefault();

        const searchTerm = document.querySelector('input[name="search_interview"]').value;

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
    });
});
