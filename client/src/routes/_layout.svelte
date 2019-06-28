<script>
	import Nav from '../components/Nav.svelte';

	export let segment;
</script>

<Nav {segment}/>

<main>
	<slot></slot>
</main>


<style>
	main {
		position: relative;
		max-width: 56em;
		margin: 0 auto;
		padding-top: 30px;
		box-sizing: border-box;
	}
</style>
