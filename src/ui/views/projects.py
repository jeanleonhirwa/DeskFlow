"""
Project management view with dashboard, creation, and detail views.
"""
import customtkinter as ctk
from typing import Optional, List, Callable
import sys
sys.path.append('..')

from models.project import Project, Milestone
from ui.components.common import (
    StatusBadge, ProgressBar, IconButton, SearchBar, EmptyState, PriorityIndicator
)
from utils.helpers import truncate_text, time_ago
from config import PROJECT_STATUS, PRIORITY_LEVELS, PROJECT_COLORS


class ProjectCard(ctk.CTkFrame):
    """Modern project card component matching mockup design."""
    
    def __init__(self, parent, project: Project, on_click: Callable, **kwargs):
        super().__init__(
            parent,
            corner_radius=16,
            fg_color=("white", "#1E1E1E"),
            border_width=1,
            border_color=("#E0E0E0", "#3C4043"),
            **kwargs
        )
        
        self.project = project
        self.on_click = on_click
        self.default_fg = ("white", "#1E1E1E")
        self.hover_fg = ("#F8F9FA", "#2A2A2A")
        
        self._create_ui()
        
        # Make card clickable with hover effect
        self.bind("<Button-1>", lambda e: on_click(project))
        self.bind("<Enter>", self._on_hover)
        self.bind("<Leave>", self._on_leave)
        self.configure(cursor="hand2")
    
    def _create_ui(self):
        """Create modern card UI."""
        # Thick color indicator bar (left side, 6px)
        color_bar = ctk.CTkFrame(
            self,
            width=6,
            fg_color=self.project.color,
            corner_radius=0
        )
        color_bar.pack(side="left", fill="y")
        
        # Main content area with generous padding
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(side="left", fill="both", expand=True, padx=24, pady=20)
        
        # === HEADER ROW ===
        header = ctk.CTkFrame(content, fg_color="transparent")
        header.pack(fill="x", pady=(0, 12))
        
        # Project name (larger, bolder)
        name_label = ctk.CTkLabel(
            header,
            text=truncate_text(self.project.name, 35),
            font=("Segoe UI", 18, "bold"),
            anchor="w"
        )
        name_label.pack(side="left", fill="x", expand=True)
        
        # Status badge (modern pill-style)
        from ui.components.modern_components import TagChip
        from config import STATUS_GRADIENTS
        
        status_colors = {
            "planning": "#4A90E2",
            "active": "#27AE60",
            "paused": "#F5A623",
            "completed": "#81C995",
            "archived": "#9B59B6"
        }
        status_badge = TagChip(
            header,
            text=self.project.status.upper(),
            color=status_colors.get(self.project.status, "#999999")
        )
        status_badge.pack(side="right", padx=(8, 0))
        
        # Priority indicator (color dot)
        priority_colors = {"high": "#E74C3C", "medium": "#F5A623", "low": "#95a5a6"}
        priority_dot = ctk.CTkFrame(
            header,
            width=10,
            height=10,
           corner_radius=5,
            fg_color=priority_colors.get(self.project.priority, "#999999")
        )
        priority_dot.pack(side="right", padx=(0, 8))
        
        # === DESCRIPTION ===
        if self.project.description:
            desc_label = ctk.CTkLabel(
                content,
                text=truncate_text(self.project.description, 100),
                font=("Segoe UI", 13),
                text_color=("#5F6368", "#9AA0A6"),
                anchor="w",
                justify="left",
                wraplength=350
            )
            desc_label.pack(fill="x", pady=(0, 16))
        
        # === PROGRESS BAR (Gradient) ===
        progress_frame = ctk.CTkFrame(content, fg_color="transparent")
        progress_frame.pack(fill="x", pady=(0, 16))
        
        from ui.components.modern_components import GradientProgress
        from config import STATUS_GRADIENTS
        
        gradient = STATUS_GRADIENTS.get(self.project.status, ["#4A90E2", "#357ABD"])
        progress_bar = GradientProgress(
            progress_frame,
            progress=self.project.progress_percentage,
            gradient_colors=gradient,
            height=10
        )
        progress_bar.pack(fill="x", side="left", expand=True)
        
        # Progress percentage label
        progress_label = ctk.CTkLabel(
            progress_frame,
            text=f"{int(self.project.progress_percentage)}%",
            font=("Segoe UI", 13, "bold"),
            text_color=self.project.color,
            width=50
        )
        progress_label.pack(side="right", padx=(12, 0))
        
        # === META INFO ROW (Icons + Text) ===
        meta_row = ctk.CTkFrame(content, fg_color="transparent")
        meta_row.pack(fill="x")
        
        # Last updated
        updated_icon = ctk.CTkLabel(
            meta_row,
            text="🕐",
            font=("Segoe UI", 14)
        )
        updated_icon.pack(side="left")
        
        updated_label = ctk.CTkLabel(
            meta_row,
            text=time_ago(self.project.updated_at),
            font=("Segoe UI", 12),
            text_color=("#80868B", "#70757A")
        )
        updated_label.pack(side="left", padx=(4, 16))
        
        # Tech stack count (if available)
        if self.project.tech_stack:
            tech_icon = ctk.CTkLabel(
                meta_row,
                text="⚙️",
                font=("Segoe UI", 14)
            )
            tech_icon.pack(side="left")
            
            tech_label = ctk.CTkLabel(
                meta_row,
                text=f"{len(self.project.tech_stack)} tech",
                font=("Segoe UI", 12),
                text_color=("#80868B", "#70757A")
            )
            tech_label.pack(side="left", padx=(4, 16))
        
        # Milestones count
        if self.project.milestones:
            milestone_icon = ctk.CTkLabel(
                meta_row,
                text="🎯",
                font=("Segoe UI", 14)
            )
            milestone_icon.pack(side="left")
            
            completed_milestones = sum(1 for m in self.project.milestones if m.completed)
            milestone_label = ctk.CTkLabel(
                meta_row,
                text=f"{completed_milestones}/{len(self.project.milestones)} milestones",
                font=("Segoe UI", 12),
                text_color=("#80868B", "#70757A")
            )
            milestone_label.pack(side="left", padx=(4, 0))
    
    def _on_hover(self, event):
        """Handle hover effect."""
        self.configure(fg_color=self.hover_fg)
    
    def _on_leave(self, event):
        """Handle leave effect."""
        self.configure(fg_color=self.default_fg)


