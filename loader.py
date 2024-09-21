from database import models
from database import crud
from database.db import engine

# Создаем таблицы в бд
models.Base.metadata.create_all(bind=engine)

# Добавляем роли сотрудников в таблицу бд
crud.table_role.add_employee_roles()

# Загружаем сотрудников в бд
crud.table_employee.load_employees()
