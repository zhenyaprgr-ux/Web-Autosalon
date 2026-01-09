// Конфигурация
const API_BASE_URL = '/api';

// Иконки для разных марок автомобилей (Font Awesome)
const CAR_ICONS = {
    'toyota': 'fas fa-car',
    'honda': 'fas fa-car',
    'bmw': 'fas fa-car-side',
    'mercedes': 'fas fa-car',
    'audi': 'fas fa-car',
    'ford': 'fas fa-truck-pickup',
    'tesla': 'fas fa-bolt',
    'volkswagen': 'fas fa-bus',
    'default': 'fas fa-car'
};

// Цвета для карточек
const CARD_COLORS = [
    'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
    'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
    'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
    'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
    'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)'
];

// Главная функция инициализации
document.addEventListener('DOMContentLoaded', function() {
    loadCars();
    checkAPIStatus();
});

// Проверка статуса API
async function checkAPIStatus() {
    const statusElement = document.getElementById('apiStatus');
    try {
        const response = await fetch(`${API_BASE_URL}/cars`);
        if (response.ok) {
            statusElement.innerHTML = '<i class="fas fa-circle"></i> Online';
            statusElement.className = 'status-online';
        } else {
            statusElement.innerHTML = '<i class="fas fa-circle"></i> Error';
            statusElement.className = 'status-offline';
        }
    } catch (error) {
        statusElement.innerHTML = '<i class="fas fa-circle"></i> Offline';
        statusElement.className = 'status-offline';
    }
}

// Загрузка всех автомобилей
async function loadCars() {
    const container = document.getElementById('carsContainer');
    container.innerHTML = '<div class="loading"><i class="fas fa-spinner fa-spin"></i> Загрузка автомобилей...</div>';

    try {
        const response = await fetch(`${API_BASE_URL}/cars`);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

        const cars = await response.json();
        displayCars(cars);

        // Обновляем счетчик
        document.getElementById('carCount').textContent = `Найдено автомобилей: ${cars.length}`;

    } catch (error) {
        container.innerHTML = `
            <div class="error-message">
                <i class="fas fa-exclamation-triangle"></i>
                <h3>Ошибка загрузки данных</h3>
                <p>${error.message}</p>
                <button onclick="loadCars()" class="btn btn-search">
                    <i class="fas fa-redo"></i> Попробовать снова
                </button>
            </div>
        `;
        console.error('Error loading cars:', error);
    }
}

// Отображение автомобилей
function displayCars(cars) {
    const container = document.getElementById('carsContainer');

    if (!cars || cars.length === 0) {
        container.innerHTML = `
            <div class="no-cars">
                <i class="fas fa-car-crash"></i>
                <h3>Автомобилей не найдено</h3>
                <p>В каталоге пока нет автомобилей</p>
            </div>
        `;
        return;
    }

    container.innerHTML = '';

    cars.forEach((car, index) => {
        const card = createCarCard(car, index);
        container.appendChild(card);
    });
}

// Создание карточки автомобиля
function createCarCard(car, index) {
    const card = document.createElement('div');
    card.className = 'car-card';

    // Определяем цвет карточки
    const colorIndex = index % CARD_COLORS.length;

    // Определяем иконку по марке
    const carBrand = car.firm.toLowerCase();
    const icon = CAR_ICONS[carBrand] || CAR_ICONS.default;

    card.innerHTML = `
        <div class="car-image" style="background: ${CARD_COLORS[colorIndex]}">
            <i class="${icon}"></i>
            <div class="car-id">ID: ${car.id}</div>
        </div>

        <div class="car-content">
            <div class="car-title">
                <h3>${car.firm} ${car.model}</h3>
                <span class="car-year">${car.year}</span>
            </div>

            <div class="car-specs">
                <div class="spec-item">
                    <span class="spec-label">Мощность:</span>
                    <span class="spec-value">${car.power} л.с.</span>
                </div>
                <div class="spec-item">
                    <span class="spec-label">Цвет:</span>
                    <span class="spec-value">${car.color}</span>
                </div>
                <div class="spec-item">
                    <span class="spec-label">Дилер ID:</span>
                    <span class="spec-value">${car.dealer_id || 'Не указан'}</span>
                </div>
            </div>

            <div class="car-price">
                ${formatPrice(car.price)} $
            </div>

            <div class="car-actions">
                <button onclick="openEditModal(${car.id})" class="btn btn-edit">
                    <i class="fas fa-edit"></i> Редактировать
                </button>
                <button onclick="deleteCar(${car.id}, '${car.firm} ${car.model}')" class="btn btn-delete">
                    <i class="fas fa-trash"></i> Удалить
                </button>
            </div>
        </div>
    `;

    return card;
}

// Форматирование цены
function formatPrice(price) {
    return new Intl.NumberFormat('ru-RU').format(price);
}

