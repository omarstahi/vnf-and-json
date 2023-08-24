from django.shortcuts import render
from django.http import HttpResponse
import json

def test(request):
    num = request.POST.get('num')
    
    if num == '1':
        json_filename = "Fichier_Conf_1.json"
    elif num == '2':
        json_filename = "Fichier_Conf_1.json"
    elif num == '3':
        json_filename = "Fichier_Conf_1.json"
    elif num == '4':
        json_filename = "Fichier_Conf_4.json"
    elif num == '5':
        json_filename = "Fichier_Conf_5.json"
    else:
        # Handle other cases or raise an error
        json_filename = None
    
    if request.method == 'POST' and 'sub' in request.POST and json_filename:
        version = request.POST.get('version')
        name = request.POST.get('nsdName')
        nsdversion = request.POST.get('nsdVersion')
        nsddesc = request.POST.get('nsdDescription')
        softwaremin = request.POST.get('softwareMin')
        
        with open(f"orange/static/{json_filename}", "r") as file:
            data = json.load(file)
            i = 0
            inp = 0
            test = 0
            vnf_cloud_index = 0
            num = int(num)
            objects = data['objects']
            
            for object in objects:
                if data['objects'][i]['type']['value'] == "vnf" and num > 0:
                    vnfname = request.POST.get('name'+str(inp))
                    data['objects'][i]['name']['value'] = vnfname
                    memory = request.POST.get('memory'+str(inp))
                    data['objects'][i]['memory']['value'] = memory
                    cpu = request.POST.get('cpu'+str(inp))
                    data['objects'][i]['nof-vcpus']['value'] = cpu
                    url = data['objects'][i]['disks']['items'][0]['location']['value']
                    url = "https://10.253.56.133/"+url.rsplit('/')[-1]
                    data['objects'][i]['disks']['items'][0]['location']['value'] = url
                    
                    #update persistance id
                    data['objects'][i]['persistence-id']['value'] = vnfname+"_3int"
                    
                    #collect Cloud-init paths and Cloud-init contents
                    
                    cloud_init_paths = []
                    cloud_init_contents = []
                    for c in range(4):
                        path = request.POST.get(f'Cloud-init-path{c+1}{vnf_cloud_index}')
                        content = request.POST.get(f'Cloud-init-content{c+1}{vnf_cloud_index}')
                        if path != "" and content != "":
                            cloud_init_paths.append(path)
                            cloud_init_contents.append(content)
                            if test == 0:    
                                data['objects'][i]['customization']['pathnames']['items'][0]['location']['value'] = path
                                data['objects'][i]['customization']['pathnames']['items'][0]['template-content']['value'] = content
                                test+=1
                            else:
                                #this way don't work because item point on items[0] so any change in item will be in items[0]
                                #item = data['objects'][i]['customization']['pathnames']['items'][0]

                                #so i used this approach
                                item={
                                    "location": {
                                        "value": "\/openstack\/latest\/user_data"
                                    },
                                    "template-definition": {
                                        "value": "base64_encoded_content"
                                    },
                                    "template-content": {
                                        "value": "CiNWTSBjb25maWcgZmlsZQpjb25maWcgdGVybWluYWwKY3J5cHRvIGtleSBnZW5lcmF0ZSBkc2EgMjA0OCBuby1jb25maXJtCmlwIHNzaCBlbmFibGUKYmluZCBzc2ggZ2lnYWJpdGV0aGVybmV0IDAvMC4zOTk4CmlwIHNzaCBhdXRoLW1ldGhvZCBhdXRvbWF0aWMKaXAgc3NoIGF1dGgtcmV0cmllcyAzCmlwIHNzaCBhdXRoLXRpbWVvdXQgMzAKaXAgc3NoIHRpbWVvdXQgNjAwCmhvc3RuYW1lICJla2kyIgppbnRlcmZhY2UgZ2lnYWJpdGV0aGVybmV0IDAvMC4zOTk4CiBlbmNhcHN1bGF0aW9uIGRvdDFxIDM5OTgKIGlwIGFkZHJlc3MgMTMuMTMuMTMuMiAyNTUuMjU1LjI1NS4wCmV4aXQKaXAgcm91dGUgMC4wLjAuMCAwLjAuMC4wIDEzLjEzLjEzLjQKCg=="
                                    }
                                }
                                data['objects'][i]['customization']['pathnames']['items'].append(item)
                                data['objects'][i]['customization']['pathnames']['items'][test]['location']['value'] = path
                                data['objects'][i]['customization']['pathnames']['items'][test]['template-content']['value'] = content
                                test+=1

                    i+=1
                    vnf_cloud_index+=1
                    num-=1
                    inp = int(inp)
                    inp+=1
                    #reinitialize test to zero to avoid index out of range
                    test = 0
                elif data['objects'][i]['type']['value'] != "vnf" and num > 0:
                    i+=1
                elif num == 0:
                    break
            data['version'] = version
            data['nsd']['properties']['name'] = name
            data['nsd']['version'] = nsdversion
            data['nsd']['properties']['description'] = nsddesc
            data['nsd']['properties']['software_min'] = softwaremin
            data['general']['id']['value'] = name + "_3int"
        
        with open(f"orange/static/{json_filename}", "w") as file:
            json.dump(data, file, indent=4)
        
        response = HttpResponse(content_type="application/octet-stream")
        response['Content-Disposition'] = f'attachment; filename="{json_filename}"'
        
        with open(f"orange/static/{json_filename}", "rb") as f:
            response.write(f.read())
        
        return response
    
    return render(request, "test.html")
