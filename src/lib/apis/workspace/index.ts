import { WEBUI_API_BASE_URL } from '$lib/constants';

// ============================================================================
// Workspace Filesystem API Client
// ============================================================================

function getHeaders(): Record<string, string> {
	const token = localStorage.getItem('token') ?? '';
	return {
		Authorization: `Bearer ${token}`,
		'Content-Type': 'application/json'
	};
}

/**
 * Get directory tree listing
 */
export async function getFileTree(
	path: string = '.',
	depth: number = 3
): Promise<any> {
	const params = new URLSearchParams({ path, depth: String(depth) });
	const res = await fetch(`${WEBUI_API_BASE_URL}/workspace/tree?${params}`, {
		headers: getHeaders()
	});
	if (!res.ok) {
		const err = await res.json().catch(() => ({ detail: res.statusText }));
		throw new Error(err.detail || 'Failed to load file tree');
	}
	return res.json();
}

/**
 * Read file content
 */
export async function readFile(path: string): Promise<{
	path: string;
	content: string;
	size: number;
	extension: string;
	name: string;
}> {
	const params = new URLSearchParams({ path });
	const res = await fetch(`${WEBUI_API_BASE_URL}/workspace/read?${params}`, {
		headers: getHeaders()
	});
	if (!res.ok) {
		const err = await res.json().catch(() => ({ detail: res.statusText }));
		throw new Error(err.detail || 'Failed to read file');
	}
	return res.json();
}

/**
 * Write/create a file
 */
export async function writeFile(
	path: string,
	content: string,
	createDirs: boolean = true
): Promise<{ status: string; path: string; action: string; size: number }> {
	const res = await fetch(`${WEBUI_API_BASE_URL}/workspace/write`, {
		method: 'POST',
		headers: getHeaders(),
		body: JSON.stringify({ path, content, create_dirs: createDirs })
	});
	if (!res.ok) {
		const err = await res.json().catch(() => ({ detail: res.statusText }));
		throw new Error(err.detail || 'Failed to write file');
	}
	return res.json();
}

/**
 * Create a directory
 */
export async function createDirectory(path: string): Promise<any> {
	const res = await fetch(`${WEBUI_API_BASE_URL}/workspace/mkdir`, {
		method: 'POST',
		headers: getHeaders(),
		body: JSON.stringify({ path })
	});
	if (!res.ok) {
		const err = await res.json().catch(() => ({ detail: res.statusText }));
		throw new Error(err.detail || 'Failed to create directory');
	}
	return res.json();
}

/**
 * Delete a file or directory
 */
export async function deleteItem(path: string): Promise<any> {
	const params = new URLSearchParams({ path });
	const res = await fetch(`${WEBUI_API_BASE_URL}/workspace/delete?${params}`, {
		method: 'DELETE',
		headers: getHeaders()
	});
	if (!res.ok) {
		const err = await res.json().catch(() => ({ detail: res.statusText }));
		throw new Error(err.detail || 'Failed to delete item');
	}
	return res.json();
}

/**
 * Rename/move a file or directory
 */
export async function renameItem(
	oldPath: string,
	newPath: string
): Promise<any> {
	const res = await fetch(`${WEBUI_API_BASE_URL}/workspace/rename`, {
		method: 'POST',
		headers: getHeaders(),
		body: JSON.stringify({ old_path: oldPath, new_path: newPath })
	});
	if (!res.ok) {
		const err = await res.json().catch(() => ({ detail: res.statusText }));
		throw new Error(err.detail || 'Failed to rename item');
	}
	return res.json();
}

/**
 * Search for text in files
 */
export async function searchFiles(
	query: string,
	path: string = '.',
	filePattern: string = '*',
	maxResults: number = 50
): Promise<{
	query: string;
	results: Array<{ path: string; line: number; content: string; file?: string }>;
	total: number;
	truncated: boolean;
}> {
	const params = new URLSearchParams({
		query,
		path,
		file_pattern: filePattern,
		max_results: String(maxResults)
	});
	const res = await fetch(`${WEBUI_API_BASE_URL}/workspace/search?${params}`, {
		headers: getHeaders()
	});
	if (!res.ok) {
		const err = await res.json().catch(() => ({ detail: res.statusText }));
		throw new Error(err.detail || 'Search failed');
	}
	return res.json();
}

/**
 * Execute a shell command
 */
export async function executeCommand(
	command: string,
	cwd: string = '.',
	timeout: number = 30
): Promise<{
	status: string;
	exit_code?: number;
	stdout?: string;
	stderr?: string;
	error?: string;
	command: string;
	cwd?: string;
}> {
	const res = await fetch(`${WEBUI_API_BASE_URL}/workspace/execute`, {
		method: 'POST',
		headers: getHeaders(),
		body: JSON.stringify({ command, cwd, timeout })
	});
	if (!res.ok) {
		const err = await res.json().catch(() => ({ detail: res.statusText }));
		throw new Error(err.detail || 'Command execution failed');
	}
	return res.json();
}

/**
 * Get workspace information
 */
export async function getWorkspaceInfo(): Promise<{
	workspace_dir: string;
	max_file_size: number;
	blocked_extensions: string[];
}> {
	const res = await fetch(`${WEBUI_API_BASE_URL}/workspace/info`, {
		headers: getHeaders()
	});
	if (!res.ok) {
		const err = await res.json().catch(() => ({ detail: res.statusText }));
		throw new Error(err.detail || 'Failed to get workspace info');
	}
	return res.json();
}
