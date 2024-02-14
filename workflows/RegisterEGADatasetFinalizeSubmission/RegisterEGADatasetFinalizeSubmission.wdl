version 1.0

workflow RegisterEGADatasetFinalizeSubmission {
    input {
        String submission_accession_id
        String ega_inbox
        String policy_title
        Array[String] library_strategy
        Array[String] run_provisional_ids
        String? dataset_title
        String? dataset_description
    }

    call RegisterDatasetFinalizeSubmission {
        input:
            submission_accession_id = submission_accession_id,
            ega_inbox = ega_inbox,
            policy_title = policy_title,
            library_strategy = library_strategy,
            run_provisional_ids = run_provisional_ids,
            dataset_title = dataset_title,
            dataset_description = dataset_description
    }

}

task RegisterDatasetFinalizeSubmission {
    input {
        String submission_accession_id
        String ega_inbox
        String policy_title
        Array[String] library_strategy
        Array[String] run_provisional_ids
        String? dataset_title
        String? dataset_description
    }

    command {
        python3 /scripts/register_dataset_and_finalize_submission.py \
            -submission_accession_id ~{submission_accession_id} \
            -user_name ~{ega_inbox} \
            -policy_title ~{policy_title} \
            -library_strategy ${sep=',' library_strategy} \
            -run_provisional_ids ${sep=',' run_provisional_ids} \
            -dataset_title ~{dataset_title} \
            -dataset_description ~{dataset_description} \
    }

    runtime {
        preemptible: 3
        docker: "us-east1-docker.pkg.dev/sc-ega-submissions/ega-submission-scripts/python-scripts:0.0.1-1706897788"
    }
}