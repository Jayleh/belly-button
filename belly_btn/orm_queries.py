# Dependencies
import pandas as pd
import numpy as np
from initdb import Otu, Samples, SamplesMetadata
from app import db


def get_samples():

    # Sample contains list of all sample ids
    sample_ids = db.session.query(Samples).first()
    sample_dict = sample_ids.__dict__

    sample_names = []

    for sample_id in sample_dict:

        if sample_id != "_sa_instance_state" and sample_id != "otu_id":

            sample_number = int(sample_id[3:])

            sample_names.append(sample_number)

    samples = []

    sorted_samples = sorted(sample_names)

    for sample in sorted_samples:

        full_sample_name = f"BB_{sample}"

        samples.append(full_sample_name)

    return samples


def get_otu_descriptions():

    # Get operation taxonomic unit (otu) description from Otu
    otu_list = db.session.query(Otu.lowest_taxonomic_unit_found).all()

    # Convert list of tuples into normal list
    otu_desc = list(np.ravel(otu_list))

    return otu_desc


def get_sample_metadata():

    # Query fields from SamplesMetadata
    results = db.session.query(SamplesMetadata.AGE, SamplesMetadata.BBTYPE, SamplesMetadata.ETHNICITY,
                               SamplesMetadata.GENDER, SamplesMetadata.LOCATION,
                               SamplesMetadata.SAMPLEID).all()

    # Create lists of dicts
    sample_metadata = []

    for result in results:

        row = {}

        row["AGE"] = result[0]
        row["BBTYPE"] = result[1]
        row["ETHNICITY"] = result[2]
        row["GENDER"] = result[3]
        row["LOCATION"] = result[4]
        row["SAMPLEID"] = result[5]

        sample_metadata.append(row)

    return sample_metadata


def get_washing_frequency():

    # Query fields from SamplesMetadata
    results = db.session.query(SamplesMetadata.SAMPLEID, SamplesMetadata.WFREQ).all()

    # Create lists of dicts
    sample_metadata = []

    for result in results:

        row = {}

        row["SAMPLEID"] = result[0]
        row["WFREQ"] = result[1]

        sample_metadata.append(row)

    return sample_metadata


def get_otu_id_values(sample_id):

    # Initialize an empty list to store the sample table
    otu_ids_by_samples = []

    for row in db.session.query(Samples).all():
        otu_ids_by_samples.append(row.__dict__)

    samples_df = pd.DataFrame.from_dict(otu_ids_by_samples)

    target_sample_df = samples_df[sample_id].sort_values(ascending=False).reset_index()

    target_sample_df.columns = ["otu_ids", "sample_values"]

    otu_id_values = [{'otu_ids': [ids for ids in target_sample_df['otu_ids']]},
                     {'sample_values': [values for values in target_sample_df['sample_values']]}]

    return otu_id_values
