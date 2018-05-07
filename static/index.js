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


dropDown();


function sampleTable(sample_id) {
    let metaUrl = `/metadata/${sample_id}`

    Plotly.d3.json(metaUrl, (error, metaData) => {
        if (error) return console.warn(error);

        console.log(metaData);

        console.log(Object.keys(metaData));

        let $tbody = Plotly.d3.select('tbody');

        $tbody.selectAll('tr')
            .data(metaData)
            .enter()
            .append('tr')
            .html(data => {
                return `<td>${Object.keys(data)}</td><td>${data[Object.keys(data)]}</td>`;
            });
    });

}


sampleTable('BB_940');


function optionChanged(sample_id) {
    console.log(sample_id);

    switch (sample_id) {
        case sample_id:
            sampleTable(sample_id);
            break;
        default:
            sampleTable("BB_940");
            break;
    }
}