import { writable, derived } from 'svelte/store';

// ============================================================================
// IDE State Management
// ============================================================================

export interface OpenFile {
	path: string;
	name: string;
	content: string;
	originalContent: string;
	language: string;
	modified: boolean;
	loading: boolean;
}

export interface TreeNode {
	name: string;
	path: string;
	type: 'file' | 'directory';
	icon: string;
	size?: number;
	extension?: string;
	children?: TreeNode[];
	collapsed?: boolean;
	error?: string;
}

export interface SearchResult {
	path: string;
	line: number;
	content: string;
	file?: string;
}

// Whether IDE mode is active
export const ideMode = writable<boolean>(false);

// List of open files (editor tabs)
export const openFiles = writable<OpenFile[]>([]);

// Currently active file path
export const activeFilePath = writable<string>('');

// File tree data
export const fileTree = writable<TreeNode | null>(null);

// Set of expanded directory paths
export const expandedDirs = writable<Set<string>>(new Set(['.']));

// Whether the file explorer panel is visible
export const showFileExplorer = writable<boolean>(true);

// Whether the terminal panel is visible
export const showTerminalPanel = writable<boolean>(true);

// Search results
export const ideSearchResults = writable<SearchResult[]>([]);

// IDE loading state
export const ideLoading = writable<boolean>(false);

// Current workspace info
export const workspaceInfo = writable<{ workspace_dir: string; max_file_size: number } | null>(null);

// Derived: get the currently active file object
export const activeFile = derived(
	[openFiles, activeFilePath],
	([$openFiles, $activeFilePath]) => {
		return $openFiles.find((f) => f.path === $activeFilePath) || null;
	}
);

// Derived: whether any files have unsaved changes
export const hasUnsavedChanges = derived(openFiles, ($openFiles) => {
	return $openFiles.some((f) => f.modified);
});

// ============================================================================
// Helper Functions
// ============================================================================

/**
 * Detect language from file extension for CodeMirror syntax highlighting
 */
export function getLanguageFromPath(path: string): string {
	const ext = path.split('.').pop()?.toLowerCase() || '';
	const langMap: Record<string, string> = {
		js: 'javascript',
		jsx: 'jsx',
		ts: 'typescript',
		tsx: 'tsx',
		py: 'python',
		css: 'css',
		scss: 'css',
		less: 'css',
		html: 'html',
		htm: 'html',
		svelte: 'html',
		vue: 'html',
		json: 'json',
		md: 'markdown',
		yaml: 'yaml',
		yml: 'yaml',
		toml: 'toml',
		xml: 'xml',
		sql: 'sql',
		sh: 'shell',
		bash: 'shell',
		zsh: 'shell',
		dockerfile: 'dockerfile',
		rs: 'rust',
		go: 'go',
		java: 'java',
		kt: 'kotlin',
		c: 'c',
		cpp: 'cpp',
		h: 'c',
		hpp: 'cpp',
		rb: 'ruby',
		php: 'php',
		r: 'r',
		swift: 'swift',
		dart: 'dart',
		lua: 'lua',
		scala: 'scala',
		ex: 'elixir',
		exs: 'elixir',
		hcl: 'hcl',
		tf: 'hcl',
	};
	return langMap[ext] || 'text';
}
