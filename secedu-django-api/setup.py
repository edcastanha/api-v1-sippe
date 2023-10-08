import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User

def create_superuser(
        username : str = 'admin',
        email : str = 'admin@admin.test',
        password : str = 'mudar1234'
    ):
    # Criando superusuário
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)
        print('Superusuário criado - Sucesso!')     
    else:
        print('O superusuário existente - OK!')

if __name__ == '__main__':
    create_superuser(username='edson.filho',email='edson.filho@secedu.com.br')

