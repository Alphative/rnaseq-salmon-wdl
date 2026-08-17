import pandas as pd
from aggregate_counts import aggregate


def test_aggregate_merges_two_samples(tmp_path):
    quant1 = tmp_path / "sample1_quant.sf"
    quant2 = tmp_path / "sample2_quant.sf"

    quant1.write_text(
        "Name\tLength\tEffectiveLength\tTPM\tNumReads\n"
        "AT1G01010.1\t500\t450\t10.5\t120.0\n"
        "AT1G01020.1\t300\t250\t5.2\t40.0\n"
    )
    quant2.write_text(
        "Name\tLength\tEffectiveLength\tTPM\tNumReads\n"
        "AT1G01010.1\t500\t450\t8.1\t95.0\n"
        "AT1G01020.1\t300\t250\t6.7\t55.0\n"
    )

    result = aggregate(
        quant_files=[str(quant1), str(quant2)],
        sample_ids=["sample1", "sample2"],
    )

    assert list(result.columns) == ["Name", "sample1", "sample2"]
    assert len(result) == 2

    row = result[result["Name"] == "AT1G01010.1"].iloc[0]
    assert row["sample1"] == 120.0
    assert row["sample2"] == 95.0


def test_aggregate_handles_mismatched_transcripts(tmp_path):
    quant1 = tmp_path / "sample1_quant.sf"
    quant2 = tmp_path / "sample2_quant.sf"

    quant1.write_text(
        "Name\tLength\tEffectiveLength\tTPM\tNumReads\n"
        "geneA\t500\t450\t10.5\t120.0\n"
    )
    quant2.write_text(
        "Name\tLength\tEffectiveLength\tTPM\tNumReads\n"
        "geneB\t300\t250\t6.7\t55.0\n"
    )

    result = aggregate(
        quant_files=[str(quant1), str(quant2)],
        sample_ids=["sample1", "sample2"],
    )

    assert len(result) == 2
    assert set(result["Name"]) == {"geneA", "geneB"}
    assert result[result["Name"] == "geneA"]["sample2"].isna().all()