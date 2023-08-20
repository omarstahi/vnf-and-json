from django.shortcuts import render
from django.http import HttpResponse
import json, os

# Create your views here.


def test(request):
    with open("orange/static/Fichier_Conf_1.json","r") as file:
        data = json.load(file)
    if request.method == 'POST':
        version = request.POST.get('version')
        name = request.POST.get('nsdName')
        nsdversion = request.POST.get('nsdVersion')
        nsddesc = request.POST.get('nsdDescription')
        softwaremin = request.POST.get('softwareMin')
        hardware = request.POST.get('hardware')
        id = request.POST.get('generalID')
        desc = request.POST.get('generalDescription')
        pmd_cpu_mask = request.POST.get('openvswitchPmdCpuMask')
        with open("orange/static/Fichier_Conf_1.json","w") as file:
            data['version'] = version
            data['nsd']['properties']['name'] = name
            data['nsd']['version'] = nsdversion
            data['nsd']['properties']['description'] = nsddesc
            data['nsd']['properties']['software_min'] = softwaremin
            data['nsd']['properties']['hardware'].append(hardware)
            data['general']['id']['value'] = id
            data['general']['description']['value'] = desc
            data['general']['open-vswitch']['pmd-cpu-mask']['value'] = pmd_cpu_mask
            json.dump(data, file, indent=4)
        response = HttpResponse(content_type="application/octet-stream")
        response['Content-Disposition'] = 'attachment; filename="result.json"'
        with open("orange/static/Fichier_Conf_1.json", "rb") as f:
            response.write(f.read())
        return response
    return render(request,"test.html")


def generateSubForms(request):
    return render(request,"test.html")
