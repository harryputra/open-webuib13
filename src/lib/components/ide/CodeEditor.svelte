<script lang="ts">
	import { onMount, onDestroy, createEventDispatcher } from 'svelte';
	import { EditorView, basicSetup } from 'codemirror';
	import { EditorState } from '@codemirror/state';
	import { oneDark } from '@codemirror/theme-one-dark';
	import { javascript } from '@codemirror/lang-javascript';
	import { python } from '@codemirror/lang-python';
	import { languageData } from '@codemirror/language-data';
	import { keymap } from '@codemirror/view';

	const dispatch = createEventDispatcher();

	export let content: string = '';
	export let language: string = 'text';
	export let filePath: string = '';
	export let readOnly: boolean = false;

	let editorEl: HTMLDivElement;
	let editorView: EditorView | null = null;
	let saveTimeout: ReturnType<typeof setTimeout> | null = null;

	function getLanguageExtension(lang: string) {
		switch (lang) {
			case 'javascript':
			case 'jsx':
				return javascript({ jsx: true });
			case 'typescript':
			case 'tsx':
				return javascript({ jsx: true, typescript: true });
			case 'python':
				return python();
			default:
				// Use language data autodetection for other languages
				return languageData;
		}
	}

	function initEditor() {
		if (!editorEl) return;

		// Clean up existing editor
		if (editorView) {
			editorView.destroy();
			editorView = null;
		}

		const langExt = getLanguageExtension(language);

		const saveKeymap = keymap.of([
			{
				key: 'Mod-s',
				run: () => {
					dispatch('save', { content: editorView?.state.doc.toString() || '', path: filePath });
					return true;
				}
			}
		]);

		const updateListener = EditorView.updateListener.of((update) => {
			if (update.docChanged) {
				const newContent = update.state.doc.toString();
				dispatch('change', { content: newContent, path: filePath });

				// Debounced auto-save
				if (saveTimeout) clearTimeout(saveTimeout);
				saveTimeout = setTimeout(() => {
					dispatch('autosave', { content: newContent, path: filePath });
				}, 2000);
			}
		});

		const state = EditorState.create({
			doc: content,
			extensions: [
				basicSetup,
				oneDark,
				langExt,
				saveKeymap,
				updateListener,
				EditorView.lineWrapping,
				EditorState.readOnly.of(readOnly),
				EditorView.theme({
					'&': {
						height: '100%',
						fontSize: '13px',
						fontFamily: "'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace",
					},
					'.cm-scroller': {
						overflow: 'auto',
					},
					'.cm-content': {
						padding: '8px 0',
					},
					'.cm-gutters': {
						background: '#0a0a0a',
						borderRight: '1px solid #1a1a1a',
						color: 'rgba(255,255,255,0.2)',
					},
					'.cm-activeLineGutter': {
						background: 'rgba(59, 130, 246, 0.1)',
						color: 'rgba(255,255,255,0.5)',
					},
					'.cm-activeLine': {
						background: 'rgba(255,255,255,0.03)',
					},
					'.cm-cursor': {
						borderLeftColor: '#3b82f6',
					},
					'.cm-selectionBackground': {
						background: 'rgba(59, 130, 246, 0.3) !important',
					},
				}),
			],
		});

		editorView = new EditorView({
			state,
			parent: editorEl,
		});
	}

	// Re-init editor when content or language changes from outside
	$: if (editorEl && content !== undefined) {
		if (editorView) {
			const currentContent = editorView.state.doc.toString();
			if (currentContent !== content) {
				editorView.dispatch({
					changes: {
						from: 0,
						to: editorView.state.doc.length,
						insert: content,
					},
				});
			}
		} else {
			initEditor();
		}
	}

	onMount(() => {
		initEditor();
	});

	onDestroy(() => {
		if (saveTimeout) clearTimeout(saveTimeout);
		editorView?.destroy();
		editorView = null;
	});
</script>

<div class="code-editor" bind:this={editorEl}></div>

<style>
	.code-editor {
		width: 100%;
		height: 100%;
		overflow: hidden;
		background: #0d0d0d;
	}

	.code-editor :global(.cm-editor) {
		height: 100%;
	}

	.code-editor :global(.cm-scroller) {
		overflow: auto;
	}
</style>
