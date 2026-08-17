import argparse
import pandas as pd
from pydeseq2.dds import DeseqDataSet
from pydeseq2.ds import DeseqStats

parser = argparse.ArgumentParser()
parser.add_argument("--counts", required=True)
parser.add_argument("--sample_sheet", required=True)
parser.add_argument("--output", required=True)
args = parser.parse_args()

counts = pd.read_csv(args.counts)
sample_sheet = pd.read_csv(args.sample_sheet)
sample_sheet = sample_sheet.set_index("sample_id")
counts = counts.set_index("Name").T
counts = counts.round().astype(int)

dds = DeseqDataSet(
    counts=counts,
    metadata=sample_sheet,
    design="~condition",
)
dds.deseq2()

stats = DeseqStats(dds)
stats.summary()

results = stats.results_df
results.to_csv(args.output)