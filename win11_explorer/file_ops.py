"""
File system operations and helpers for Win11 Explorer.
Handles clipboard cut/copy/paste, trash, launches, file info, and drive metrics.
"""

import os
import shutil
import subprocess
import mimetypes
from datetime import datetime
from pathlib import Path
from typing import List, Tuple, Optional
import send2trash

class ClipboardMode:
    NONE = 0
    COPY = 1
    CUT = 2

class ExplorerClipboard:
    """Singleton clipboard for file operations."""
    paths: List[str] = []
    mode: int = ClipboardMode.NONE

    @classmethod
    def set_copy(cls, paths: List[str]):
        cls.paths = [os.path.abspath(p) for p in paths]
        cls.mode = ClipboardMode.COPY

    @classmethod
    def set_cut(cls, paths: List[str]):
        cls.paths = [os.path.abspath(p) for p in paths]
        cls.mode = ClipboardMode.CUT

    @classmethod
    def clear(cls):
        cls.paths = []
        cls.mode = ClipboardMode.NONE

    @classmethod
    def has_files(cls) -> bool:
        return bool(cls.paths and cls.mode != ClipboardMode.NONE)


def format_size(bytes_size: int) -> str:
    """Format bytes into readable Windows-style units (KB, MB, GB)."""
    if bytes_size < 1024:
        return f"{bytes_size} B"
    elif bytes_size < 1024 * 1024:
        return f"{bytes_size / 1024:.1f} KB"
    elif bytes_size < 1024 * 1024 * 1024:
        return f"{bytes_size / (1024 * 1024):.1f} MB"
    else:
        return f"{bytes_size / (1024 * 1024 * 1024):.1f} GB"


def format_datetime(timestamp: float) -> str:
    """Format a timestamp in Windows Explorer format (dd.mm.yyyy hh:mm)."""
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime("%d.%m.%Y  %H:%M")


def get_file_type_description(path: str, is_dir: bool) -> str:
    """Get a user-friendly type name like 'File folder', 'Python File', etc."""
    if is_dir:
        return "File folder"
    
    ext = os.path.splitext(path)[1].lower()
    type_map = {
        ".txt": "Text Document",
        ".py": "Python Source File",
        ".js": "JavaScript File",
        ".ts": "TypeScript File",
        ".html": "HTML Document",
        ".css": "CSS Stylesheet",
        ".json": "JSON File",
        ".xml": "XML File",
        ".md": "Markdown Document",
        ".pdf": "PDF Document",
        ".png": "PNG Image",
        ".jpg": "JPEG Image",
        ".jpeg": "JPEG Image",
        ".gif": "GIF Image",
        ".svg": "SVG Document",
        ".mp3": "MP3 Audio",
        ".wav": "WAV Audio",
        ".flac": "FLAC Audio",
        ".mp4": "MP4 Video",
        ".mkv": "MKV Video",
        ".avi": "AVI Video",
        ".zip": "Compressed (zipped) Folder",
        ".tar": "TAR Archive",
        ".gz": "GZ Archive",
        ".xz": "XZ Archive",
        ".sh": "Shell Script",
        ".rs": "Rust Source File",
        ".c": "C Source File",
        ".cpp": "C++ Source File",
        ".h": "Header File",
    }
    if ext in type_map:
        return type_map[ext]
    if ext:
        return f"{ext[1:].upper()} File"
    return "File"


def get_file_icon_name(path: str, is_dir: bool) -> str:
    """Return the SVG icon name for a given file or folder."""
    if is_dir:
        # Check special folder names
        norm = os.path.normpath(path)
        user_home = os.path.expanduser("~")
        if norm == user_home:
            return "folder-home"
        elif norm == os.path.join(user_home, "Desktop"):
            return "folder-desktop"
        elif norm == os.path.join(user_home, "Downloads"):
            return "folder-downloads"
        elif norm == os.path.join(user_home, "Documents"):
            return "folder-documents"
        elif norm == os.path.join(user_home, "Pictures"):
            return "folder-pictures"
        elif norm == os.path.join(user_home, "Music"):
            return "folder-music"
        elif norm == os.path.join(user_home, "Videos"):
            return "folder-videos"
        return "folder"

    ext = os.path.splitext(path)[1].lower()
    if ext in [".py", ".rs", ".c", ".cpp", ".h", ".js", ".ts", ".html", ".css", ".json", ".sh"]:
        return "file-code"
    elif ext in [".txt", ".md", ".log", ".ini", ".cfg", ".yaml", ".yml", ".toml"]:
        return "file-text"
    elif ext in [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".svg", ".webp", ".ico"]:
        return "file-image"
    elif ext in [".mp3", ".wav", ".flac", ".ogg", ".m4a", ".aac"]:
        return "file-audio"
    elif ext in [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".webm"]:
        return "file-video"
    elif ext in [".zip", ".tar", ".gz", ".xz", ".bz2", ".7z", ".rar"]:
        return "file-archive"
    elif ext == ".pdf":
        return "file-pdf"
    return "file"


