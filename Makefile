default_target: local

local:
	DOCKER_BUILDKIT=1 docker build --no-cache -t swatch -f docker/Dockerfile .

push:
	docker buildx build --push --platform linux/arm64/v8,linux/amd64,linux/arm/v7 --tag crzynik/swatch:latest --file docker/Dockerfile .

push_beta:
	docker buildx build --push --platform linux/arm64/v8,linux/amd64,linux/arm/v7 --tag crzynik/swatch:beta --file docker/Dockerfile .
