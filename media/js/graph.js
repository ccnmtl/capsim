//var margin = 15;
//width = 860;
//height = 200;
var makeGraph = function (loc, data, width, height, yAxisLabel) {
    var margin = {top: 30, right: 20, bottom: 30, left: 50};
    var w = width - margin.left - margin.right;
    var h = height - margin.top - margin.bottom;

    y = d3.scale.linear().domain([120, 80]).range([0, h]);
    x = d3.scale.linear().domain([0, data.length]).range([0, w]);

    var xAxis = d3.svg.axis().scale(x)
         .orient("bottom").ticks(5);
    var yAxis = d3.svg.axis().scale(y)
         .orient("left").ticks(5);
    var valueLine = d3.svg.line()
		    .x(function(d,i) { return x(i); })
		    .y(function(d) { return y(d); });
    var svg = d3.select(loc)
        .append("svg:svg")
            .attr("width", width)
            .attr("height", height)
        .append("svg:g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    svg.append("path")
       .attr("d", valueLine(data))
       .attr("class", "mean");

    svg.append("g")
        .attr("class", "x-axis")
        .attr("transform", "translate(0," + h + ")")
        .call(xAxis);

    svg.append("text")
        .attr("transform", "translate(" + (w / 2) + " ," + (h + margin.bottom) + ")")
        .style("text-anchor", "middle")
        .text("Simulation Time");

    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis);

    svg.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 0 - margin.left)
        .attr("x", 0 - (h / 2))
        .attr("dy", "1em")
        .style("text-anchor", "middle")
        .text(yAxisLabel);
};
