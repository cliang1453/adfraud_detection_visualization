// calculate the most fraud lead values for each attribute
data_generation()

function data_processing(X, y) {
	var statistics = {}
	for (var attr in X[0]) {
		statistics[attr] = {}
	}
	for (var i = 0; i < y.length; i++) {
		if (y[i] == 0) {
			for (var attr in X[i]) {
				if (!statistics[attr].hasOwnProperty(X[i][attr])) {
					statistics[attr][X[i][attr]] = 1;
				}
				statistics[attr][X[i][attr]]++;
			}
		}
	}
	var bar_chart_data = [];
	function comp(a, b) {
		if (a.count - b.count < 0) {
			return 1;
		} else if (a.count - b.count > 0) {
			return -1;
		} else {
			return 0;
		}
	}
	for (var attr in statistics) {
		data = [];
		for (var item in statistics[attr]) {
			data.push({name: item, count: statistics[attr][item]});
		}
		data.sort(comp);
		data10 = data.slice(0, 11);
		bar_chart_data.push({title: attr, data: data10});
	}

	console.log(bar_chart_data);
	return bar_chart_data;
}

function add_buttons(data) {
	var margin = {top: 120, right: 70, bottom: 0, left: 75};
	var width = 1000-margin.left-margin.right;
	var height = 1500-margin.top-margin.bottom;

	var svg = d3.select("body").append("svg")
		.attr("width", width+margin.left+margin.right)
		.attr("height", height+margin.top+margin.bottom);
		//.append("g")
		//.attr("transform", "translate("+margin.left+","+margin.top+")");
	//bars contains all the data
	var title = svg.append("text")
		.attr("x", margin.left+width/2)
		.attr("y", margin.top/2)
		.attr("fill", "black")
		.style("font-size", "30px")
		.attr("text-anchor", "middle")
		.text("Feature Statistics of Fraud Clicks");

    var buttons = svg.selectAll("circle")
		.data(data)
		.enter();
	
	var colors = ["#ff00ff","#ff69b4","#daa520","#4b0082","#7b68ee","#00bfff","#00ced1","#00fa9a","#ffff00", "#ff8c00"];
			
	//add mouse over and mouse out
	//each city contains data that only for that city
	buttons.append("circle")
		.attr("fill", function(d, i) {
			return colors[i%10];
		})
		.attr("cx", 100)
		.attr("cy", function(d, i) {
			return margin.top/2+(i+1)*100;
		})
		.attr("r", 40)
		.on("mouseover", function (d) {
			console.log(d);
			d3.select(this).transition().duration(8).attr("fill", "grey");
			
			var bar_colors = ["#ffffd9","#edf8b1","#c7e9b4","#7fcdbb","#41b6c4","#1d91c0","#225ea8","#225ea8","#225ea8", "#225ea8"];
			//draw_bar_chart(svg, d);
			xScale = d3.scaleLinear()
				.domain([0, d3.max(d.data, function(d) {
					return d.count;
				})])
				.range([0, 300]);

			svg.append("text")
				.attr("class", "bar_title")
				.attr("x", 400)
				.attr("y", 110)
				.attr("fill", "black")
				.style("font-size", "20px")
				.attr("text-anchor", "start")
				.text("Top "+d.title+" occurred in fraud clicks (counts)");

			var bars = svg.selectAll("rect")
				.data(d.data)
				.enter();
		
			bars.append("rect")
				.attr("class", "bar")
				.attr("fill", function(d, i) {
					return bar_colors[9-i];
				})
				.attr("x", 400)
				.attr("y", function(d, i) {
					return 150+50*i;
				})
				.attr("height", 30)
				.attr("width", 0)
				.transition().duration(1000)
				.attr("width", function(d, i) {
					return xScale(d.count);
				});

			bars.append("text")
				.attr("class", "bar_name")
				.attr("fill", "black")
				.attr("x", 390)
				.attr("y", function(d, i) {
					return 170+50*i;
				})
				.style("font-size", "14px")
				.attr("text-anchor", "end")
				.text(function(d) {
					return d.name;
				});

			bars.append("text")
				.attr("class", "bar_number")
				.attr("fill", "white")
				.attr("x", function(d) {
					return 390+xScale(d.count);
				})
				.attr("y", function(d, i) {
					return 170+50*i;
				})
				.style("font-size", "14px")
				.attr("text-anchor", "end")
				.text(function(d) {
					return d.count;
				});

        })
		.on("mouseout", function(d, i)
		{		
			d3.select(this).transition().duration(500).attr("fill", colors[i%10]);
			//disappear
			disappear();
		})
	//show numbers in the bar
	buttons.append("text")
		.attr("fill", "white")
		.attr("x", 100)
		.attr("y", function(d, i){
			return (i+1)*100+5+margin.top/2;
		})
		.attr("text-anchor", "middle")
		.style("font-weight", "bold")
		.style("font-size", "14px")
		.text(function(d){
			return d.title;
		});
}

function disappear() {
	//d3.selectAll("#line-x").style("visibility", "hidden").remove();	
	d3.selectAll(".bar").style("visibility", "hidden").remove();
	d3.selectAll(".bar_name").style("visibility", "hidden").remove();
	d3.selectAll(".bar_number").style("visibility", "hidden").remove();
	d3.selectAll(".bar_title").style("visibility", "hidden").remove();
}

function data_generation() {
	/*var X = 
	[
		{ip: '0.0.0.0', app: 'abb', device: 'iphone X', os: 'iOS 12', channel: '025'},
		{ip: '0.0.0.0', app: 'abb', device: 'Pixel 3', os: 'Android 8', channel: '995'},
		{ip: '0.0.0.0', app: 'dds', device: 'Nokia 95', os: 'sybian', channel: '221'},
		{ip: '0.0.0.0', app: 'asd', device: 'iphone X', os: 'iOS 12', channel: '221'},
		{ip: '0.0.0.1', app: 'asc', device: 'iphone X', os: 'iOS 12', channel: '774'},
		{ip: '0.0.0.1', app: 'abb', device: 'Pixel 3', os: 'Android 8', channel: '221'},
		{ip: '0.0.1.0', app: 'bvv', device: 'Nokia 95', os: 'sybian', channel: '221'},
		{ip: '0.0.1.0', app: 'abb', device: 'iphone X', os: 'iOS 12', channel: '966'},
		{ip: '0.1.0.0', app: 'bvv', device: 'Huawei mate 20pro', os: 'Android 8', channel: '774'}
	]
	var y = [0,0,0,1,0,1,0,0,0,1]*/
	d3.csv("mat1.csv").then(function(rows) {
		var X = [], y = [];
		//console.log(rows);
		//console.log(rows.length);
		for (var i = 0; i < rows.length; i++) {
			X.push({
				ip: rows[i].ip, 
				app: rows[i].app, 
				device: rows[i].device, 
				os: rows[i].os, 
				channel: rows[i].channel,
				click_time: rows[i].click_scalar,
			});
			y.push(+rows[i].is_attributed);
		}
		bar_chart_data = data_processing(X, y);
		//draw the bar graph
		add_buttons(bar_chart_data);
	})
}	
