# EGA Submissions

## Overview
The EGA Submissions repository is dedicated to managing submissions to the European Genome-phenome Archive (EGA). It provides a set of tools and resources for efficiently submitting and managing genomic data. Sample submission will be executed in the order of File Transfer -> Registering fo the Experiment and Run ->  Finalizing the Dataset.

## Features
- **Workflows:** This directory will house all of the WDLS responsible for Sample submission. I.e - EGAFileTransfer.wdl, RegisterEGAExperimentAndRunRegister.wdl EGADatasetFinalizeSubmission.wdl.
- **Scripts:** This directory will contain all the python code that is responsible for the delivery of samples

## Making Changes
Deploying any changes to this repo has to different methods based on where the changes are made. 

### Workflow Updates
Making any changes inside of the workflows directory is very simple. Just push your changes to repository. Since we are using github apps these changes will be automatically loaded into Terra. Then inside of Terra simply select your branch

TODO - add picture from terra

### Script Updates
When making any changes to the python code you will need to rebuild and push the docker images. You can follow these commands below 
TODO - update this when we get the new docker image
```
docker build . -t schaluvadi/horsefish:submissionV2GDC
docker push schaluvadi/horsefish:submissionV2GDC
```

Sometimes it is helpful to view the contents of the docker image. To do this we can simply ssh into the image
```
docker pull schaluvadi/horsefish:submissionV2GDC
docker run -it schaluvadi/horsefish:submissionV2GDC
```