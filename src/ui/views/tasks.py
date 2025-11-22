"""
Task management view with Kanban board.
"""
import customtkinter as ctk
from typing import Optional, List, Callable
import sys
sys.path.append('..')

from models.task import Task, ChecklistItem
from models.project import Project
from ui.components.common import (
    StatusBadge, IconButton, SearchBar, EmptyState, PriorityIndicator
)
from utils.helpers import truncate_text, format_date
from config import TASK_STATUS, PRIORITY_LEVELS


class TaskCard(ctk.CTkFrame):
    """Task card component for Kanban board."""
    
    def __init__(self, parent, task: Task, project_name: Optional[str], 
                 on_click: Callable, **kwargs):
        super().__init__(parent, corner_radius=8, fg_color=("white", "#2D2D2D"), **kwargs)
        
        self.task = task
        self.on_click = on_click
        
        self._create_ui(project_name)
        
        # Make card clickable
        self.bind("<Button-1>", lambda e: on_click(task))
        for child in self.winfo_children():
            child.bind("<Button-1>", lambda e: on_click(task))
    
    def _create_ui(self, project_name: Optional[str]):
        """Create card UI."""
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=12, pady=10)
        
        # Header row
        header = ctk.CTkFrame(content, fg_color="transparent")
        header.pack(fill="x")
        
        # Priority indicator
        priority_ind = PriorityIndicator(header, self.task.priority)
        priority_ind.pack(side="left", padx=(0, 8))
        
        # Title
        title_label = ctk.CTkLabel(
            header,
            text=truncate_text(self.task.title, 35),
            font=("Segoe UI", 13, "bold"),
            anchor="w"
        )
        title_label.pack(side="left", fill="x", expand=True)
        
        # Project tag if present
        if project_name:
            project_tag = ctk.CTkLabel(
                content,
                text=f"📁 {truncate_text(project_name, 25)}",
                font=("Segoe UI", 11),
                text_color="gray60"
            )
            project_tag.pack(anchor="w", pady=(6, 0))
        
        # Due date if set
        if self.task.due_date:
            due_text = f"📅 {format_date(self.task.due_date, '%b %d')}"
            color = "red" if self.task.is_overdue else "gray60"
            due_label = ctk.CTkLabel(
                content,
                text=due_text,
                font=("Segoe UI", 11),
                text_color=color
            )
            due_label.pack(anchor="w", pady=(4, 0))
        
        # Checklist progress if present
        if self.task.checklist:
            completed, total = self.task.checklist_progress
            checklist_label = ctk.CTkLabel(
                content,
                text=f"☑️ {completed}/{total} items",
                font=("Segoe UI", 11),
                text_color="gray60"
            )
            checklist_label.pack(anchor="w", pady=(4, 0))
        
        # Tags if present
        if self.task.tags:
            tags_frame = ctk.CTkFrame(content, fg_color="transparent")
            tags_frame.pack(fill="x", pady=(6, 0))
            
            for tag in self.task.tags[:3]:  # Show max 3 tags
                tag_label = ctk.CTkLabel(
                    tags_frame,
                    text=f"#{tag}",
                    font=("Segoe UI", 10),
                    text_color=("#E07B53", "#F4A261")
                )
                tag_label.pack(side="left", padx=(0, 6))


class KanbanColumn(ctk.CTkFrame):
    """Kanban column for a specific task status."""
    
    def __init__(self, parent, status: str, title: str, tasks: List[Task],
                 projects: List[Project], on_task_click: Callable, **kwargs):
        super().__init__(parent, corner_radius=12, fg_color=("#F5F5F0", "#3A3A3A"), **kwargs)
        
        self.status = status
        self.tasks = tasks
        self.projects = projects
        self.on_task_click = on_task_click
        
        self._create_ui(title)
    
    def _create_ui(self, title: str):
        """Create column UI."""
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=16, pady=12)
        
        title_label = ctk.CTkLabel(
            header,
            text=title,
            font=("Segoe UI", 14, "bold")
        )
        title_label.pack(side="left")
        
        count_label = ctk.CTkLabel(
            header,
            text=str(len(self.tasks)),
            font=("Segoe UI", 12),
            text_color="gray60"
        )
        count_label.pack(side="right")
        
        # Tasks container - scrollable
        self.tasks_container = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )
        self.tasks_container.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        
        # Render tasks
        self._render_tasks()
    
    def _render_tasks(self):
        """Render task cards."""
        for task in self.tasks:
            # Find project name if task has project_id
            project_name = None
            if task.project_id:
                for project in self.projects:
                    if project.id == task.project_id:
                        project_name = project.name
                        break
            
            card = TaskCard(
                self.tasks_container,
                task=task,
                project_name=project_name,
                on_click=self.on_task_click
            )
            card.pack(fill="x", pady=6)


