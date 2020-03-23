from app.clients.clearbit import ClearBitClient
from django.conf import settings

clearbit_client = ClearBitClient(key=settings.CLEARBIT_API_KEY)
