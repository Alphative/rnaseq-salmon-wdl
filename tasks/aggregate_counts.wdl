version 1.0
task aggregate_counts {
    input{
        Array[String] sample_ids
        String output_name
        Array[File] quant_results
    }

    command <<<
    python3 /opt/scripts/aggregate_counts.py \
    --quant_files ~{sep=' ' quant_results} \
    --sample_ids ~{sep=' ' sample_ids} \
    --output ~{output_name}
    >>>

    output {
        File counts_matrix = output_name
    }

    runtime{
        docker: "rnaseq-salmon-wdl:analysis"
    }
}