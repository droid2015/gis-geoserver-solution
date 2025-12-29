.PHONY: help setup start stop restart logs clean test seed

help:
	@echo "GIS GeoServer Solution - Available Commands"
	@echo ""
	@echo "  make setup      - Initial setup (copy .env, create directories)"
	@echo "  make start      - Start all services"
	@echo "  make stop       - Stop all services"
	@echo "  make restart    - Restart all services"
	@echo "  make logs       - View logs (tail -f)"
	@echo "  make clean      - Stop and remove volumes"
	@echo "  make test       - Run backend tests"
	@echo "  make seed       - Seed sample data"
	@echo ""

setup:
	@echo "Setting up GIS GeoServer Solution..."
	@cp -n .env.example .env || true
	@mkdir -p pgdata geoserver_data uploads
	@echo "✅ Setup complete!"
	@echo "📝 Edit .env file if needed, then run: make start"

start:
	@echo "Starting services..."
	@docker-compose up -d
	@echo "⏳ Waiting for services to be ready..."
	@sleep 10
	@echo "✅ Services started!"
	@echo ""
	@echo "🌐 Frontend: http://localhost:3000"
	@echo "📡 Backend API: http://localhost:8000/docs"
	@echo "🗺️  GeoServer: http://localhost:8080/geoserver"
	@echo ""

stop:
	@echo "Stopping services..."
	@docker-compose down
	@echo "✅ Services stopped"

restart:
	@echo "Restarting services..."
	@docker-compose restart
	@echo "✅ Services restarted"

logs:
	@docker-compose logs -f

clean:
	@echo "⚠️  This will remove all data volumes!"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo ""; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		docker-compose down -v; \
		rm -rf pgdata/ geoserver_data/; \
		echo "✅ Cleanup complete"; \
	fi

test:
	@echo "Running backend tests..."
	@docker-compose exec backend pytest -v

seed:
	@echo "Seeding sample data..."
	@docker-compose exec backend python scripts/seed_data.py
	@echo "✅ Sample data seeded"
