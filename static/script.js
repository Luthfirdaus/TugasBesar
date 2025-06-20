let dataKelembapan = [];
let threshold = 40;

document.addEventListener("DOMContentLoaded", async function () {
    const ctx = document.getElementById('moistureChart').getContext('2d');
    const currentMoisture = document.getElementById('currentMoisture');
    const wateringStatus = document.getElementById('wateringStatus');
    const autoCheckbox = document.getElementById('autoMode');
    const manualCheckbox = document.getElementById('manualMode');
    const thresholdValue = document.getElementById('thresholdValue');

    async function ambilDataSensor() {
        const res = await fetch('/api/data');
        const json = await res.json();
        dataKelembapan = json.data || [];
        return dataKelembapan[dataKelembapan.length - 1] || 0;
    }

    const currentValue = await ambilDataSensor();
    currentMoisture.innerText = currentValue;

    const chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: dataKelembapan.map(() => ''),
            datasets: [{
                label: 'Kelembapan Sensor (%)',
                data: dataKelembapan,
                borderColor: 'blue',
                backgroundColor: 'rgba(0,0,255,0.1)',
                fill: true,
                tension: 0.4,
                pointBackgroundColor: dataKelembapan.map(val => val < threshold ? 'red' : 'blue')
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: { beginAtZero: true, max: 100 },
                x: { ticks: { display: false } }
            }
        }
    });

    function updateWateringStatus() {
        const isAuto = autoCheckbox.checked;
        const isManual = manualCheckbox.checked;
        const isKering = dataKelembapan[dataKelembapan.length - 1] > threshold;

        if ((isAuto && isKering) || isManual) {
            wateringStatus.style.color = 'red';
        } else {
            wateringStatus.style.color = '#f0f0f0';
        }
    }

    function updateStatusKeServer() {
        fetch('/api/status', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                auto: autoCheckbox.checked,
                manual: manualCheckbox.checked
            })
        });
    }

    autoCheckbox.addEventListener('change', function () {
        manualCheckbox.disabled = this.checked;
        updateWateringStatus();
        updateStatusKeServer();
    });

    manualCheckbox.addEventListener('change', function () {
        updateWateringStatus();
        updateStatusKeServer();
    });

    window.changeThreshold = function (val) {
        threshold += val;
        thresholdValue.innerText = threshold;
        chart.data.datasets[0].pointBackgroundColor = dataKelembapan.map(val => val < threshold ? 'red' : 'blue');
        chart.update();
        updateWateringStatus();
    };

    updateWateringStatus();
});
