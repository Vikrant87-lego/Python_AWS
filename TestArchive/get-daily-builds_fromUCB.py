import http.client
import urllib.request
import os
import requests
import json
import sys
import boto3
import json
import dotenv
import shutil
from botocore.exceptions import ClientError
from dotenv import find_dotenv, load_dotenv



dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
encoded_credentials = os.environ["UCB_API_KEY"]
auth_header = f'Basic {encoded_credentials}'

config = {

    "orgid":"5772500085490",
    "projectid":"89b57718-ac69-4d2c-ae37-6e9dbd02c20d",
    "androidbuildtargetid":"lego-building-instructions-global-android-dev-altunitytester",
    "iosbuildtargetid":"lego-building-instructions-global-ios-dev-altunitytester",
    "androidchinatargetid":"lego-building-instructions-china-android-dev-altunitytester",
    "iosChinatargetid":"lego-building-instructions-china-ios-dev-altunitytester"
}
conn = http.client.HTTPSConnection("build-api.cloud.unity3d.com")
payload = ''

headers = {
  'Content-Type': 'application/json',
  'Authorization': auth_header
}

target_id_array = [config['androidbuildtargetid'], config['iosbuildtargetid'],config['androidchinatargetid'],config['iosChinatargetid']]

for buildtarget in target_id_array: 

    print ("Build to download: "+buildtarget)
    def get_lastbuild_number(buildtarget):
        conn.request("GET", "/api/v1/orgs/"+config['orgid']+"/projects/"+config['projectid']+"/buildtargets/"+buildtarget+"/builds/", payload, headers)
        res = conn.getresponse()
        builds_data = json.loads(res.read())
        print ("Get last build info")
        buildnumber = builds_data[0]['build']
        buildstatus=builds_data[0]['buildStatus'] 
        print("Build Number           : " + str(builds_data[0]['build']))
        print("Build Buildtargetid    : " + str(builds_data[0]['buildtargetid']))
        #print("Build BuildGUID        : " + str(builds_data[0]['buildGUID']))
        print("Build BuildStatus      : " + str(builds_data[0]['buildStatus']))
        print("Build Platform         : " + str(builds_data[0]['platform']))
        print("Build Created          : " + str(builds_data[0]['created']))
        # Print only after checking if the Build Status is success otherwise the field values are not available
        if buildstatus == 'success': 
           print("Build Finished         : " + str(builds_data[0]['finished']))
           print("Build BuiltRevision:   : " + str(builds_data[0]['lastBuiltRevision']))
        return {"buildnum":buildnumber,"buildstat":buildstatus}
        
    # Get last build number
    returnval = get_lastbuild_number(buildtarget)
    buildnumber=returnval["buildnum"]
    if returnval["buildstat"] == 'success':
    
        # Get android build to test info: apk file name and download link 
    
        conn.request("GET", "/api/v1/orgs/"+config['orgid']+"/projects/"+config['projectid']+"/buildtargets/"+buildtarget+"/builds/"+str(buildnumber), payload, headers)
        build_res = conn.getresponse()
        json_res = json.loads(build_res.read())
        download_link = json_res['links']['download_primary']['href']
        file_name = download_link.partition("filename%3D")[2]
    
    
        def download (url):
            with open(file_name, "wb") as f:
                print("Downloading: " +file_name)
                this_name  = file_name
                get_response = requests.get(url, stream=True)
                total_length = get_response.headers.get('content-length')
    
                if total_length is None: # no content length header
                    f.write(get_response.content)
                else:
                    dl = 0
                    total_length = int(total_length)
                    for data in get_response.iter_content(chunk_size=4096):
                        dl += len(data)
                        f.write(data)
                        done = int(50 * dl / total_length)
                    #    sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )    
                    #    sys.stdout.flush()
                sys.stdout.write ("\nDownload Completed!\n")        
    
        # call download 
        download(download_link)
        conn.close()
        # Move China Builds in Seperate Folder       
        def copyCertainFiles(source_folder, china_dest_folder,global_dest_folder,string_to_match_CN,string_to_match_GL, file_type=None):
            # Check all files in source_folder
            for filename in os.listdir(source_folder):
                # Move the file if the filename contains the string to match
                if file_type == None:
                    if string_to_match_CN in filename:
                        shutil.move(os.path.join(source_folder, filename), os.path.join(china_dest_folder,filename))
                    elif string_to_match_GL in filename:
                        shutil.move(os.path.join(source_folder, filename), os.path.join(global_dest_folder,filename))  
        
                #  Can be used in future Check if the keyword and the file type both match
                elif isinstance(file_type, str):
                    if string_to_match_CN in filename and file_type in filename:
                        shutil.move(os.path.join(source_folder, filename), os.path.join(china_dest_folder,filename))
        # Call Move files
        copyCertainFiles(os.getcwd(),'../_artifacts/China','../_artifacts/Global','china','global')
    else:
        print("Latest Build is Not Available or is Building")