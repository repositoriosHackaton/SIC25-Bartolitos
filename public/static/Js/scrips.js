// Esperar a que el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', function() {
    // Manejador de cambio entre formularios
    document.querySelectorAll('.toggle-button').forEach(button => {
        button.addEventListener('click', () => {
            const formId = button.getAttribute('data-form');
            const targetForm = document.getElementById(formId);
            updateResultSection(-1);
            
            // Ocultar todos los formularios y remover active de los botones
            document.querySelectorAll('.formulario').forEach(form => {
                form.style.display = 'none';
                form.classList.remove('active');
            });
            document.querySelectorAll('.toggle-button').forEach(btn => {
                btn.classList.remove('active');
            });
            
            // Mostrar el formulario seleccionado y activar el botón
            if (targetForm) {
                targetForm.style.display = 'grid';
                targetForm.classList.add('active');
                button.classList.add('active');
            }
        });
    });

    // Manejador de previsualización de imagen
    const imageInput = document.getElementById('imageInput');
    if (imageInput) {
        imageInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    document.getElementById('uploadPreview').src = e.target.result;
                }
                reader.readAsDataURL(file);
            }
        });
    }

    // Manejador para limpiar imagen
    const clearImageBtn = document.querySelector('.clear-image');
    if (clearImageBtn) {
        clearImageBtn.addEventListener('click', function() {
            document.getElementById('imageInput').value = '';
            document.getElementById('uploadPreview').src = imagePaths.preview;
            updateResultSection(-1);
        });
    }

    // Manejador del formulario de predicción manual
    const weatherForm = document.querySelector("#weatherForm");
    if (weatherForm) {
        weatherForm.addEventListener("submit", function (event) {
            event.preventDefault();  
            const formData = new FormData(this);

            fetch("/predict", {
                method: "POST",
                body: formData,
            })
            .then(response => response.json()) 
            .then(data => {
                updateResultSection(data.result);
            })
            .catch(error => {
                console.error("Error:", error);
            });
        });
    }

    // Manejador del formulario de predicción por imagen
    const imageForm = document.querySelector("#imageForm");
    if (imageForm) {
        imageForm.addEventListener("submit", function (event) {
            event.preventDefault();  
            const formData = new FormData(this);

            fetch("/predict_image", {
                method: "POST",
                body: formData,
            })
            .then(response => response.json()) 
            .then(data => {
                updateResultSection(data.result);
            })
            .catch(error => {
                console.error("Error:", error);
            });
        });
    }

    // Manejador para el botón de limpiar del formulario manual
    const clearButton = document.getElementById("clearButton");
    if (clearButton) {
        clearButton.addEventListener("click", function () {
            weatherForm.reset();
            updateResultSection(-1);
        });
    }

    // Función para actualizar la sección de resultados
    function updateResultSection(result) {
        const resultSection = document.querySelector(".resultados");
        if (!resultSection) return;

        if (result === -1) {
            resultSection.innerHTML = `
                <div>
                    <h3>¿Deseas saber el clima?</h3>
                </div>
                <img src="${imagePaths.preview}" alt="Gato clima">
                <p>Ingresa los datos solicitados y presiona el botón "Predecir"</p>
            `;
        } else if (result === 0) {
            resultSection.innerHTML = `
                <h1>El clima es <strong>Lluvioso</strong></h1>
                <img src="${imagePaths.rainy}" alt="Gato lluvioso">
                <p>Los días de lluvia son perfectos para jugar dentro de casa. Usa juguetes que imiten el movimiento de presas, como plumas o pelotas que reboten, para mantener a tu gato entretenido.</p>
            `;
        } else if (result === 1) {
            resultSection.innerHTML = `
                <h1>El clima está <strong>Nublado</strong></h1>
                <img src="${imagePaths.cloudy}" alt="Gato nublado">
                <p>Si a tu gato le gusta salir, un día nublado puede ser ideal para dar un paseo corto con arnés y correa. La luz difusa y la temperatura fresca son cómodas para explorar sin el riesgo de quemaduras solares.</p>
            `;
        } else if (result === 2) {
            resultSection.innerHTML = `
                <h1>El clima está <strong>Soleado</strong></h1>
                <img src="${imagePaths.sunny}" alt="Gato soleado">
                <p><strong>Aprovecha el sol para jugar con tu gato en áreas sombreadas, como bajo un árbol o en una terraza cubierta. Usa juguetes interactivos, como cañas con plumas o láser, para mantenerlo activo sin exponerlo demasiado al calor.</strong></p>
            `;
        } else {
            resultSection.innerHTML = `
                <h1>Está <strong>Nevando</strong></h1>
                <img src="${imagePaths.snowy}" alt="Gato Nevado">
                <p>Si tu gato está acostumbrado al frío, puedes llevarlo afuera por cortos períodos con un suéter o abrigo para gatos (si lo tolera). Asegúrate de secarlo bien al regresar.</p>
            `;
        }
    }
});
