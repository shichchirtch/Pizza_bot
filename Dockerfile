FROM python:3.11.7
# Обновляем пакеты и устанавливаем зависимости
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*
# Устанавливаем Node.js (обновлённую версию)
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs
# Проверка установки Node.js и npm
RUN node -v && npm -v
# Устанавливаем рабочую директорию
WORKDIR /bot
# Копируем файл зависимостей и устанавливаем Python-пакеты
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Копируем весь код проекта
COPY ./bot .
# Запускаем бота
CMD ["python", "main.py"]
