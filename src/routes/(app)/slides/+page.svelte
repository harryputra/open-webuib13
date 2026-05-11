<script lang="ts">
	import MarpSlideGenerator from '$lib/components/slides/MarpSlideGenerator.svelte';
</script>

<svelte:head>
	<title>Slide Generator (Marp)</title>
	<meta name="description" content="Generate slides from Markdown using Marp" />
</svelte:head>

<div class="slides-page">
	<MarpSlideGenerator />
</div>

<style>
	.slides-page {
		width: 100%;
		height: 100%;
		overflow: hidden;
	}
</style>
