from .views import CodeView


class SMSBackend:
    def get_device_model(self):
        return SMSDevice

    def is_enabled(self, user):
        return SMSDevice.objects.filter(user=user).exists()

    def get_device(self, device_id):
        return SMSDevice.objects.get(pk=device_id)

    def start_verification(self, request):
        if SMSDevice.objects.filter(user=user).exists():
            # Generate code
            # save code
            code = SMSCode.objects.create(
                device=SMSDevice.objects.get(user=user))
            # send code
            print(code)
            return CodeView.as_view()(request).render()
        return None
