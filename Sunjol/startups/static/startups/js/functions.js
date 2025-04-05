// Анимация загрузки
function showLoading() {
    const loading = document.createElement('div');
    loading.className = 'loading-overlay';
    loading.innerHTML = `
        <div class="loading-spinner">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Загрузка...</span>
            </div>
        </div>
    `;
    document.body.appendChild(loading);
}

function hideLoading() {
    const loading = document.querySelector('.loading-overlay');
    if (loading) {
        loading.remove();
    }
}

// Плавная прокрутка
function smoothScroll(target) {
    const element = document.querySelector(target);
    if (element) {
        element.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

// Анимация появления элементов при прокрутке
function initScrollAnimation() {
    const elements = document.querySelectorAll('.animate-on-scroll');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, {
        threshold: 0.1
    });
    
    elements.forEach(element => {
        observer.observe(element);
    });
}

// Переключение темы
function toggleTheme() {
    const html = document.documentElement;
    const currentTheme = html.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    html.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
}

// Инициализация темы
function initTheme() {
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    const theme = savedTheme || (prefersDark ? 'dark' : 'light');
    document.documentElement.setAttribute('data-theme', theme);
}

// Обработка форм с AJAX
function handleFormSubmit(form, successCallback, errorCallback) {
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        showLoading();
        
        try {
            const formData = new FormData(form);
            const response = await fetch(form.action, {
                method: form.method,
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            
            const data = await response.json();
            
            if (response.ok) {
                if (successCallback) successCallback(data);
            } else {
                if (errorCallback) errorCallback(data);
            }
        } catch (error) {
            if (errorCallback) errorCallback(error);
        } finally {
            hideLoading();
        }
    });
}

// Инициализация всех функций при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    initScrollAnimation();
    
    // Добавление обработчиков для всех форм с классом ajax-form
    document.querySelectorAll('.ajax-form').forEach(form => {
        handleFormSubmit(form, 
            (data) => {
                // Обработка успешного ответа
                console.log('Success:', data);
            },
            (error) => {
                // Обработка ошибки
                console.error('Error:', error);
            }
        );
    });
}); 