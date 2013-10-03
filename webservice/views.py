from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from base64 import b64decode
import traceback
import zipfile
import os.path

@csrf_exempt
def submit_answer(request):
    if request.method != 'POST':
        return HttpResponse(status=404)
    try:
        #get file data from POST
        encodedZipFileData = request.POST["zipFile"]
        print(4 - len(encodedZipFileData) % 4)
        zipFileData = b64decode(encodedZipFileData + '=' * (4 - len(encodedZipFileData) % 4))

        #write file to filesystem
        tmpZipFileBase = "tmpZip"
        i = 0
        tmpZipFileName = ""
        while True:
            tmpZipFileName = tmpZipFileBase + str(i) + ".zip"
            if not os.path.isfile(tmpZipFileName):
                break
            i += 1
        tmpZipFile = open(tmpZipFileName, "w")
        tmpZipFile.write(zipFileData)
        tmpZipFile.close()

        #unzip file
        zfile = zipfile.ZipFile(tmpZipFileName)
        for name in zfile.namelist():
            print "Decompressing " + name
            fd = open(name, "w")
            fd.write(zfile.read(name))
            fd.close()

        os.remove(tmpZipFileName)
    except:
        traceback.print_exc()
    return HttpResponse("Custom response goes here...")
