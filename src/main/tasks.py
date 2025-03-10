from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .fuzzy import Cooler_fan_fuzzy
import logging
from .models import Fan_speed


logging.basicConfig(
    level=logging.INFO,  
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

logger = logging.getLogger(__name__)


@shared_task
def calculate_fan_speed(data):
    
    serverroom_temperature = data['serverroom_temperature']
    softwareroom_temperature = data['softwareroom_temperature']
    serverroom_humidity = data['serverroom_humidity']

    # logging.info(serverroom_temperature)
    # logging.info(softwareroom_temperature)
    # logging.info(serverroom_humidity)

    fuzzy = Cooler_fan_fuzzy()
    res = fuzzy.compute_fan_speed(serverroom_temperature, softwareroom_temperature, serverroom_humidity)
    fan_speed = Fan_speed.objects.create(value=res, 
                                         serverroom_temperature=serverroom_temperature,
                                         softwareroom_temperature=softwareroom_temperature,
                                         serverroom_humidity=serverroom_humidity)


