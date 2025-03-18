function fetchData() {
    fetch("/get_data")
        .then(response => response.json())
        .then(data => {
            document.getElementById("data").innerText = data.data;
        })
        .catch(error => console.error("Ошибка получения данных:", error));
}

setInterval(fetchData, 1000);
