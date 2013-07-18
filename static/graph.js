function graph(data) {
    var margin = {top: 20, right: 20, bottom: 30, left: 50},
        width = 780 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom;

    var parseDate = d3.time.format("%Y-%m-%d").parse;

    var x = d3.time.scale()
        .range([0, width]);

    var y = d3.scale.linear()
        .range([height, 0]);

    var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom");

    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left")
        .ticks(10);

    var avg_line = d3.svg.line()
        .interpolate('basis')
        .x(function(d) { return x(d.date); })
        .y(function(d) { return y(d.avg); });

    var data_line = d3.svg.line()
        .x(function(d) { return x(d.date); })
        .y(function(d) { return y(d.count); });

    var goal_line = d3.svg.line()
        .x(function(d) { return x(d.date); })
        .y(function(d) { return y(4); });

    var ideal_line = d3.svg.line()
        .x(function(d) { return x(d.date); })
        .y(function(d) { return y(d.ideal); });

    var svg = d3.select("#graph").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    data.forEach(function(d) {
        d.date = parseDate(d.date);
    });

    x.domain(d3.extent(data, function(d) { return d.date; }));
    y.domain([0, 8]);

    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);

    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis)
        .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 5)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text("Closed");

    svg.append("path")
        .datum(data)
        .attr("class", "goal_line")
        .attr("d", goal_line);

    svg.append("path")
        .datum(data)
        .attr("class", "avg_line")
        .attr("d", avg_line);

    svg.append("path")
        .datum(data)
        .attr("class", "data_line")
        .attr("d", data_line);

    svg.append("path")
        .datum(data)
        .attr("class", "ideal_line")
        .attr("d", ideal_line)
}
