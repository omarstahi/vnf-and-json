from django.shortcuts import render
from django.http import HttpResponse
import json
import os

def test(request):
    num = request.POST.get('num')
    vlan_option = request.POST.get('vlan_option')  # Assuming you have a form input for this
    type = request.POST.get('type')
    
    if num in ['1', '2', '3', '4']:
        print(f"vlan_option: {vlan_option}")

        if vlan_option == 'with':
            json_filename = f"with_vlan/nsd_{num}vnf.json"
        else:
            json_filename = f"without_vlan/nsd_{num}vnf.json"
        response_file = f"response_nsd_{num}_vnf.json"
    else:
        # Handle other cases or raise an error
        json_filename = None
    
    if request.method == 'POST' and 'sub' in request.POST and json_filename:
        version = request.POST.get('version')
        name = request.POST.get('nsdName')
        nsdversion = request.POST.get('nsdVersion')
        nsddesc = request.POST.get('nsdDescription')
        numHard = request.POST.get('numHard')
                           

        with open(f"orange/static/{json_filename}", "r") as file:
            data = json.load(file)
            i = 0
            inp = 0
            test = 0
            cpuset = 3
            vnf_cloud_index = 0
            #hardware_index = 0
            num = int(num)
            objects = data['objects']
            memory_sum = 0
            cpu_sum = 0

            for object in objects:
                if data['objects'][i]['type']['value'] == "vnf" and num > 0:
                    vnfname = request.POST.get('name'+str(inp))
                    data['objects'][i]['name']['value'] = vnfname
                    memory = request.POST.get('memory'+str(inp))
                    data['objects'][i]['memory']['value'] = memory
                    cpu = request.POST.get('cpu'+str(inp))
                    data['objects'][i]['nof-vcpus']['value'] = cpu
                    location = request.POST.get('location'+str(inp))
                    data['objects'][i]['disks']['items'][0]['location']['value'] = "https://10.253.56.133/" + location
                    bus = request.POST.get('bus'+str(inp))
                    data['objects'][i]['disks']['items'][0]['bus']['value'] = bus
                    cpu_sum+=int(cpu)
                    memory_sum+=int(memory)

                    #update persistance id
                    data['objects'][i]['persistence-id']['value'] = vnfname+"_3int"
                    
                    #cpu-pinning
                    for j in range( int(cpu) ):
                        cpuItem = {
                                "cpuset": {
                                    "value": cpuset
                                }
                            }
                        data['objects'][i]['cpu-pinning']['items'].append(cpuItem)
                        cpuset += 1
                    
                    #collect Cloud-init paths and Cloud-init contents
                    
                    cloud_init_paths = []
                    cloud_init_contents = []
                    index = request.POST.get('numCloud'+str(inp))
                    if index != "":
                        for c in range(int(index)):
                            path = request.POST.get(f'Cloud-init-path-{vnf_cloud_index}-{c}')
                            content = request.POST.get(f'Cloud-init-content-{vnf_cloud_index}-{c}')
                            if path != "" and content != "":
                                cloud_init_paths.append(path)
                                cloud_init_contents.append(content)
                                #this way don't work because item point on items[0] so any change in item will be in items[0]
                                #item = data['objects'][i]['customization']['pathnames']['items'][0]

                                #so i used this approach
                                item = {
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
            data['general']['id']['value'] = name + "_3int"
            if numHard in ["1", "2", "3"]:
                for h in range(1, int(numHard) + 1):
                    hardName = request.POST.get('hard_name' + str(h))
                    data['nsd']['properties']['hardware'].append(hardName)  # Append hardware name to the list
                    
            if type == "small" and cpu_sum > 3 or memory_sum > 8:
                return HttpResponse("aaaaa")
            elif type == "medium" and cpu_sum > 5 or memory_sum > 16:
                return HttpResponse("aaaaa")
            elif type == "big" and cpu_sum > 8 or memory_sum > 32:
                return HttpResponse("aaaaa")
        with open(f"orange/static/{response_file}", "w") as file:
            json.dump(data, file, indent=4)
        
        response = HttpResponse(content_type="application/octet-stream")
        response['Content-Disposition'] = f'attachment; filename={response_file}'
        
        with open(f"orange/static/{response_file}", "rb") as f:
            response.write(f.read())
        
        #remove temp file
        os.remove(f"orange/static/{response_file}")
        
        return response
    
    return render(request, "test.html")


