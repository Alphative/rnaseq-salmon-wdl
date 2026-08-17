version 1.0
task salmon_quant{
    input {
        String sample_id
        File read1
        File read2
        Array[File] index_files
        Int cpus = 4
    }

    command <<<
    mkdir salmon_index
    cp ~{sep=' ' index_files} salmon_index/
    salmon quant \
    -i salmon_index \
    -l A \
    -1 ~{read1} -2 ~{read2} \
    -p ~{cpus} \
    -o ~{sample_id}_salmon_quant/
    >>>

    output{
        File quant_results = glob("~{sample_id}_salmon_quant/quant.sf")[0]
    }

    runtime{
        docker: "rnaseq-salmon-wdl:salmon"
        cpu: cpus
        memory: "8 GB"
    }
}