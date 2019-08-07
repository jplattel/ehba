<script>
	import Nav from '../components/Nav.svelte';
	import Footer from '../components/Footer.svelte';
	export let segment;
</script>

<Nav {segment}/>

<main>
	<slot></slot>
</main>

<Footer />

<style>
	main {
		position: relative;
		max-width: 56em;
		margin: 0 auto;
		padding-top: 40px;
		box-sizing: border-box;
		margin-bottom: 100px;
	}
</style>
