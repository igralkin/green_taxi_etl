import pandas as pd


if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):

    data = data[(data['passenger_count'] > 0) & (data['trip_distance'] > 0)]

    print(len(data.index))
    data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date

    def transform_name_from_camel_to_snake(name: str) -> str:
        import re
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    for col in data.columns:
        print(col)
    data.columns = [transform_name_from_camel_to_snake(column) for column in data.columns]

    #current_vendor_ids = sorted(data['vendor_id'].unique())
    current_vendor_ids = [1, 2]
    print(current_vendor_ids)

    assert data['vendor_id'].isin(current_vendor_ids).all()
    assert all(data['passenger_count'] > 0)
    assert all(data['trip_distance'] > 0)

    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
