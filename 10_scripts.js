// Load Google Charts
google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawStep1Chart);
google.charts.setOnLoadCallback(drawStep2Chart);

function drawStep1Chart() {
    var data = google.visualization.arrayToDataTable([
        ['Step', 'Time (hours)'],
        ['Problem Identification', 10],
        ['Data Collection', 20],
        ['Data Preparation', 30],
        ['Model Development', 40],
        ['Model Evaluation', 25],
        ['Deployment', 15],
        ['Monitoring and Maintenance', 10],
    ]);

    var options = {
        title: 'Time Spent on Each Step',
        pieHole: 0.4,
        is3D: true,
        colors: ['#4CAF50', '#2196F3', '#FFC107', '#FF5722', '#9C27B0', '#3F51B5', '#009688'],
        legend: { position: 'bottom' }
    };

    var chart = new google.visualization.PieChart(document.getElementById('step1-chart'));
    chart.draw(data, options);
}

function drawStep2Chart() {
    var data = google.visualization.arrayToDataTable([
        ['Step', 'Value'],
        ['Data Preparation', 30],
        ['Model Development', 50],
        ['Model Evaluation', 20],
    ]);

    var options = {
        title: 'Bar Chart of Steps',
        hAxis: { title: 'Steps' },
        vAxis: { title: 'Value' },
        colors: ['#3F51B5'],
        legend: { position: 'none' },
    };

    var chart = new google.visualization.BarChart(document.getElementById('step2-chart'));
    chart.draw(data, options);
}

// D3.js Line Chart with Variations
const lineData = [
    { step: 'Step 1', value: 10 },
    { step: 'Step 2', value: 20 },
    { step: 'Step 3', value: 30 },
    { step: 'Step 4', value: 40 },
    { step: 'Step 5', value: 35 },
    { step: 'Step 6', value: 50 },
];

const lineSvg = d3.select("#step3-chart")
    .append("svg")
    .attr("width", 400)
    .attr("height", 300);

// Define scales
const xScale = d3.scalePoint()
    .domain(lineData.map(d => d.step))
    .range([0, 380]);

const yScale = d3.scaleLinear()
    .domain([0, d3.max(lineData, d => d.value)])
    .range([250, 0]);

// Add axes
lineSvg.append("g")
    .attr("transform", "translate(0,250)")
    .call(d3.axisBottom(xScale));

lineSvg.append("g")
    .call(d3.axisLeft(yScale));

// Line generator with curve
const lineGenerator = d3.line()
    .x(d => xScale(d.step))
    .y(d => yScale(d.value))
    .curve(d3.curveNatural);  // Change curve type here

// Draw the line
lineSvg.append("path")
    .datum(lineData)
    .attr("fill", "none")
    .attr("stroke", "#FF5722")
    .attr("stroke-width", 2)
    .attr("d", lineGenerator);

// Add circles at data points
lineSvg.selectAll("circle")
    .data(lineData)
    .enter()
    .append("circle")
    .attr("cx", d => xScale(d.step))
    .attr("cy", d => yScale(d.value))
    .attr("r", 5)
    .attr("fill", (d, i) => d3.schemeCategory10[i % 10]); // Different colors for circles

// Add labels to data points
lineSvg.selectAll("text")
    .data(lineData)
    .enter()
    .append("text")
    .attr("x", d => xScale(d.step))
    .attr("y", d => yScale(d.value) - 10)
    .attr("text-anchor", "middle")
    .text(d => d.value);

// Area Chart
const areaData = [
    { step: 'Step 1', value: 10 },
    { step: 'Step 2', value: 20 },
    { step: 'Step 3', value: 30 },
    { step: 'Step 4', value: 40 },
    { step: 'Step 5', value: 35 },
    { step: 'Step 6', value: 50 },
];

const areaSvg = d3.select("#step4-chart")
    .append("svg")
    .attr("width", 400)
    .attr("height", 300);

const areaXScale = d3.scaleBand()
    .domain(areaData.map(d => d.step))
    .range([0, 380])
    .padding(0.1);

const areaYScale = d3.scaleLinear()
    .domain([0, d3.max(areaData, d => d.value)])
    .range([250, 0]);

areaSvg.append("g")
    .attr("transform", "translate(0,250)")
    .call(d3.axisBottom(areaXScale));

areaSvg.append("g")
    .call(d3.axisLeft(areaYScale));

const areaGenerator = d3.area()
    .x(d => areaXScale(d.step) + areaXScale.bandwidth() / 2)
    .y0(250)
    .y1(d => areaYScale(d.value));

areaSvg.append("path")
    .datum(areaData)
    .attr("fill", "#2196F3")
    .attr("d", areaGenerator);

// Scatter Plot
const scatterData = [
    { x: 1, y: 5, label: 'Step 1' },
    { x: 2, y: 15, label: 'Step 2' },
    { x: 3, y: 10, label: 'Step 3' },
    { x: 4, y: 25, label: 'Step 4' },
    { x: 5, y: 20, label: 'Step 5' },
    { x: 6, y: 30, label: 'Step 6' },
];

const scatterSvg = d3.select("#step5-chart")
    .append("svg")
    .attr("width", 400)
    .attr("height", 300);

const scatterXScale = d3.scaleLinear()
    .domain([0, d3.max(scatterData, d => d.x)])
    .range([40, 360]);

const scatterYScale = d3.scaleLinear()
    .domain([0, d3.max(scatterData, d => d.y)])
    .range([250, 0]);

