<script>
	export let segment;
</script>

<style>
	nav {
		position: relative;
		border-bottom: 1px solid rgba(255,62,0,0.1);
		font-weight: 300;
		padding: 0 1em;
		background-color: #ffc917;
	}

	.triangle {
	  	position: relative;
	  	border-top: 10px solid #ffc917
	}

	.triangle::before {
		background-repeat: no-repeat;
		background-size: 100% 100%;
		content: '';
		display: block;
		position: absolute;
		width: 100%;
		left: 0;
		bottom: -50px;
		height: 50px;
		background-image: url("data:image/svg+xml;charset=utf8,%3Csvg xmlns='http://www.w3.org/2000/svg' width='100' height='100' viewBox='0 0 100 100' preserveAspectRatio='none'%3E%3Cpolygon points='0,0 100,0 100,100' style='fill:%23ffc917;' /%3E%3C/svg%3E");
	}

	@media only screen and (max-width: 420px) {
		.triangle::before {
			height: 20px;
			bottom: -20px;
		}
	}

	ul {
		margin: 0;
		padding: 0;
		z-index: 10;
	}

	/* clearfix */
	ul::after {
		content: '';
		display: block;
		clear: both;
	}

	li {
		display: block;
		float: left;
		z-index: 10;
	}

	.selected {
		position: relative;
		display: inline-block;
	}

	.selected::after {
		position: absolute;
		content: '';
		width: calc(100% - 1em);
		height: 2px;
		background-color: #003082;
		display: block;
		bottom: -1px;
	}

	a {
		text-decoration: none;
		padding: 1em 0.5em;
		display: block;
		color: #003082
	}
</style>

<nav>
	<ul>
		<li><a class='{segment === undefined ? "selected" : ""}' href='.'>🚆 EHBA</a></li>
		<li><a class='{segment === "howto" ? "selected" : ""}' href='howto'>📚 Hoe werkt het?</a></li>
		<li><a class='{segment === "about" ? "selected" : ""}' href='about'>📜 Over</a></li>
	</ul>
</nav>
<div class="triangle"></div>