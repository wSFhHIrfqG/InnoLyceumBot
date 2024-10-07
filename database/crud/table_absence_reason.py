from database import db
from database import models


def get_all():
	"""Получить все данные из таблицы AbsenceReason"""
	session = db.SessionLocal()
	query = session.query(models.AbsenceReason)

	data = query.filter().all()
	return data


def load_reasons():
	"""
	Добавить причины отсутствия в таблицу AbsenceReason.
	Используется один раз при запуске.
	При использовании таблица со старыми причинами ОЧИЩАЕТСЯ.
	"""
	session = db.SessionLocal()
	reasons = [
		models.AbsenceReason(title="ОРЗ, ОРВИ, ГРИПП", description="ОРЗ, ОРВИ, грипп и аналогичные болезни"),
		models.AbsenceReason(title="Болеет в Лицее", description="До приезда родителей или в изоляторе"),
		models.AbsenceReason(title="По заявлению", description="По заявлению или уважительной причине"),
		models.AbsenceReason(title="Олимпиада", description="Участи в олимпиадах, конкурсах и т.д."),
		models.AbsenceReason(title="Олимпиада в Лицее",
							 description="Участи в олимпиадах, конкурсах и т.д. но находится в Лицее"),
		models.AbsenceReason(title="УТС", description="Уехал на сборы"),
		models.AbsenceReason(title="УТС в Лицее", description="В Лицее на сборах или подготовке"),
		models.AbsenceReason(title="Другое", description="Причина не известна"),
	]
	session.query(models.AbsenceReason).delete()  # Очищаем таблицу
	session.add_all(reasons)  # Загружаем причины
	session.commit()
