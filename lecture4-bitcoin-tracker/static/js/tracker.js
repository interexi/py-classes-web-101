// Initialize chart / Ініціалізація графіку
let priceChart;
const priceHistory = [];
const timeHistory = [];

// Create chart function / Функція створення графіку
function createChart() {
    const ctx = document.getElementById('priceChart').getContext('2d');
    priceChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: timeHistory,
            datasets: [{
                label: 'Bitcoin Price (USD)',
                data: priceHistory,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: false
                }
            }
        }
    });
}

// Update price function / Функція оновлення ціни
async function updatePrice() {
    try {
        const response = await fetch('/api/price');
        const data = await response.json();
        
        // Update price display / Оновлення відображення ціни
        document.getElementById('currentPrice').textContent = `$${data.price.toFixed(2)}`;
        document.getElementById('lastUpdated').textContent = new Date(data.timestamp).toLocaleString();
        
        // Update chart / Оновлення графіку
        priceHistory.push(data.price);
        timeHistory.push(new Date(data.timestamp).toLocaleTimeString());
        
        // Keep only last 20 points / Зберігати тільки останні 20 точок
        if (priceHistory.length > 20) {
            priceHistory.shift();
            timeHistory.shift();
        }
        
        priceChart.update();
    } catch (error) {
        console.error('Error fetching price:', error);
    }
}

// Initialize on page load / Ініціалізація при завантаженні сторінки
document.addEventListener('DOMContentLoaded', () => {
    createChart();
    updatePrice();
    // Update every 15 seconds / Оновлення кожні 15 секунд
    setInterval(updatePrice, 15000);
}); 