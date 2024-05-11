# ипользуемый образ (OS) +  установленный Python
FROM python:3.12-slim

# установка библиотек при помощи команды pip3 install
RUN pip3 install Flask-login
RUN pip3 install Flask-SQLAlchemy

# переместить все что находится в папке, где находится
# данный Dockerfile в ууказанную директорию контейнера
COPY . /opt/app

# переход на указнаную директорию
# для выполнения след. команды
WORKDIR /opt/app

# команда выполняемая при запуске контейнера
CMD ["python", "./app.py"]