version 1.0

import "tasks/fastp.wdl" as fastp_task
import "tasks/salmon_index.wdl" as salmon_index_task
import "tasks/salmon_quant.wdl" as salmon_quant_task
import "tasks/aggregate_counts.wdl" as aggregate_task
import "tasks/differential_expression.wdl" as de_task

struct Sample {
  String sample_id
  File fastq_1
  File fastq_2
}

workflow rnaseq_pipeline {
    input {
    File cdna_reference
    File samples_tsv
    File condition_sheet
    }

    Array[Sample] samples = read_objects(samples_tsv)

    scatter (s in samples) {
        call fastp_task.fastp_trim {
            input:
            sample_id = s.sample_id,
            read1 = s.fastq_1,
            read2 = s.fastq_2
        }
    }

    call salmon_index_task.salmon_index {
        input :
        ref_cdna = cdna_reference
    }

    scatter (s in samples) {
        call salmon_quant_task.salmon_quant {
            input :
            sample_id = s.sample_id,
            read1 = s.fastq_1,
            read2 = s.fastq_2,
            index_files = salmon_index.index_files
        }
    }

    scatter (s in samples) {
        String sample_id_list = s.sample_id
    }

    call aggregate_task.aggregate_counts {
        input :
        sample_ids = sample_id_list,
        output_name = "counts.csv",
        quant_results = salmon_quant.quant_results

    }

    call de_task.differential_expression {
        input :
        counts_file = aggregate_counts.counts_matrix,
        sample_sheet_file = condition_sheet,
        output_name = "de_results.csv"
    }
}