import africastalking
from django.conf import settings




africastalking.initialize(settings.AFRICASTALKING_USERNAME, settings.AFRICASTALKING_API_KEY)
sms = africastalking.SMS


class Sendsms:

    def send(self,message,recipients):

      try:
        response=sms.send(message,recipients)
        return response
      except Exception as e:
         raise Exception(f'error sending sms: {e}')

