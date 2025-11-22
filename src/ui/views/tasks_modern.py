"""
Modern Task Card and Kanban Column components.
This file contains the redesigned components for the Tasks Kanban view.
"""
import customtkinter as ctk
from typing import Optional, List, Callable
from models.task import Task
from models.project import Project
from utils.helpers import truncate_text, format_date


class ModernTaskCard(ctk.CTkFrame):
    """Modern task card component matching mockup design."""
    
    def __init__(self, parent, task: Task, project_name: Optional[str], on_click: Callable, **kwargs):
        # Priority color for left border
        priority_colors = {"high": "#E74C3C", "medium": "#F5A623", "low": "#95a5a6"}
        border_color = priority_colors.get(task.priority, "#E0E0E0")
        
        super().__init__(
            parent,
            corner_radius=12,
            fg_color=("white", "#1E1E1E"),
            border_width=0,
            **kwargs
        )
        
        self.task = task
        self.on_click = on_click
        self.default_fg = ("white", "#1E1E1E")
        self.hover_fg = ("#F8F9FA", "#2A2A2A")
        
        # Priority indicator bar (left side)
        self.priority_bar = ctk.CTkFrame(
            self,
            width=4,
            fg_color=border_color,
            corner_radius=0
        )
        self.priority_bar.pack(side="left", fill="y")
        
        self._create_ui(project_name)
        
        # Make card clickable with hover effect
        self.bind("<Button-1>", lambda e: on_click(task))
        self.bind("<Enter>", self._on_hover)
        self.bind("<Leave>", self._on_leave)
        self.configure(cursor="hand2")
        
        # Bind children
        for child in self.winfo_children():
            child.bind("<Button-1>", lambda e: on_click(task))
    
    def _create_ui(self, project_name: Optional[str]):
        """Create modern card UI."""
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=16, pady=14)
        
        # === TITLE ===
        title_label = ctk.CTkLabel(
            content,
            text=truncate_text(self.task.title, 40),
            font=("Segoe UI", 14, "bold"),
            anchor="w",
            justify="left"
        )
        title_label.pack(fill="x", pady=(0, 8))
        
        # === PROJECT BADGE ===
        if project_name:
            from ui.components.modern_components import TagChip
            project_badge = TagChip(
                content,
                text=project_name[:15],
                color=("#E8EAED", "#353535"),
                text_color=("#5F6368", "#9AA0A6")
            )
            project_badge.pack(anchor="w", pady=(0, 8))
        
        # === META INFO ROW ===
        if self.task.due_date or self.task.checklist or self.task.timer_running:
            meta_row = ctk.CTkFrame(content, fg_color="transparent")
            meta_row.pack(fill="x", pady=(0, 8))
            
            # Due date with icon
            if self.task.due_date:
                due_icon = "📅" if not self.task.is_overdue else "⚠️"
                due_color = ("#E74C3C", "#F28B82") if self.task.is_overdue else ("#80868B", "#70757A")
                
                due_label = ctk.CTkLabel(
                    meta_row,
                    text=f"{due_icon} {format_date(self.task.due_date, '%b %d')}",
                    font=("Segoe UI", 11),
                    text_color=due_color
                )
                due_label.pack(side="left", padx=(0, 12))
            
            # Checklist progress
            if self.task.checklist:
                completed, total = self.task.checklist_progress
                check_label = ctk.CTkLabel(
                    meta_row,
                    text=f"☑️ {completed}/{total}",
                    font=("Segoe UI", 11),
                    text_color=("#80868B", "#70757A")
                )
                check_label.pack(side="left", padx=(0, 12))
            
            # Timer indicator
            if self.task.timer_running:
                timer_label = ctk.CTkLabel(
                    meta_row,
                    text="⏱️",
                    font=("Segoe UI", 14),
                    text_color=("#27AE60", "#81C995")
                )
                timer_label.pack(side="left")
        
        # === TAGS ===
        if self.task.tags:
            tags_row = ctk.CTkFrame(content, fg_color="transparent")
            tags_row.pack(fill="x", pady=(0, 4))
            
            from ui.components.modern_components import TagChip
            tag_colors = ["#4A90E2", "#F5A623", "#9B59B6", "#1ABC9C"]
            
            for i, tag in enumerate(self.task.tags[:3]):  # Max 3 tags
                tag_chip = TagChip(
                    tags_row,
                    text=f"#{tag[:10]}",
                    color=tag_colors[i % len(tag_colors)],
                    text_color="white"
                )
                tag_chip.pack(side="left", padx=(0, 6))
        
        # === DEPENDENCIES INDICATOR ===
        if self.task.dependencies:
            dep_label = ctk.CTkLabel(
                content,
                text=f"🔗 {len(self.task.dependencies)} linked",
                font=("Segoe UI", 10),
                text_color=("#80868B", "#70757A")
            )
            dep_label.pack(anchor="w", pady=(4, 0))
    
    def _on_hover(self, event):
        """Handle hover effect."""
        self.configure(fg_color=self.hover_fg)
    
    def _on_leave(self, event):
        """Handle leave effect."""
        self.configure(fg_color=self.default_fg)


