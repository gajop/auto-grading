from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from base64 import b64decode
import traceback

@csrf_exempt
def submit_answer(request):
    if request.method != 'POST':
        return HttpResponse(status=404)
    try:
        encodedZipFile = request.POST["zipFile"]
        zipFile = b64decode(encodedZipFile + '=' * (4 - len(encodedZipFile) % 4))
    except:
        traceback.print_exc()
    return HttpResponse("Custom response goes here...")
