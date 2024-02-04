import pyarrow as pa
import pyarrow.parquet as pq
import os


if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/home/src/XXXXXX.json"

bucket_name = 'mage-zoomcamp-maratsh'
project_id = 'rosy-element-294708'

table_name = "green_taxi"

root_path = f'{bucket_name}/{table_name}'


@data_exporter
def export_data(data, *args, **kwargs):

    data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date
    #print(data)
    dates = sorted(data['lpep_pickup_date'].unique())
    #print(dates)
    table = pa.Table.from_pandas(data)
    #print(table)
 
    gcs = pa.fs.GcsFileSystem()

    pq.write_to_dataset(
        table,
        root_path=root_path,
        partition_cols=['lpep_pickup_date'],
        filesystem=gcs
    )
 
