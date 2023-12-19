import subprocess
import argparse
import Utilities.tools as toolsrun,Utilities.common as common
import os

def do_upload_testresult_testmo(test_finale_output_path,devicename,batchname,TestmoKey,testmoSource):
    print(f"Uploading Testresults.xml file for job_id: {batchname} and path: {test_finale_output_path}")
        #testmo automation:run:submit --instance https://legogroup.testmo.net --project-id: 12 --name Sprint9 --source Smoketest1 --results “./Testresult.xml”
    
    testmo_resource=testmoSource
    
    results_xml_file=f'{test_finale_output_path}/TestResults.xml'
    device_name= common.sanitize_string(devicename)
    test_suite_name=batchname+"-"+device_name

    os.environ['TESTMO_TOKEN']
    args = [toolsrun.testmo, "automation:run:submit", 
            "--instance", toolsrun.INSTANCE, 
            "--project-id", "12", 
            "--name", test_suite_name, 
            "--source", testmo_resource,
            "--tags", device_name,
             "--milestone-id", "115",   
            "--results", results_xml_file
            ]
    print(f"Uploading Testresults.xml file for job_id: {batchname} and path: {args}")
    output = subprocess.run(args, capture_output=True, text=True)
    print(output.stdout)
    print(output.stderr)
    #print("Output",str(output.stdout.decode()))
    #print('Results:\n'+ output.stdout)+'\n')
    #print('Errors',str(output.stderr.decode())) 
