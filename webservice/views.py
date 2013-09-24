from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def submit_answer(request, pk):
    if request.method == 'GET':
        pass

    elif request.method == 'PUT':
        pass

    else:
        return HttpResponse(status=204)
