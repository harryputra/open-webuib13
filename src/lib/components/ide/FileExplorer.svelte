<script lang="ts">
	import { onMount, createEventDispatcher } from 'svelte';
	import { toast } from 'svelte-sonner';
	import { fileTree, expandedDirs, ideLoading } from '$lib/stores/ide';
	import { getFileTree, createDirectory, deleteItem } from '$lib/apis/workspace';
	import FileTreeNode from './FileTreeNode.svelte';

	const dispatch = createEventDispatcher();

	let searchQuery = '';
	let treeData: any = null;
	let loading = false;
	let error = '';

	async function loadTree(path: string = '.', depth: number = 3) {
		loading = true;
		error = '';
		try {
			treeData = await getFileTree(path, depth);
			fileTree.set(treeData);
		} catch (e: any) {
			error = e.message || 'Failed to load file tree';
			console.error('FileExplorer loadTree error:', e);
		} finally {
			loading = false;
		}
	}

	function handleFileClick(e: CustomEvent) {
		dispatch('openfile', e.detail);
	}

	async function handleExpand(e: CustomEvent) {
		const { path, expanded } = e.detail;
		if (expanded) {
			// Lazy load children for expanded directory
			try {
				const subtree = await getFileTree(path, 2);
				if (subtree && subtree.children) {
					// Update the tree in place
					updateTreeNode(treeData, path, subtree.children);
					treeData = { ...treeData }; // trigger reactivity
					fileTree.set(treeData);
				}
			} catch (err) {
				console.error('Failed to expand directory:', err);
			}
		}
	}

	function updateTreeNode(node: any, targetPath: string, children: any[]) {
		if (!node) return;
		if (node.path === targetPath) {
			node.children = children;
			return;
		}
		if (node.children) {
			for (const child of node.children) {
				updateTreeNode(child, targetPath, children);
			}
		}
	}

	async function handleRefresh() {
		await loadTree();
		toast.success('File tree refreshed');
	}

	async function handleNewFile() {
		const name = prompt('Enter file name:');
		if (!name) return;
		dispatch('newfile', { name });
	}

	async function handleNewFolder() {
		const name = prompt('Enter folder name:');
		if (!name) return;
		try {
			await createDirectory(name);
			await loadTree();
			toast.success(`Created folder: ${name}`);
		} catch (e: any) {
			toast.error(e.message);
		}
	}

	onMount(() => {
		loadTree();
	});
</script>

