FROM python:3.12

# Копирование файлов
WORKDIR /app
COPY . /app

# Установка зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Открытие портов
# WEB
EXPOSE 5001
# UDP
EXPOSE 1201
# TCP
EXPOSE 1202

# Точка входа
CMD ["python3", "main.py"]
