// Function to handle form submission
document.getElementById("addDeviceForm").addEventListener("submit", function(event) {
    event.preventDefault();

    const ip = document.getElementById("ip").value;
    const port = document.getElementById("port").value;

    // Basic validation
    if (!ip || !port) {
        document.getElementById("formAlert").textContent = "Пожалуйста, введите оба значения!";
        return;
    }

    // Send the data to the server (via AJAX or WebSocket)
    addDeviceToServer(ip, port);
});

// Function to add device to the server
function addDeviceToServer(ip, port) {
    // Example using Fetch API (you could also use WebSocket or another method)
    fetch('/add_device', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ ip, port })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Устройство добавлено успешно!");
            loadDevices();  // Reload device list
            document.getElementById("formAlert").textContent = "";
        } else {
            document.getElementById("formAlert").textContent = "Ошибка при добавлении устройства.";
        }
    })
    .catch(error => {
        document.getElementById("formAlert").textContent = "Ошибка связи с сервером.";
    });
}

// Function to load the list of devices from the server
function loadDevices() {
    // Fetch the device list from the server (Example)
    fetch('/get_devices')
        .then(response => response.json())
        .then(devices => {
            const tableBody = document.getElementById("devicesTable").getElementsByTagName('tbody')[0];
            tableBody.innerHTML = "";  // Clear current table
            devices.forEach(device => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${device.ip}</td>
                    <td>${device.port}</td>
                    <td><button onclick="deleteDevice('${device.ip}', ${device.port})">Удалить</button></td>
                `;
                tableBody.appendChild(row);
            });
        });
}

// Function to delete device
function deleteDevice(ip, port) {
    // Send delete request to the server
    fetch('/delete_device', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ ip, port })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Устройство удалено!");
            loadDevices();  // Reload device list
        } else {
            alert("Ошибка при удалении устройства.");
        }
    });
}

// Load devices when the page is loaded
window.onload = loadDevices;