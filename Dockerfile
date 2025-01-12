FROM python:3.7
# docker run --rm -it -v $(pwd):/app ~/.aws:/root/.aws infinite:poetry bash

# docker build argument (--build-arg)
ARG SOFTWARE_ENV
# set up environment variables
ENV POETRY_VERSION=1.1.7 \
    SOFTWARE_ENV=${SOFTWARE_ENV} \
    POETRY_CACHE_DIR='/var/cache/pypoetry'

# System dependencies for audio handling (for librosa)
RUN apt-get update -y \
    && apt-get install -y --no-install-recommends build-essential gcc \
                                        libsndfile1 \
                                        ffmpeg \
    # Remove apt cache after installing. lighter image
    && rm -rf /var/lib/apt/lists/*

# Install awscli (if you are testing locally)
RUN if [ "$SOFTWARE_ENV" = "dev" ] ; \
    then curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install; fi

# Project initialization
RUN pip install "poetry==$POETRY_VERSION"

# Set working directory
WORKDIR /app
COPY poetry.lock pyproject.toml /app/

# Project initialization
RUN poetry config virtualenvs.create false \
    && poetry install \
        $(if [ "$SOFTWARE_ENV" = "prod" ]; then echo '--no-dev'; fi) \ 
        # Don't require user input
        --no-interaction --no-ansi \
    # Cleaning poetry installation's cache por production
    && if [ "$SOFTWARE_ENV" = "prod" ]; then rm -rf "$POETRY_CACHE_DIR"; fi

# Install requirements
COPY . /app
# CMD ["bash"]