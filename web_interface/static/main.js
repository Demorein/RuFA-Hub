function fetchData() {
    fetch("/get_data")
        .then(response => response.json())
        .then(data => {
            document.getElementById("data").innerText = data.data;
        })
        .catch(error => console.error("Ошибка получения данных:", error));
}

setInterval(fetchData, 1000);

function updateHardwareData() {
    // Отправляем GET-запрос к серверу по маршруту "/get_hardware_data"
    fetch("/get_hardware_data")
        .then(response => response.json())  // Преобразуем полученный ответ в JSON
        .then(data => {
            // Обновляем текст элемента <p> с id "cpu-info", вставляя туда данные о загрузке CPU
            document.getElementById("cpu").innerText = "CPU: " + data.CPU + "%";
            
            // Обновляем текст элемента <p> с id "ram-info", вставляя туда данные об используемой RAM
            document.getElementById("ram").innerText = "RAM: " + data.RAM + " MB";
        })
        .catch(error => console.error("Ошибка загрузки данных:", error)); // Вывод ошибки в консоль, если запрос не удался
}

// Устанавливаем автоматическое обновление данных каждые 5 секунд (5000 миллисекунд)
setInterval(updateHardwareData, 5000);

// Вызываем функцию сразу после загрузки страницы, чтобы данные отобразились без ожидания
updateHardwareData();

