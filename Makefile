default_target: local

COMMIT_HASH := $(shell git log -1 --pretty=format:"%h"|tail -1)

local:
	DOCKER_BUILDKIT=1 docker build --no-cache -t swatch -f docker/Dockerfile .

swatch_push:
	docker buildx build --push --platform linux/arm64/v8,linux/amd64 --tag crzynik/swatch:latest --file docker/Dockerfile .
