<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import { expandedDirs } from '$lib/stores/ide';
	import type { TreeNode } from '$lib/stores/ide';

	const dispatch = createEventDispatcher();

	export let node: TreeNode;
	export let depth: number = 0;

	let isExpanded = false;
	let isHovered = false;

	// Sync expanded state with store
	$: isExpanded = $expandedDirs.has(node.path);

	function toggleExpand() {
		if (node.type !== 'directory') return;

		expandedDirs.update((dirs) => {
			const next = new Set(dirs);
			if (next.has(node.path)) {
				next.delete(node.path);
			} else {
				next.add(node.path);
			}
			return next;
		});

		// Dispatch event to load children if needed
		dispatch('expand', { path: node.path, expanded: !isExpanded });
	}

	function handleClick() {
		if (node.type === 'file') {
			dispatch('fileclick', { path: node.path, name: node.name });
		} else {
			toggleExpand();
		}
	}

	function handleKeydown(e: KeyboardEvent) {
		if (e.key === 'Enter' || e.key === ' ') {
			e.preventDefault();
			handleClick();
		}
	}

	function formatSize(bytes: number): string {
		if (bytes < 1024) return `${bytes} B`;
		if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
		return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
	}
</script>

<!-- svelte-ignore a11y_no_noninteractive_tabindex -->
<div class="tree-node" style="--depth: {depth}">
	<div
		class="node-row"
		class:selected={false}
		class:hovered={isHovered}
		on:click={handleClick}
		on:keydown={handleKeydown}
		on:mouseenter={() => (isHovered = true)}
		on:mouseleave={() => (isHovered = false)}
		tabindex="0"
		role="treeitem"
		aria-expanded={node.type === 'directory' ? isExpanded : undefined}
	>
		<div class="node-indent" style="width: {depth * 16}px"></div>

		{#if node.type === 'directory'}
			<span class="expand-icon" class:expanded={isExpanded}>
				<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="currentColor" class="chevron-icon">
					<path
						fill-rule="evenodd"
						d="M6.22 4.22a.75.75 0 0 1 1.06 0l3.25 3.25a.75.75 0 0 1 0 1.06l-3.25 3.25a.75.75 0 0 1-1.06-1.06L8.94 8 6.22 5.28a.75.75 0 0 1 0-1.06Z"
						clip-rule="evenodd"
					/>
				</svg>
			</span>
		{:else}
			<span class="expand-icon placeholder"></span>
		{/if}

		<span class="node-icon">{node.icon}</span>
		<span class="node-name" title={node.path}>
			{node.name}
		</span>

		{#if isHovered && node.type === 'file' && node.size}
			<span class="node-size">{formatSize(node.size)}</span>
		{/if}
	</div>

	{#if node.type === 'directory' && isExpanded && node.children}
		<div class="node-children">
			{#each node.children as child (child.path)}
				<svelte:self
					node={child}
					depth={depth + 1}
					on:fileclick
					on:expand
				/>
			{/each}
			{#if node.children.length === 0}
				<div class="empty-dir" style="padding-left: {(depth + 1) * 16 + 24}px">
					<span class="empty-text">Empty directory</span>
				</div>
			{/if}
		</div>
	{/if}
</div>

<style>
	.tree-node {
		user-select: none;
	}

	.node-row {
		display: flex;
		align-items: center;
		padding: 2px 8px 2px 0;
		cursor: pointer;
		border-radius: 4px;
		font-size: 13px;
		line-height: 22px;
		color: var(--text-secondary, #ccc);
		transition: background-color 0.1s;
	}

	.node-row:hover,
	.node-row.hovered {
		background-color: rgba(255, 255, 255, 0.06);
	}

	.node-row.selected {
		background-color: rgba(59, 130, 246, 0.2);
		color: #fff;
	}

	.node-row:focus {
		outline: 1px solid rgba(59, 130, 246, 0.5);
		outline-offset: -1px;
	}

	.node-indent {
		flex-shrink: 0;
	}

	.expand-icon {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 16px;
		height: 16px;
		flex-shrink: 0;
		transition: transform 0.15s ease;
	}

	.expand-icon.expanded {
		transform: rotate(90deg);
	}

	.expand-icon.placeholder {
		opacity: 0;
	}

	.chevron-icon {
		width: 12px;
		height: 12px;
		opacity: 0.5;
	}

	.node-icon {
		font-size: 14px;
		margin: 0 4px;
		flex-shrink: 0;
		line-height: 1;
	}

	.node-name {
		flex: 1;
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
		font-family: 'JetBrains Mono', 'Fira Code', monospace;
	}

	.node-size {
		font-size: 11px;
		color: rgba(255, 255, 255, 0.3);
		margin-left: auto;
		padding-left: 8px;
		flex-shrink: 0;
		font-family: 'JetBrains Mono', 'Fira Code', monospace;
	}

	.empty-dir {
		padding: 2px 0;
	}

	.empty-text {
		font-size: 11px;
		color: rgba(255, 255, 255, 0.2);
		font-style: italic;
	}
</style>
