version 1.0
task salmon_index{
    input{
        File ref_cdna
    }
    
    command <<<
    salmon index \
    -t ~{ref_cdna} \
    -i salmon_index
    >>>

    output {
        Array[File] index_files = glob("salmon_index/*")
    }

    runtime {
        docker: "rnaseq-salmon-wdl:salmon"
        cpu: 4
        memory: "16 GB"
        maxRetries: 2
    }
}
