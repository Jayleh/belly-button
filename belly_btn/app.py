from flask import Flask, render_template, jsonify
from orm_queries import (get_samples,
                         get_otu_descriptions,
                         get_sample_metadata,
                         get_washing_frequency,
                         get_otu_id_values)

app = Flask(__name__)


@app.route('/')
def home():
    """Return to homepage"""
    return render_template("index.html")


@app.route('/names')
def names():
    """List of sample names.

    Returns a list of sample names in the format
    [
        "BB_940",
        "BB_941",
        "BB_943",
        "BB_944",
        "BB_945",
        "BB_946",
        "BB_947",
        ...
    ]
    """
    return jsonify(get_samples())


@app.route('/otu')
def otu():
    """List of OTU descriptions.

    Returns a list of OTU descriptions in the following format

    [
        "Archaea;Euryarchaeota;Halobacteria;Halobacteriales;Halobacteriaceae;Halococcus",
        "Archaea;Euryarchaeota;Halobacteria;Halobacteriales;Halobacteriaceae;Halococcus",
        "Bacteria",
        "Bacteria",
        "Bacteria",
        ...
    ]
    """
    return jsonify(get_otu_descriptions())


@app.route('/metadata')
def metadata():
    """MetaData for all samples.

    Returns a list of json of sample metadata in the format

    {
        AGE: 24,
        BBTYPE: "I",
        ETHNICITY: "Caucasian",
        GENDER: "F",
        LOCATION: "Beaufort/NC",
        SAMPLEID: 940
    }
    """
    return jsonify(get_sample_metadata())


@app.route('/metadata/<sample>')
def metadata_sample(sample):
    """MetaData for a given sample.

    Args: Sample in the format: `BB_940`

    Returns a json dictionary of sample metadata in the format

    {
        AGE: 24,
        BBTYPE: "I",
        ETHNICITY: "Caucasian",
        GENDER: "F",
        LOCATION: "Beaufort/NC",
        SAMPLEID: 940
    }
    """
    sample_metadata = get_sample_metadata()

    for metadata in sample_metadata:

        sample_id = int(sample[3:])

        if metadata['SAMPLEID'] == sample_id:

            return jsonify(metadata)

    return jsonify({"error": f"Sample name of '{sample}' not found."}), 404


@app.route('/wfreq/<sample>')
def wfreq(sample):
    """Weekly Washing Frequency as a number.

    Args: Sample in the format: `BB_940`

    Returns a json dictionary of sample and the weekly washing frequency `WFREQ`
    """
    sample_metadata = get_washing_frequency()

    for metadata in sample_metadata:

        sample_id = int(sample[3:])

        if metadata['SAMPLEID'] == sample_id:

            return jsonify(metadata)

    return jsonify({"error": f"Sample name of '{sample}' not found."}), 404


@app.route('/samples/<sample>')
def samples(sample):
    """OTU IDs and Sample Values for a given sample.

    Sort your Pandas DataFrame (OTU ID and Sample Value)
    in Descending Order by Sample Value

    Return a list of dictionaries containing sorted lists  for `otu_ids`
    and `sample_values`

    [
        {
            otu_ids: [
                1166,
                2858,
                481,
                ...
            ],
            sample_values: [
                163,
                126,
                113,
                ...
            ]
        }
    ]
    """
    try:
        otu_id_values = get_otu_id_values(sample)
    except KeyError:
        return jsonify({"error": f"Sample name of '{sample}' not found."}), 404

    return jsonify(otu_id_values)


if __name__ == '__main__':
    app.run(debug=True)
