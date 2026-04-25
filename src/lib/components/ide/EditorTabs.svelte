<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import type { OpenFile } from '$lib/stores/ide';

	const dispatch = createEventDispatcher();

	export let files: OpenFile[] = [];
	export let activeFilePath: string = '';

	function handleTabClick(path: string) {
		dispatch('select', { path });
	}

	function handleTabClose(e: Event, path: string) {
		e.stopPropagation();
		dispatch('close', { path });
	}

	function getFileIcon(name: string): string {
		const ext = name.split('.').pop()?.toLowerCase() || '';
		const icons: Record<string, string> = {
			py: '🐍', js: '📜', ts: '📘', tsx: '⚛️', jsx: '⚛️',
			html: '🌐', css: '🎨', json: '📋', md: '📝',
			svelte: '🔥', vue: '💚', yaml: '⚙️', yml: '⚙️',
			sql: '🗃️', sh: '🖥️', go: '🐹', rs: '🦀',
		};
		return icons[ext] || '📄';
	}
</script>

<div class="editor-tabs">
	<div class="tabs-scroll">
		{#each files as file (file.path)}
			<div
				class="tab"
				class:active={file.path === activeFilePath}
				on:click={() => handleTabClick(file.path)}
				on:keydown={(e) => e.key === 'Enter' && handleTabClick(file.path)}
				role="tab"
				tabindex="0"
				title={file.path}
				aria-selected={file.path === activeFilePath}
			>
				<span class="tab-icon">{getFileIcon(file.name)}</span>
				<span class="tab-name">{file.name}</span>
				{#if file.modified}
					<span class="tab-modified">●</span>
				{/if}
				<button
					type="button"
					class="tab-close"
					on:click={(e) => handleTabClose(e, file.path)}
					title="Close"
					aria-label="Close Tab"
				>
					<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="currentColor" class="close-icon">
						<path d="M5.28 4.22a.75.75 0 0 0-1.06 1.06L6.94 8l-2.72 2.72a.75.75 0 1 0 1.06 1.06L8 9.06l2.72 2.72a.75.75 0 1 0 1.06-1.06L9.06 8l2.72-2.72a.75.75 0 0 0-1.06-1.06L8 6.94 5.28 4.22Z" />
					</svg>
				</button>
			</div>
		{/each}
	</div>
</div>

<style>
	.editor-tabs {
		display: flex;
		background: #0a0a0a;
		border-bottom: 1px solid #1a1a1a;
		min-height: 35px;
		overflow: hidden;
	}

	.tabs-scroll {
		display: flex;
		overflow-x: auto;
		overflow-y: hidden;
		flex: 1;
		scrollbar-width: none;
	}

	.tabs-scroll::-webkit-scrollbar {
		display: none;
	}

	.tab {
		display: flex;
		align-items: center;
		gap: 4px;
		padding: 0 12px;
		min-width: 0;
		max-width: 200px;
		height: 35px;
		background: transparent;
		border: none;
		border-right: 1px solid #1a1a1a;
		color: rgba(255, 255, 255, 0.5);
		font-size: 12px;
		cursor: pointer;
		flex-shrink: 0;
		transition: all 0.15s;
		font-family: inherit;
	}

	.tab:hover {
		background: rgba(255, 255, 255, 0.04);
		color: rgba(255, 255, 255, 0.8);
	}

	.tab.active {
		background: #111;
		color: #fff;
		border-bottom: 2px solid #3b82f6;
	}

	.tab-icon {
		font-size: 13px;
		flex-shrink: 0;
	}

	.tab-name {
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
		font-family: 'JetBrains Mono', 'Fira Code', monospace;
		font-size: 12px;
	}

	.tab-modified {
		color: #f59e0b;
		font-size: 10px;
		flex-shrink: 0;
		margin-left: -2px;
	}

	.tab-close {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 18px;
		height: 18px;
		border: none;
		background: transparent;
		color: rgba(255, 255, 255, 0.3);
		cursor: pointer;
		border-radius: 3px;
		flex-shrink: 0;
		padding: 0;
		margin-left: 2px;
		opacity: 0;
		transition: all 0.15s;
	}

	.tab:hover .tab-close {
		opacity: 1;
	}

	.tab-close:hover {
		background: rgba(255, 255, 255, 0.1);
		color: #fff;
	}

	.close-icon {
		width: 12px;
		height: 12px;
	}
</style>
