default_target: swatch

COMMIT_HASH := $(shell git log -1 --pretty=format:"%h"|tail -1)

version:
	echo "VERSION='0.1.0-$(COMMIT_HASH)'" > swatch/version.py

swatch: version
	DOCKER_BUILDKIT=1 docker build --platform linux/amd64 -t swatch -f docker/Dockerfile .

swatch_push: version
	docker buildx build --push --platform linux/arm64/v8,linux/amd64 --tag crzynik/swatch:latest --file docker/Dockerfile .