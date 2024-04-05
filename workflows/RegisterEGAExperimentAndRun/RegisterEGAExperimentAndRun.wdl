version 1.0

workflow RegisterEGAExperimentAndRun {
    input {
        String workspace_name
        String workspace_project
        String submission_accession_id
        String study_accession_id
        String ega_inbox
        String illumina_instrument
        String library_layout
        String library_strategy
        String library_source
        String library_selection
        String run_file_type
        String sample_alias
        String sample_id
        String group_library_name
        Float avg_mean_insert_size
        Float avg_standard_deviation
        String sample_material_type
        String construction_protocol
        String aggregation_path
        Boolean delete_files = false
    }

    # Check the file status
    call CheckEGAFileValidationStatus {
        input:
            submission_accession_id = submission_accession_id,
            ega_inbox = ega_inbox,
            sample_alias = sample_alias,
            sample_id = sample_id
    }

    # Write the validation status to the Terra data tables
    call UpsertMetadataToDataModel as UpsertFileValidation {
        input:
            workspace_name = workspace_name,
            workspace_project = workspace_project,
            tsv = CheckEGAFileValidationStatus.sample_id_validation_status_tsv
    }

    # Check the validation status and only continue to registering the metadata if the file is valid
    if (CheckEGAFileValidationStatus.validation_status == "validated") {

        call RegisterExperimentAndRun {
            input:
                submission_accession_id = submission_accession_id,
                study_accession_id = study_accession_id,
                ega_inbox = ega_inbox,
                illumina_instrument = illumina_instrument,
                library_layout = library_layout,
                library_strategy = library_strategy,
                library_source = library_source,
                library_selection = library_selection,
                run_file_type = run_file_type,
                sample_alias = sample_alias,
                sample_id = sample_id,
                group_library_name = group_library_name,
                avg_mean_insert_size = avg_mean_insert_size,
                avg_standard_deviation = avg_standard_deviation,
                sample_material_type = sample_material_type,
                construction_protocol = construction_protocol
        }

        call UpsertMetadataToDataModel as UpsertRunProvisionalId{
            input:
                workspace_name = workspace_name,
                workspace_project = workspace_project,
                tsv = RegisterExperimentAndRun.run_provisional_tsv
        }

        # If delete_files is set to true, proceed with deleting the cram/crai/md5 from the Terra bucket
        if (delete_files) {

            call DeleteFileFromBucket {
                input:
                    aggregation_path = aggregation_path
            }
        }
    }
}


task RegisterExperimentAndRun{
    input {
        String submission_accession_id
        String study_accession_id
        String ega_inbox
        String illumina_instrument
        String library_layout
        String library_strategy
        String library_source
        String library_selection
        String run_file_type
        String sample_alias
        String sample_id
        String group_library_name
        Float avg_mean_insert_size
        Float avg_standard_deviation
        String sample_material_type
        String construction_protocol
    }

    command {
        python3 /scripts/register_experiment_and_run_metadata.py \
            -submission_accession_id ~{submission_accession_id} \
            -study_accession_id ~{study_accession_id} \
            -user_name ~{ega_inbox} \
            -instrument_model ~{illumina_instrument} \
            -library_layout ~{library_layout} \
            -library_strategy ~{library_strategy} \
            -library_source ~{library_source} \
            -library_selection "~{library_selection}" \
            -run_file_type ~{run_file_type} \
            -run_file_type ~{run_file_type} \
            -technology ILLUMINA \
            -run_file_type ~{run_file_type} \
            -sample_alias ~{sample_alias} \
            -sample_id ~{sample_id} \
            -library_name ~{group_library_name} \
            -mean_insert_size ~{avg_mean_insert_size} \
            -standard_deviation ~{avg_standard_deviation} \
            -sample_material_type "~{sample_material_type}" \
            -construction_protocol "~{construction_protocol}" \
    }

    runtime {
        docker: "us-east1-docker.pkg.dev/sc-ega-submissions/ega-submission-scripts/python-scripts:0.0.1-1712000151"
    }

    output {
        File run_provisional_tsv = "sample_id_and_run_provisional_id.tsv"
    }
}

task CheckEGAFileValidationStatus {
    input {
        String submission_accession_id
        String ega_inbox
        String sample_alias
        String sample_id
    }

    command {
        python3 /scripts/check_file_validation_status.py \
            -submission_accession_id ~{submission_accession_id} \
            -user_name ~{ega_inbox} \
            -sample_alias ~{sample_alias} \
            -sample_id ~{sample_id} \
    }

    runtime {
        preemptible: 3
        docker: "us-east1-docker.pkg.dev/sc-ega-submissions/ega-submission-scripts/python-scripts:0.0.1-1712000151"
    }

    output {
        String validation_status = read_string("file_validation_status.tsv")
        File sample_id_validation_status_tsv = "sample_id_validation_status.tsv"
    }
}

task DeleteFileFromBucket {
    input {
        String aggregation_path
    }

    String aggregation_md5_path  = aggregation_path + ".md5"

    command <<<
        set -eo pipefail
        gsutil rm -a ~{aggregation_path}
        gsutil rm -a ~{aggregation_md5_path}
    >>>

    runtime {
        preemptible: 3
        docker: "us-east1-docker.pkg.dev/sc-ega-submissions/ega-submission-scripts/python-scripts:0.0.1-1712000151"
    }
}

task UpsertMetadataToDataModel {
    input {
        # workspace details
        String workspace_name
        String workspace_project
    
        # load file with sample metadata to ingest to table
        File   tsv
    }

    parameter_meta {
        workspace_name: "Name of the workspace to which WDL should push the additional sample metadata."
        workspace_project: "Namespace/project of workspace to which WDL should push the additional sample metadata."
        tsv: "Load tsv file formatted in the Terra required format to update the sample table."
    }

    command {
        set -eo pipefail
        python3 /scripts/batch_upsert_entities.py -w ~{workspace_name} \
                                                      -p ~{workspace_project} \
                                                      -t ~{tsv}
    }

    runtime {
        preemptible: 3
        docker: "us-east1-docker.pkg.dev/sc-ega-submissions/ega-submission-scripts/python-scripts:0.0.1-1712000151"
    }

    output {
        File ingest_logs = stdout()
    }
}