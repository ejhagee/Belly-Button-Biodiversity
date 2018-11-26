//function to build metadata panel
function buildMetadata(sample) {

    //build url
    var url = `/metadata/${sample}`;

    //get json output with d3 and build panel
    d3.json(url).then(function(response) {

        console.log(response);

        //use d3 to select the panel with id of #sample-metadata
        var panel = d3.select("#sample-metadata");

        //save wfreq
        var wfreq = response['WFREQ'];

        console.log(wfreq);

        //clear any existing metadata
        panel.html("");

        //use object.entries to add each key and value pair to the panel
        Object.entries(response).forEach(([key, value]) => {
            //append a paragraph tag
            var entryTag = panel.append("p");

            //write text for the tag
            entryTag.text(`${key}: ${value}`);
        });

        //build the gauge chart
        buildGauge(wfreq);
    });
}

//function to build the bubble and pie charts
function buildCharts(sample) {
    
    //build url
    var url = `/samples/${sample}`;

    //get json output with d3 and build plots
    d3.json(url).then(function(response) {

        //build bubble chart

        //save arrays
        var otu_ids = response['otu_ids'];
        var sample_values = response['sample_values'];
        var otu_labels = response['otu_labels'];

        //slice for top ten of each
        var otu_ids_10 = otu_ids.slice(0, 10);
        var sample_values_10 = sample_values.slice(0, 10);
        var otu_labels_10 = otu_labels.slice(0, 10);

        //log some data
        console.log(otu_ids_10);
        console.log(otu_labels_10);
        console.log(sample_values_10);

        //build trace and data
        var trace1 = {
            x: otu_ids,
            y: sample_values,
            mode: "markers",
            marker: {
                size: sample_values,
                color: otu_ids
            },
            text: otu_labels,
            textinfo: 'none',
            hoverinfo: 'x+y+z+text',
            type: 'scatter'
        };
        var data1 = [trace1];

        //build bubble plot layout
        var layout1 = {
            showlegend: false,
            title: `All Data for Sample ${sample}`,
            xaxis: {title: "OTU ID"},
            yaxis: {title: "Value"}
        };

        //plot bubble plot
        Plotly.newPlot("bubble", data1, layout1);

        //build pie chart with top ten entries (already sorted in response)
        //build data
        var trace2 = {
            values: sample_values_10,
            labels: otu_ids_10,
            type: 'pie',
            text: otu_labels_10,
            textinfo: 'percent',
            hoverinfo: 'label+text+value+percent'
        };
        var data2 = [trace2];

        //build layout
        var layout2 = {
            title: `Top Ten Measurements for Sample ${sample}`,
        };

        //build plot
        Plotly.newPlot("pie", data2, layout2);

    });
}

//function to initiate plots
function init() {
    //grab a reference to the dropdown select
    var selector = d3.select("#selDataset");

    //use the list of sample names to populate the select options
    d3.json("/names").then((sampleNames) => {
        sampleNames.forEach((sample) => {
            selector.append("option").text(sample).property("value", sample);
        });

        //use the first sample from list to build the initial plots
        const firstSample = sampleNames[0];
        buildCharts(firstSample);
        buildMetadata(firstSample);
    });
}

//function to change charts when a new sample is selected
function optionChanged(newSample) {
    //fetch new data and build charts
    buildCharts(newSample);
    buildMetadata(newSample);
}

//Initialize the dashboard
init();