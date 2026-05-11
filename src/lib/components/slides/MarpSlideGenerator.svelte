<script lang="ts">
	import { onMount, getContext, tick } from 'svelte';
	import { toast } from 'svelte-sonner';

	import {
		listSlides,
		loadSlide,
		saveSlide,
		deleteSlide,
		exportSlide,
		type MarpSlideFile,
		type MarpExportFormat
	} from '$lib/apis/marp';

	const i18n: any = getContext('i18n');

	const STARTER_MARKDOWN = `---
marp: true
theme: default
paginate: true
size: 16:9
backgroundColor: #fff
---

# Slide Generator
### dengan Marp + Antigravity

Tulis Markdown di kiri, lihat preview di kanan.
Pisahkan setiap slide dengan \`---\`.

---

## Fitur

- Live preview pakai **Marp Core**
- Simpan ke \`projects/marp_slides\`
- Export ke **PDF**, **PPTX**, atau **HTML**
- Tema bawaan Marp: \`default\`, \`gaia\`, \`uncover\`

---

## Contoh Kode

\`\`\`ts
function hello(name: string) {
	return \`Halo, \${name}!\`;
}
\`\`\`

---

<!-- _class: lead -->

# Terima Kasih
**POLMAN Bandung** — Antigravity Project
`;

	let markdown = STARTER_MARKDOWN;
	let filename = 'untitled.md';
	let previewHtml = '';
	let previewCss = '';
	let renderError = '';
	let renderingDone = false;

	let slidesList: MarpSlideFile[] = [];
	let listLoading = false;
	let saving = false;
	let exporting: MarpExportFormat | '' = '';

	let marpInstance: any = null;
	let editorEl: HTMLTextAreaElement;
	let previewIframe: HTMLIFrameElement;

	let renderTimer: ReturnType<typeof setTimeout> | null = null;

	const ensureMarp = async () => {
		if (marpInstance) return marpInstance;
		const mod = await import('@marp-team/marp-core');
		const Marp = mod.Marp ?? (mod as any).default;
		marpInstance = new Marp({ html: true, math: 'katex' });
		return marpInstance;
	};

	const renderPreview = async () => {
		try {
			const marp = await ensureMarp();
			const { html, css } = marp.render(markdown);
			previewHtml = html;
			previewCss = css;
			renderError = '';
			renderingDone = true;
			await tick();
			updateIframe();
		} catch (e: any) {
			renderError = e?.message || String(e);
		}
	};

	const scheduleRender = () => {
		if (renderTimer) clearTimeout(renderTimer);
		renderTimer = setTimeout(renderPreview, 200);
	};

	const updateIframe = () => {
		if (!previewIframe) return;
		// NB: tag CSS sengaja di-pecah pakai concat string supaya Svelte preprocessor
		// gak salah anggap konten di dalam template literal ini sebagai CSS komponen.
		const styleOpen = '<sty' + 'le>';
		const styleClose = '</sty' + 'le>';
		const doc = `<!DOCTYPE html>
<html><head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
${styleOpen}
	html, body { margin:0; padding:0; background:#1a1a1a; }
	body { display:flex; flex-direction:column; align-items:center; gap:16px; padding:16px; }
	${previewCss}
	svg[data-marpit-svg] { box-shadow: 0 4px 18px rgba(0,0,0,0.4); border-radius: 6px; max-width: 100%; height: auto; }
${styleClose}
</head><body>${previewHtml}</body></html>`;
		previewIframe.srcdoc = doc;
	};

	const handleEditorInput = () => {
		scheduleRender();
	};

	const refreshList = async () => {
		listLoading = true;
		try {
			slidesList = await listSlides(localStorage.token);
		} catch (e: any) {
			toast.error(e?.message || 'Failed to list slides');
		} finally {
			listLoading = false;
		}
	};

	const handleNew = () => {
		if (markdown.trim() && !confirm('Ganti deck saat ini dengan template baru?')) return;
		markdown = STARTER_MARKDOWN;
		filename = 'untitled.md';
		scheduleRender();
	};

	const handleSave = async () => {
		const name = (prompt('Simpan sebagai (nama file .md):', filename) || '').trim();
		if (!name) return;
		saving = true;
		try {
			const res = await saveSlide(localStorage.token, name, markdown);
			filename = res.filename;
			toast.success(`Tersimpan: ${res.path}`);
			await refreshList();
		} catch (e: any) {
			toast.error(e?.message || 'Save failed');
		} finally {
			saving = false;
		}
	};

	const handleLoad = async (name: string) => {
		try {
			const res = await loadSlide(localStorage.token, name);
			markdown = res.content;
			filename = res.filename;
			scheduleRender();
			toast.success(`Dibuka: ${name}`);
		} catch (e: any) {
			toast.error(e?.message || 'Load failed');
		}
	};

	const handleDelete = async (name: string) => {
		if (!confirm(`Hapus "${name}"?`)) return;
		try {
			await deleteSlide(localStorage.token, name);
			toast.success(`Dihapus: ${name}`);
			await refreshList();
		} catch (e: any) {
			toast.error(e?.message || 'Delete failed');
		}
	};

	const downloadBlob = (blob: Blob, name: string) => {
		const url = URL.createObjectURL(blob);
		const a = document.createElement('a');
		a.href = url;
		a.download = name;
		document.body.appendChild(a);
		a.click();
		document.body.removeChild(a);
		URL.revokeObjectURL(url);
	};

	const handleExport = async (format: MarpExportFormat) => {
		exporting = format;
		try {
			if (format === 'html') {
				// Render fully self-contained HTML on the client (no backend dep).
				const marp = await ensureMarp();
				const { html, css } = marp.render(markdown);
				// Pecah tag CSS biar Svelte preprocessor gak salah anggap sebagai CSS komponen.
				const sOpen = '<sty' + 'le>';
				const sClose = '</sty' + 'le>';
				const doc = `<!DOCTYPE html>
<html><head>
<meta charset="utf-8"/>
<title>${filename.replace(/\.md$/i, '')}</title>
${sOpen}${css}${sClose}
</head><body>${html}</body></html>`;
				const blob = new Blob([doc], { type: 'text/html;charset=utf-8' });
				downloadBlob(blob, filename.replace(/\.md$/i, '') + '.html');
				toast.success('HTML siap diunduh');
				return;
			}

			const blob = await exportSlide(localStorage.token, filename, markdown, format);
			downloadBlob(blob, filename.replace(/\.md$/i, '') + `.${format}`);
			toast.success(`${format.toUpperCase()} siap diunduh`);
		} catch (e: any) {
			toast.error(e?.message || `Export ${format} failed`);
		} finally {
			exporting = '';
		}
	};

	const formatDate = (epochSeconds: number) => {
		try {
			return new Date(epochSeconds * 1000).toLocaleString();
		} catch {
			return '';
		}
	};

	onMount(() => {
		renderPreview();
		refreshList();
	});