class ProjectsView(ctk.CTkScrollableFrame):
    """Projects dashboard view."""
    
    def __init__(self, parent, storage_manager, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        
        self.storage = storage_manager
        self.projects: List[Project] = []
        self.filtered_projects: List[Project] = []
        self.current_filter = "all"
        self.search_query = ""
        
        self._create_ui()
        self.refresh()
    
    def _create_ui(self):
        """Create view UI."""
        # Header section with better spacing
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=32, pady=(32, 16))
        
        # Title (larger, bolder)
        title = ctk.CTkLabel(
            header,
            text="Projects",
            font=("Segoe UI", 28, "bold")
        )
        title.pack(side="left")
        
        # Create button (modern styling)
        create_btn = IconButton(
            header,
            text="+ New Project",
            command=self._on_create_project,
            fg_color=("#D93025", "#8AB4F8"),
            hover_color=("#C5221F", "#AECBFA"),
            text_color="white",
            font=("Segoe UI", 14, "bold"),
            height=44,
            corner_radius=12
        )
        create_btn.pack(side="right")
        
        # Filters and search with better spacing
        filters_frame = ctk.CTkFrame(self, fg_color="transparent")
        filters_frame.pack(fill="x", padx=32, pady=(0, 24))
        
        # Search bar
        self.search_bar = SearchBar(
            filters_frame,
            placeholder="Search projects...",
            on_change=self._on_search
        )
        self.search_bar.pack(side="left", fill="x", expand=True, padx=(0, 16))
        
        # Filter dropdown
        filter_label = ctk.CTkLabel(filters_frame, text="Filter:", font=("Segoe UI", 13))
        filter_label.pack(side="left", padx=(0, 12))
        
        self.filter_menu = ctk.CTkOptionMenu(
            filters_frame,
            values=["All", "Active", "Planning", "Paused", "Completed", "Archived"],
            command=self._on_filter_change,
            width=150,
            font=("Segoe UI", 13),
            corner_radius=10
        )
        self.filter_menu.pack(side="left")
        
        # Projects grid container
        self.projects_container = ctk.CTkFrame(self, fg_color="transparent")
        self.projects_container.pack(fill="both", expand=True, padx=32, pady=(0, 24))
    
    def refresh(self):
        """Refresh projects list from storage."""
        self.projects = self.storage.get_all_projects()
        self._apply_filters()
        self._render_projects()
    
    def _apply_filters(self):
        """Apply search and filter to projects."""
        self.filtered_projects = self.projects
        
        # Apply status filter
        if self.current_filter != "all":
            self.filtered_projects = [
                p for p in self.filtered_projects 
                if p.status == self.current_filter
            ]
        
        # Apply search
        if self.search_query:
            query = self.search_query.lower()
            self.filtered_projects = [
                p for p in self.filtered_projects
                if query in p.name.lower() or query in p.description.lower()
            ]
    
    def _render_projects(self):
        """Render projects grid."""
        # Clear container
        for widget in self.projects_container.winfo_children():
            widget.destroy()
        
        if not self.filtered_projects:
            # Show empty state
            empty = EmptyState(
                self.projects_container,
                message="No projects found",
                action_text="Create Project" if not self.search_query else None,
                action_command=self._on_create_project if not self.search_query else None
            )
            empty.pack(fill="both", expand=True)
            return
        
        # Render project cards with better spacing
        for i, project in enumerate(self.filtered_projects):
            # Inject storage reference for progress calculation
            project._storage = self.storage
            
            card = ProjectCard(
                self.projects_container,
                project=project,
                on_click=self._on_project_click
            )
            card.pack(fill="x", pady=12)
    
    def _on_search(self, query: str):
        """Handle search query change."""
        self.search_query = query
        self._apply_filters()
        self._render_projects()
    
    def _on_filter_change(self, value: str):
        """Handle filter change."""
        self.current_filter = value.lower()
        self._apply_filters()
        self._render_projects()
    
    def _on_create_project(self):
        """Handle create project button."""
        dialog = ProjectFormDialog(self, self.storage)
        dialog.wait_window()
        self.refresh()
    
    def _on_project_click(self, project: Project):
        """Handle project card click."""
        print(f"Project clicked: {project.name}")
        # TODO: Show project detail view


