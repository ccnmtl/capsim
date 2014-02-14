//var margin = 15;
//width = 860;
//height = 200;
var makeGraph = function (loc, data, stddevs, width, height, margin) {
    var w = width;
    var h = height;

    y = d3.scale.linear().domain([0, d3.max(data)]).range([0 + margin, height - margin]);
    x = d3.scale.linear().domain([0, data.length]).range([0 + margin, width - margin]);

    var vis = d3.select(loc)
        .append("svg:svg")
        .attr("width", w)
        .attr("height", h);

    var g = vis.append("svg:g")
        .attr("transform", "translate(0, " + height + ")");
		
    var line = d3.svg.line()
		    .x(function(d,i) { return x(i); })
		    .y(function(d) { return -1 * y(d); });
		
    g.append("svg:path").attr("d", line(data)).attr("class", "mean");
    g.append("svg:path").attr("d", line(stddevs)).attr("class", "stddev");
		
    g.append("svg:line")
		    .attr("x1", x(0))
		    .attr("y1", -1 * y(0))
		    .attr("x2", x(w))
		    .attr("y2", -1 * y(0));

    g.append("svg:line")
		    .attr("x1", x(0))
		    .attr("y1", -1 * y(0))
		    .attr("x2", x(0))
		    .attr("y2", -1 * y(d3.max(data)));
		
    g.selectAll(".xLabel")
		    .data(x.ticks(5))
		    .enter().append("svg:text")
		    .attr("class", "xLabel")
		    .text(String)
		    .attr("x", function(d) { return x(d) })
		    .attr("y", 0)
		    .attr("text-anchor", "middle");

    g.selectAll(".yLabel")
		    .data(y.ticks(4))
		    .enter().append("svg:text")
		    .attr("class", "yLabel")
		    .text(String)
		    .attr("x", 0)
		    .attr("y", function(d) { return -1 * y(d) })
		    .attr("text-anchor", "right")
		    .attr("dy", 4);
		
    g.selectAll(".xTicks")
		    .data(x.ticks(5))
		    .enter().append("svg:line")
		    .attr("class", "xTicks")
		    .attr("x1", function(d) { return x(d); })
		    .attr("y1", -1 * y(0))
		    .attr("x2", function(d) { return x(d); })
		    .attr("y2", -1 * y(-0.3));

    g.selectAll(".yTicks")
		    .data(y.ticks(4))
		    .enter().append("svg:line")
		    .attr("class", "yTicks")
		    .attr("y1", function(d) { return -1 * y(d); })
		    .attr("x1", x(-0.3))
		    .attr("y2", function(d) { return -1 * y(d); })
		    .attr("x2", x(0));
};
