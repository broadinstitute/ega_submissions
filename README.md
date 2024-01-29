# EGA Submissions

## Overview
The EGA Submissions repository serves as a comprehensive solution for orchestrating submissions to the European Genome-phenome Archive (EGA). It encompasses three distinct Workflow Description Language (WDL) scripts, each responsible for a crucial step in the submission process:

1. **File Transfer WDL**: 
   - This script is designed for submitting data files to the EGA. It manages the efficient and secure transfer of genomic data to the archive, ensuring a seamless submission process.

2. **Experiment and Run Registration WDL**: 
   - Responsible for registering the experiment and run details associated with the submitted data. This step ensures accurate tracking and metadata association, enhancing the organization of genomic information within the EGA.

3. **Dataset Finalization WDL**: 
   - This script handles the finalization of datasets, ensuring completeness and integrity. It encompasses any necessary post-submission steps, providing a comprehensive end-to-end solution for EGA submissions.

The workflow execution follows a sequential order:

- **Step 1: File Transfer**
  - Initiates the secure transfer of genomic data files to the EGA.

- **Step 2: Experiment and Run Registration**
  - Registers essential metadata related to the experiment and run, facilitating proper organization within the EGA.

- **Step 3: Dataset Finalization**
  - Completes the submission process by finalizing datasets and performing any post-submission tasks.

This repository equips users with the necessary tools and resources to streamline the submission of genomic data to the EGA, ensuring a well-organized and efficient workflow from file transfer to dataset finalization.

## Features
- **Workflows:** This directory will house all of the WDLS responsible for Sample submission. (e.g., EGAFileTransfer.wdl, RegisterEGAExperimentAndRunRegister.wdl, EGADatasetFinalizeSubmission.wdl).
- **Scripts:** This directory contains all the Python code responsible for the delivery of samples.

## Making Changes
Deploying any changes to this repo has two different methods based on where the changes are made. 

### Workflow Updates
Making any changes inside of the workflows directory is straightforward. Simply push your changes to the repository. Since we are using GitHub Apps, these changes will be automatically loaded into Terra. Then inside of Terra, select your branch.

![Updating version in Terra](images/workspace_info.png)

### Script Updates
When making changes to the Python code, you will need to rebuild and push the Docker images. Follow these commands below:
```bash
docker build . -t gcr.io/gdc-submissions/ega-submission-scripts:1.0.0
docker push gcr.io/gdc-submissions/ega-submission-scripts:1.0.0

Sometimes, it is helpful to view the contents of the Docker image. To do this, we can simply SSH into the image:
```
docker pull gcr.io/gdc-submissions/ega-submission-scripts:1.0.0
docker run -it gcr.io/gdc-submissions/ega-submission-scripts:1.0.0
```