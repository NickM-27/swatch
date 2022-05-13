default_target: local

COMMIT_HASH := $(shell git log -1 --pretty=format:"%h"|tail -1)
VERSION = 1.4.1

local:
	DOCKER_BUILDKIT=1 docker build --no-cache -t swatch -f docker/Dockerfile .

push:
	docker buildx build --push --platform linux/arm64/v8,linux/amd64 --tag crzynik/swatch:latest --file docker/Dockerfile .
	docker pull crzynik/swatch:latest
	docker tag crzynik/swatch:latest crzynik/swatch:${VERSION}-${COMMIT_HASH}
	docker push crzynik/swatch:${VERSION}-${COMMIT_HASH}

push_beta:
	docker buildx build --push --platform linux/arm64/v8,linux/amd64 --tag crzynik/swatch:beta --file docker/Dockerfile .