<div class="file-explorer">
	<!-- Header -->
	<div class="explorer-header">
		<span class="explorer-title">EXPLORER</span>
		<div class="explorer-actions">
			<button class="action-btn" on:click={handleNewFile} title="New File">
				<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="currentColor" class="action-icon">
					<path d="M3.75 2A1.75 1.75 0 0 0 2 3.75v8.5c0 .966.784 1.75 1.75 1.75h8.5A1.75 1.75 0 0 0 14 12.25v-5.5a.75.75 0 0 0-1.5 0v5.5a.25.25 0 0 1-.25.25h-8.5a.25.25 0 0 1-.25-.25v-8.5a.25.25 0 0 1 .25-.25h5.5a.75.75 0 0 0 0-1.5h-5.5Z" />
					<path d="M11.5 1.75a.75.75 0 0 1 1.5 0v1.5h1.5a.75.75 0 0 1 0 1.5H13v1.5a.75.75 0 0 1-1.5 0v-1.5H10a.75.75 0 0 1 0-1.5h1.5v-1.5Z" />
				</svg>
			</button>
			<button class="action-btn" on:click={handleNewFolder} title="New Folder">
				<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="currentColor" class="action-icon">
					<path d="M2 4.75C2 3.784 2.784 3 3.75 3h2.697a.75.75 0 0 1 .53.22L8.54 4.78a.25.25 0 0 0 .177.073h3.534c.966 0 1.75.784 1.75 1.75v5.647c0 .966-.784 1.75-1.75 1.75H3.75A1.75 1.75 0 0 1 2 12.25V4.75Z" />
				</svg>
			</button>
			<button class="action-btn" on:click={handleRefresh} title="Refresh">
				<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="currentColor" class="action-icon">
					<path fill-rule="evenodd" d="M13.836 2.477a.75.75 0 0 1 .75.75v3.182a.75.75 0 0 1-.75.75h-3.182a.75.75 0 0 1 0-1.5h1.37l-.84-.841a4.5 4.5 0 0 0-7.08.681.75.75 0 0 1-1.3-.75 6 6 0 0 1 9.44-.908l.842.842V3.227a.75.75 0 0 1 .75-.75Zm-.911 7.5A.75.75 0 0 1 13.199 11a6 6 0 0 1-9.44.908l-.842-.842v1.282a.75.75 0 0 1-1.5 0V9.166a.75.75 0 0 1 .75-.75h3.182a.75.75 0 0 1 0 1.5h-1.37l.84.841a4.5 4.5 0 0 0 7.08-.681.75.75 0 0 1 1.274.401Z" clip-rule="evenodd" />
				</svg>
			</button>
		</div>
	</div>

	<!-- Search -->
	<div class="explorer-search">
		<input
			type="text"
			placeholder="Search files..."
			bind:value={searchQuery}
			class="search-input"
		/>
	</div>

	<!-- Tree -->
	<div class="explorer-tree">
		{#if loading && !treeData}
			<div class="loading-state">
				<div class="loading-spinner"></div>
				<span>Loading workspace...</span>
			</div>
		{:else if error}
			<div class="error-state">
				<span class="error-icon">⚠️</span>
				<span class="error-text">{error}</span>
				<button class="retry-btn" on:click={() => loadTree()}>Retry</button>
			</div>
		{:else if treeData}
			{#if treeData.children}
				{#each treeData.children as child (child.path)}
					<FileTreeNode
						node={child}
						depth={0}
						on:fileclick={handleFileClick}
						on:expand={handleExpand}
					/>
				{/each}
			{/if}
		{/if}
	</div>
</div>

<style>
	.file-explorer {
		display: flex;
		flex-direction: column;
		height: 100%;
		background: #0d0d0d;
		color: #ccc;
		font-size: 13px;
		overflow: hidden;
	}

	.explorer-header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 10px 12px 6px;
		border-bottom: 1px solid #1a1a1a;
	}

	.explorer-title {
		font-size: 11px;
		font-weight: 600;
		letter-spacing: 1.2px;
		color: rgba(255, 255, 255, 0.5);
		text-transform: uppercase;
	}

	.explorer-actions {
		display: flex;
		gap: 2px;
	}

	.action-btn {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 24px;
		height: 24px;
		border: none;
		background: transparent;
		color: rgba(255, 255, 255, 0.5);
		cursor: pointer;
		border-radius: 4px;
		transition: all 0.15s;
	}

	.action-btn:hover {
		background: rgba(255, 255, 255, 0.1);
		color: #fff;
	}

	.action-icon {
		width: 14px;
		height: 14px;
	}

	.explorer-search {
		padding: 6px 8px;
		border-bottom: 1px solid #1a1a1a;
	}

	.search-input {
		width: 100%;
		padding: 5px 8px;
		background: #151515;
		border: 1px solid #222;
		border-radius: 4px;
		color: #ccc;
		font-size: 12px;
		outline: none;
		font-family: inherit;
	}

	.search-input:focus {
		border-color: #3b82f6;
	}

	.search-input::placeholder {
		color: rgba(255, 255, 255, 0.25);
	}

	.explorer-tree {
		flex: 1;
		overflow-y: auto;
		overflow-x: hidden;
		padding: 4px 0;
	}

	.explorer-tree::-webkit-scrollbar {
		width: 6px;
	}

	.explorer-tree::-webkit-scrollbar-track {
		background: transparent;
	}

	.explorer-tree::-webkit-scrollbar-thumb {
		background: rgba(255, 255, 255, 0.1);
		border-radius: 3px;
	}

	.explorer-tree::-webkit-scrollbar-thumb:hover {
		background: rgba(255, 255, 255, 0.2);
	}

	.loading-state {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		padding: 40px 20px;
		gap: 12px;
		color: rgba(255, 255, 255, 0.4);
		font-size: 12px;
	}

	.loading-spinner {
		width: 24px;
		height: 24px;
		border: 2px solid rgba(255, 255, 255, 0.1);
		border-top-color: #3b82f6;
		border-radius: 50%;
		animation: spin 0.8s linear infinite;
	}

	@keyframes spin {
		to { transform: rotate(360deg); }
	}

	.error-state {
		display: flex;
		flex-direction: column;
		align-items: center;
		padding: 40px 20px;
		gap: 8px;
	}

	.error-icon {
		font-size: 24px;
	}

	.error-text {
		color: #f87171;
		font-size: 12px;
		text-align: center;
	}

	.retry-btn {
		margin-top: 8px;
		padding: 4px 12px;
		background: rgba(59, 130, 246, 0.2);
		color: #60a5fa;
		border: 1px solid rgba(59, 130, 246, 0.3);
		border-radius: 4px;
		cursor: pointer;
		font-size: 12px;
	}

	.retry-btn:hover {
		background: rgba(59, 130, 246, 0.3);
	}
</style>
