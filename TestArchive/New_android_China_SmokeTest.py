import boto3
import os
import requests
import time
import fnmatch
import datetime
from dotenv import find_dotenv, load_dotenv
import Utilities.common as common,Utilities.applitools as applitools, Utilities.Testmo as testmorun
# Set Error color to Red when printing Output
red_code = "\033[91m"
reset_code = "\033[0m"

# Get AppliTools credentials 

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
appli_tools_key = os.environ["APPLITOOLS_API_KEY"]

# The following script runs a test through Device Farm

# get app build path from artifacts folder
def get_app_path():
    for file in os.listdir('./_artifacts/China'):
        if fnmatch.fnmatch(file, '*.apk'):
            app_file_name = file
        
    return app_file_name

app_build_path = get_app_path()
print("path: "+app_build_path)
build_version=""
for c in app_build_path:
    if c.isdigit():
        build_version =  build_version + c
#build_version = app_build_path[len(app_build_path)-6:len(app_build_path)-4]

print("version: "+build_version)
print("BI-App-Android-China-"+build_version+"-SmokeTest")

config = {
    
    # This is the app under test.
     "appFilePath":"./_artifacts/China/"+app_build_path,
     
    # Project Arn
    "projectArn":"arn:aws:devicefarm:us-west-2:138464956925:project:58974e4d-91a5-48c3-a18f-a41c45e1a496",
    
    # Android smoke test Pool arn (Xiaomi 12 and Xiomi Redmi Note 10)
    "poolArn": "arn:aws:devicefarm:us-west-2:138464956925:devicepool:58974e4d-91a5-48c3-a18f-a41c45e1a496/5269b8c3-c002-455f-ae96-3dd206abdd11",

    # Test Spec Arn - Dotnet_Android.yml 
    "testSpecArn": "arn:aws:devicefarm:us-west-2:138464956925:upload:58974e4d-91a5-48c3-a18f-a41c45e1a496/36c49c5d-5180-4a5e-a086-f09471367cea",

    # Test Mame Prefix  - Build number is hard coded. TO-DO: it should be added from a global variable   
    "namePrefix": "BI-App-Android-China-"+build_version+"-SmokeTest",
    
    # Test Package Arn (new CN & GL version) This is the test package arn - for now, it's NOT needed to re- upload
    "testPackageArn": "arn:aws:devicefarm:us-west-2:138464956925:upload:58974e4d-91a5-48c3-a18f-a41c45e1a496/b699a9ae-cc58-449e-8e8d-1bfbe87f3747"
    
}


client = boto3.client('devicefarm', region_name='us-west-2')
timestamp = str(int(time.time()))
unique = config['namePrefix'] + '-' + datetime.date.today().isoformat() + '-' + timestamp

print(f"The unique identifier for this run is going to be {unique} -- all uploads will be prefixed with this.")

def upload_df_file(filename, type_, mime='application/octet-stream'):
    response = client.create_upload(projectArn=config['projectArn'],
        name = (unique)+"_"+os.path.basename(filename),
        type=type_,
        contentType=mime
        )
    # Get the upload ARN, which we'll return later.
    upload_arn = response['upload']['arn']
    # We're going to extract the URL of the upload and use Requests to upload it 
    upload_url = response['upload']['url']
    with open(filename, 'rb') as file_stream:
        print(f"Uploading {filename} to Device Farm as {response['upload']['name']}... ",end='')
        put_req = requests.put(upload_url, data=file_stream, headers={"content-type":mime})
        print(' done')
        if not put_req.ok: 
            raise Exception("Couldn't upload, requests said we're not ok. Requests says: "+put_req.reason)
    started = datetime.datetime.now()
    while True:
        print(f"Upload of {filename} in state {response['upload']['status']} after "+str(datetime.datetime.now() - started))
        if response['upload']['status'] == 'FAILED':
            raise Exception("The upload failed processing. DeviceFarm says reason is: \n"+(response['upload']['message'] if 'message' in response['upload'] else response['upload']['metadata']))
        if response['upload']['status'] == 'SUCCEEDED':
            break
        time.sleep(5)
        response = client.get_upload(arn=upload_arn)
    print("")
    return upload_arn

# Below line should be included when new build should be uploded 
our_upload_arn = upload_df_file(config['appFilePath'], "ANDROID_APP")

# Below line should be included when new test package should be uploded
# our_test_package_arn = upload_df_file(config['testPackage'], 'APPIUM_NODE_TEST_PACKAGE')
# Below line is used to use an existing test package to skip the upload step
our_test_package_arn = config['testPackageArn']

print("our_upload_arn       : " + our_upload_arn) 
print("our_test_package_arn : " + our_test_package_arn)
print("testSpecArn          : " + config["testSpecArn"])
print("projectArn           : " + config["projectArn"] )
print("appArn               : " + our_upload_arn) 
print("DevicePool           : " + config["poolArn"] )
# Now that we have those out of the way, we can start the test run...
print (" schedule run start")

