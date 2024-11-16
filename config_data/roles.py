# Для корректной работы role_id каждой роли должен быть добавлен хотя бы в одну из групп ниже
ADMIN_ROLES = [1, 2]  # role_id администраторов
TEACHER_ROLES = [3, 4, 5, 6, 7]  # role_id учителей
EMPLOYEE_ROLES = [4, 5, 8]  # role_id сотрудников

ROLES = [
	{
		'role_id': 1,
		'title': 'Директор',
		'description': 'Директор лицея'
	},
	{
		'role_id': 2,
		'title': 'Заместитель директора',
		'description': 'Заместитель директора'
	},
	{
		'role_id': 3,
		'title': 'Учитель',
		'description': 'Учитель'},
	{
		'role_id': 4,
		'title': 'Заведующий библиотекой',
		'description': 'Заведующий библиотекой'},
	{
		'role_id': 5,
		'title': 'Воспитатель',
		'description': 'Воспитатель'},
	{
		'role_id': 6,
		'title': 'Классный руководитель',
		'description': 'Классный руководитель'},
	{
		'role_id': 7,
		'title': 'Педагог-психолог',
		'description': 'Педагог-психолог'},
	{
		'role_id': 8,
		'title': 'Тех. персонал',
		'description': 'Технический персонал'}
]
