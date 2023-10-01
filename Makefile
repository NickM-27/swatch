default_target: local

COMMIT_HASH := $(shell git log -1 --pretty=format:"%h"|tail -1)
VERSION = 3.1.1

local:
	cd web; flutter build web;
	DOCKER_BUILDKIT=1 docker build --no-cache -t swatch -f docker/Dockerfile .

push:
	cd web; flutter build web;
	docker buildx build --push --platform linux/arm64/v8,linux/amd64 --tag crzynik/swatch:latest --file docker/Dockerfile .
	docker buildx build --push --platform linux/arm64/v8,linux/amd64 --tag crzynik/swatch:${VERSION}-${COMMIT_HASH} --file docker/Dockerfile .

push_beta:
	cd web; flutter build web;
	docker buildx build --push --platform linux/arm64/v8,linux/amd64 --tag crzynik/swatch:beta --file docker/Dockerfile .
