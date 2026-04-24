<script lang="ts">
	import IDELayout from '$lib/components/ide/IDELayout.svelte';
</script>

<svelte:head>
	<title>Antigravity AI IDE</title>
	<meta name="description" content="AI-powered Developer IDE with file editing, terminal, and AI assistant" />
</svelte:head>

<div class="ide-page">
	<IDELayout />
</div>

<style>
	.ide-page {
		width: 100%;
		height: 100%;
		overflow: hidden;
	}
</style>
