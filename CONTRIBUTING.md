# Setup

## 1. Build the docker container locally with

```bash
make
```

## 2. Create a local config file for testing#
Place the file at config/config.yml in the root of the repo.

Here is an example, but modify for your needs:

```yaml
objects:
  green_object:
    color_lower: 70, 70, 0
    color_upper: 110, 100, 50
    min_area: 1000
    max_area: 100000

cameras:
  camera:
    zones:
      zone:
        coordinates: 230, 530, 325, 610
        objects:
          - green_object
```

## 3. Open the repo with Visual Studio Code

Upon opening, you should be prompted to open the project in a remote container. This will build a container on top of the base swatch container with all the development dependencies installed. This ensures everyone uses a consistent development environment without the need to install any dependencies on your host machine.

## 4. Run the app

The backend runs in python and the frontend runs in flutter:

```python
python3 -m swatch
```

```bash
flutter run web
```

## 5. Teardown

After closing VSCode, you may still have containers running. To close everything down, just run docker-compose down -v to cleanup all containers.
