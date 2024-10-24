# InnoLyceumBot

Бот помощник для ГАОУ "Лицей Иннополис"

![Static Badge](https://img.shields.io/badge/release-v0.1-blue)
## Функции

- Учителя могут отмечать отсутствующих
- Отчеты об отсутствующих отправляются в чат администраторам
## Переменные окружения

Чтобы запустить бота, вам нужно добавить следующие переменные окружения в файл .env

`TOKEN` Токен бота, полученный от BotFather  
`SUPER_ADMIN_TELEGRAM_ID` Telegram ID главного администратора  

`DATABASE_NAME ` Имя файла базы данных  
`EMPLOYEE_DATA_FILENAME` Имя файла с данными о сотрудниках. Должен находиться в папке input  
`STUDENT_DATA_FILENAME` Имя файла с данными об учениках. Должен находиться в папке input'  
`ABSENT_REPORT_TEMPLATE_FILENAME ` Имя файла с шаблоном отчета об отсутствующих. Должен находиться в папке input  
## Подготовка к запуску

- Добавьте excel файлы с сотрудниками и учениками в папку input проекта и загрузите в них данные. Имена файлов сохраните в переменных окружения  
- Проверьте шаблон  отчета в папке input  
- Убедитесь, что все уникальные должности сотрудников в excel файле будут сохранены в таблице Role при запуске (См. InnoLyceumBot/database/crud/table_role) 
- Для корректной id каждой "роли" из таблицы Role должен быть добавлен в одну из групп ADMIN_ROLES, TEACHER_ROLES, EMPLOYEE_ROLES (См. InnoLyceumBot/config_data/roles)