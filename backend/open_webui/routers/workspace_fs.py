"""Workspace Filesystem API for Antigravity AI IDE.

Provides REST endpoints for browsing, reading, writing, and searching files
within a configured workspace directory on the host filesystem.

Security:
  - All paths are sanitized to prevent directory traversal
  - Operations are restricted to WORKSPACE_DIR
  - Only verified users can access the API
  - Admin-configurable workspace roots
"""

import asyncio
import fnmatch
import logging
import os
import posixpath
import subprocess
import stat
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from pydantic import BaseModel

from open_webui.utils.auth import get_verified_user

log = logging.getLogger(__name__)

router = APIRouter()

# Maximum file size for read/write operations (5MB default)
MAX_FILE_SIZE = int(os.environ.get('WORKSPACE_MAX_FILE_SIZE', 5 * 1024 * 1024))

# File extensions that are blocked from write operations
BLOCKED_EXTENSIONS = {'.exe', '.dll', '.so', '.bin', '.msi', '.bat', '.cmd', '.com', '.scr'}

# Maximum depth for tree listing to prevent excessive recursion
MAX_TREE_DEPTH = 10

# Maximum number of search results
MAX_SEARCH_RESULTS = 100

# Directories to always skip in tree listing
SKIP_DIRS = {
    'node_modules', '.git', '__pycache__', '.venv', 'venv',
    '.next', '.nuxt', 'dist', 'build', '.cache', '.tox',
    '.mypy_cache', '.pytest_cache', '.ruff_cache',
    'target', 'vendor', '.svn', '.hg',
}


def _get_workspace_dir() -> Path:
    """Get the configured workspace directory."""
    workspace = os.environ.get('WORKSPACE_DIR', '')
    if not workspace:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail='WORKSPACE_DIR not configured. Set WORKSPACE_DIR environment variable.',
        )
    ws_path = Path(workspace).resolve()
    if not ws_path.is_dir():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f'WORKSPACE_DIR "{workspace}" does not exist or is not a directory.',
        )
    return ws_path


def _safe_resolve(workspace: Path, relative_path: str) -> Path:
    """Resolve a relative path within the workspace, preventing directory traversal.

    Raises HTTPException if the path escapes the workspace root.
    """
    # Normalize the path
    cleaned = posixpath.normpath(relative_path)

    # Reject absolute paths and parent traversal
    if cleaned.startswith('/') or cleaned.startswith('\\') or cleaned.startswith('..'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid path: directory traversal not allowed.',
        )

    resolved = (workspace / cleaned).resolve()

    # Ensure the resolved path is within the workspace
    try:
        resolved.relative_to(workspace)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid path: escapes workspace directory.',
        )

    return resolved


def _get_file_icon(name: str, is_dir: bool) -> str:
    """Return an emoji icon based on file extension."""
    if is_dir:
        return '📁'

    ext = Path(name).suffix.lower()
    icons = {
        '.py': '🐍', '.js': '📜', '.ts': '📘', '.tsx': '⚛️', '.jsx': '⚛️',
        '.html': '🌐', '.css': '🎨', '.scss': '🎨', '.less': '🎨',
        '.json': '📋', '.yaml': '⚙️', '.yml': '⚙️', '.toml': '⚙️',
        '.md': '📝', '.txt': '📄', '.csv': '📊', '.xml': '📰',
        '.sql': '🗃️', '.sh': '🖥️', '.bash': '🖥️', '.zsh': '🖥️',
        '.dockerfile': '🐳', '.docker': '🐳',
        '.rs': '🦀', '.go': '🐹', '.java': '☕', '.kt': '🟣',
        '.c': '©️', '.cpp': '➕', '.h': '📎',
        '.png': '🖼️', '.jpg': '🖼️', '.jpeg': '🖼️', '.svg': '🖼️', '.gif': '🖼️',
        '.pdf': '📕', '.doc': '📘', '.docx': '📘',
        '.zip': '📦', '.tar': '📦', '.gz': '📦',
        '.env': '🔑', '.gitignore': '🚫', '.lock': '🔒',
        '.svelte': '🔥', '.vue': '💚', '.rb': '💎', '.php': '🐘',
    }

    # Check if filename matches special patterns
    lower_name = name.lower()
    if lower_name == 'dockerfile' or lower_name.startswith('dockerfile'):
        return '🐳'
    if lower_name == 'makefile':
        return '🛠️'

    return icons.get(ext, '📄')


