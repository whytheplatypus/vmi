from .views import CodeView
from .models import (
    SMSDevice,
    SMSCode,
)


class SMSBackend:
    def get_device_model(self):
        return SMSDevice

    def is_enabled(self, user):
        return SMSDevice.objects.filter(user=user).exists()

    def get_device(self, device_id):
        return SMSDevice.objects.get(pk=device_id)

    def start_verification(self, request):
        if SMSDevice.objects.filter(user=request.user).exists():
            # Generate code
            # save code
            code = SMSCode.objects.create(
                device=SMSDevice.objects.get(user=request.user))
            # send code
            print(code.code)
            response = CodeView.as_view()(request)
            if hasattr(response, 'render'):
                return response.render()
            return response
        return None
