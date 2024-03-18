version 1.0

workflow EGAFileTransfer {
    input {
      File aggregation_path
      File crypt4gh_encryption_key
      String ega_inbox
  }

  call EncryptDataFiles {
      input:
        aggregation_path = aggregation_path,
        crypt4gh_encryption_key = crypt4gh_encryption_key
  }

  call InboxFileTransfer {
    input:
      encrypted_data_file = EncryptDataFiles.encrypted_data_file,
      ega_inbox = ega_inbox
  }
}

task EncryptDataFiles {
    input {
        File aggregation_path
        File crypt4gh_encryption_key
    }

    Int disk_size = ceil(size(aggregation_path, "GiB") * 2.5)

    command {
        set -eo pipefail
        python3 /scripts/encrypt_data_file.py \
            --aggregation_path ~{aggregation_path} \
            --crypt4gh_encryption_key ~{crypt4gh_encryption_key} \
    }

    runtime {
        memory: "30 GB"
        docker: "us-east1-docker.pkg.dev/sc-ega-submissions/ega-submission-scripts/python-scripts:0.0.1-1709154068"
        cpu: 2
        disks: "local-disk " + disk_size + " HDD"
    }

    output {
        File encrypted_data_file = basename(aggregation_path)
    }
}

task InboxFileTransfer {
    input {
        File encrypted_data_file
        String ega_inbox
    }

    Int disk_size = ceil(size(encrypted_data_file, "GiB") * 2.5)

    command {
        set -eo pipefail
        python3 /scripts/transfer_ega_file.py \
            --encrypted_data_file ~{encrypted_data_file} \
            --ega_inbox ~{ega_inbox} \
    }

    runtime {
        memory: "30 GB"
        docker: "us-east1-docker.pkg.dev/sc-ega-submissions/ega-submission-scripts/python-scripts:0.0.1-1709154068"
        cpu: 2
        disks: "local-disk " + disk_size + " HDD"
    }

    output {}
}