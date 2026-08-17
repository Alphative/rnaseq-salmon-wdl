import argparse
import pandas as pd


def aggregate(quant_files, sample_ids):
    merged = None

    for quant_file, sample_id in zip(quant_files, sample_ids):
        df = pd.read_csv(quant_file, sep="\t")
        df = df[["Name", "NumReads"]].rename(columns={"NumReads": sample_id})

        if merged is None:
            merged = df
        else:
            merged = merged.merge(df, on="Name", how="outer")

    return merged


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--quant_files", nargs="+", required=True)
    parser.add_argument("--sample_ids", nargs="+", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    merged = aggregate(args.quant_files, args.sample_ids)
    merged.to_csv(args.output, index=False)