#!/bin/sh
# ==========================================
# ENTRYPOINT SCRIPT
# ==========================================

set -e

echo "🚀 Starting Student Registry Blockchain Application..."

# Attendre que les services soient prêts (si nécessaire)
echo "⏳ Waiting for services to be ready..."
sleep 2

# Appliquer les migrations
echo "📦 Applying database migrations..."
python manage.py migrate --noinput || echo "⚠️ Migrations skipped"

# Collecter les fichiers statiques
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput --clear || echo "⚠️ Static collection skipped"

# Créer un superuser si demandé
if [ "$DJANGO_SUPERUSER_USERNAME" ] && [ "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "👤 Creating superuser..."
    python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists():
    User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD')
    print('✅ Superuser created')
else:
    print('ℹ️ Superuser already exists')
END
fi

echo "✅ Application ready!"
echo "🌐 Starting server on http://0.0.0.0:8000"

# Exécuter la commande passée en argument
exec "$@"