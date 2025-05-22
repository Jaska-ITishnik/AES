from django.shortcuts import render
from django.views import View

from apps.utils import Aes


class AesLogicView(View):
    def get(self, request):
        return render(request, template_name='index.html')

    def post(self, *args, **kwargs):
        input_key = self.request.POST.get('input_key')
        cipher_key = self.request.POST.get('cipher_key')
        obj = Aes().encryption(input_key, cipher_key)
        context = {
            "ciphertext": obj['ciphertext'],
            "key_schedule": Aes().gen_key(input_key, cipher_key).values(),
            "rounds": obj['encrypting']
        }
        return render(self.request, template_name='index.html', context=context)
