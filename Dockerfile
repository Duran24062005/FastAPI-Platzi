# FROM python:3.12-slim

# # Instalar dependencias del sistema
# RUN apt-get update && apt-get install -y \
#     gcc \
#     libmysqlclient-dev \
#     pkg-config \
#     && rm -rf /var/lib/apt/lists/*



# ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# ENV PYTHONUMBUFFERED=1

# WORKDIR /app


# COPY requirements.txt .

# RUN python -m venv venv

# RUN /bin/bash -c "source venv/bin/activate"

# RUN pip install --no-cache-dir -r requirements.txt

# COPY . .

# EXPOSE 8000

# CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000" ]


FROM python:3.12-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    libmariadb-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

# RUN python -m venv venv

# RUN venv/scripts/activate

# Activar el entorno virtual y luego instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000",  "--reload"]