def _build_tree_node(path: Path, workspace: Path, depth: int, max_depth: int) -> dict:
    """Recursively build a tree node for a file or directory."""
    relative = str(path.relative_to(workspace)).replace('\\', '/')
    name = path.name
    is_dir = path.is_dir()

    node = {
        'name': name,
        'path': relative,
        'type': 'directory' if is_dir else 'file',
        'icon': _get_file_icon(name, is_dir),
    }

    if is_dir:
        node['children'] = []
        if depth < max_depth:
            try:
                entries = sorted(path.iterdir(), key=lambda e: (not e.is_dir(), e.name.lower()))
                for entry in entries:
                    # Skip hidden files/dirs and known heavy directories
                    if entry.name.startswith('.') and entry.name not in ('.env', '.gitignore', '.dockerignore'):
                        if entry.is_dir():
                            continue
                    if entry.is_dir() and entry.name in SKIP_DIRS:
                        # Show the directory but don't expand it
                        node['children'].append({
                            'name': entry.name,
                            'path': str(entry.relative_to(workspace)).replace('\\', '/'),
                            'type': 'directory',
                            'icon': '📁',
                            'children': [],
                            'collapsed': True,
                        })
                        continue
                    node['children'].append(
                        _build_tree_node(entry, workspace, depth + 1, max_depth)
                    )
            except PermissionError:
                node['error'] = 'Permission denied'
    else:
        try:
            node['size'] = path.stat().st_size
            node['extension'] = path.suffix.lower()
        except OSError:
            node['size'] = 0

    return node


# ============================================================================
# Endpoints
# ============================================================================


@router.get('/tree')
async def get_file_tree(
    path: str = Query('.', description='Relative path within workspace'),
    depth: int = Query(3, ge=1, le=MAX_TREE_DEPTH, description='Max depth to traverse'),
    user=Depends(get_verified_user),
):
    """Get directory tree listing for the workspace."""
    workspace = _get_workspace_dir()
    target = _safe_resolve(workspace, path)

    if not target.is_dir():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Directory not found: {path}',
        )

    tree = await asyncio.to_thread(_build_tree_node, target, workspace, 0, depth)
    return tree


@router.get('/read')
async def read_file(
    path: str = Query(..., description='Relative file path within workspace'),
    user=Depends(get_verified_user),
):
    """Read the content of a file."""
    workspace = _get_workspace_dir()
    target = _safe_resolve(workspace, path)

    if not target.is_file():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'File not found: {path}',
        )

    file_size = target.stat().st_size
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f'File too large ({file_size} bytes). Max: {MAX_FILE_SIZE} bytes.',
        )

    try:
        content = await asyncio.to_thread(target.read_text, 'utf-8')
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail='File appears to be binary and cannot be read as text.',
        )

    return {
        'path': path,
        'content': content,
        'size': file_size,
        'extension': target.suffix.lower(),
        'name': target.name,
    }


class WriteFileForm(BaseModel):
    path: str
    content: str
    create_dirs: bool = True


@router.post('/write')
async def write_file(
    form_data: WriteFileForm,
    user=Depends(get_verified_user),
):
    """Write content to a file. Creates the file if it doesn't exist."""
    workspace = _get_workspace_dir()

    ext = Path(form_data.path).suffix.lower()
    if ext in BLOCKED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'File extension "{ext}" is not allowed.',
        )

    content_size = len(form_data.content.encode('utf-8'))
    if content_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f'Content too large ({content_size} bytes). Max: {MAX_FILE_SIZE} bytes.',
        )

    target = _safe_resolve(workspace, form_data.path)

    if form_data.create_dirs:
        target.parent.mkdir(parents=True, exist_ok=True)

    existed = target.is_file()
    await asyncio.to_thread(target.write_text, form_data.content, 'utf-8')

    return {
        'status': 'success',
        'path': form_data.path,
        'action': 'updated' if existed else 'created',
        'size': content_size,
    }


class MkdirForm(BaseModel):
    path: str


@router.post('/mkdir')
async def make_directory(
    form_data: MkdirForm,
    user=Depends(get_verified_user),
):
    """Create a directory (and any parent directories)."""
    workspace = _get_workspace_dir()
    target = _safe_resolve(workspace, form_data.path)

    if target.exists():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'Path already exists: {form_data.path}',
        )

    target.mkdir(parents=True, exist_ok=True)

    return {
        'status': 'success',
        'path': form_data.path,
    }


@router.delete('/delete')
async def delete_item(
    path: str = Query(..., description='Relative path to delete'),
    user=Depends(get_verified_user),
):
    """Delete a file or empty directory."""
    workspace = _get_workspace_dir()
    target = _safe_resolve(workspace, path)

    if not target.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Path not found: {path}',
        )

    # Prevent deleting the workspace root
    if target == workspace:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Cannot delete workspace root.',
        )

    if target.is_file():
        await asyncio.to_thread(target.unlink)
    elif target.is_dir():
        import shutil
        await asyncio.to_thread(shutil.rmtree, target)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Path is neither a file nor directory.',
        )

    return {
        'status': 'success',
        'path': path,
        'action': 'deleted',
    }


