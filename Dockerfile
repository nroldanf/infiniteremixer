FROM python:3.8-slim
# System dependencies for audio handling (for librosa)
# Remove apt cache after installing. lighter image
RUN apt-get update -y \
    && apt-get install -y --no-install-recommends build-essential gcc \
                                        libsndfile1 \
                                        ffmpeg \
    && rm -rf /var/lib/apt/lists/*
# Set working directory
WORKDIR /app
# Set virtual environment with venv
ENV VIRTUAL_ENV=/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN python3 -m venv $VIRTUAL_ENV \
    && pip install --upgrade pip \
# Install requirements
COPY . /app
RUN pip install -r requirements.txt --no-cache-dir
CMD ["bash"]