class ProjectFormDialog(ctk.CTkToplevel):
    """Project creation/edit form dialog."""
    
    def __init__(self, parent, storage_manager, project: Optional[Project] = None):
        super().__init__(parent)
        
        self.storage = storage_manager
        self.project = project
        self.result = None
        
        # Configure window
        self.title("New Project" if not project else "Edit Project")
        self.geometry("600x700")
        self.resizable(False, False)
        
        # Make modal
        self.transient(parent)
        self.grab_set()
        
        self._create_ui()
        
        # Populate if editing
        if project:
            self._populate_fields()
    
    def _create_ui(self):
        """Create form UI."""
        # Main container
        container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Name
        ctk.CTkLabel(container, text="Project Name *", font=("Segoe UI", 13, "bold")).pack(anchor="w", pady=(0, 4))
        self.name_entry = ctk.CTkEntry(container, font=("Segoe UI", 13), height=40)
        self.name_entry.pack(fill="x", pady=(0, 16))
        
        # Description
        ctk.CTkLabel(container, text="Description", font=("Segoe UI", 13, "bold")).pack(anchor="w", pady=(0, 4))
        self.desc_text = ctk.CTkTextbox(container, font=("Segoe UI", 13), height=100)
        self.desc_text.pack(fill="x", pady=(0, 16))
        
        # Status and Priority row
        row1 = ctk.CTkFrame(container, fg_color="transparent")
        row1.pack(fill="x", pady=(0, 16))
        
        # Status
        status_frame = ctk.CTkFrame(row1, fg_color="transparent")
        status_frame.pack(side="left", fill="x", expand=True, padx=(0, 8))
        ctk.CTkLabel(status_frame, text="Status", font=("Segoe UI", 13, "bold")).pack(anchor="w", pady=(0, 4))
        self.status_menu = ctk.CTkOptionMenu(
            status_frame,
            values=[s.capitalize() for s in PROJECT_STATUS],
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
        
        # Color picker
        ctk.CTkLabel(container, text="Project Color", font=("Segoe UI", 13, "bold")).pack(anchor="w", pady=(0, 4))
        colors_frame = ctk.CTkFrame(container, fg_color="transparent")
        colors_frame.pack(fill="x", pady=(0, 16))
        
        self.selected_color = PROJECT_COLORS[0]
        self.color_buttons = []
        for color in PROJECT_COLORS:
            btn = ctk.CTkButton(
                colors_frame,
                text="",
                width=30,
                height=30,
                corner_radius=15,
                fg_color=color,
                hover_color=color,
                command=lambda c=color: self._select_color(c)
            )
            btn.pack(side="left", padx=4)
            self.color_buttons.append((btn, color))
        
        # Repository URL
        ctk.CTkLabel(container, text="Repository URL", font=("Segoe UI", 13, "bold")).pack(anchor="w", pady=(0, 4))
        self.repo_entry = ctk.CTkEntry(container, font=("Segoe UI", 13), height=40)
        self.repo_entry.pack(fill="x", pady=(0, 16))
        
        # Tech stack
        ctk.CTkLabel(container, text="Tech Stack (comma-separated)", font=("Segoe UI", 13, "bold")).pack(anchor="w", pady=(0, 4))
        self.tech_entry = ctk.CTkEntry(container, font=("Segoe UI", 13), height=40)
        self.tech_entry.pack(fill="x", pady=(0, 16))
        
        # Notes
        ctk.CTkLabel(container, text="Notes", font=("Segoe UI", 13, "bold")).pack(anchor="w", pady=(0, 4))
        self.notes_text = ctk.CTkTextbox(container, font=("Segoe UI", 13), height=100)
        self.notes_text.pack(fill="x", pady=(0, 16))
        
        # Buttons
        buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=(0, 20))
        
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
            text="Save Project",
            command=self._on_save,
            fg_color=("#E07B53", "#F4A261"),
            hover_color=("#D06B43", "#E49251"),
            text_color="white",
            font=("Segoe UI", 13, "bold")
        )
        save_btn.pack(side="right")
    
    def _select_color(self, color: str):
        """Select project color."""
        self.selected_color = color
        # Visual feedback could be added here
    
    def _populate_fields(self):
        """Populate form with existing project data."""
        if not self.project:
            return
        
        self.name_entry.insert(0, self.project.name)
        self.desc_text.insert("1.0", self.project.description)
        self.status_menu.set(self.project.status.capitalize())
        self.priority_menu.set(self.project.priority.capitalize())
        self.selected_color = self.project.color
        
        if self.project.repository_url:
            self.repo_entry.insert(0, self.project.repository_url)
        
        if self.project.tech_stack:
            self.tech_entry.insert(0, ", ".join(self.project.tech_stack))
        
        if self.project.notes:
            self.notes_text.insert("1.0", self.project.notes)
    
    def _on_save(self):
        """Handle save button."""
        # Validate
        name = self.name_entry.get().strip()
        if not name:
            # TODO: Show error message
            return
        
        # Create or update project
        if self.project:
            # Update existing
            self.project.update(
                name=name,
                description=self.desc_text.get("1.0", "end-1c").strip(),
                status=self.status_menu.get().lower(),
                priority=self.priority_menu.get().lower(),
                color=self.selected_color,
                repository_url=self.repo_entry.get().strip() or None,
                tech_stack=[t.strip() for t in self.tech_entry.get().split(",") if t.strip()],
                notes=self.notes_text.get("1.0", "end-1c").strip()
            )
        else:
            # Create new
            self.project = Project(
                name=name,
                description=self.desc_text.get("1.0", "end-1c").strip(),
                status=self.status_menu.get().lower(),
                priority=self.priority_menu.get().lower(),
                color=self.selected_color,
                repository_url=self.repo_entry.get().strip() or None,
                tech_stack=[t.strip() for t in self.tech_entry.get().split(",") if t.strip()],
                notes=self.notes_text.get("1.0", "end-1c").strip()
            )
        
        # Validate
        valid, error = self.project.validate()
        if not valid:
            # TODO: Show error message
            print(f"Validation error: {error}")
            return
        
        # Save to storage
        self.storage.save_project(self.project)
        self.result = self.project
        self.destroy()