// Поиск автомобиля по ID
async function searchCar() {
    const searchId = document.getElementById('searchId').value;

    if (!searchId) {
        showNotification('Введите ID автомобиля для поиска', 'info');
        return;
    }

    const container = document.getElementById('carsContainer');
    container.innerHTML = '<div class="loading"><i class="fas fa-spinner fa-spin"></i> Поиск автомобиля...</div>';

    try {
        const response = await fetch(`${API_BASE_URL}/cars/${searchId}`);

        if (response.status === 404) {
            container.innerHTML = `
                <div class="no-cars">
                    <i class="fas fa-search"></i>
                    <h3>Автомобиль не найден</h3>
                    <p>Автомобиль с ID ${searchId} не существует</p>
                    <button onclick="resetSearch()" class="btn btn-search">
                        <i class="fas fa-redo"></i> Вернуться к списку
                    </button>
                </div>
            `;
            return;
        }

        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

        const car = await response.json();
        displayCars([car]);

        document.getElementById('carCount').textContent = `Найден 1 автомобиль`;
        showNotification(`Найден автомобиль: ${car.firm} ${car.model}`, 'success');

    } catch (error) {
        showNotification(`Ошибка поиска: ${error.message}`, 'error');
        console.error('Error searching car:', error);
    }
}

// Сброс поиска
function resetSearch() {
    document.getElementById('searchId').value = '';
    loadCars();
    showNotification('Отображены все автомобили', 'info');
}

// Открытие модального окна для редактирования
async function openEditModal(carId) {
    try {
        const response = await fetch(`${API_BASE_URL}/cars/${carId}`);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

        const car = await response.json();

        // Заполняем форму данными автомобиля
        document.getElementById('editCarId').value = car.id;
        document.getElementById('editFirm').value = car.firm;
        document.getElementById('editModel').value = car.model;
        document.getElementById('editYear').value = car.year;
        document.getElementById('editPower').value = car.power;
        document.getElementById('editColor').value = car.color;
        document.getElementById('editPrice').value = car.price;
        document.getElementById('editDealerId').value = car.dealer_id || '';

        // Показываем модальное окно
        document.getElementById('editModal').style.display = 'flex';

    } catch (error) {
        showNotification(`Ошибка загрузки данных автомобиля: ${error.message}`, 'error');
    }
}

// Закрытие модального окна
function closeEditModal() {
    document.getElementById('editModal').style.display = 'none';
    document.getElementById('editForm').reset();
}

// Обработка формы редактирования
document.getElementById('editForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const carId = document.getElementById('editCarId').value;
    const carData = {
        firm: document.getElementById('editFirm').value,
        model: document.getElementById('editModel').value,
        year: parseInt(document.getElementById('editYear').value),
        power: parseInt(document.getElementById('editPower').value),
        color: document.getElementById('editColor').value,
        price: parseFloat(document.getElementById('editPrice').value),
        dealer_id: document.getElementById('editDealerId').value || null
    };

    try {
        const response = await fetch(`${API_BASE_URL}/cars/${carId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(carData)
        });

        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

        const updatedCar = await response.json();

        closeEditModal();
        showNotification(`Автомобиль ${updatedCar.firm} ${updatedCar.model} успешно обновлен!`, 'success');

        // Обновляем список автомобилей
        setTimeout(() => {
            if (document.getElementById('searchId').value) {
                searchCar();
            } else {
                loadCars();
            }
        }, 500);

    } catch (error) {
        showNotification(`Ошибка обновления: ${error.message}`, 'error');
    }
});

// Удаление автомобиля
async function deleteCar(carId, carName) {
    if (!confirm(`Вы уверены, что хотите удалить автомобиль "${carName}"?`)) {
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/cars/${carId}`, {
            method: 'DELETE'
        });

        if (response.status === 204) {
            showNotification(`Автомобиль "${carName}" успешно удален!`, 'success');

            // Обновляем список автомобилей
            setTimeout(() => {
                if (document.getElementById('searchId').value) {
                    searchCar();
                } else {
                    loadCars();
                }
            }, 500);

        } else {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

    } catch (error) {
        showNotification(`Ошибка удаления: ${error.message}`, 'error');
    }
}

// Показ уведомлений
function showNotification(message, type = 'info') {
    const notification = document.getElementById('notification');

    notification.textContent = message;
    notification.className = `notification ${type}`;
    notification.style.display = 'block';

    // Автоматическое скрытие через 5 секунд
    setTimeout(() => {
        notification.style.display = 'none';
    }, 5000);
}

// Закрытие модального окна по клику вне его
window.onclick = function(event) {
    const modal = document.getElementById('editModal');
    if (event.target === modal) {
        closeEditModal();
    }
};

// Обработка нажатия Enter в поле поиска
document.getElementById('searchId').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        searchCar();
    }
});