up:
	sudo docker compose up -d --build
down:
	sudo docker compose down
logs:
	sudo docker compose logs -f etl
run-once:
	sudo docker compose run --rm etl python -m scripts.pipeline
clean-all:
	sudo rm -rf ./data-config/data/*
	sudo rm -rf ./data-config/embeddings/chroma/*