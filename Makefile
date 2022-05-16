default_target: local

COMMIT_HASH := $(shell git log -1 --pretty=format:"%h"|tail -1)
VERSION = 1.5.0

local:
	cd web; ./gradlew zip; unzip build/libs/project-1.0.0-SNAPSHOT.zip -d dist/;
	DOCKER_BUILDKIT=1 docker build --no-cache -t swatch -f docker/Dockerfile .

push:
	cd web; ./gradlew zip; unzip build/libs/project-1.0.0-SNAPSHOT.zip -d dist/;
	docker buildx build --push --platform linux/arm64/v8,linux/amd64 --tag crzynik/swatch:latest --file docker/Dockerfile .
	docker pull crzynik/swatch:latest
	docker tag crzynik/swatch:latest crzynik/swatch:${VERSION}-${COMMIT_HASH}
	docker push crzynik/swatch:${VERSION}-${COMMIT_HASH}
	rm -rf web/dist/

push_beta:
	cd web; ./gradlew zip; unzip build/libs/project-1.0.0-SNAPSHOT.zip -d dist/;
	docker buildx build --push --platform linux/arm64/v8,linux/amd64 --tag crzynik/swatch:beta --file docker/Dockerfile .
	rm -rf web/dist/
