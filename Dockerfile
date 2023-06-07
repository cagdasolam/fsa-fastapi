# ---- Base Python ----
FROM python:3.9 AS base
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app

# ---- Dependencies ----
FROM base AS dependencies
# Install pip
RUN pip install --upgrade pip
# Copy only requirements to cache them in docker layer
COPY ./fsa_fastapi /app/fsa_fastapi
COPY model2.model pyproject.toml poetry.lock /app/
# Project initialization
RUN pip install poetry \
    && poetry config virtualenvs.create false \
    # Install PyTorch CPU only
    && pip install torch==1.9.0+cpu torchvision==0.10.0+cpu torchaudio==0.9.0 -f https://download.pytorch.org/whl/torch_stable.html \
    && poetry install --no-interaction --no-ansi

# ---- Copy Code ----
FROM dependencies AS release
# Copy the code

# Expose the port the app runs on
EXPOSE 8000

# List all installed packages
RUN poetry show

# Ensure that Python knows where to find your application
ENV PYTHONPATH=/app/fsa_fastapi

# Run the application
CMD ["poetry", "run", "uvicorn", "fsa_fastapi.main:app", "--host", "0.0.0.0", "--port", "8000"]
