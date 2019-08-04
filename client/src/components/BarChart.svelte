<style>
.chart{
	/* height: 250px; */
	float: left;
	display: block;
	box-sizing: border-box;
	padding: 10px;
	background-color: white;
	border: 2px solid #e6e6e9;
}

.chart-canvas{
	padding-bottom: 10px;
	display: block;
	clear: both;
}
</style>

<script>
	export let data;
	export let chartId = 'chart-' + btoa(Math.random()).substring(0,12).toLowerCase();
	
	import { onMount } from 'svelte';

	// Build the chart data we expect for Chart.js
    let chartData = {
			labels: Object.keys(data),
			datasets: [{
				label: 'Aantal (#)',
				backgroundColor: '#ffc917',
				borderColor: '#ffc917',
				data: Object.values(data).map(i => i.count),
				hidden: true,
			},{
				label: 'Kosten (€)',
				borderColor: '#0063d3',
				backgroundColor: '#0063d3',
				borderWidth: 1,
				borderWidth: 1,
				data: Object.values(data).map(i => i.sum)
			}]
		}

	// Only on mounting we start the charting, otherwise we 
	// cannot find the div we are looking for... (pun intended)
	onMount(() => {
		new Chart(chartId, {
            type: 'bar',
            data: chartData,
        });
	});
</script>

<div class="chart">
	<h2>
		<slot name="title"></slot>
	</h2>
	<p>
		<slot name="description"></slot>
	</p>
	<canvas class="chart-canvas" id='{chartId}'></canvas>
</div>