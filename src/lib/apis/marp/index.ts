import { WEBUI_API_BASE_URL } from '$lib/constants';

const BASE = `${WEBUI_API_BASE_URL}/antigravity/marp`;

export type MarpSlideFile = {
	filename: string;
	size: number;
	modified_at: number;
};

export type MarpSaveResult = {
	status: string;
	filename: string;
	path: string;
	size: number;
	modified_at: number;
};

export type MarpExportFormat = 'pdf' | 'pptx' | 'html' | 'png';

const authHeaders = (token: string) => ({
	Accept: 'application/json',
	'Content-Type': 'application/json',
	authorization: `Bearer ${token}`
});

export const listSlides = async (token: string): Promise<MarpSlideFile[]> => {
	const res = await fetch(`${BASE}/list`, {
		method: 'GET',
		headers: authHeaders(token)
	});
	if (!res.ok) {
		const err = await res.json().catch(() => ({}));
		throw new Error(err.detail || `Failed to list slides (${res.status})`);
	}
	const data = await res.json();
	return data.items ?? [];
};

export const loadSlide = async (
	token: string,
	filename: string
): Promise<{ filename: string; content: string }> => {
	const res = await fetch(`${BASE}/load?filename=${encodeURIComponent(filename)}`, {
		method: 'GET',
		headers: authHeaders(token)
	});
	if (!res.ok) {
		const err = await res.json().catch(() => ({}));
		throw new Error(err.detail || `Failed to load slide (${res.status})`);
	}
	return res.json();
};

export const saveSlide = async (
	token: string,
	filename: string,
	content: string
): Promise<MarpSaveResult> => {
	const res = await fetch(`${BASE}/save`, {
		method: 'POST',
		headers: authHeaders(token),
		body: JSON.stringify({ filename, content })
	});
	if (!res.ok) {
		const err = await res.json().catch(() => ({}));
		throw new Error(err.detail || `Failed to save slide (${res.status})`);
	}
	return res.json();
};

export const deleteSlide = async (token: string, filename: string): Promise<void> => {
	const res = await fetch(`${BASE}/delete?filename=${encodeURIComponent(filename)}`, {
		method: 'DELETE',
		headers: authHeaders(token)
	});
	if (!res.ok) {
		const err = await res.json().catch(() => ({}));
		throw new Error(err.detail || `Failed to delete slide (${res.status})`);
	}
};

export const exportSlide = async (
	token: string,
	filename: string,
	content: string,
	format: MarpExportFormat
): Promise<Blob> => {
	const res = await fetch(`${BASE}/export`, {
		method: 'POST',
		headers: authHeaders(token),
		body: JSON.stringify({ filename, content, format })
	});
	if (!res.ok) {
		const err = await res.json().catch(() => ({}));
		throw new Error(err.detail || `Export failed (${res.status})`);
	}
	return res.blob();
};
