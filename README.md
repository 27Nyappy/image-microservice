# image-microservice

Microservice that manages the processing and handling of sprite sheets and icons

## Requirements

- Python `^3.14`,`<4.0`
- Poetry `^2.0`,`<3.0`
- Pipx `1.8.0`

To install Poetry follow [their installation documentation](https://python-poetry.org/docs/) using `pipx`

```
pipx install poetry
```

## Installation

1. Clone the repository

```
git clone https://github.com/27Nyappy/image-microservice.git
cd image-microservice
```

2. Set up the environment and dependencies

```
poetry install
```

This creates a virtual environment and installs all the required libraries (Flask, Pillow, etc...) as well as the internal project scripts.

## Running the Microservice

Use the custom Poetry script to ensure everyone runs the project with the correct environment settings.

```
poetry run start
```

This executes the `main()` function in `src/service.py`
