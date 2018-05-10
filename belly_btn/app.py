import os
from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
import numpy as np
import pandas as pd
from initdb import Otu, Samples, SamplesMetadata

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', '') or "sqlite:///data/belly_button_biodiversity.sqlite"

db = SQLAlchemy(app)


@app.route('/')
def home():
    """Return to homepage"""
    return render_template("index.html")


@app.route('/names')
def names():

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

    return jsonify(samples)


@app.route('/otu')
def otu():

    # Get operation taxonomic unit (otu) description from Otu
    otu_list = db.session.query(Otu.lowest_taxonomic_unit_found).all()

    # Convert list of tuples into normal list
    otu_desc = list(np.ravel(otu_list))

    return jsonify(otu_desc)


@app.route('/metadata')
def metadata():

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

    return jsonify(sample_metadata)


@app.route('/metadata/<sample>')
def metadata_sample(sample):

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

    for metadata in sample_metadata:

        sample_id = int(sample[3:])

        if metadata['SAMPLEID'] == sample_id:

            return jsonify(metadata)

    return jsonify({"error": f"Sample name of '{sample}' not found."}), 404


@app.route('/wfreq/<sample>')
def wfreq(sample):

    # Query fields from SamplesMetadata
    results = db.session.query(SamplesMetadata.SAMPLEID, SamplesMetadata.WFREQ).all()

    # Create lists of dicts
    sample_metadata = []

    for result in results:

        row = {}

        row["SAMPLEID"] = result[0]
        row["WFREQ"] = result[1]

        sample_metadata.append(row)

    for metadata in sample_metadata:

        sample_id = int(sample[3:])

        if metadata['SAMPLEID'] == sample_id:

            return jsonify(metadata)

    return jsonify({"error": f"Sample name of '{sample}' not found."}), 404


@app.route('/samples/<sample>')
def samples(sample):

    # Initialize an empty list to store the sample table
    otu_ids_by_samples = []

    for row in db.session.query(Samples).all():
        otu_ids_by_samples.append(row.__dict__)

    samples_df = pd.DataFrame.from_dict(otu_ids_by_samples)

    target_sample_df = samples_df[sample_id].sort_values(ascending=False).reset_index()

    target_sample_df.columns = ["otu_ids", "sample_values"]

    otu_id_values = [{'otu_ids': [ids for ids in target_sample_df['otu_ids']]},
                     {'sample_values': [values for values in target_sample_df['sample_values']]}]

    try:
        otu_id_values = get_otu_id_values(sample)
    except KeyError:
        return jsonify({"error": f"Sample name of '{sample}' not found."}), 404

    return jsonify(otu_id_values)


if __name__ == '__main__':
    app.run(debug=True)
