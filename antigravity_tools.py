"""
title: Antigravity Auto-Coding Engine
description: Allows the LLM to read, write, list, and create files directly within the local workspace (E:/AntiGravityProject).
author: Antigravity Architect
version: 1.0.0
"""
import os
import json
from pydantic import BaseModel, Field

class Tools:
    class Valves(BaseModel):
        workspace_path: str = Field(
            default=os.environ.get("WORKSPACE_DIR", "/workspace"),
            description="Path to the primary workspace directory inside the container (e.g., /workspace or E:/AntiGravityProject)."
        )
        rag_path: str = Field(
            default="/file_rag",
            description="Path to the RAG vault directory inside the container (e.g., /file_rag or E:/file_rag)."
        )

    def __init__(self, valves=None):
        self.valves = valves if valves else self.Valves()

    def list_files(self, path: str = ".") -> str:
        """
        Lists files and directories in a specific path within the workspace.
        
        :param path: The relative directory path to list (default is root '.').
        :return: JSON string array of file and directory names.
        """
        try:
            # Normalize path for Linux container (replace backslashes with forward slashes)
            path = path.replace("\\", "/")
            
            # Ambil konfigurasi path dari Valves
            workspace_dir = self.valves.workspace_path.replace("\\", "/")
            rag_dir = self.valves.rag_path.replace("\\", "/")
            
            # Check if path specifically asks for file_rag
            if "E:/file_rag" in path or "/file_rag" in path:
                base_dir = rag_dir
                relative_path = path.replace("E:/file_rag", "").replace("/file_rag", "").strip("/")
            elif "E:/AntiGravityProject" in path:
                base_dir = workspace_dir
                relative_path = path.replace("E:/AntiGravityProject", "").strip("/")
            else:
                base_dir = workspace_dir
                relative_path = path.strip("/")
                
            full_path = os.path.join(base_dir, relative_path)
            
            # Security check to prevent path traversal
            if not os.path.abspath(full_path).startswith(os.path.abspath(base_dir)):
                return f"Error: Access denied. Path must be within {base_dir}."
            
            items = os.listdir(full_path)
            return json.dumps(items)
        except Exception as e:
            return f"Error: {e}"

    def read_file(self, file_path: str) -> str:
        """
        Reads the content of a file from the workspace.
        
        :param file_path: The relative path to the file.
        :return: The string content of the file.
        """
        try:
            # Normalize path for Linux container
            file_path = file_path.replace("\\", "/")
            
            # Ambil konfigurasi path dari Valves
            workspace_dir = self.valves.workspace_path.replace("\\", "/")
            rag_dir = self.valves.rag_path.replace("\\", "/")
            
            # Check if path specifically asks for file_rag
            if "E:/file_rag" in file_path or "/file_rag" in file_path:
                base_dir = rag_dir
                relative_path = file_path.replace("E:/file_rag", "").replace("/file_rag", "").strip("/")
            elif "E:/AntiGravityProject" in file_path:
                base_dir = workspace_dir
                relative_path = file_path.replace("E:/AntiGravityProject", "").strip("/")
            else:
                base_dir = workspace_dir
                relative_path = file_path.strip("/")
                
            full_path = os.path.join(base_dir, relative_path)
            
            if not os.path.abspath(full_path).startswith(os.path.abspath(base_dir)):
                return f"Error: Access denied. Path must be within {base_dir}."
                
            if not os.path.exists(full_path):
                return f"Error: File '{file_path}' not found."
                
            with open(full_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"Error: {e}"

    def write_file(self, file_path: str, content: str) -> str:
        """
        Writes content to a file in the workspace. Creates parent directories if they don't exist.
        
        :param file_path: The relative path to the new or existing file.
        :param content: The exact source code or text to write into the file.
        :return: A success message or an error string.
        """
        try:
            # Normalize path for Linux container
            file_path = file_path.replace("\\", "/")
            
            # Ambil konfigurasi path dari Valves
            workspace_dir = self.valves.workspace_path.replace("\\", "/")
            rag_dir = self.valves.rag_path.replace("\\", "/")
            
            # Check if path specifically asks for file_rag
            if "E:/file_rag" in file_path or "/file_rag" in file_path:
                base_dir = rag_dir
                relative_path = file_path.replace("E:/file_rag", "").replace("/file_rag", "").strip("/")
            elif "E:/AntiGravityProject" in file_path:
                base_dir = workspace_dir
                relative_path = file_path.replace("E:/AntiGravityProject", "").strip("/")
            else:
                base_dir = workspace_dir
                relative_path = file_path.strip("/")
                
            full_path = os.path.join(base_dir, relative_path)
            
            if not os.path.abspath(full_path).startswith(os.path.abspath(base_dir)):
                return f"Error: Access denied. Path must be within {base_dir}."
                
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
                
            return f"Success: File '{file_path}' has been written/updated successfully."
        except Exception as e:
            return f"Error: {e}"
