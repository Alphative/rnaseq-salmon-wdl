version 1.0
task differential_expression{
    input{
        File counts_file
        File sample_sheet_file
        String output_name
    }

    command<<<
    python3 /opt/scripts/differential_expression.py \
    --counts ~{counts_file} \
    --sample_sheet ~{sample_sheet_file} \
    --output ~{output_name}
    >>>

    output{
        File de_results = output_name
    }

    runtime{
        docker : "rnaseq-salmon-wdl:analysis"
    }
}