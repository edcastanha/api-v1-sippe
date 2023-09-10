import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User

def create_superuser():
    username = 'edson.filho'
    email = 'edson.filho@secedu.com.br'
    password = 'mudar1234'
    # Executando migrate
    os.system('python manage.py migrate --noinput | exit 1')
    # Criando superusuário
    if not User.objects.filter(username=username).exists():
        os.system('python manage.py makemigrations  --noinput | exit 1')
        os.system('python manage.py migrate --noinput | exit 1')
        os.system('python manage.py collectstatic  --noinput | exit 1')
        User.objects.create_superuser(username=username, email=email, password=password)
        print('Superusuário criado - Sucesso!')     
    else:
        print('O superusuário existente - OK!')

if __name__ == '__main__':
    create_superuser()
