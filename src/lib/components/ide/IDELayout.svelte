<script lang="ts">
	import { onMount } from 'svelte';
	import { toast } from 'svelte-sonner';
	import { PaneGroup, Pane, PaneResizer } from 'paneforge';

	import {
		openFiles,
		activeFilePath,
		showFileExplorer,
		showTerminalPanel,
		getLanguageFromPath,
	} from '$lib/stores/ide';
	import type { OpenFile } from '$lib/stores/ide';
	import { readFile, writeFile } from '$lib/apis/workspace';

	import FileExplorer from './FileExplorer.svelte';
	import EditorTabs from './EditorTabs.svelte';
	import CodeEditor from './CodeEditor.svelte';
	import XTerminal from '$lib/components/chat/XTerminal.svelte';

	let terminalConnected = false;
	let terminalConnecting = false;

	// ================================================================
	// File Operations
	// ================================================================

	async function handleOpenFile(e: CustomEvent) {
		const { path, name } = e.detail;

		// Check if already open
		const existing = $openFiles.find((f) => f.path === path);
		if (existing) {
			activeFilePath.set(path);
			return;
		}

		// Load file content
		try {
			const data = await readFile(path);
			const newFile: OpenFile = {
				path,
				name: data.name,
				content: data.content,
				originalContent: data.content,
				language: getLanguageFromPath(path),
				modified: false,
				loading: false,
			};

			openFiles.update((files) => [...files, newFile]);
			activeFilePath.set(path);
		} catch (e: any) {
			toast.error(`Failed to open file: ${e.message}`);
		}
	}

	function handleNewFile(e: CustomEvent) {
		const { name } = e.detail;
		const newFile: OpenFile = {
			path: name,
			name: name,
			content: '',
			originalContent: '',
			language: getLanguageFromPath(name),
			modified: true,
			loading: false,
		};

		openFiles.update((files) => [...files, newFile]);
		activeFilePath.set(name);
	}

	function handleTabSelect(e: CustomEvent) {
		activeFilePath.set(e.detail.path);
	}

	function handleTabClose(e: CustomEvent) {
		const { path } = e.detail;
		const file = $openFiles.find((f) => f.path === path);

		if (file?.modified) {
			if (!confirm(`"${file.name}" has unsaved changes. Close anyway?`)) {
				return;
			}
		}

		openFiles.update((files) => files.filter((f) => f.path !== path));

		// If closing active tab, switch to another
		if ($activeFilePath === path) {
			const remaining = $openFiles.filter((f) => f.path !== path);
			activeFilePath.set(remaining.length > 0 ? remaining[remaining.length - 1].path : '');
		}
	}

	function handleEditorChange(e: CustomEvent) {
		const { content, path } = e.detail;
		openFiles.update((files) =>
			files.map((f) =>
				f.path === path
					? { ...f, content, modified: content !== f.originalContent }
					: f
			)
		);
	}

	async function handleEditorSave(e: CustomEvent) {
		const { content, path } = e.detail;
		try {
			await writeFile(path, content);
			openFiles.update((files) =>
				files.map((f) =>
					f.path === path
						? { ...f, originalContent: content, modified: false }
						: f
				)
			);
			toast.success(`Saved: ${path.split('/').pop()}`);
		} catch (err: any) {
			toast.error(`Save failed: ${err.message}`);
		}
	}

	// Get the active file object
	$: currentFile = $openFiles.find((f) => f.path === $activeFilePath) || null;

	// ================================================================
	// Keyboard Shortcuts
	// ================================================================

	function handleKeydown(e: KeyboardEvent) {
		// Ctrl+B: Toggle file explorer
		if (e.ctrlKey && e.key === 'b') {
			e.preventDefault();
			showFileExplorer.update((v) => !v);
		}
		// Ctrl+`: Toggle terminal
		if (e.ctrlKey && e.key === '`') {
			e.preventDefault();
			showTerminalPanel.update((v) => !v);
		}
	}

	onMount(() => {
		window.addEventListener('keydown', handleKeydown);
		return () => {
			window.removeEventListener('keydown', handleKeydown);
		};
	});
</script>