class TasksView(ctk.CTkFrame):
    """Tasks Kanban board view."""
    
    def __init__(self, parent, storage_manager, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        
        self.storage = storage_manager
        self.tasks: List[Task] = []
        self.projects: List[Project] = []
        self.filtered_tasks: List[Task] = []
        
        self._create_ui()
        self.refresh()
    
    def _create_ui(self):
        """Create view UI."""
        # Header section
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=20)
        
        # Title
        title = ctk.CTkLabel(
            header,
            text="Tasks",
            font=("Segoe UI", 24, "bold")
        )
        title.pack(side="left")
        
        # Create button
        create_btn = IconButton(
            header,
            text="+ New Task",
            command=self._on_create_task,
            fg_color=("#E07B53", "#F4A261"),
            hover_color=("#D06B43", "#E49251"),
            text_color="white",
            font=("Segoe UI", 13, "bold")
        )
        create_btn.pack(side="right")
        
        # Filters
        filters_frame = ctk.CTkFrame(self, fg_color="transparent")
        filters_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Search bar
        self.search_bar = SearchBar(
            filters_frame,
            placeholder="Search tasks...",
            on_change=self._on_search
        )
        self.search_bar.pack(side="left", fill="x", expand=True, padx=(0, 16))
        
        # Filter by priority
        priority_label = ctk.CTkLabel(filters_frame, text="Priority:", font=("Segoe UI", 13))
        priority_label.pack(side="left", padx=(0, 8))
        
        self.priority_filter = ctk.CTkOptionMenu(
            filters_frame,
            values=["All", "High", "Medium", "Low"],
            command=lambda _: self._apply_filters(),
            width=120,
            font=("Segoe UI", 13)
        )
        self.priority_filter.pack(side="left", padx=(0, 16))
        
        # Filter by project
        project_label = ctk.CTkLabel(filters_frame, text="Project:", font=("Segoe UI", 13))
        project_label.pack(side="left", padx=(0, 8))
        
        self.project_filter = ctk.CTkOptionMenu(
            filters_frame,
            values=["All Projects"],
            command=lambda _: self._apply_filters(),
            width=150,
            font=("Segoe UI", 13)
        )
        self.project_filter.pack(side="left")
        
        # Kanban board container
        self.board_container = ctk.CTkFrame(self, fg_color="transparent")
        self.board_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    
    def refresh(self):
        """Refresh tasks and projects from storage."""
        self.tasks = self.storage.get_all_tasks()
        self.projects = self.storage.get_all_projects()
        
        # Update project filter options
        project_names = ["All Projects"] + [p.name for p in self.projects]
        self.project_filter.configure(values=project_names)
        
        self._apply_filters()
        self._render_kanban()
    
    def _apply_filters(self):
        """Apply search and filters to tasks."""
        self.filtered_tasks = self.tasks
        
        # Filter by priority
        priority = self.priority_filter.get().lower()
        if priority != "all":
            self.filtered_tasks = [t for t in self.filtered_tasks if t.priority == priority]
        
        # Filter by project
        if self.project_filter.get() != "All Projects":
            project_name = self.project_filter.get()
            # Find project ID from name
            project_id = None
            for p in self.projects:
                if p.name == project_name:
                    project_id = p.id
                    break
            
            if project_id:
                self.filtered_tasks = [t for t in self.filtered_tasks if t.project_id == project_id]
        
        # Filter by search query
        search_query = self.search_bar.get().lower()
        if search_query:
            self.filtered_tasks = [
                t for t in self.filtered_tasks
                if search_query in t.title.lower() or search_query in t.description.lower()
            ]
    
    def _render_kanban(self):
        """Render Kanban board with columns."""
        # Clear board
        for widget in self.board_container.winfo_children():
            widget.destroy()
        
        # Create columns for each status
        columns_data = [
            ("todo", "To Do"),
            ("in_progress", "In Progress"),
            ("blocked", "Blocked"),
            ("completed", "Completed")
        ]
        
        for status, title in columns_data:
            # Filter tasks by status
            status_tasks = [t for t in self.filtered_tasks if t.status == status]
            
            column = KanbanColumn(
                self.board_container,
                status=status,
                title=title,
                tasks=status_tasks,
                projects=self.projects,
                on_task_click=self._on_task_click
            )
            column.pack(side="left", fill="both", expand=True, padx=8)
    
    def _on_search(self, query: str):
        """Handle search query change."""
        self._apply_filters()
        self._render_kanban()
    
    def _on_create_task(self):
        """Handle create task button."""
        dialog = TaskFormDialog(self, self.storage, self.projects)
        dialog.wait_window()
        self.refresh()
    
    def _on_task_click(self, task: Task):
        """Handle task card click."""
        dialog = TaskFormDialog(self, self.storage, self.projects, task)
        dialog.wait_window()
        self.refresh()


