version 1.0
task fastp_trim {
    input {
        String sample_id
        File read1
        File read2
    }

    command <<<
    fastp \
    -i ~{read1} -I ~{read2} \
    -o ~{sample_id}_trimmed_1.fastq.gz -O ~{sample_id}_trimmed_2.fastq.gz \
    --html ~{sample_id}_fastp.html \
    --json ~{sample_id}_fastp.json
    >>>

    output {
        File trimmed_read1 = "~{sample_id}_trimmed_1.fastq.gz"
        File trimmed_read2 = "~{sample_id}_trimmed_2.fastq.gz"
        File html_report = "~{sample_id}_fastp.html"
        File json_report = "~{sample_id}_fastp.json"
    }

    runtime {
        docker: ""
    }
}