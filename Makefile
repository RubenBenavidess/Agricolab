up:
	sudo docker compose up -d --build
run-api:
	sudo docker compose run --rm api
run-etl:
	sudo docker compose run --rm etl
down:
	sudo docker compose down
logs:
	sudo docker compose logs -f etl
clean-all:
	sudo rm -rf ./data-config/data/*
	sudo rm -rf ./data-config/embeddings/chroma/*