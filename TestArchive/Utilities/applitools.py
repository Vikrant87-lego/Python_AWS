
import os
from pathlib import Path
import Utilities.tools as tools
import eyes_settings
import subprocess


# Organizing Screenshot directory
def do_organize_screenshots_test_name(original_dir,batch_name):
 print("Organize screenshots by test name folders")
 for device_dir, _, test_files in os.walk(original_dir):
    screenshots_dir = Path(device_dir)
    png_files = screenshots_dir.glob("*.png")  # traverse all subfolders
    for fn in png_files:
        file_base_name = "_".join(fn.stem.split("_")[:-1])
        scenario_name = file_base_name.split("SCREENSHOT_", 1)[-1] 
        scenario_dir = os.path.join(original_dir,batch_name,scenario_name)
        print('scenario_dir: '+scenario_dir)
        os.makedirs(scenario_dir, exist_ok=True)
        fn.rename(Path(scenario_dir) / fn.name)

        


# Upload Screenshots to AppliTools dashboard        
def do_upload_screenshots(test_finale_output_path, job_id,appli_tools_key):
    #print("current working directory is:"+os.getcwd())
 
    print(f"Uploading screenshots for job_id: {job_id} and path: {test_finale_output_path}")
    args = [tools.java, "-Xms128m", "-Xmx1024m", "-jar", tools.image_tester, "-k",
            f"{appli_tools_key}", "-f",
            f"{test_finale_output_path}", "-dn",
            f"{job_id}", "-os", f"{'Android'}", "-a",
            f"{eyes_settings.GL_app_name}"
            ]
    print('Sending Images To AppliTools..')
    output = subprocess.run(args, capture_output=True,text=True)
    #print(output)
    print(output.stdout)
     
    print(output.stderr)



    
