document.addEventListener("DOMContentLoaded", function () {
    console.log("✅ Главная страница загружена!");
    if (window.Telegram && Telegram.WebApp) {
        console.log("✅ Telegram WebApp API подключен");
        const initData = Telegram.WebApp.initDataUnsafe;
        console.log("📦 Данные от Telegram:", initData);
        const HOST_PATH='https://fourpizzabot.com'
        fetch(`${HOST_PATH}/receive_telegram_data`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(initData)
        })
        .then(response => response.json())
        .then(data => console.log("✅ Сервер ответил:", data))
        .catch(error => console.error("❌ Ошибка при отправке:", error));

        // Сохраняем в localStorage
        localStorage.setItem("telegramData", JSON.stringify(initData));
    } else {
        console.warn("⚠️ Telegram WebApp API не подключен!");
    }


    // Логика перехода по картинкам (если нужно)
    document.querySelectorAll(".pizza-list a").forEach(link => {
        link.addEventListener("click", function (event) {
            console.log(`➡️ Переход к пицце: ${this.href}`);
        });
    });
});
