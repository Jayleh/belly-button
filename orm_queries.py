# Dependencies
import sqlalchemy
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

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

        if sample_id != '_sa_instance_state':
            sample_names.append(sample_id)

    return sample_names
