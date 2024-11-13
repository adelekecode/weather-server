import random
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.contrib.auth import get_user_model
from config import settings
import time
from .views import data_signal
from django.utils import timezone
from .models import *
import hashlib
import os




User = get_user_model()




@receiver(post_save, sender=User)
def welcome_user_mail(sender, instance, created, **kwargs):

    if created:

        if instance.role == "user":

            subject = "openapi welcomes you"

            message = f"Dear {instance.first_name}, welcome to my system. My name is Openapi. I am here to help you. If you have any questions, please feel free to ask me. I am always here to help you. Thank you."

            print("sending mail")
            time.sleep(5)
            print("mail sent")

            print(f"""

            subject: {subject}
            message: {message}

            """)
        else:
            print("Admin created")
            print(f"""

            subject: openapi welcomes Admin
            message: Dear Admin, welcome to my system. My name is Openapi. I am here to help you. If you have any questions, please feel free to ask me. I am always here to help you. Thank you.

            """)


@receiver(data_signal)
def data_signal_receiver(sender, data, **kwargs):
    print("data_signal_receiver")
    print(sender.first_name)
    print(kwargs)
    print(data)


