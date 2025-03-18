const ctx = document.getElementById('CpuUsage').getContext('2d');
const cpuChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: Array(30).fill(''), // 30 последних секунд
        datasets: [
            {
                label: 'CPU Load (%)',
                data: Array(30).fill(0),
                borderColor: '#4caf50',
                backgroundColor: 'rgba(76, 175, 80, 0.2)',
                fill: true
            },
            {
                label: 'RAM Usage (%)',
                data: Array(30).fill(0),
                borderColor: '#2196f3',
                backgroundColor: 'rgba(33, 150, 243, 0.2)',
                fill: true
            }
        ]
    },
    options: {
        animation: false,
        responsive: true,
        scales: {
            y: { min: 0, max: 100 }
        }
    }
});

function updateCPU() {
    fetch('/get_hardware_data') // API с данными
        .then(response => response.json())
        .then(data => {
            const cpuLoad = data.CPU;  // Достаем CPU
            const ramUsage = data.RAM; // Достаем RAM

            cpuChart.data.labels.push(''); // Добавляем пустую метку (новая секунда)
            cpuChart.data.labels.shift(); // Удаляем старую

            cpuChart.data.datasets[0].data.push(cpuLoad); // CPU
            cpuChart.data.datasets[0].data.shift();

            cpuChart.data.datasets[1].data.push(ramUsage); // RAM
            cpuChart.data.datasets[1].data.shift();

            cpuChart.update(); // Обновляем график
        });
}

// Запускаем обновление каждую секунду
setInterval(updateCPU, 1500);
