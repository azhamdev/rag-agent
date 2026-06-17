dev:
	uv run uvicorn app.main:app --reload

worker:
# 	uv run celery -A app.worker.celery_app worker --loglevel=info
	uv run celery -A app.worker.celery_app worker --loglevel=info --pool=solo

format:
	uv run ruff format .
	uv run ruff check . --fix