class TaskFormDialog(ctk.CTkToplevel):
    """Task creation/edit form dialog."""
    
    def __init__(self, parent, storage_manager, projects: List[Project], 
                 task: Optional[Task] = None):
        super().__init__(parent)
        
        self.storage = storage_manager
        self.projects = projects
        self.task = task
        
        # Configure window
        self.title("New Task" if not task else "Edit Task")
        self.geometry("600x650")
        self.resizable(True, True)
        self.minsize(550, 600)
        
        # Make modal
        self.transient(parent)
        self.grab_set()
        
        self._create_ui()
        
        if task:
            self._populate_fields()
    
    def _create_ui(self):
        """Create form UI."""
        container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        ctk.CTkLabel(container, text="Task Title *", font=("Segoe UI", 13, "bold")).pack(anchor="w", pady=(0, 4))
        self.title_entry = ctk.CTkEntry(container, font=("Segoe UI", 13), height=40)
        self.title_entry.pack(fill="x", pady=(0, 16))
        
        # Project
        ctk.CTkLabel(container, text="Project", font=("Segoe UI", 13, "bold")).pack(anchor="w", pady=(0, 4))
        project_options = ["No Project"] + [p.name for p in self.projects]
        self.project_menu = ctk.CTkOptionMenu(
            container,
            values=project_options,
            font=("Segoe UI", 13)
        )
        self.project_menu.pack(fill="x", pady=(0, 16))
        
        # Status and Priority row
        row1 = ctk.CTkFrame(container, fg_color="transparent")
        row1.pack(fill="x", pady=(0, 16))
        
        # Status
        status_frame = ctk.CTkFrame(row1, fg_color="transparent")
        status_frame.pack(side="left", fill="x", expand=True, padx=(0, 8))
        ctk.CTkLabel(status_frame, text="Status", font=("Segoe UI", 13, "bold")).pack(anchor="w", pady=(0, 4))
        self.status_menu = ctk.CTkOptionMenu(
            status_frame,
            values=["To Do", "In Progress", "Blocked", "Completed"],
            font=("Segoe UI", 13)
        )
        self.status_menu.pack(fill="x")
        
        # Priority
        priority_frame = ctk.CTkFrame(row1, fg_color="transparent")
        priority_frame.pack(side="left", fill="x", expand=True, padx=(8, 0))
        ctk.CTkLabel(priority_frame, text="Priority", font=("Segoe UI", 13, "bold")).pack(anchor="w", pady=(0, 4))
        self.priority_menu = ctk.CTkOptionMenu(
            priority_frame,
            values=[p.capitalize() for p in PRIORITY_LEVELS],
            font=("Segoe UI", 13)
        )
        self.priority_menu.pack(fill="x")
        
        # Description
        ctk.CTkLabel(container, text="Description", font=("Segoe UI", 13, "bold")).pack(anchor="w", pady=(0, 4))
        self.desc_text = ctk.CTkTextbox(container, font=("Segoe UI", 13), height=100)
        self.desc_text.pack(fill="x", pady=(0, 16))
        
        # Due date
        ctk.CTkLabel(container, text="Due Date (YYYY-MM-DD)", font=("Segoe UI", 13, "bold")).pack(anchor="w", pady=(0, 4))
        self.due_entry = ctk.CTkEntry(container, font=("Segoe UI", 13), height=40)
        self.due_entry.pack(fill="x", pady=(0, 16))
        
        # Tags
        ctk.CTkLabel(container, text="Tags (comma-separated)", font=("Segoe UI", 13, "bold")).pack(anchor="w", pady=(0, 4))
        self.tags_entry = ctk.CTkEntry(container, font=("Segoe UI", 13), height=40)
        self.tags_entry.pack(fill="x", pady=(0, 16))
        
        # Blocked reason (conditional)
        ctk.CTkLabel(container, text="Blocked Reason", font=("Segoe UI", 13, "bold")).pack(anchor="w", pady=(0, 4))
        self.blocked_entry = ctk.CTkEntry(container, font=("Segoe UI", 13), height=40)
        self.blocked_entry.pack(fill="x", pady=(0, 16))
        
        # Buttons
        buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Delete button (only for existing tasks)
        if self.task:
            delete_btn = IconButton(
                buttons_frame,
                text="Delete",
                command=self._on_delete,
                fg_color="red",
                hover_color="darkred",
                text_color="white"
            )
            delete_btn.pack(side="left")
        
        cancel_btn = IconButton(
            buttons_frame,
            text="Cancel",
            command=self.destroy,
            fg_color="gray70",
            hover_color="gray60"
        )
        cancel_btn.pack(side="right", padx=(8, 0))
        
        save_btn = IconButton(
            buttons_frame,
            text="Save Task",
            command=self._on_save,
            fg_color=("#E07B53", "#F4A261"),
            hover_color=("#D06B43", "#E49251"),
            text_color="white",
            font=("Segoe UI", 13, "bold")
        )
        save_btn.pack(side="right")
    
    def _populate_fields(self):
        """Populate form with existing task data."""
        if not self.task:
            return
        
        self.title_entry.insert(0, self.task.title)
        
        # Set project
        if self.task.project_id:
            for project in self.projects:
                if project.id == self.task.project_id:
                    self.project_menu.set(project.name)
                    break
        
        # Map status
        status_map = {
            "todo": "To Do",
            "in_progress": "In Progress",
            "blocked": "Blocked",
            "completed": "Completed"
        }
        self.status_menu.set(status_map.get(self.task.status, "To Do"))
        self.priority_menu.set(self.task.priority.capitalize())
        
        if self.task.description:
            self.desc_text.insert("1.0", self.task.description)
        
        if self.task.due_date:
            self.due_entry.insert(0, self.task.due_date)
        
        if self.task.tags:
            self.tags_entry.insert(0, ", ".join(self.task.tags))
        
        if self.task.blocked_reason:
            self.blocked_entry.insert(0, self.task.blocked_reason)
    
    def _on_save(self):
        """Handle save button."""
        # Validate
        title = self.title_entry.get().strip()
        if not title:
            return
        
        # Get project ID
        project_id = None
        if self.project_menu.get() != "No Project":
            for project in self.projects:
                if project.name == self.project_menu.get():
                    project_id = project.id
                    break
        
        # Map status back
        status_map = {
            "To Do": "todo",
            "In Progress": "in_progress",
            "Blocked": "blocked",
            "Completed": "completed"
        }
        status = status_map.get(self.status_menu.get(), "todo")
        
        # Parse tags
        tags = [t.strip() for t in self.tags_entry.get().split(",") if t.strip()]
        
        if self.task:
            # Update existing
            self.task.update(
                title=title,
                project_id=project_id,
                description=self.desc_text.get("1.0", "end-1c").strip(),
                status=status,
                priority=self.priority_menu.get().lower(),
                due_date=self.due_entry.get().strip() or None,
                tags=tags,
                blocked_reason=self.blocked_entry.get().strip() or None
            )
        else:
            # Create new
            self.task = Task(
                title=title,
                project_id=project_id,
                description=self.desc_text.get("1.0", "end-1c").strip(),
                status=status,
                priority=self.priority_menu.get().lower(),
                due_date=self.due_entry.get().strip() or None,
                tags=tags,
                blocked_reason=self.blocked_entry.get().strip() or None
            )
        
        # Validate
        valid, error = self.task.validate()
        if not valid:
            print(f"Validation error: {error}")
            return
        
        # Save
        self.storage.save_task(self.task)
        self.destroy()
    
    def _on_delete(self):
        """Handle delete button."""
        if self.task:
            self.storage.delete_task(self.task.id)
            self.destroy()
