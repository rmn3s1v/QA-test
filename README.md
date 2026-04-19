# Avito QA Internship — API Tests

## Описание
Проект содержит решение первой задачи и автоматизированные тесты для API микросервиса объявлений.

Покрытие:
- Позитивные сценарии
- Негативные сценарии
- Корнер-кейсы
- E2E сценарии
- Нефункциональные проверки
---
## Технологии
- Python 3
- pytest
- requests
- allure
---

## Как протестить
```bash
git clone <repo>
cd <repo>
pip install -r requirements.txt
pytest test/test_api.py -v
