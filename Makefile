.PHONY: dev dev-frontend dev-backend install migrate superuser poll clean backend-shell

dev:
	npm run dev

dev-frontend:
	npm run dev -- --filter=@piromail/frontend

dev-backend:
	npm run dev -- --filter=@piromail/backend

install:
	npm install
	cd apps/backend && uv pip install -r pyproject.toml || uv pip install .

migrate:
	cd apps/backend && uv run python manage.py migrate

superuser:
	cd apps/backend && uv run python manage.py createsuperuser

poll:
	cd apps/backend && uv run python manage.py poll_emails

backend-shell:
	cd apps/backend && uv run python manage.py shell

clean:
	rm -rf node_modules apps/frontend/node_modules apps/backend/.venv apps/backend/__pycache__ apps/frontend/dist .turbo

