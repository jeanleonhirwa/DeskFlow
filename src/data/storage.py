"""
JSON storage manager with atomic writes and backup support.
"""
import json
import os
import shutil
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import tempfile

from config import (
    DATA_DIR, BACKUP_DIR, LOGS_DIR,
    PROJECTS_FILE, TASKS_FILE, SETTINGS_FILE,
    DEFAULT_SETTINGS,
    MAX_BACKUPS, BACKUP_FILE_PREFIX
)
from models.project import Project
from models.task import Task
from models.settings import Settings


class StorageManager:
    """Manages JSON file storage with atomic writes and backups."""
    
    def __init__(self):
        """Initialize storage manager and create necessary directories."""
        self._ensure_directories()
        self._ensure_data_files()
    
    def _ensure_directories(self):
        """Create data directories if they don't exist."""
        for directory in [DATA_DIR, BACKUP_DIR, LOGS_DIR]:
            directory.mkdir(parents=True, exist_ok=True)
    
    def _ensure_data_files(self):
        """Create default data files if they don't exist."""
        # Projects file
        if not PROJECTS_FILE.exists():
            self._write_json(PROJECTS_FILE, [])
        
        # Tasks file
        if not TASKS_FILE.exists():
            self._write_json(TASKS_FILE, [])
        
        # Settings file
        if not SETTINGS_FILE.exists():
            self._write_json(SETTINGS_FILE, DEFAULT_SETTINGS)
    
    def _write_json(self, file_path: Path, data: Any):
        """Write JSON data to file atomically using temp file + rename."""
        # Create temporary file in the same directory
        temp_fd, temp_path = tempfile.mkstemp(
            dir=file_path.parent,
            prefix=".tmp_",
            suffix=".json"
        )
        
        try:
            # Write to temp file
            with os.fdopen(temp_fd, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            # Atomic rename
            shutil.move(temp_path, file_path)
        except Exception as e:
            # Clean up temp file on error
            try:
                os.unlink(temp_path)
            except:
                pass
            raise e
    
    def _read_json(self, file_path: Path) -> Any:
        """Read JSON data from file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            # Corrupted file - try to restore from backup
            print(f"Warning: Corrupted file {file_path}. Attempting restore from backup...")
            return self._restore_from_backup(file_path)
        except FileNotFoundError:
            return None
    
    def _create_backup(self, file_path: Path):
        """Create a timestamped backup of a data file."""
        if not file_path.exists():
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{BACKUP_FILE_PREFIX}{file_path.stem}_{timestamp}.json"
        backup_path = BACKUP_DIR / backup_name
        
        shutil.copy2(file_path, backup_path)
        self._cleanup_old_backups(file_path.stem)
    
    def _cleanup_old_backups(self, file_stem: str):
        """Remove old backups, keeping only MAX_BACKUPS most recent."""
        prefix = f"{BACKUP_FILE_PREFIX}{file_stem}_"
        backups = sorted(
            [f for f in BACKUP_DIR.iterdir() if f.name.startswith(prefix)],
            key=lambda x: x.stat().st_mtime,
            reverse=True
        )
        
        # Remove old backups
        for backup in backups[MAX_BACKUPS:]:
            backup.unlink()
    
    def _restore_from_backup(self, file_path: Path) -> Any:
        """Restore data from the most recent backup."""
        prefix = f"{BACKUP_FILE_PREFIX}{file_path.stem}_"
        backups = sorted(
            [f for f in BACKUP_DIR.iterdir() if f.name.startswith(prefix)],
            key=lambda x: x.stat().st_mtime,
            reverse=True
        )
        
        if backups:
            print(f"Restoring from backup: {backups[0].name}")
            shutil.copy2(backups[0], file_path)
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # No backups available, return default
        print("No backups available. Returning empty data.")
        return [] if file_path != SETTINGS_FILE else DEFAULT_SETTINGS
    
    # Project CRUD Operations
    
    def get_all_projects(self) -> List[Project]:
        """Get all projects."""
        data = self._read_json(PROJECTS_FILE)
        return [Project.from_dict(p) for p in data]
    
    def get_project(self, project_id: str) -> Optional[Project]:
        """Get a specific project by ID."""
        projects = self.get_all_projects()
        for project in projects:
            if project.id == project_id:
                return project
        return None
    
    def save_project(self, project: Project):
        """Save a project (create or update)."""
        self._create_backup(PROJECTS_FILE)
        projects = self.get_all_projects()
        
        # Update existing or add new
        updated = False
        for i, p in enumerate(projects):
            if p.id == project.id:
                projects[i] = project
                updated = True
                break
        
        if not updated:
            projects.append(project)
        
        # Save to file
        data = [p.to_dict() for p in projects]
        self._write_json(PROJECTS_FILE, data)
    
    def delete_project(self, project_id: str):
        """Delete a project."""
        self._create_backup(PROJECTS_FILE)
        projects = self.get_all_projects()
        projects = [p for p in projects if p.id != project_id]
        
        data = [p.to_dict() for p in projects]
        self._write_json(PROJECTS_FILE, data)
    
    # Task CRUD Operations
    
    def get_all_tasks(self) -> List[Task]:
        """Get all tasks."""
        data = self._read_json(TASKS_FILE)
        return [Task.from_dict(t) for t in data]
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a specific task by ID."""
        tasks = self.get_all_tasks()
        for task in tasks:
            if task.id == task_id:
                return task
        return None
    
    def get_tasks_by_project(self, project_id: str) -> List[Task]:
        """Get all tasks for a specific project."""
        tasks = self.get_all_tasks()
        return [t for t in tasks if t.project_id == project_id]
    
    def save_task(self, task: Task):
        """Save a task (create or update)."""
        self._create_backup(TASKS_FILE)
        tasks = self.get_all_tasks()
        
        # Update existing or add new
        updated = False
        for i, t in enumerate(tasks):
            if t.id == task.id:
                tasks[i] = task
                updated = True
                break
        
        if not updated:
            tasks.append(task)
        
        # Save to file
        data = [t.to_dict() for t in tasks]
        self._write_json(TASKS_FILE, data)
    
    def delete_task(self, task_id: str):
        """Delete a task."""
        self._create_backup(TASKS_FILE)
        tasks = self.get_all_tasks()
        tasks = [t for t in tasks if t.id != task_id]
        
        data = [t.to_dict() for t in tasks]
        self._write_json(TASKS_FILE, data)
    
    # Settings Operations
    
    def get_settings(self) -> Settings:
        """Get application settings."""
        data = self._read_json(SETTINGS_FILE)
        return Settings.from_dict(data)
    
    def save_settings(self, settings: Settings):
        """Save application settings."""
        self._write_json(SETTINGS_FILE, settings.to_dict())
