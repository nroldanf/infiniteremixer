FROM python:3.8-slim
# Set working directory
WORKDIR /app
# Set virtual environment with venv
ENV VIRTUAL_ENV=/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN python3 -m venv $VIRTUAL_ENV \
    && pip install --upgrade pip \
    && pip install --upgrade setuptools wheel
# Install requirements
COPY requirements.txt .
RUN pip install -r requirements.txt
# Copy the code inside app folder
COPY . /app
# Something
CMD ["python"]