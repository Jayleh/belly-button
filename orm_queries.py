# Dependencies
import sqlalchemy
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import numpy as np

# Create engine
engine = create_engine("sqlite:///data/belly_button_biodiversity.sqlite")

# Declare Base
Base = automap_base()

# Use Base class to reflect database tables
Base.prepare(engine, reflect=True)

# Assign classes to variables
Otu = Base.classes.otu
Samples = Base.classes.samples
SamplesMetadata = Base.classes.samples_metadata

# Create a session
session = Session(engine)


def get_samples():

    # Sample contains list of all sample ids
    sample_ids = session.query(Samples).first()
    sample_dict = sample_ids.__dict__

    sample_names = []

    for sample_id in sample_dict:

        if sample_id != '_sa_instance_state' and sample_id != 'otu_id':

            sample_number = int(sample_id[3:])

            sample_names.append(sample_number)

    samples = []

    sorted_samples = sorted(sample_names)

    for sample in sorted_samples:

        full_sample_name = f'BB_{sample}'

        samples.append(full_sample_name)

    return samples


def get_otu_descriptions():

    # Get operation taxonomic unit (otu) description from Otu
    otu_list = session.query(Otu.lowest_taxonomic_unit_found).all()

    # Convert list of tuples into normal list
    otu_desc = list(np.ravel(otu_list))

    return otu_desc


def get_sample_metadata():

    # Query fields from SamplesMetadata
    results = session.query(SamplesMetadata.AGE, SamplesMetadata.BBTYPE, SamplesMetadata.ETHNICITY,
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
