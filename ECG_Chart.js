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
		dps.splice(0, count);
	}

	chartECG.render();
};

function updateChartWarning(data){
	for(i=0; i<100; i++){
		dpsWarning.push({
			x: xVal++,
			y: data[i]
		})
	}
	for(i=0; i<data.length; i++){
		dpsWarning.push({
			x: xVal++,
			y: data[i]
		})
	}
	for(i=data.length - 100; i<data.length; i++){
		dpsWarning.push({
			x: xVal++,
			y: data[i]
		})
	}
	if(dpsWarning.length > 700){
		dpsWarning.splice(0, data.length + 200)	
	}
	chartWarning.render()
}