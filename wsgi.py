import os
#my comment here
DJANGO_PATH =  os.path.join(os.path.abspath(os.path.dirname(__file__)), '..')
sys.path.append(DJANGO_PATH)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

from django.core.wsgi import get_wsgi_application

from dj_static import Cling

application = Cling(get_wsgi_application())