</script>

<div class="marp-shell">
	<aside class="sidebar">
		<div class="sidebar-header">
			<span class="sidebar-title">SLIDES</span>
			<button class="icon-btn" title="Refresh" on:click={refreshList} disabled={listLoading}>
				<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="size-3.5">
					<path fill-rule="evenodd" d="M15.312 11.424a5.5 5.5 0 0 1-9.201 2.466l-.312-.311h2.433a.75.75 0 0 0 0-1.5H3.989a.75.75 0 0 0-.75.75v4.242a.75.75 0 0 0 1.5 0v-2.43l.31.31a7 7 0 0 0 11.712-3.138.75.75 0 0 0-1.449-.39Zm1.23-3.723a.75.75 0 0 0 .219-.53V2.929a.75.75 0 0 0-1.5 0V5.36l-.31-.31A7 7 0 0 0 3.239 8.188a.75.75 0 1 0 1.448.389A5.5 5.5 0 0 1 13.89 6.11l.311.31h-2.432a.75.75 0 0 0 0 1.5h4.243a.75.75 0 0 0 .53-.219Z" clip-rule="evenodd"/>
				</svg>
			</button>
		</div>

		<div class="sidebar-actions">
			<button class="primary-btn" on:click={handleNew}>+ New deck</button>
		</div>

		<div class="slide-list">
			{#if listLoading}
				<div class="muted">Loading...</div>
			{:else if slidesList.length === 0}
				<div class="muted">Belum ada slide tersimpan.</div>
			{:else}
				{#each slidesList as item (item.filename)}
					<div class="slide-item" class:active={item.filename === filename}>
						<button class="slide-name" on:click={() => handleLoad(item.filename)} title={item.filename}>
							<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="size-3.5 shrink-0">
								<path d="M3.5 3A1.5 1.5 0 0 0 2 4.5v11A1.5 1.5 0 0 0 3.5 17h13a1.5 1.5 0 0 0 1.5-1.5v-11A1.5 1.5 0 0 0 16.5 3h-13Z"/>
							</svg>
							<span class="truncate">{item.filename}</span>
						</button>
						<button class="icon-btn danger" title="Delete" on:click={() => handleDelete(item.filename)}>
							<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="size-3.5">
								<path fill-rule="evenodd" d="M8.75 1A2.75 2.75 0 0 0 6 3.75v.443c-.795.077-1.584.176-2.365.298a.75.75 0 1 0 .23 1.482l.149-.022.841 10.518A2.75 2.75 0 0 0 7.596 19h4.807a2.75 2.75 0 0 0 2.742-2.53l.841-10.52.149.023a.75.75 0 0 0 .23-1.482A41.03 41.03 0 0 0 14 4.193V3.75A2.75 2.75 0 0 0 11.25 1h-2.5ZM10 4c.84 0 1.673.025 2.5.075V3.75c0-.69-.56-1.25-1.25-1.25h-2.5c-.69 0-1.25.56-1.25 1.25v.325C8.327 4.025 9.16 4 10 4ZM8.58 7.72a.75.75 0 0 0-1.5.06l.3 7.5a.75.75 0 1 0 1.5-.06l-.3-7.5Zm4.34.06a.75.75 0 1 0-1.5-.06l-.3 7.5a.75.75 0 1 0 1.5.06l.3-7.5Z" clip-rule="evenodd"/>
							</svg>
						</button>
					</div>
					<div class="slide-meta">{formatDate(item.modified_at)}</div>
				{/each}
			{/if}
		</div>
	</aside>

	<section class="editor-pane">
		<header class="pane-header">
			<div class="filename">
				<input bind:value={filename} class="filename-input" spellcheck="false" />
			</div>
			<div class="actions">
				<button class="action-btn" on:click={handleSave} disabled={saving}>
					{saving ? 'Saving...' : 'Save'}
				</button>
				<button class="action-btn" on:click={() => handleExport('html')} disabled={!!exporting}>
					{exporting === 'html' ? 'HTML...' : 'Export HTML'}
				</button>
				<button class="action-btn" on:click={() => handleExport('pdf')} disabled={!!exporting}>
					{exporting === 'pdf' ? 'PDF...' : 'Export PDF'}
				</button>
				<button class="action-btn" on:click={() => handleExport('pptx')} disabled={!!exporting}>
					{exporting === 'pptx' ? 'PPTX...' : 'Export PPTX'}
				</button>
			</div>
		</header>
		<textarea
			bind:this={editorEl}
			bind:value={markdown}
			class="editor"
			spellcheck="false"
			on:input={handleEditorInput}
		></textarea>
	</section>

	<section class="preview-pane">
		<header class="pane-header">
			<span class="pane-title">PREVIEW</span>
			{#if renderError}
				<span class="error">{renderError}</span>
			{/if}
		</header>
		<iframe
			bind:this={previewIframe}
			title="Marp preview"
			class="preview-frame"
			sandbox="allow-same-origin"
		></iframe>
	</section>
</div>

<style>
	.marp-shell {
		display: grid;
		grid-template-columns: 240px 1fr 1fr;
		width: 100%;
		height: 100%;
		min-height: 0;
		background: #0a0a0a;
		color: #e5e5e5;
		font-family: 'Inter', system-ui, sans-serif;
	}

	.sidebar {
		display: flex;
		flex-direction: column;
		border-right: 1px solid #1a1a1a;
		min-height: 0;
	}

	.sidebar-header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 10px 12px;
		border-bottom: 1px solid #1a1a1a;
	}

	.sidebar-title {
		font-size: 11px;
		letter-spacing: 1px;
		font-weight: 600;
		color: rgba(255, 255, 255, 0.5);
	}

	.sidebar-actions {
		padding: 10px;
	}

	.slide-list {
		flex: 1;
		overflow-y: auto;
		padding: 0 6px 8px;
	}

	.slide-item {
		display: flex;
		align-items: center;
		gap: 4px;
		padding: 4px 6px;
		border-radius: 6px;
	}

	.slide-item:hover {
		background: rgba(255, 255, 255, 0.04);
	}

	.slide-item.active {
		background: rgba(59, 130, 246, 0.15);
	}

	.slide-name {
		flex: 1;
		display: flex;
		align-items: center;
		gap: 6px;
		background: none;
		border: none;
		color: #e5e5e5;
		font-size: 12px;
		padding: 2px 4px;
		text-align: left;
		cursor: pointer;
		min-width: 0;
	}

	.slide-name .truncate {
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}

	.slide-meta {
		font-size: 10px;
		color: rgba(255, 255, 255, 0.3);
		padding: 0 12px 4px 26px;
		font-family: 'JetBrains Mono', monospace;
	}

	.muted {
		color: rgba(255, 255, 255, 0.35);
		font-size: 12px;
		padding: 8px 10px;
	}

	.icon-btn {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		width: 22px;
		height: 22px;
		background: none;
		border: none;
		border-radius: 4px;
		color: rgba(255, 255, 255, 0.5);
		cursor: pointer;
	}

	.icon-btn:hover {
		background: rgba(255, 255, 255, 0.06);
		color: #fff;
	}

	.icon-btn.danger:hover {
		background: rgba(239, 68, 68, 0.15);
		color: #f87171;
	}

	.primary-btn {
		width: 100%;
		padding: 7px 10px;
		background: linear-gradient(135deg, #3b82f6, #8b5cf6);
		color: #fff;
		font-size: 12px;
		font-weight: 600;
		border: none;
		border-radius: 8px;
		cursor: pointer;
	}

	.primary-btn:hover {
		filter: brightness(1.1);
	}

	.editor-pane,
	.preview-pane {
		display: flex;
		flex-direction: column;
		min-height: 0;
		min-width: 0;
	}

	.editor-pane {
		border-right: 1px solid #1a1a1a;
	}

	.pane-header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 8px;
		padding: 6px 10px;
		background: #0a0a0a;
		border-bottom: 1px solid #1a1a1a;
	}

	.pane-title {
		font-size: 11px;
		letter-spacing: 1px;
		font-weight: 600;
		color: rgba(255, 255, 255, 0.5);
	}

	.filename {
		flex: 1;
		min-width: 0;
	}

	.filename-input {
		width: 100%;
		background: transparent;
		border: 1px solid transparent;
		color: #e5e5e5;
		font-size: 12px;
		padding: 3px 6px;
		border-radius: 4px;
		font-family: 'JetBrains Mono', monospace;
	}

	.filename-input:hover,
	.filename-input:focus {
		background: rgba(255, 255, 255, 0.04);
		border-color: rgba(255, 255, 255, 0.08);
		outline: none;
	}

	.actions {
		display: flex;
		gap: 6px;
		flex-wrap: wrap;
	}

	.action-btn {
		padding: 4px 10px;
		background: rgba(255, 255, 255, 0.06);
		border: 1px solid rgba(255, 255, 255, 0.08);
		color: #e5e5e5;
		font-size: 11px;
		border-radius: 6px;
		cursor: pointer;
	}

	.action-btn:hover:not(:disabled) {
		background: rgba(59, 130, 246, 0.2);
		border-color: rgba(59, 130, 246, 0.4);
	}

	.action-btn:disabled {
		opacity: 0.5;
		cursor: not-allowed;
	}

	.editor {
		flex: 1;
		min-height: 0;
		resize: none;
		background: #0a0a0a;
		color: #e5e5e5;
		font-family: 'JetBrains Mono', 'Fira Code', monospace;
		font-size: 13px;
		line-height: 1.55;
		padding: 14px;
		border: none;
		outline: none;
	}

	.preview-frame {
		flex: 1;
		min-height: 0;
		width: 100%;
		border: none;
		background: #1a1a1a;
	}

	.error {
		font-size: 11px;
		color: #f87171;
		font-family: 'JetBrains Mono', monospace;
		max-width: 60%;
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}
</style>