class RenameForm(BaseModel):
    old_path: str
    new_path: str


@router.post('/rename')
async def rename_item(
    form_data: RenameForm,
    user=Depends(get_verified_user),
):
    """Rename/move a file or directory."""
    workspace = _get_workspace_dir()
    source = _safe_resolve(workspace, form_data.old_path)
    destination = _safe_resolve(workspace, form_data.new_path)

    if not source.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Source not found: {form_data.old_path}',
        )

    if destination.exists():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'Destination already exists: {form_data.new_path}',
        )

    destination.parent.mkdir(parents=True, exist_ok=True)
    await asyncio.to_thread(source.rename, destination)

    return {
        'status': 'success',
        'old_path': form_data.old_path,
        'new_path': form_data.new_path,
    }


@router.get('/search')
async def search_files(
    query: str = Query(..., description='Search query (text to find in files)'),
    path: str = Query('.', description='Relative path to search within'),
    file_pattern: str = Query('*', description='Glob pattern for files (e.g., *.py)'),
    max_results: int = Query(50, ge=1, le=MAX_SEARCH_RESULTS),
    user=Depends(get_verified_user),
):
    """Search for text within files in the workspace."""
    workspace = _get_workspace_dir()
    search_root = _safe_resolve(workspace, path)

    if not search_root.is_dir():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Search directory not found: {path}',
        )

    results = []

    def _search():
        count = 0
        for root, dirs, files in os.walk(search_root):
            # Skip heavy directories
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith('.')]

            for filename in files:
                if count >= max_results:
                    return
                if not fnmatch.fnmatch(filename, file_pattern):
                    continue

                filepath = Path(root) / filename
                try:
                    if filepath.stat().st_size > MAX_FILE_SIZE:
                        continue
                    content = filepath.read_text('utf-8')
                except (UnicodeDecodeError, PermissionError, OSError):
                    continue

                # Find matching lines
                for line_num, line in enumerate(content.split('\n'), 1):
                    if query.lower() in line.lower():
                        if count >= max_results:
                            return
                        relative = str(filepath.relative_to(workspace)).replace('\\', '/')
                        results.append({
                            'path': relative,
                            'line': line_num,
                            'content': line.strip()[:200],
                            'file': filename,
                        })
                        count += 1

    await asyncio.to_thread(_search)

    return {
        'query': query,
        'results': results,
        'total': len(results),
        'truncated': len(results) >= max_results,
    }


class ExecuteCommandForm(BaseModel):
    command: str
    cwd: str = '.'
    timeout: int = 30


@router.post('/execute')
async def execute_command(
    form_data: ExecuteCommandForm,
    user=Depends(get_verified_user),
):
    """Execute a shell command within the workspace directory.

    WARNING: This is a powerful operation. The command runs on the server.
    """
    workspace = _get_workspace_dir()
    work_dir = _safe_resolve(workspace, form_data.cwd)

    if not work_dir.is_dir():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Working directory not found: {form_data.cwd}',
        )

    # Limit timeout to prevent long-running commands
    timeout = min(form_data.timeout, 120)

    def _run():
        try:
            # Determine if we're on Windows or Unix
            is_windows = os.name == 'nt'

            if is_windows:
                result = subprocess.run(
                    form_data.command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    cwd=str(work_dir),
                    timeout=timeout,
                    env={**os.environ, 'PYTHONIOENCODING': 'utf-8'},
                )
            else:
                result = subprocess.run(
                    form_data.command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    cwd=str(work_dir),
                    timeout=timeout,
                    executable='/bin/bash',
                    env={**os.environ, 'PYTHONIOENCODING': 'utf-8'},
                )

            return {
                'status': 'success',
                'exit_code': result.returncode,
                'stdout': result.stdout[-10000:] if result.stdout else '',  # Limit output
                'stderr': result.stderr[-5000:] if result.stderr else '',
                'command': form_data.command,
                'cwd': form_data.cwd,
            }
        except subprocess.TimeoutExpired:
            return {
                'status': 'timeout',
                'error': f'Command timed out after {timeout}s',
                'command': form_data.command,
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'command': form_data.command,
            }

    result = await asyncio.to_thread(_run)
    return result


@router.get('/info')
async def workspace_info(
    user=Depends(get_verified_user),
):
    """Get workspace information."""
    workspace = _get_workspace_dir()

    return {
        'workspace_dir': str(workspace),
        'max_file_size': MAX_FILE_SIZE,
        'blocked_extensions': list(BLOCKED_EXTENSIONS),
    }
