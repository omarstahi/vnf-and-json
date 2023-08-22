from django.shortcuts import render
from django.http import HttpResponse
import json

def test(request):
    with open("orange/static/Fichier_Conf_1.json","r") as file:
        data = json.load(file)
    if request.method == 'POST':
        version = request.POST.get('version')
        name = request.POST.get('nsdName')
        nsdversion = request.POST.get('nsdVersion')
        nsddesc = request.POST.get('nsdDescription')
        softwaremin = request.POST.get('softwareMin')
        
        with open("orange/static/Fichier_Conf_1.json","w") as file:
            data['version'] = version
            data['nsd']['properties']['name'] = name
            data['nsd']['version'] = nsdversion
            data['nsd']['properties']['description'] = nsddesc
            data['nsd']['properties']['software_min'] = softwaremin
            data['general']['id']['value'] = name+"_3int"
            json.dump(data, file, indent=4)
            
        response = HttpResponse(content_type="application/octet-stream")
        response['Content-Disposition'] = 'attachment; filename="result.json"'
        with open("orange/static/Fichier_Conf_1.json", "rb") as f:
            response.write(f.read())
        return response
    return render(request,"test.html")


def vnfconfig(request):
    #test to know witch file we will open
    i=0
    with open("orange/static/Fichier_Conf_1.json","r") as file:
        data = json.load(file)
    if request.method == 'POST':
        vnfname = request.POST.get('name${i}')
        nsdversion = request.POST.get('nsdVersion')
        nsddesc = request.POST.get('nsdDescription')
        softwaremin = request.POST.get('softwareMin')
        
        with open("orange/static/Fichier_Conf_1.json","w") as file:
            data['objects'][i]['name']['value'] = vnfname
            data['nsd']['version'] = nsdversion
            data['nsd']['properties']['description'] = nsddesc
            data['nsd']['properties']['software_min'] = softwaremin
            data['general']['id']['value'] = name+"_3int"
    return render(request,"test.html")

'''
**********objects[type==vnf].name.value ==> VNF Name

**********objects[type==vnf].persistence-id.value ==> <VNF_Name>_3int

**********objects[type==vnf].memory.value ==> VNF memory (en GiB)

**********objects[type==vnf].nof-vcpus.value ==> VNF CPUs

objects[type==vnf].cpu-pinning ===> à poser la questionb à Imane

objects[type==vnf].customization.pathnames.items[i].location ===> Cloud-init path i+1

objects[type==vnf].customization.pathnames.items[i].template-content ===> Cloud-init content i+1 (base64)

objects[type==vnf].disks.items[0].location.value ===> "https://10.253.56.133/<VNF File>"


 "location": {
                #file#            "value": "OneOS-vCPE-x86_pi1-6.6.1m2.qcow2"
            },
                       
'''