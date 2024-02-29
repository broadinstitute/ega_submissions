# EGA Submissions

## Overview
The EGA Submissions repository serves as a comprehensive solution for orchestrating submissions to the [European Genome-Phenome Archive](https://ega-archive.org/) (EGA). It encompasses three distinct [Workflow Description Language](https://openwdl.org/) (WDL) scripts, each responsible for a crucial step in the submission process:

1. **[File Transfer WDL](workflows/EGAFileTransfer/EGAFileTransfer.wdl)**: 
   - This script is designed for submitting data files to the EGA. It manages the efficient and secure transfer of genomic data to the archive, ensuring a seamless submission process.

2. **[Experiment and Run Registration WDL](workflows/RegisterEGAExperimentAndRun/RegisterEGAExperimentAndRun.wdl)**: 
   - Responsible for registering the experiment and run details associated with the submitted data. This step ensures accurate tracking and metadata association, enhancing the organization of genomic information within the EGA.

3. **[Dataset Finalization WDL](workflows/RegisterEGADatasetFinalizeSubmission/RegisterEGADatasetFinalizeSubmission.wdl)**: 
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
- **[Workflows](workflows):** This directory will house all the WDLs responsible for Sample submission. (e.g., [EGAFileTransfer.wdl](workflows/EGAFileTransfer/EGAFileTransfer.wdl), [RegisterEGAExperimentAndRun.wdl](workflows/RegisterEGAExperimentAndRun/RegisterEGAExperimentAndRun.wdl), and [EGADatasetFinalizeSubmission.wdl](workflows/RegisterEGADatasetFinalizeSubmission/RegisterEGADatasetFinalizeSubmission.wdl)).
- **[Scripts](scripts):** This directory contains all the Python code responsible for the delivery of samples and registering metadata using the [EGA APIs](https://submission.ega-archive.org/api/spec/#/).

## Making Changes
Deploying any changes to this repository has two different methods based on where the changes are made.
In order to push changes to the Python code to GCR, you'll need the `gcloud` CLI (Command Line Interface) installed. See directions [here](https://cloud.google.com/sdk/docs/install).

### Script Updates
All Python code is contained in a Docker image, which is stored in Google Container Registry. The Terra workflows then pull these Docker images in the WDLs.
With every change to the Python code, you will need to rebuild and push the Docker image. You will need write access to the Container Registry in the `sc-ega-submissions` project. Reach out to Sam Bryant if you need these permissions.
To rebuild and push the Docker images, run the [docker_build.sh](docker_build.sh) script from the root of the repository: 
```commandline
./docker_build.sh
```

If you're not already logged in via gcloud, you will have to run `gcloud auth login` first and login via your Broad account.

Sometimes, it is helpful to view the contents of the Docker image. To do this, we can simply SSH into the image:
```bash
docker pull gcr.io/gdc-submissions/ega-submission-scripts:1.0.0
docker run -it gcr.io/gdc-submissions/ega-submission-scripts:1.0.0
```

Once you've built and pushed your Docker image, you'll have to find the Docker tag and update all the WDL workflows to use the new tag. 
To find the new Docker tag, you can navigate to GCR via the Google console [here](https://console.cloud.google.com/artifacts?authuser=0&project=sc-ega-submissions). Select the image name (in this case `ega-submission-scripts`), select `python-scripts`, and copy the latest tag. See screenshot below. In this example, the tag you'll want to copy is `0.0.1-1709154068`.

---
![Updating version in Terra](images/GCR_tag.png)

---

Once you have the tag, update the tag in all the WDL files where there is a docker image in the runtime attributes. The part you'll want to replace is everything after the `:`. 
So for example, this old tag would get changed in the following manner to the new tag:
```
OLD: us-east1-docker.pkg.dev/sc-ega-submissions/ega-submission-scripts/python-scripts:0.0.1-1708546220
NEW: us-east1-docker.pkg.dev/sc-ega-submissions/ega-submission-scripts/python-scripts:0.0.1-1709154068
```
Once you've made this change, push the changed to the GitHub repository. See [Workflow Updates](#workflow-updates) for how to implement changes in WDL files.

### Workflow Updates
Making any changes inside the workflows directory (i.e. to any WDL files) is straightforward. Simply push your changes to the GitHub repository. Since we are using GitHub Apps, these changes will be automatically loaded into Terra. If you'd like to test a feature branch, select your feature branch when running the workflow in Terra (see screenshot below). Alternatively, if you've merged your changes into `main`, ensure that `main` is selected as the branch (this should be the default branch).

---
![Updating version in Terra](images/workspace_info.png)

---


## Running an EGA Submission end-to-end
### One-time pre-requisites
1. Register your [EGA account](https://ega-archive.org/register/) and receive credentials (i.e. a username/inbox and password combination)
2. Submit [a request](https://profile.ega-archive.org/submitter-request) to receive a "Submitter" role status 

### One-time set up for each new Submission 
1. Create an initial "parent" Submission (once your request for the "Submitter" role is approved, you'll see an option in the [Submitter portal](https://submission.ega-archive.org/) to "Create a Submission")
2. Submit at least one Study (see detailed instructions [here](https://ega-archive.org/submission/metadata/submission/sequencing-phenotype/submitter-portal/))
3. Upload a cohort of Samples 
4. Register your DAC/Policy 
5. Fill out [this form](https://data-operations-portal.gotc-prod.broadinstitute.org/jira/ega_sample_submission/), including the same samples from your Study in the tsv which you upload to the form. Filling out this form will create a new Terra workspace, import all the necessary metadata into the data tables, and import all necessary workflows. All workflows will be pre-configured with inputs, there will be little that needs to changed manually. 
6. Once the ticket generated by the form is auto-resolved, this will indicate that your workspace is ready to go. 
7. Open your Terra workspace and navigate to the "Workflows" tab. 
8. The first workflow to be run is the `egaFileTransfer` workflow, which will encrypt and upload your bam/cram files to the EGA. 
   * All workflow inputs and outputs are pre-configured here, and nothing has to be changed. 
   * Ensure that `Run workflow(s) with inputs defined by data table` is selected
   * Ensure that the root entity type selected is `sample`
   * Ensure that `Use call caching` is selected
   * Ensure that `Delete intermediate outputs` is selected 
   * Now click `SELECT DATA` and from the little arrow at the top left box, select `All` and click `OK` then `RUN ANALYSIS` to submit your run(s). 
   * This workflow runs at the sample-level (i.e. if you have 100 samples in your workspace, 100 analysis will be submitted). 
   * Though encrypting and uploading the files does not take very long, the EGA validation of files may take a while. It's best to submit this workflow, ensure it finishes and wait at least a day before moving on to the next workflow.
9. The second workflow to be run is the `registerEGAExperimentAndRuns` workflow, which will register an experiment and run for each sample in the EGA submission. Only run this workflow once all samples have run to successful completion in the previous step. _**Note that this workflow will not complete unless the file has been validated on EGA's end. If the file has been validated, the metadata in the workspace will be updated to indicate its valid status and the workflow will continue (you'll see `validated` show up under the `file_validation_status` column in the workspace metadata). If not, the workflow will exit.**_ If a file has not been validated, you will have to wait and resubmit at a later date since we have no control over how long it takes for EGA to validate a file.
   * All workflow inputs and outputs are pre-configured here. The only parameter that you are welcome to change is the `delete_files` parameter. This is by default set to false, but setting it to true will delete the bam/cram after the file has been validated and the experiment/run have been registered in the EGA.
   * Ensure that `Run workflow(s) with inputs defined by data table` is selected
   * Ensure that the root entity type selected is `sample`
   * Ensure that `Use call caching` is selected
   * Ensure that `Delete intermediate outputs` is selected 
   * Now click `SELECT DATA` and from the little arrow at the top left box, select `All` and click `OK` then `RUN ANALYSIS` to submit your run(s).
   * This workflow runs at the sample-level (i.e. if you have 100 samples in your workspace, 100 analysis will be submitted).
10. The third and last workflow to be run is the `registerEGADataset`. Only run this workflow once all samples have run to successful completion in the previous step.
    * All workflow inputs and outputs are pre-configured here, however there are two that you may change: `dataset_description` and `dataset_title`. If these are not set, defaults will be used. However, we recommend that you fill these in if you know what you'd like these to be. These can be changed via the EGA Submitter Portal UI at any time once the dataset has been successfully created. 
    * Ensure that `Run workflow(s) with inputs defined by data table` is selected
    * Ensure that the root entity type selected is `sample_set`
    * Ensure that `Use call caching` is selected
    * Ensure that `Delete intermediate outputs` is selected 
    * Now click `SELECT DATA` and chose your sample set that includes ALL of your samples (i.e. if you have 100 samples, select the sample set that indicates that it includes 100 entities). Select `OK`, then `RUN ANALYSIS` to submit your _run_ (should only be 1 in this case!). 
    * This workflow runs at the sample set-level (i.e. even if you have 100 samples in your workspace, only 1 analysis should be submitted).
11. Once all 3 workflows have run to completion, your submission is finalized! You'll be able to view it in the Submitter Portal in the EGA. All metadata can be changed via the UI if desired.