response = client.schedule_run(
    projectArn = config["projectArn"],
    appArn = our_upload_arn,
    devicePoolArn = config["poolArn"],
    name=unique,
    test = {
        "type":"APPIUM_NODE",
        "testSpecArn": config["testSpecArn"],
        "testPackageArn": our_test_package_arn
        }
    )
run_arn = response['run']['arn']
start_time = datetime.datetime.now()
print(f"Run {unique} is scheduled as arn {run_arn} ")

try:

    while True:
        response = client.get_run(arn=run_arn)
        state = response['run']['status']
        if state == 'COMPLETED' or state == 'ERRORED':
            break
        else:
            print(f" Run {unique} in state {state}, total time "+str(datetime.datetime.now()-start_time))
            time.sleep(10)
except:
    # If something goes wrong in this process, we stop the run and exit. 

    client.stop_run(arn=run_arn)
    exit(1)
print(f"Tests finished in state {state} after "+str(datetime.datetime.now() - start_time))
# now, we pull all the logs.
jobs_response = client.list_jobs(arn=run_arn)
# Save the output somewhere. We're using the unique value, but you could use something else
save_path = os.path.join(os.getcwd(), unique)
os.mkdir(save_path)
print(f"save path: {save_path}")
# Save the last run information
for job in jobs_response['jobs'] :
    # Make a directory for our information
    job_name = job['name']
    print(f"job_name: {job_name}")
    os.makedirs(os.path.join(save_path, job_name), exist_ok=True)
    # Get each suite within the job
    suites = client.list_suites(arn=job['arn'])['suites']
    for suite in suites:
        for test in client.list_tests(arn=suite['arn'])['tests']:
            # Get the artifacts
            for artifact_type in ['FILE','SCREENSHOT','LOG']:
                artifacts = client.list_artifacts(
                    type=artifact_type,
                    arn = test['arn']
                )['artifacts']
                for artifact in artifacts:
                    # We replace : because it has a special meaning in Windows & macos
                    if(suite['name']=="Tests Suite" and test['name']=="Tests"):
                        path_to = os.path.join(save_path, job_name, suite['name'], test['name'].replace(':','_') )
                        os.makedirs(path_to, exist_ok=True)
                        filename = artifact['type']+"_"+artifact['name']+"."+artifact['extension']
                        if (filename=="CUSTOMER_ARTIFACT_Customer Artifacts.zip"):
                            artifact_save_path = os.path.join(path_to, filename)
                            print("Downloading "+artifact_save_path)
                            with open(artifact_save_path, 'wb') as fn, requests.get(artifact['url'],allow_redirects=True) as request:
                                fn.write(request.content)
                            zipfilepath = os.path.dirname(os.path.abspath(artifact_save_path))
                            common.unzip_artifacts(zipfilepath)

                    #/for artifact in artifacts
                #/for artifact type in []
            #/ for test in ()[]
        #/ for suite in suites
    #/ for job in _[]
    print("AppliTools Job for device..."+job_name)
    screenshot_dir=f'{save_path}/{job_name}'
    directory_to_search = screenshot_dir  # Replace with your desired directory
    screenshots_directory = common.search_directory(directory_to_search,'Screenshots')
    if screenshots_directory:
        print(f"Found 'Screenshots' directory: {screenshots_directory}")
        if len(os.listdir(screenshots_directory)) == 0:
            print(f"{red_code} Screenshots directory is empty.{reset_code}")
        else:
            applitools.do_organize_screenshots_test_name(screenshot_dir,unique)
            job_id= job_name.replace(' ', '_')
            test_results_output_path = f"{save_path}/{job_name}/{unique}"
            try:
                applitools.do_upload_screenshots(test_results_output_path,job_id,appli_tools_key)
            except:
                pass
    else:
        print(f"{red_code} No 'Screenshots' directory found.{reset_code}")

    xmlpath=common.find_file_get_path("TestResults.xml",".xml",screenshot_dir)
    resultspath=f"{xmlpath}/TestResults.xml"
    test_results_xml_path = xmlpath
    batch_name=os.path.basename(save_path)
    TestmoKey=os.getenv('testmo_key')
    if (os.path.isfile(resultspath) and os.path.getsize(resultspath) > 0):
        print("Running TestmoCLI Command"+os.getcwd())
        testmorun.do_upload_testresult_testmo(test_results_xml_path,job_name,batch_name,TestmoKey,"smoketest-china")

    else:
        print(f"{red_code} Test Results file not found {reset_code}")
        xml_report_error_path=f"{batch_name}/TestReports/test_report_gl_errors.xml"
        testmorun.do_upload_testresult_testmo(xml_report_error_path,job_name,batch_name,TestmoKey,"smoketest-china") 
