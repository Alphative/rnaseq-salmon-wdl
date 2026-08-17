import argparse
import pandas as pd
from pydeseq2.dds import DeseqDataSet
from pydeseq2.ds import DeseqStats


def prepare_data(counts, sample_sheet):
    sample_sheet = sample_sheet.set_index("sample_id")
    counts = counts.set_index("Name").T
    counts = counts.round().astype(int)
    return counts, sample_sheet


def run_differential_expression(counts_path, sample_sheet_path, output_path):
    counts = pd.read_csv(counts_path)
    sample_sheet = pd.read_csv(sample_sheet_path)
    counts, sample_sheet = prepare_data(counts, sample_sheet)

    dds = DeseqDataSet(
        counts=counts,
        metadata=sample_sheet,
        design="~condition",
    )
    dds.deseq2()

    stats = DeseqStats(dds, contrast=["condition", "treatment", "control"])
    stats.summary()

    results = stats.results_df
    results.to_csv(output_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--counts", required=True)
    parser.add_argument("--sample_sheet", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    run_differential_expression(args.counts, args.sample_sheet, args.output)