function dropDown() {
    let $select = Plotly.d3.select('#selDataset');

    let namesUrl = '/names';

    Plotly.d3.json(namesUrl, (error, nameList) => {
        if (error) return console.warn(error);

        // console.log(nameList);

        $select.selectAll('option')
            .data(nameList)
            .enter()
            .append('option')
            .attr('value', data => data)
            .text(data => data);
    });
}


function sampleTable(sample_id) {
    let metaUrl = `/metadata/${sample_id}`;

    let $tbody = Plotly.d3.select('table#data-table tbody');

    Plotly.d3.json(metaUrl, (error, metaData) => {
        if (error) return console.warn(error);

        // console.log(metaData);
        // console.log(Object.keys(metaData));

        $tbody.selectAll('tr').remove();

        for (let key in metaData) {
            $tbody.append('tr')
                .html(`<td>${key}</td><td>${metaData[key]}</td>`);
        }
    });
}


function getClassification(otuIds) {
    let otuUrl = '/otu';

    let otuList = [];

    Plotly.d3.json(otuUrl, (error, otuData) => {
        if (error) return console.warn(error);

        // console.log(otuData);

        for (let i = 0, ii = otuData.length; i < ii; i++) {
            for (let j = 0, jj = otuIds.length; j < jj; j++) {
                if (i === +otuIds[j]) {
                    otuList.push(otuData[i]);
                }
            }
        }
    });

    return otuList;
}


function pieChart(sample_id) {
    let samplesUrl = `/samples/${sample_id}`;

    Plotly.d3.json(samplesUrl, (error, samplesData) => {
        if (error) return console.warn(error);

        // console.log(samplesData);

        let otuIds = samplesData[0].otu_ids.slice(0, 10);
        let sampleValues = samplesData[1].sample_values.slice(0, 10);

        let otuList = getClassification(otuIds);

        let pieTrace = {
            labels: otuIds,
            values: sampleValues,
            type: 'pie',
            text: otuList,
            textinfo: 'percent',
            textposition: 'inside'
            // hoverinfo: `label+percent+value+${otuList}`
        };

        let pieData = [pieTrace];

        let pieLayout = {
            height: 300,
            width: 500,
            margin: {
                l: 0,
                r: 20,
                b: 0,
                t: 30,
            }
        };

        Plotly.react('pie', pieData, pieLayout);

        // let hasChart = Plotly.d3.select('#pie').classed('js-plotly-plot');

        // if (hasChart === true) {
        //     Plotly.restyle('pie', pieTrace);
        // }
        // else {
        //     Plotly.newPlot('pie', pieData, pieLayout);
        // }
    });
}


function bubbleChart(sample_id) {
    let samplesUrl = `/samples/${sample_id}`;

    Plotly.d3.json(samplesUrl, (error, samplesData) => {
        if (error) return console.warn(error);

        // console.log(samplesData);

        let sampleValues = samplesData[1].sample_values.filter(num => { return num !== 0; });
        let otuIds = samplesData[0].otu_ids.slice(0, sampleValues.length);

        // console.log(sampleValues);
        // console.log(otuIds);

        let otuList = getClassification(otuIds);

        let bubbleTrace = {
            x: otuIds,
            y: sampleValues,
            text: otuList,
            mode: 'markers',
            marker: {
                size: sampleValues,
                colorscale: 'Portland',
                color: otuIds
            }
        };

        let bubbleData = [bubbleTrace];

        let bubbleLayout = {
            hovermode: 'closest',
            xaxis: {
                title: 'Operational Taxonomic Unit (OTU) ID'
            },
            yaxis: {
                title: 'Sample Values'
            },
            height: 600,
            width: 1200,
            margin: {
                l: 80,
                r: 100,
                b: 100,
                t: 30,
            }
        };

        Plotly.react('bubble', bubbleData, bubbleLayout);

        // let hasChart = Plotly.d3.select('#bubble').classed('js-plotly-plot');

        // if (hasChart === true) {
        //     Plotly.restyle('bubble', bubbleTrace);
        // }
        // else {
        //     Plotly.newPlot('bubble', bubbleData, bubbleLayout);
        // }
    });
}


function optionChanged(sample_id) {
    // console.log(sample_id);

    switch (sample_id) {
        case sample_id:
            sampleTable(sample_id);
            pieChart(sample_id);
            bubbleChart(sample_id);
            break;
        default:
            sampleTable("BB_940");
            pieChart("BB_940");
            bubbleChart("BB_940");
            break;
    }
}


function init() {
    dropDown();
    sampleTable('BB_940');
    pieChart('BB_940');
    bubbleChart('BB_940');
}


init();