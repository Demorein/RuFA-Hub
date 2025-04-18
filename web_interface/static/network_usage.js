const netCtx = document.getElementById('NetworkUsage').getContext('2d');
const networkChart = new Chart(netCtx, {
    type: 'line',
    data: {
        labels: Array(30).fill(''), // 30 последних секунд
        datasets: [
            {
                label: 'Download',
                data: Array(30).fill(0),
                borderColor: 'rgb(76, 139, 175)',
                backgroundColor: 'rgba(76, 139, 175, 0.2)',
                fill: true
            },
            {
                label: 'Upload',
                data: Array(30).fill(0),
                borderColor: 'rgba(243, 33, 33, 1)',
                backgroundColor: 'rgba(243, 33, 33, 0.2)',
                fill: true
            }
        ]
    },
    options: {
        animation: false,
        responsive: true,
        scales: {
            y: { min: 0, max: 300 }
        }
    }
});

function updateNetwork() {
    fetch('/get_network_data') // API с данными
        .then(response => response.json())
        .then(data => {
            const download = data.download;
            const upload = data.upload;

            networkChart.data.labels.push('');
            networkChart.data.labels.shift();

            networkChart.data.datasets[0].data.push(download);
            networkChart.data.datasets[0].data.shift();

            networkChart.data.datasets[1].data.push(upload);
            networkChart.data.datasets[1].data.shift();

            networkChart.update();
        });
}

// Запускаем обновление каждые 1.5 секунды
setInterval(updateNetwork, 1500);
