from database import models
from database.db import engine

# Создаем таблицы в бд
models.Base.metadata.create_all(bind=engine)
