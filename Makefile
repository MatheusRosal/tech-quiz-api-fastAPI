.PHONY: test dev down logs docker-build prod-up prod-down prod-logs ci-local

test:
	pytest -v
dev:
	docker compose up --build

down:
	docker compose down

logs:
	docker compose logs -f

docker-build:
	docker build -t tech-quiz-api .

prod-up:
	docker compose -f docker-compose.yml up --build -d

prod-down:
	docker compose -f docker-compose.yml down

prod-logs:
	docker compose -f docker-compose.yml logs -f

ci-local:
	pytest -v
	docker build -t tech-quiz-api .
	docker compose -f docker-compose.yml up --build -d
	sleep 5
	curl -f http://localhost:8000/health
	docker compose -f docker-compose.yml logs
	docker compose -f docker-compose.yml down

