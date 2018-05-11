# Dependencies
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base

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
