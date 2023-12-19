import os

#git_proj_dir= os.environ['CI_PROJECT_DIR']
git_proj_dir='/Users/dkviksar/lego-bi-app'
jar_file_path = os.path.join(git_proj_dir, 'CiPipeline', 'ImageTesterArchive','ImageTester_3.4.0.jar')
java = "java"
image_tester = jar_file_path
#image_tester = "$CI_PROJECT_DIR/CiPipeline/ImageTesterArchive/ImageTester_3.4.0.jar"
testmo = "testmo"
INSTANCE = "https://legogroup.testmo.net"