scatterSvg.append("g")
    .attr("transform", "translate(0,250)")
    .call(d3.axisBottom(scatterXScale));

scatterSvg.append("g")
    .call(d3.axisLeft(scatterYScale));

const tooltip = d3.select("body").append("div")
    .attr("class", "tooltip");

scatterSvg.selectAll("circle")
    .data(scatterData)
    .enter()
    .append("circle")
    .attr("cx", d => scatterXScale(d.x))
    .attr("cy", d => scatterYScale(d.y))
    .attr("r", 5)
    .attr("fill", "#FF5722")
    .on("mouseover", function(event, d) {
        tooltip.transition()
            .duration(200)
            .style("opacity", .9);
        tooltip.html(`Label: ${d.label}<br/>X: ${d.x}<br/>Y: ${d.y}`)
            .style("left", (event.pageX + 5) + "px")
            .style("top", (event.pageY - 28) + "px");
    })
    .on("mouseout", function() {
        tooltip.transition()
            .duration(500)
            .style("opacity", 0);
    });

// Donut Chart
function drawDonutChart() {
    var data = google.visualization.arrayToDataTable([
        ['Step', 'Value'],
        ['Step 1', 10],
        ['Step 2', 20],
        ['Step 3', 30],
        ['Step 4', 40],
        ['Step 5', 50]
    ]);

    var options = {
        title: 'Donut Chart of Steps',
        pieHole: 0.4,
        colors: ['#FF5722', '#3F51B5', '#009688', '#FFC107', '#4CAF50'],
        legend: { position: 'right' }
    };

    var chart = new google.visualization.PieChart(document.getElementById('step6-chart'));
    chart.draw(data, options);
}

// Histogram
function drawHistogram() {
    const histogramData = [10, 15, 20, 30, 35, 40, 45, 50, 55, 60, 70];
    const histogramSvg = d3.select("#histogram-chart")
        .append("svg")
        .attr("width", 400)
        .attr("height", 300);

    const histogramXScale = d3.scaleBand()
        .domain(histogramData.map((d, i) => `Bin ${i + 1}`))
        .range([0, 380])
        .padding(0.1);

    const histogramYScale = d3.scaleLinear()
        .domain([0, d3.max(histogramData)])
        .range([250, 0]);

    histogramSvg.append("g")
        .attr("transform", "translate(0,250)")
        .call(d3.axisBottom(histogramXScale));

    histogramSvg.append("g")
        .call(d3.axisLeft(histogramYScale));

    histogramSvg.selectAll("rect")
        .data(histogramData)
        .enter()
        .append("rect")
        .attr("x", (d, i) => histogramXScale(`Bin ${i + 1}`))
        .attr("y", d => histogramYScale(d))
        .attr("width", histogramXScale.bandwidth())
        .attr("height", d => 250 - histogramYScale(d))
        .attr("fill", "#FFC107");
}

// Boxplot
function drawBoxplot() {
    const boxplotData = [10, 15, 20, 25, 30, 35, 40, 45, 50];
    const boxplotSvg = d3.select("#boxplot-chart")
        .append("svg")
        .attr("width", 400)
        .attr("height", 300);

    const boxplotXScale = d3.scaleBand()
        .domain(['Boxplot'])
        .range([0, 380])
        .padding(0.1);

    const boxplotYScale = d3.scaleLinear()
        .domain([0, d3.max(boxplotData)])
        .range([250, 0]);

    boxplotSvg.append("g")
        .attr("transform", "translate(0,250)")
        .call(d3.axisBottom(boxplotXScale));

    boxplotSvg.append("g")
        .call(d3.axisLeft(boxplotYScale));

    const q1 = d3.quantile(boxplotData, 0.25);
    const median = d3.quantile(boxplotData, 0.5);
    const q3 = d3.quantile(boxplotData, 0.75);
    const interquartileRange = q3 - q1;
    const min = d3.min(boxplotData);
    const max = d3.max(boxplotData);

    // Draw the box
    boxplotSvg.append("rect")
        .attr("x", boxplotXScale('Boxplot'))
        .attr("y", boxplotYScale(q3))
        .attr("width", boxplotXScale.bandwidth())
        .attr("height", boxplotYScale(q1) - boxplotYScale(q3))
        .attr("fill", "#2196F3");

    // Draw median line
    boxplotSvg.append("line")
        .attr("x1", boxplotXScale('Boxplot'))
        .attr("x2", boxplotXScale('Boxplot') + boxplotXScale.bandwidth())
        .attr("y1", boxplotYScale(median))
        .attr("y2", boxplotYScale(median))
        .attr("stroke", "#FF5722")
        .attr("stroke-width", 2);

    // Draw whiskers
    boxplotSvg.append("line")
        .attr("x1", boxplotXScale('Boxplot') + boxplotXScale.bandwidth() / 2)
        .attr("x2", boxplotXScale('Boxplot') + boxplotXScale.bandwidth() / 2)
        .attr("y1", boxplotYScale(min))
        .attr("y2", boxplotYScale(q1))
        .attr("stroke", "#000");

    boxplotSvg.append("line")
        .attr("x1", boxplotXScale('Boxplot') + boxplotXScale.bandwidth() / 2)
        .attr("x2", boxplotXScale('Boxplot') + boxplotXScale.bandwidth() / 2)
        .attr("y1", boxplotYScale(q3))
        .attr("y2", boxplotYScale(max))
        .attr("stroke", "#000");
}

google.charts.setOnLoadCallback(drawDonutChart);
drawHistogram();
drawBoxplot();