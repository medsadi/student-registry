# ==========================================
# DOCKERFILE - Student Registry Blockchain
# ==========================================

FROM python:3.11-slim

# Variables d'environnement
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    DEBIAN_FRONTEND=noninteractive

# Créer un utilisateur non-root
RUN useradd -m -u 1000 appuser

# Installer dépendances système minimales
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    netcat-openbsd \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copier requirements pour profiter du cache Docker
COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copier le code de l'application
COPY --chown=appuser:appuser manage.py .
COPY --chown=appuser:appuser docker-entrypoint.sh .
COPY --chown=appuser:appuser ethsite/ ./ethsite/
COPY --chown=appuser:appuser walletapp/ ./walletapp/

# Créer les dossiers nécessaires pour volumes
RUN mkdir -p staticfiles media logs && \
    chown -R appuser:appuser /app

# Passer à l'utilisateur non-root
USER appuser

# Collecter les fichiers statiques depuis walletapp/static vers staticfiles/
RUN python manage.py collectstatic --noinput || true

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

ENTRYPOINT ["/app/docker-entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
