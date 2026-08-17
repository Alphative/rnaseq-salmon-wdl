import pandas as pd
from differential_expression import prepare_data


def test_prepare_data_transposes_counts_and_indexes_metadata():
    counts = pd.DataFrame({
        "Name": ["geneA", "geneB"],
        "control_1": [100.4, 20.1],
        "control_2": [95.6, 18.9],
    })
    sample_sheet = pd.DataFrame({
        "sample_id": ["control_1", "control_2"],
        "condition": ["control", "control"],
    })

    prepared_counts, prepared_sheet = prepare_data(counts, sample_sheet)

    assert list(prepared_counts.index) == ["control_1", "control_2"]
    assert list(prepared_counts.columns) == ["geneA", "geneB"]
    assert prepared_sheet.index.name == "sample_id"


def test_prepare_data_rounds_fractional_counts_to_integers():
    counts = pd.DataFrame({
        "Name": ["geneA"],
        "sample1": [12.7],
    })
    sample_sheet = pd.DataFrame({
        "sample_id": ["sample1"],
        "condition": ["control"],
    })

    prepared_counts, _ = prepare_data(counts, sample_sheet)

    assert prepared_counts.loc["sample1", "geneA"] == 13
    assert prepared_counts.dtypes["geneA"].kind == "i"