<div class="ide-layout">
	<PaneGroup direction="horizontal">
		<!-- File Explorer Panel -->
		{#if $showFileExplorer}
			<Pane defaultSize={18} minSize={12} maxSize={35}>
				<FileExplorer
					on:openfile={handleOpenFile}
					on:newfile={handleNewFile}
				/>
			</Pane>
			<PaneResizer class="ide-resizer-h" />
		{/if}

		<!-- Main Content: Editor + Terminal -->
		<Pane defaultSize={$showFileExplorer ? 82 : 100}>
			<PaneGroup direction="vertical">
				<!-- Editor Area -->
				<Pane defaultSize={$showTerminalPanel ? 65 : 100} minSize={30}>
					<div class="editor-area">
						<!-- Tabs -->
						<EditorTabs
							files={$openFiles}
							activeFilePath={$activeFilePath}
							on:select={handleTabSelect}
							on:close={handleTabClose}
						/>

						<!-- Editor Content -->
						<div class="editor-content">
							{#if currentFile}
								<CodeEditor
									content={currentFile.content}
									language={currentFile.language}
									filePath={currentFile.path}
									on:change={handleEditorChange}
									on:save={handleEditorSave}
									on:autosave={handleEditorSave}
								/>
							{:else}
								<!-- Empty state -->
								<div class="empty-editor">
									<div class="empty-icon">
										<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1" stroke="currentColor" class="empty-svg">
											<path stroke-linecap="round" stroke-linejoin="round" d="M17.25 6.75 22.5 12l-5.25 5.25m-10.5 0L1.5 12l5.25-5.25m7.5-3-4.5 16.5" />
										</svg>
									</div>
									<h3 class="empty-title">Antigravity AI IDE</h3>
									<p class="empty-subtitle">Open a file from the explorer to start editing</p>
									<div class="empty-shortcuts">
										<div class="shortcut"><kbd>Ctrl</kbd>+<kbd>B</kbd> Toggle Explorer</div>
										<div class="shortcut"><kbd>Ctrl</kbd>+<kbd>`</kbd> Toggle Terminal</div>
										<div class="shortcut"><kbd>Ctrl</kbd>+<kbd>S</kbd> Save File</div>
									</div>
								</div>
							{/if}
						</div>
					</div>
				</Pane>

				<!-- Terminal Panel -->
				{#if $showTerminalPanel}
					<PaneResizer class="ide-resizer-v" />
					<Pane defaultSize={35} minSize={15} maxSize={60}>
						<div class="terminal-panel">
							<div class="terminal-header">
								<span class="terminal-title">
									<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="currentColor" class="terminal-icon">
										<path fill-rule="evenodd" d="M2 4.25A2.25 2.25 0 0 1 4.25 2h7.5A2.25 2.25 0 0 1 14 4.25v7.5A2.25 2.25 0 0 1 11.75 14h-7.5A2.25 2.25 0 0 1 2 11.75v-7.5ZM4.438 6.56a.75.75 0 0 1 1.06-.001L7.22 8.28a.75.75 0 0 1 0 1.06L5.5 11.06a.75.75 0 0 1-1.06-1.06l1.22-1.22L4.44 7.56a.75.75 0 0 1-.002-1Zm3.812 4.19a.75.75 0 0 1 .75-.75h2.5a.75.75 0 0 1 0 1.5H9a.75.75 0 0 1-.75-.75Z" clip-rule="evenodd" />
									</svg>
									TERMINAL
								</span>
								<div class="terminal-status" class:connected={terminalConnected}>
									{terminalConnected ? '● Connected' : terminalConnecting ? '◌ Connecting...' : '○ Disconnected'}
								</div>
							</div>
							<div class="terminal-content">
								<XTerminal bind:connected={terminalConnected} bind:connecting={terminalConnecting} />
							</div>
						</div>
					</Pane>
				{/if}
			</PaneGroup>
		</Pane>
	</PaneGroup>
</div>

<style>
	.ide-layout {
		width: 100%;
		height: 100%;
		background: #0a0a0a;
		display: flex;
		overflow: hidden;
	}

	.ide-layout :global(.ide-resizer-h) {
		width: 4px;
		background: #1a1a1a;
		cursor: col-resize;
		transition: background 0.15s;
	}

	.ide-layout :global(.ide-resizer-h:hover),
	.ide-layout :global(.ide-resizer-h[data-state="dragging"]) {
		background: #3b82f6;
	}

	.ide-layout :global(.ide-resizer-v) {
		height: 4px;
		background: #1a1a1a;
		cursor: row-resize;
		transition: background 0.15s;
	}

	.ide-layout :global(.ide-resizer-v:hover),
	.ide-layout :global(.ide-resizer-v[data-state="dragging"]) {
		background: #3b82f6;
	}

	.editor-area {
		display: flex;
		flex-direction: column;
		height: 100%;
		overflow: hidden;
	}

	.editor-content {
		flex: 1;
		overflow: hidden;
	}

	.empty-editor {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		height: 100%;
		color: rgba(255, 255, 255, 0.3);
		gap: 16px;
	}

	.empty-icon {
		opacity: 0.15;
	}

	.empty-svg {
		width: 64px;
		height: 64px;
	}

	.empty-title {
		font-size: 24px;
		font-weight: 700;
		color: rgba(255, 255, 255, 0.4);
		margin: 0;
		background: linear-gradient(135deg, #3b82f6, #8b5cf6);
		-webkit-background-clip: text;
		-webkit-text-fill-color: transparent;
		background-clip: text;
	}

	.empty-subtitle {
		font-size: 14px;
		margin: 0;
	}

	.empty-shortcuts {
		display: flex;
		flex-direction: column;
		gap: 8px;
		margin-top: 24px;
	}

	.shortcut {
		display: flex;
		align-items: center;
		gap: 4px;
		font-size: 12px;
		color: rgba(255, 255, 255, 0.2);
	}

	.shortcut :global(kbd) {
		display: inline-flex;
		padding: 2px 6px;
		background: rgba(255, 255, 255, 0.06);
		border: 1px solid rgba(255, 255, 255, 0.1);
		border-radius: 4px;
		font-size: 11px;
		font-family: 'JetBrains Mono', monospace;
		color: rgba(255, 255, 255, 0.4);
	}

	.terminal-panel {
		display: flex;
		flex-direction: column;
		height: 100%;
		background: #000;
		overflow: hidden;
	}

	.terminal-header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 6px 12px;
		background: #0a0a0a;
		border-top: 1px solid #1a1a1a;
		border-bottom: 1px solid #1a1a1a;
		font-size: 11px;
	}

	.terminal-title {
		display: flex;
		align-items: center;
		gap: 6px;
		font-weight: 600;
		letter-spacing: 1px;
		color: rgba(255, 255, 255, 0.5);
		text-transform: uppercase;
	}

	.terminal-icon {
		width: 14px;
		height: 14px;
	}

	.terminal-status {
		font-size: 11px;
		color: rgba(255, 255, 255, 0.3);
		font-family: 'JetBrains Mono', monospace;
	}

	.terminal-status.connected {
		color: #22c55e;
	}

	.terminal-content {
		flex: 1;
		overflow: hidden;
	}
</style>