def open_with_default(path: str):
    """Launch file with system default handler (xdg-open)."""
    try:
        subprocess.Popen(["xdg-open", path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"Error opening {path}: {e}")


def open_terminal(directory: str):
    """Open a terminal emulator at the given directory."""
    dir_path = os.path.abspath(directory)
    terminals = [
        ["konsole", "--workdir", dir_path],
        ["alacritty", "--working-directory", dir_path],
        ["kitty", "--directory", dir_path],
        ["xterm", "-e", f"cd '{dir_path}' && $SHELL"],
    ]
    for term_cmd in terminals:
        binary = shutil.which(term_cmd[0])
        if binary:
            try:
                subprocess.Popen(term_cmd)
                return
            except Exception:
                continue
    # Fallback
    try:
        subprocess.Popen(["sh", "-c", f"cd '{dir_path}' && x-terminal-emulator"])
    except Exception:
        pass


def delete_to_trash(paths: List[str]) -> Tuple[int, List[str]]:
    """Move files or directories to system trash. Returns (success_count, errors)."""
    success = 0
    errors = []
    for p in paths:
        try:
            send2trash.send2trash(p)
            success += 1
        except Exception as e:
            errors.append(f"{p}: {e}")
    return success, errors


def create_new_folder(target_dir: str) -> str:
    """Create a new folder named 'New folder' or 'New folder (N)'."""
    base_name = "New folder"
    new_path = os.path.join(target_dir, base_name)
    counter = 2
    while os.path.exists(new_path):
        new_path = os.path.join(target_dir, f"{base_name} ({counter})")
        counter += 1
    os.makedirs(new_path)
    return new_path


def create_new_file(target_dir: str) -> str:
    """Create a new text file named 'New Text Document.txt'."""
    base_name = "New Text Document.txt"
    new_path = os.path.join(target_dir, base_name)
    counter = 2
    while os.path.exists(new_path):
        new_path = os.path.join(target_dir, f"New Text Document ({counter}).txt")
        counter += 1
    with open(new_path, "w", encoding="utf-8") as f:
        f.write("")
    return new_path


def paste_files(dest_dir: str) -> Tuple[int, List[str]]:
    """Paste clipboard files into target destination. Handles both Copy and Cut."""
    if not ExplorerClipboard.has_files():
        return 0, []

    success = 0
    errors = []
    is_cut = (ExplorerClipboard.mode == ClipboardMode.CUT)

    for src in ExplorerClipboard.paths:
        if not os.path.exists(src):
            errors.append(f"Source not found: {src}")
            continue

        base_name = os.path.basename(src)
        dest = os.path.join(dest_dir, base_name)

        # Handle name conflict
        if os.path.exists(dest) and not (is_cut and os.path.abspath(src) == os.path.abspath(dest)):
            root, ext = os.path.splitext(base_name)
            counter = 2
            while os.path.exists(dest):
                dest = os.path.join(dest_dir, f"{root} - Copy ({counter}){ext}")
                counter += 1

        try:
            if is_cut:
                shutil.move(src, dest)
            else:
                if os.path.isdir(src):
                    shutil.copytree(src, dest)
                else:
                    shutil.copy2(src, dest)
            success += 1
        except Exception as e:
            errors.append(f"Failed to transfer {src}: {e}")

    if is_cut:
        ExplorerClipboard.clear()

    return success, errors


def get_drive_info() -> List[dict]:
    """Retrieve mounted partitions / drives info for This PC view."""
    drives = []
    # Check root /
    try:
        usage = shutil.disk_usage("/")
        drives.append({
            "name": "Local Disk (C: Linux Root)",
            "path": "/",
            "total": usage.total,
            "used": usage.used,
            "free": usage.free,
            "percent": int((usage.used / usage.total) * 100) if usage.total > 0 else 0
        })
    except Exception:
        pass

    # Check /home if separate
    try:
        home_path = os.path.expanduser("~")
        if os.path.exists("/home"):
            stat_root = os.stat("/")
            stat_home = os.stat("/home")
            if stat_root.st_dev != stat_home.st_dev:
                usage = shutil.disk_usage("/home")
                drives.append({
                    "name": "Local Disk (D: Home)",
                    "path": "/home",
                    "total": usage.total,
                    "used": usage.used,
                    "free": usage.free,
                    "percent": int((usage.used / usage.total) * 100) if usage.total > 0 else 0
                })
    except Exception:
        pass

    # Removable media in /run/media/$USER or /media
    user = os.environ.get("USER", "apex")
    media_paths = [f"/run/media/{user}", "/media"]
    for m in media_paths:
        if os.path.isdir(m):
            try:
                for entry in os.listdir(m):
                    full = os.path.join(m, entry)
                    if os.path.ismount(full):
                        usage = shutil.disk_usage(full)
                        drives.append({
                            "name": f"Removable Disk ({entry})",
                            "path": full,
                            "total": usage.total,
                            "used": usage.used,
                            "free": usage.free,
                            "percent": int((usage.used / usage.total) * 100) if usage.total > 0 else 0
                        })
            except Exception:
                pass

    return drives
