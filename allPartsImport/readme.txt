How to Create a lego image database

1. Download all ofiicial latest parts "complete.zip" from https://www.ldraw.org/parts/latest-parts.html
2. Unzip all 'parts' in to a 'parts' folder
3. run importAllPartReferencesfromFolder.py to create subfolders and coresponding .ldr files
4. Open each .ldr with LDCAd and run the parade script for testing
5. Export image to 'unlabeled_images' via LDCad using Session -> Animation -> OpenGL animation Export
6. run moveImageFilesToTrainingFolderForFolder.py to label and copy the partimages to the 'training_images_all'-folder