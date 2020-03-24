from app.clients.clearbit import ClearBitClient
from app.clients.pyhunter import PyHunterClient
from django.conf import settings

clearbit_client = ClearBitClient(key=settings.CLEARBIT_API_KEY)

pyhunter_client = PyHunterClient(key=settings.PYHUNTER_API_KEY)