class ModernKanbanColumn(ctk.CTkFrame):
    """Modern kanban column with gradient header."""
    
    def __init__(self, parent, status: str, title: str, tasks: List[Task],
                 projects: List[Project], on_task_click: Callable, **kwargs):
        super().__init__(
            parent,
            corner_radius=0,
            fg_color=("transparent", "transparent"),
            **kwargs
        )
        
        self.status = status
        self.tasks = tasks
        self.projects = projects
        self.on_task_click = on_task_click
        
        self._create_ui(title)
    
    def _create_ui(self, title: str):
        """Create column UI with gradient header."""
        from config import STATUS_GRADIENTS
        
        # Gradient header background color (using first color of gradient)
        gradient_colors = STATUS_GRADIENTS.get(self.status, ["#4A90E2", "#357ABD"])
        header_color = gradient_colors[0]
        
        # Header with gradient color
        header = ctk.CTkFrame(
            self,
            fg_color=header_color,
            corner_radius=12,
            height=60
        )
        header.pack(fill="x", padx=0, pady=(0, 16))
        header.pack_propagate(False)
        
        # Header content
        header_content = ctk.CTkFrame(header, fg_color="transparent")
        header_content.pack(fill="both", expand=True, padx=20, pady=12)
        
        # Title and count row
        title_row = ctk.CTkFrame(header_content, fg_color="transparent")
        title_row.pack(fill="x")
        
        # Column title
        title_label = ctk.CTkLabel(
            title_row,
            text=title,
            font=("Segoe UI", 16, "bold"),
            text_color="white",
            anchor="w"
        )
        title_label.pack(side="left")
        
        # Task count badge
        count_badge = ctk.CTkFrame(
            title_row,
            fg_color="rgba(255,255,255,0.2)",
            corner_radius=12
        )
        count_badge.pack(side="right")
        
        count_label = ctk.CTkLabel(
            count_badge,
            text=str(len(self.tasks)),
            font=("Segoe UI", 14, "bold"),
            text_color="white"
        )
        count_label.pack(padx=12, pady=4)
        
        # Scrollable tasks container
        tasks_container = ctk.CTkScrollableFrame(
            self,
            fg_color=("transparent", "transparent"),
            corner_radius=0
        )
        tasks_container.pack(fill="both", expand=True, padx=0)
        
        # Render task cards
        if not self.tasks:
            # Empty state
            empty_label = ctk.CTkLabel(
                tasks_container,
                text=f"No {title.lower()} tasks",
                font=("Segoe UI", 12),
                text_color=("#80868B", "#70757A")
            )
            empty_label.pack(pady=40)
        else:
            for task in self.tasks:
                # Get project name
                project_name = None
                if task.project_id:
                    project = next((p for p in self.projects if p.id == task.project_id), None)
                    project_name = project.name if project else None
                
                card = ModernTaskCard(
                    tasks_container,
                    task=task,
                    project_name=project_name,
                    on_click=self.on_task_click
                )
                card.pack(fill="x", pady=(0, 12))
