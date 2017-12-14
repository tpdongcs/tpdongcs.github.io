var dps = []; // dataPoints
var dpsWarning = []
var chartWarning = new CanvasJS.Chart("chartWarning", {
	title :{
		text: "Warning Signal"
	},
	animationEnabled: true,
	axisY: {
		includeZero: false
	},      
	data: [{
		type: "line",
		dataPoints: dpsWarning
	}]
});

var chartECG = new CanvasJS.Chart("chartECG", {
	title :{
		text: "ECG Data"
	},
	animationEnabled: true,
	axisY: {
		includeZero: false
	},      
	data: [{
		type: "spline",
		dataPoints: dps
	}]
});

var xVal = 0;
var yVal = 100; 
var xWarningVal = 0;
var updateInterval = 1000;
var dataLength = 1250; // number of dataPoints visible at any point

function updateChart(count, data) {
	if(data == undefined)
		return
	count = count || 1;

	for (var j = 0; j < count; j++) {
		yVal = data[j];
		dps.push({
			x: xVal,
			y: yVal
		});
		xVal++;
	}

	if (dps.length > dataLength) {
		dps.splice(0, 100);
	}

	chartECG.render();
};

function updateChartWarning(data){
	for(i=0; i<data.length; i++){
		dpsWarning.push({
			x: xVal++,
			y: data[i]
		})
	}
	dpsWarning.splice(0, data.length)
	chartWarning.render()
}