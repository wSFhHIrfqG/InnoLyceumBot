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
		models.AbsenceReason(title="ОРЗ, ОРВИ, ГРИПП", description="ОРЗ, ОРВИ, грипп и аналогичные болезни",
							 in_lyceum=False),
		models.AbsenceReason(title="Болеет в Лицее", description="До приезда родителей или в изоляторе",
							 in_lyceum=True),
		models.AbsenceReason(title="По заявлению", description="По заявлению или уважительной причине",
							 in_lyceum=False),
		models.AbsenceReason(title="Олимпиада", description="Участи в олимпиадах, конкурсах и т.д.",
							 in_lyceum=False),
		models.AbsenceReason(title="Олимпиада в Лицее",
							 description="Участи в олимпиадах, конкурсах и т.д. но находится в Лицее",
							 in_lyceum=True),
		models.AbsenceReason(title="УТС", description="Уехал на сборы",
							 in_lyceum=False),
		models.AbsenceReason(title="УТС в Лицее", description="В Лицее на сборах или подготовке",
							 in_lyceum=True),
		models.AbsenceReason(title="Мероприятия вне лицея",
							 description="Конференции, соревнования, мероприятия вне лицея",
							 in_lyceum=False),
		models.AbsenceReason(title="Другое", description="Причина не известна", in_lyceum=False),
	]
	session.query(models.AbsenceReason).delete()  # Очищаем таблицу
	session.add_all(reasons)  # Загружаем причины
	session.commit()


def get_reason(reason_id: int):
	session = db.SessionLocal()
	query = session.query(models.AbsenceReason)
	return query.filter(models.AbsenceReason.reason_id == reason_id).one_or_none()
