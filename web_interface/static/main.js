//MC DATA

//function fetchData() {
//    fetch("/get_data")
//        .then(response => response.json())
//        .then(data => {
//            document.getElementById("data").innerText = data.data;
//        })
//        .catch(error => console.error("Ошибка получения данных:", error));
//}

//setInterval(fetchData, 1000);


//HARDWARE DATA

function updateHardwareData() {
    // Отправляем GET-запрос к серверу по маршруту "/get_hardware_data"
    fetch("/get_hardware_data")
        .then(response => response.json())  // Преобразуем полученный ответ в JSON
        .then(data => {
            // Обновляем текст элемента <p> с id "cpu-info", вставляя туда данные о загрузке CPU
            document.getElementById("cpu").innerText = "CPU: " + data.CPU + " %";
            
            // Обновляем текст элемента <p> с id "ram-info", вставляя туда данные об используемой RAM
            document.getElementById("ram").innerText = "RAM: " + data.RAM + " %";
        })
}


//UPTIME DATA

function updateUptimeData() {
    // Отправляем GET-запрос к серверу по маршруту "/get_hardware_data"
    fetch("/get_uptime_data")
        .then(response => response.json())  // Преобразуем полученный ответ в JSON
        .then(data => {
            // Обновляем текст элемента <p> с id "cpu-info", вставляя туда данные о загрузке CPU
            document.getElementById("uptime").innerText = "Uptime: " + data.h + " " + data.m;
        })
}


function updateHostsData() {
    // Отправляем GET-запрос к серверу по маршруту "/get_hardware_data"
    fetch("/get_hosts_data")
        .then(response => response.json())  // Преобразуем полученный ответ в JSON
        .then(data => {
            // Обновляем текст элемента <p> с id "cpu-info", вставляя туда данные о загрузке CPU
            document.getElementById("flaskhost").innerText = "Flask Host: " + data.flhost;
            document.getElementById("mcishost").innerText = "MCIS Host: " + data.srvhost;
        })
}


function updateNetworkData() {
    // Отправляем GET-запрос к серверу по маршруту "/get_hardware_data"
    fetch("/get_network_data")
        .then(response => response.json())  // Преобразуем полученный ответ в JSON
        .then(data => {
            // Обновляем текст элемента <p> с id "cpu-info", вставляя туда данные о загрузке CPU
            document.getElementById("download").innerText = "Download: " + data.download;
            document.getElementById("upload").innerText = "Upload: " + data.upload;
        })
}

//mainloop modules
// Устанавливаем автоматическое обновление данных каждые 5 секунд (5000 миллисекунд)
setInterval(updateHardwareData, 5000);
setInterval(updateUptimeData, 60000);
setInterval(updateNetworkData, 1000)
//start
// Вызываем функцию сразу после загрузки страницы, чтобы данные отобразились без ожидания
updateNetworkData
updateHostsData();
updateHardwareData();
updateUptimeData();

