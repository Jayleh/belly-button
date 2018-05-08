// // get value on change select
// function getValue() {
//     value = document.querySelector("select").value;
//     getDataPie(value);
//     getDataTable(value);
//     getDataGauge(value);
//     getDataBubble(value);
// }


function dropDown() {
    let $select = Plotly.d3.select('#selDataset');

    let namesUrl = '/names'

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

    let $tbody = Plotly.d3.select('#data-table');

    Plotly.d3.json(metaUrl, (error, metaData) => {
        if (error) return console.warn(error);

        console.log(metaData);

        console.log(Object.keys(metaData));

        $tbody.append('tbody')
            .selectAll('tr')
            .data(metaData)
            .enter()
            .append('tr')
            .html(data => {
                return `<td>${Object.keys(data)}</td><td>${data[Object.keys(data)]}</td>`;
            });
    });
}


function pieChart(sample_id) {
    let samplesUrl = `/samples/${sample_id}`;

    Plotly.d3.json(samplesUrl, (error, samplesData) => {
        if (error) return console.warn(error);

        // console.log(samplesData);

        let pieTrace = {
            labels: samplesData[0].otu_ids.slice(0, 10),
            values: samplesData[1].sample_values.slice(0, 10),
            type: 'pie'
        };

        let pieData = [pieTrace];

        let pieLayout = {

        };

        Plotly.newPlot('pie', pieData, pieLayout);
    });
}


function bubbleChart(sample_id) {
    let samplesUrl = `/samples/${sample_id}`;

    Plotly.d3.json(samplesUrl, (error, samplesData) => {
        if (error) return console.warn(error);

        // console.log(samplesData);

        let bubbleTrace = {
            x: samplesData[0].otu_ids,
            y: samplesData[1].sample_values,
            mode: 'markers',
            marker: {
                size: samplesData[1].sample_values,
                colorscale: 'Portland',
                color: samplesData[0].otu_ids
            }
        };

        let bubbleData = [bubbleTrace];

        let bubbleLayout = {
            xaxis: {
                title: 'Operational Taxonomic Unit (OTU) ID'
            },
            yaxis: {
                title: 'Sample Values'
            },
            height: 600,
            width: 1200
        };

        Plotly.newPlot('bubble', bubbleData, bubbleLayout);
    });
}


function optionChanged(sample_id) {
    console.log(sample_id);

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