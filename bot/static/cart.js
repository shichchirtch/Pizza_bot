document.addEventListener("DOMContentLoaded", function () {
    const orderForm = document.getElementById("orderForm");
    const resetOrder = document.getElementById("resetOrder");
    const HOST_PATH = "https://f777-2a00-20-5-96e1-b54a-9741-728d-21ea.ngrok-free.app";

    if (!orderForm || !resetOrder) {
        console.error("Ошибка: Не найден один из элементов формы заказа!");
        return;
    }

    orderForm.addEventListener("submit", function (event) {
        event.preventDefault();

        const telegramData = JSON.parse(localStorage.getItem("telegramData")) || {};
        const name = telegramData.user.first_name || "Неизвестный пользователь";
        const user_id = telegramData.user.id;

        const address = document.getElementById("address").value;
        const phone = document.getElementById("phone").value;
        const payment = document.getElementById("payment").value;
        const cartItems = JSON.parse(localStorage.getItem("cart")) || []; // получаю корзину из локального хранилища
        console.log(`➡️ В локал-сторадж по ключу cart : ${cartItems}`);
        if (cartItems.length === 0) {
            alert("Корзина пуста! Добавьте товары перед заказом.");
            return;
        }

        if (!/\D/.test(address) || address.length < 10) {
            alert("Адрес должен содержать хотя бы одну букву и быть не короче 10 символов.");
            return;
        }

        if (!/^\+?\d[\d\s]{11,13}$/.test(phone)) {
            alert("Телефон должен содержать только цифры и знак +, длиной от 12 до 14 символов.");
            return;
        }

        fetch(`${HOST_PATH}/cart`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, user_id, address, phone, payment, order: cartItems })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                //alert("Заказ успешно оформлен!");
                localStorage.removeItem("cart");
                window.location.href = "/";
            } else {
                alert("50 Ошибка: " + data.error);
            }
        })
        .catch(() => {
            alert("54 Ошибка сети при отправке заказа!");
        });
    });

    resetOrder.addEventListener("click", function (event) {
        event.preventDefault();

        const telegramData = JSON.parse(localStorage.getItem("telegramData")) || {};
        const user_id = telegramData.user.id;

        fetch(`${HOST_PATH}/reset-cart`, { method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({user_id})
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                localStorage.removeItem("cart");
                alert("Заказ отменен. Возвращаемся в меню.");
                window.location.href = "/";
            } else {
                alert("69 Ошибка при очистке корзины!");
            }
        })
        .catch(() => {
            alert("73 Ошибка сети при очистке корзины!");
        });
    });
});




