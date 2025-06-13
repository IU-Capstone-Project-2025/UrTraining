# Активируем виртуальное окружение

python -m venv venv
venv/Scripts/activate

# Закачиваем зависимости

pip install -r requirements.txt

# Запускаем сервак

uvicorn main:app --reload

# Радуемся жизни и переходим на http://localhost:8000/