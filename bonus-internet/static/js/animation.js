document.addEventListener('DOMContentLoaded', () => {
    const sendRequestBtn = document.getElementById('sendRequest');
    const packet = document.getElementById('packet');
    const requestData = document.getElementById('requestData');
    const responseData = document.getElementById('responseData');
    const browserDisplay = document.getElementById('browserDisplay');
    const steps = document.querySelectorAll('.step');

    // Example requests to demonstrate / Приклади запитів для демонстрації
    const requests = [
        {
            url: 'https://example.com',
            method: 'GET',
            headers: {
                'Accept': 'text/html',
                'User-Agent': 'Demo Browser'
            }
        },
        {
            url: 'https://api.example.com/data',
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: {
                name: 'User',
                action: 'demo'
            }
        }
    ];

    let currentRequestIndex = 0;

    // Format request/response for display / Форматування запиту/відповіді для відображення
    function formatData(data) {
        return JSON.stringify(data, null, 2);
    }

    // Highlight active step / Підсвічування активного кроку
    function highlightStep(index) {
        steps.forEach(step => step.classList.remove('highlight'));
        if (steps[index]) {
            steps[index].classList.add('highlight');
        }
    }

    // Simulate request-response cycle / Симуляція циклу запит-відповідь
    async function simulateRequest() {
        const request = requests[currentRequestIndex];
        
        // Step 1: Show request / Крок 1: Показати запит
        highlightStep(0);
        requestData.querySelector('.code-block').textContent = formatData(request);
        responseData.querySelector('.code-block').textContent = '';
        browserDisplay.innerHTML = 'Sending request... / Надсилання запиту...';

        // Step 2: Animate packet to server / Крок 2: Анімація пакету до сервера
        packet.style.left = '0';
        packet.classList.add('sending');
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // Step 3: Server processing / Крок 3: Обробка на сервері
        highlightStep(1);
        await new Promise(resolve => setTimeout(resolve, 1000));

        // Step 4: Generate response / Крок 4: Генерація відповіді
        highlightStep(2);
        const response = {
            status: 200,
            headers: {
                'Content-Type': request.headers['Accept'],
                'Server': 'Demo Server'
            },
            body: request.method === 'GET' 
                ? '<h1>Welcome to Example.com</h1><p>This is a demo page.</p>'
                : { message: 'Success', data: { id: 123 } }
        };

        // Step 5: Send response back / Крок 5: Надсилання відповіді
        packet.classList.remove('sending');
        packet.classList.add('receiving');
        responseData.querySelector('.code-block').textContent = formatData(response);
        await new Promise(resolve => setTimeout(resolve, 1000));

        // Step 6: Display in browser / Крок 6: Відображення у браузері
        highlightStep(3);
        browserDisplay.innerHTML = response.headers['Content-Type'].includes('html')
            ? response.body
            : `<pre>${formatData(response.body)}</pre>`;

        // Reset animations / Скидання анімацій
        packet.classList.remove('receiving');
        currentRequestIndex = (currentRequestIndex + 1) % requests.length;
    }

    // Add click handler / Додавання обробника кліків
    sendRequestBtn.addEventListener('click', () => {
        sendRequestBtn.disabled = true;
        simulateRequest().then(() => {
            sendRequestBtn.disabled = false;
        });
    });
}); 