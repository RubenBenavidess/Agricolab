build:        ## Build image
	sudo docker build -f Dockerfile.fastapi -t fastapi-image .

run:       	  ## Create container and run it
	sudo docker run --gpus all --name agricolab_api -p 8080:8000 fastapi-image

test:	# TODO

