document.addEventListener("DOMContentLoaded", function () {
    console.log("Скрипт загружен, начинаем выполнение...");
    // Ожидаем небольшую задержку, чтобы убедиться, что все элементы загружены
    setTimeout(() => {
        const decreaseBtn = document.querySelector("#decrease");
        const increaseBtn = document.querySelector("#increase");
        const quantitySpan = document.querySelector("#quantity");
        const priceElement = document.querySelector("#price");
        const addToCartBtn = document.querySelector("#add-to-cart");
        const confirmOrderBtn = document.querySelector("#confirm-order");
        if (!decreaseBtn || !increaseBtn || !quantitySpan || !priceElement || !addToCartBtn) {
            console.error("❌ Ошибка: Один из элементов не найден на странице!");
            return;
        }

        const telegramData = localStorage.getItem("telegramData");
    let user_id = 1
    if (telegramData) {
        const userData = JSON.parse(telegramData);
        console.log("📦 Восстановленные данные от Telegram: ", userData);
        user_id = userData.user.id
    }


        let pricePizzaElement = document.querySelector("#price");
        let basePrice = parseFloat(pricePizzaElement.getAttribute("data-price")); // Берём цену из HTML
        let quantity = 1;
        const BASE_URL = "https://fe2d-2a00-20-5-96e1-a933-df32-3f83-7e19.ngrok-free.app";

        decreaseBtn.addEventListener("click", function () {
            if (quantity > 1) {
                quantity--;
                quantitySpan.textContent = quantity;
                priceElement.textContent = (basePrice * quantity).toFixed(2) + "€";
            }
        });
        increaseBtn.addEventListener("click", function () {
            quantity++;
            quantitySpan.textContent = quantity;
            priceElement.textContent = (basePrice * quantity).toFixed(2) + "€"; // Округление до сотых
        });


        addToCartBtn.addEventListener("click", function (event) {
    event.preventDefault(); // Предотвращает повторную отправку формы, если вдруг она есть

    if (addToCartBtn.disabled) return; // Если кнопка уже нажата, не выполняем код
    addToCartBtn.disabled = true;

    const pizzaId = addToCartBtn.getAttribute("data-pizza-id");
    if (!pizzaId) {
        console.error("❌ Ошибка: ID пиццы не найден!");
        alert("Ошибка: ID пиццы не найден!");
        addToCartBtn.disabled = false;
        return;
    }

    let pizzaName = document.querySelector(".pizza-title").textContent;
    let pizzaPrice = parseFloat(document.querySelector("#price").getAttribute("data-price"));
    let quantity = parseInt(document.querySelector("#quantity").textContent); // Количество

    function addToCart(pizzaName, pizzaPrice, quantity) {
        let frontSrotage = JSON.parse(localStorage.getItem("cart")) || []; // Загружаем корзину из localStorage
    let item = frontSrotage.find(p => p.name === pizzaName); // Ищем пиццу в корзине
    if (item) {
        item.quantity += quantity; // Если уже есть, увеличиваем количество
    } else {
        frontSrotage.push({ name: pizzaName, quantity: quantity, price:pizzaPrice}); // Иначе добавляем новый товар
    }
    localStorage.setItem("cart", JSON.stringify(frontSrotage)); // Сохраняем обратно в localStorage
    console.log("Корзина обновлена:", frontSrotage); // Проверяем в консоли
}
    console.log(`🍕 Добавляем пиццу (ID: ${pizzaId}, ${pizzaName}, ${pizzaPrice} €, ${quantity} шт.) в корзину...`);


    addToCart(pizzaName, pizzaPrice, quantity);  // [{'name': 'Маргарита', 'quantity': 1, 'price': 15}]

    //alert("Добавлено в корзину! Открываю консоль...");
    fetch(`${BASE_URL}/add-to-cart`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ pizza_id: pizzaId, quantity: quantity, price:pizzaPrice, user_id:user_id })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log("✅ Пицца добавлена в корзину!");
            setTimeout(() =>

                window.location.href = `/cart?user_id=${user_id}`, 500); // Добавляем задержку


        } else {
            console.error("❌ Ошибка сервера:", data.error);
            alert("95 Ошибка при добавлении в корзину!");
            addToCartBtn.disabled = false;
        }
    })
    .catch(error => {
        console.error("❌ Ошибка сети:", error);
        alert("101 Ошибка сети при отправке запроса!");
        addToCartBtn.disabled = false;
    });
});


        // Подтверждение заказа
        if (confirmOrderBtn) {
            confirmOrderBtn.addEventListener("click", function () {
                fetch(`${BASE_URL}/confirm_order`, { method: "POST" })
                .then(response => {
                    if (response.ok) {
                        window.location.href = "/";  // Переход на главную
                    }
                });
            });
        }

        console.log("✅ Скрипт успешно загружен и готов к работе!");
    }, 500);  // Дадим 500мс на загрузку страницы
});



