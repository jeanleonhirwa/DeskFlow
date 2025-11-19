"""
Daily Planner view with focus goals, tasks, and time blocks.
"""
import customtkinter as ctk
from datetime import datetime, timedelta
from typing import List, Optional
import sys
sys.path.append('..')

from models.daily_plan import DailyPlan, TimeBlock
from models.task import Task
from ui.components.common import IconButton, EmptyState
from config import TASK_STATUS


class DailyPlannerView(ctk.CTkFrame):
    """Daily planner view."""
    
    def __init__(self, parent, storage_manager, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        
        self.storage = storage_manager
        self.current_date = datetime.now().strftime("%Y-%m-%d")
        self.current_plan: Optional[DailyPlan] = None
        self.available_tasks: List[Task] = []
        
        self._create_ui()
        self.refresh()
    
    def _create_ui(self):
        """Create daily planner UI."""
        # Header with date navigation
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=20)
        
        # Date navigation
        nav_frame = ctk.CTkFrame(header, fg_color="transparent")
        nav_frame.pack(side="left")
        
        IconButton(
            nav_frame,
            text="◀ Previous",
            command=self._previous_day,
            width=100
        ).pack(side="left", padx=(0, 8))
        
        self.date_label = ctk.CTkLabel(
            nav_frame,
            text="",
            font=("Segoe UI", 18, "bold")
        )
        self.date_label.pack(side="left", padx=16)
        
        IconButton(
            nav_frame,
            text="Today",
            command=self._go_to_today,
            fg_color=("#E07B53", "#F4A261"),
            hover_color=("#D06B43", "#E49251"),
            text_color="white",
            width=80
        ).pack(side="left", padx=8)
        
        IconButton(
            nav_frame,
            text="Next ▶",
            command=self._next_day,
            width=100
        ).pack(side="left")
        
        # Main content - scrollable
        self.content = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.content.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    
    def refresh(self):
        """Refresh daily planner data."""
        # Load current plan
        self.current_plan = self.storage.get_daily_plan(self.current_date)
        
        # If no plan exists, create empty one
        if not self.current_plan:
            self.current_plan = DailyPlan(plan_date=self.current_date)
        
        # Load available tasks
        self.available_tasks = [t for t in self.storage.get_all_tasks() if t.status != "completed"]
        
        # Update UI
        self._update_date_label()
        self._render_content()
    
    def _update_date_label(self):
        """Update date label."""
        date_obj = datetime.fromisoformat(self.current_date)
        
        # Check if today
        today = datetime.now().strftime("%Y-%m-%d")
        if self.current_date == today:
            date_str = f"Today - {date_obj.strftime('%A, %B %d, %Y')}"
        else:
            date_str = date_obj.strftime("%A, %B %d, %Y")
        
        self.date_label.configure(text=date_str)
    
    def _render_content(self):
        """Render daily plan content."""
        # Clear content
        for widget in self.content.winfo_children():
            widget.destroy()
        
        # Focus Goal Section
        self._render_focus_goal()
        
        # Scheduled Tasks Section
        self._render_scheduled_tasks()
        
        # Time Blocks Section
        self._render_time_blocks()
        
        # Notes Section
        self._render_notes()
        
        # Mood Tracker
        self._render_mood()
        
        # Stats
        self._render_stats()
    
    def _render_focus_goal(self):
        """Render focus goal section."""
        section = ctk.CTkFrame(self.content, fg_color=("white", "#2D2D2D"), corner_radius=12)
        section.pack(fill="x", pady=(0, 16))
        
        ctk.CTkLabel(
            section,
            text="🎯 Focus Goal",
            font=("Segoe UI", 16, "bold")
        ).pack(anchor="w", padx=16, pady=(16, 8))
        
        self.focus_entry = ctk.CTkEntry(
            section,
            placeholder_text="What's your main goal for today?",
            font=("Segoe UI", 14),
            height=45
        )
        self.focus_entry.pack(fill="x", padx=16, pady=(0, 16))
        
        if self.current_plan.focus_goal:
            self.focus_entry.insert(0, self.current_plan.focus_goal)
        
        # Auto-save on focus out
        self.focus_entry.bind("<FocusOut>", lambda e: self._save_plan())
    
    def _render_scheduled_tasks(self):
        """Render scheduled tasks section."""
        section = ctk.CTkFrame(self.content, fg_color=("white", "#2D2D2D"), corner_radius=12)
        section.pack(fill="x", pady=(0, 16))
        
        header = ctk.CTkFrame(section, fg_color="transparent")
        header.pack(fill="x", padx=16, pady=(16, 8))
        
        ctk.CTkLabel(
            header,
            text="📋 Scheduled Tasks",
            font=("Segoe UI", 16, "bold")
        ).pack(side="left")
        
        # Add task button
        IconButton(
            header,
            text="+ Add Task",
            command=self._show_add_task_menu,
            width=100,
            height=30,
            font=("Segoe UI", 12)
        ).pack(side="right")
        
        # Tasks list
        tasks_container = ctk.CTkFrame(section, fg_color="transparent")
        tasks_container.pack(fill="x", padx=16, pady=(0, 16))
        
        if not self.current_plan.tasks:
            ctk.CTkLabel(
                tasks_container,
                text="No tasks scheduled yet",
                font=("Segoe UI", 12),
                text_color="gray60"
            ).pack(pady=8)
        else:
            # Get actual task objects
            all_tasks = {t.id: t for t in self.storage.get_all_tasks()}
            
            for task_id in self.current_plan.tasks:
                task = all_tasks.get(task_id)
                if task:
                    self._render_task_item(tasks_container, task)
    
    def _render_task_item(self, parent, task: Task):
        """Render a single task item."""
        item = ctk.CTkFrame(parent, fg_color=("#F5F5F0", "#3A3A3A"), corner_radius=8)
        item.pack(fill="x", pady=4)
        
        content = ctk.CTkFrame(item, fg_color="transparent")
        content.pack(fill="x", padx=12, pady=10)
        
        # Checkbox
        completed = task.status == "completed"
        checkbox = ctk.CTkCheckBox(
            content,
            text=task.title,
            font=("Segoe UI", 13),
            command=lambda: self._toggle_task_completion(task)
        )
        if completed:
            checkbox.select()
        checkbox.pack(side="left", fill="x", expand=True)
        
        # Remove button
        remove_btn = ctk.CTkButton(
            content,
            text="×",
            width=30,
            height=30,
            corner_radius=15,
            fg_color="transparent",
            hover_color=("gray85", "gray25"),
            font=("Segoe UI", 18),
            command=lambda: self._remove_task(task.id)
        )
        remove_btn.pack(side="right")
    
    def _render_time_blocks(self):
        """Render time blocks section."""
        section = ctk.CTkFrame(self.content, fg_color=("white", "#2D2D2D"), corner_radius=12)
        section.pack(fill="x", pady=(0, 16))
        
        header = ctk.CTkFrame(section, fg_color="transparent")
        header.pack(fill="x", padx=16, pady=(16, 8))
        
        ctk.CTkLabel(
            header,
            text="⏰ Time Blocks",
            font=("Segoe UI", 16, "bold")
        ).pack(side="left")
        
        # Add time block button
        IconButton(
            header,
            text="+ Add Block",
            command=self._add_time_block,
            width=110,
            height=30,
            font=("Segoe UI", 12)
        ).pack(side="right")
        
        # Time blocks list
        blocks_container = ctk.CTkFrame(section, fg_color="transparent")
        blocks_container.pack(fill="x", padx=16, pady=(0, 16))
        
        if not self.current_plan.time_blocks:
            ctk.CTkLabel(
                blocks_container,
                text="No time blocks yet",
                font=("Segoe UI", 12),
                text_color="gray60"
            ).pack(pady=8)
        else:
            for block in sorted(self.current_plan.time_blocks, key=lambda b: b.start_time):
                self._render_time_block(blocks_container, block)
    
    def _render_time_block(self, parent, block: TimeBlock):
        """Render a single time block."""
        item = ctk.CTkFrame(parent, fg_color=("#F5F5F0", "#3A3A3A"), corner_radius=8)
        item.pack(fill="x", pady=4)
        
        content = ctk.CTkFrame(item, fg_color="transparent")
        content.pack(fill="x", padx=12, pady=10)
        
        # Checkbox
        checkbox = ctk.CTkCheckBox(
            content,
            text="",
            width=20,
            command=lambda: self._toggle_block_completion(block)
        )
        if block.completed:
            checkbox.select()
        checkbox.pack(side="left", padx=(0, 12))
        
        # Time and activity
        info_frame = ctk.CTkFrame(content, fg_color="transparent")
        info_frame.pack(side="left", fill="x", expand=True)
        
        ctk.CTkLabel(
            info_frame,
            text=f"{block.start_time} - {block.end_time}",
            font=("Segoe UI", 12, "bold")
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            info_frame,
            text=block.activity,
            font=("Segoe UI", 12),
            text_color="gray60"
        ).pack(anchor="w")
        
        # Delete button
        delete_btn = ctk.CTkButton(
            content,
            text="×",
            width=30,
            height=30,
            corner_radius=15,
            fg_color="transparent",
            hover_color=("gray85", "gray25"),
            font=("Segoe UI", 18),
            command=lambda: self._delete_time_block(block.id)
        )
        delete_btn.pack(side="right")
    
    def _render_notes(self):
        """Render notes section."""
        section = ctk.CTkFrame(self.content, fg_color=("white", "#2D2D2D"), corner_radius=12)
        section.pack(fill="x", pady=(0, 16))
        
        ctk.CTkLabel(
            section,
            text="📝 Notes",
            font=("Segoe UI", 16, "bold")
        ).pack(anchor="w", padx=16, pady=(16, 8))
        
        self.notes_text = ctk.CTkTextbox(
            section,
            font=("Segoe UI", 13),
            height=100
        )
        self.notes_text.pack(fill="x", padx=16, pady=(0, 16))
        
        if self.current_plan.notes:
            self.notes_text.insert("1.0", self.current_plan.notes)
        
        # Auto-save on focus out
        self.notes_text.bind("<FocusOut>", lambda e: self._save_plan())
    
    def _render_mood(self):
        """Render mood tracker."""
        section = ctk.CTkFrame(self.content, fg_color=("white", "#2D2D2D"), corner_radius=12)
        section.pack(fill="x", pady=(0, 16))
        
        ctk.CTkLabel(
            section,
            text="😊 How are you feeling?",
            font=("Segoe UI", 16, "bold")
        ).pack(anchor="w", padx=16, pady=(16, 8))
        
        moods_frame = ctk.CTkFrame(section, fg_color="transparent")
        moods_frame.pack(fill="x", padx=16, pady=(0, 16))
        
        moods = [
            ("excellent", "😊"),
            ("good", "🙂"),
            ("neutral", "😐"),
            ("tired", "😴"),
            ("stressed", "😓")
        ]
        
        self.mood_var = ctk.StringVar(value=self.current_plan.mood or "")
        
        for value, emoji in moods:
            radio = ctk.CTkRadioButton(
                moods_frame,
                text=emoji,
                variable=self.mood_var,
                value=value,
                font=("Segoe UI", 24),
                command=self._save_plan
            )
            radio.pack(side="left", padx=8)
    
    def _render_stats(self):
        """Render daily stats."""
        section = ctk.CTkFrame(self.content, fg_color=("white", "#2D2D2D"), corner_radius=12)
        section.pack(fill="x")
        
        stats_frame = ctk.CTkFrame(section, fg_color="transparent")
        stats_frame.pack(fill="x", padx=16, pady=16)
        
        # Task completion
        all_tasks = {t.id: t for t in self.storage.get_all_tasks()}
        completed_tasks = sum(1 for tid in self.current_plan.tasks 
                             if tid in all_tasks and all_tasks[tid].status == "completed")
        total_tasks = len(self.current_plan.tasks)
        
        task_stat = ctk.CTkFrame(stats_frame, fg_color="transparent")
        task_stat.pack(side="left", expand=True)
        
        ctk.CTkLabel(
            task_stat,
            text=f"{completed_tasks}/{total_tasks}",
            font=("Segoe UI", 24, "bold")
        ).pack()
        
        ctk.CTkLabel(
            task_stat,
            text="Tasks Completed",
            font=("Segoe UI", 12),
            text_color="gray60"
        ).pack()
        
        # Time blocks completion
        completed_blocks, total_blocks = self.current_plan.time_blocks_progress
        
        block_stat = ctk.CTkFrame(stats_frame, fg_color="transparent")
        block_stat.pack(side="left", expand=True)
        
        ctk.CTkLabel(
            block_stat,
            text=f"{completed_blocks}/{total_blocks}",
            font=("Segoe UI", 24, "bold")
        ).pack()
        
        ctk.CTkLabel(
            block_stat,
            text="Blocks Completed",
            font=("Segoe UI", 12),
            text_color="gray60"
        ).pack()
    
    def _previous_day(self):
        """Navigate to previous day."""
        date_obj = datetime.fromisoformat(self.current_date)
        self.current_date = (date_obj - timedelta(days=1)).strftime("%Y-%m-%d")
        self.refresh()
    
    def _next_day(self):
        """Navigate to next day."""
        date_obj = datetime.fromisoformat(self.current_date)
        self.current_date = (date_obj + timedelta(days=1)).strftime("%Y-%m-%d")
        self.refresh()
    
    def _go_to_today(self):
        """Navigate to today."""
        self.current_date = datetime.now().strftime("%Y-%m-%d")
        self.refresh()
    
    def _show_add_task_menu(self):
        """Show menu to add task to plan."""
        if not self.available_tasks:
            return
        
        # Create simple dialog
        dialog = ctk.CTkToplevel(self)
        dialog.title("Add Task to Plan")
        dialog.geometry("400x500")
        dialog.transient(self)
        dialog.grab_set()
        
        ctk.CTkLabel(dialog, text="Select a task:", font=("Segoe UI", 14, "bold")).pack(padx=20, pady=(20, 10))
        
        # Scrollable task list
        task_list = ctk.CTkScrollableFrame(dialog, fg_color="transparent")
        task_list.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        for task in self.available_tasks:
            if task.id not in self.current_plan.tasks:
                btn = ctk.CTkButton(
                    task_list,
                    text=task.title,
                    command=lambda t=task: self._add_task_to_plan(t.id, dialog),
                    anchor="w",
                    fg_color="transparent",
                    hover_color=("gray85", "gray25")
                )
                btn.pack(fill="x", pady=2)
    
    def _add_task_to_plan(self, task_id: str, dialog):
        """Add task to daily plan."""
        self.current_plan.add_task(task_id)
        self._save_plan()
        dialog.destroy()
        self.refresh()
    
    def _remove_task(self, task_id: str):
        """Remove task from daily plan."""
        self.current_plan.remove_task(task_id)
        self._save_plan()
        self.refresh()
    
    def _toggle_task_completion(self, task: Task):
        """Toggle task completion status."""
        new_status = "completed" if task.status != "completed" else "todo"
        task.update(status=new_status)
        self.storage.save_task(task)
        self.refresh()
    
    def _add_time_block(self):
        """Show dialog to add time block."""
        TimeBlockDialog(self, self.current_plan, self.storage, self.refresh)
    
    def _delete_time_block(self, block_id: str):
        """Delete a time block."""
        self.current_plan.remove_time_block(block_id)
        self._save_plan()
        self.refresh()
    
    def _toggle_block_completion(self, block: TimeBlock):
        """Toggle time block completion."""
        block.completed = not block.completed
        self._save_plan()
        self.refresh()
    
    def _save_plan(self):
        """Save current plan."""
        # Update from UI
        self.current_plan.focus_goal = self.focus_entry.get()
        self.current_plan.notes = self.notes_text.get("1.0", "end-1c")
        self.current_plan.mood = self.mood_var.get() if self.mood_var.get() else None
        
        # Save to storage
        self.storage.save_daily_plan(self.current_plan)


class TimeBlockDialog(ctk.CTkToplevel):
    """Dialog to add/edit time block."""
    
    def __init__(self, parent, plan: DailyPlan, storage, on_save: callable):
        super().__init__(parent)
        
        self.plan = plan
        self.storage = storage
        self.on_save = on_save
        
        self.title("Add Time Block")
        self.geometry("400x350")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        self._create_ui()
    
    def _create_ui(self):
        """Create dialog UI."""
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Start time
        ctk.CTkLabel(container, text="Start Time (HH:MM)", font=("Segoe UI", 13, "bold")).pack(anchor="w", pady=(0, 4))
        self.start_entry = ctk.CTkEntry(container, placeholder_text="09:00", font=("Segoe UI", 13))
        self.start_entry.pack(fill="x", pady=(0, 16))
        
        # End time
        ctk.CTkLabel(container, text="End Time (HH:MM)", font=("Segoe UI", 13, "bold")).pack(anchor="w", pady=(0, 4))
        self.end_entry = ctk.CTkEntry(container, placeholder_text="11:00", font=("Segoe UI", 13))
        self.end_entry.pack(fill="x", pady=(0, 16))
        
        # Activity
        ctk.CTkLabel(container, text="Activity", font=("Segoe UI", 13, "bold")).pack(anchor="w", pady=(0, 4))
        self.activity_entry = ctk.CTkEntry(container, placeholder_text="Development work", font=("Segoe UI", 13))
        self.activity_entry.pack(fill="x", pady=(0, 16))
        
        # Buttons
        buttons = ctk.CTkFrame(self, fg_color="transparent")
        buttons.pack(fill="x", padx=20, pady=(0, 20))
        
        IconButton(
            buttons,
            text="Cancel",
            command=self.destroy,
            fg_color="gray70",
            hover_color="gray60"
        ).pack(side="right", padx=(8, 0))
        
        IconButton(
            buttons,
            text="Add Block",
            command=self._save,
            fg_color=("#E07B53", "#F4A261"),
            hover_color=("#D06B43", "#E49251"),
            text_color="white"
        ).pack(side="right")
    
    def _save(self):
        """Save time block."""
        start = self.start_entry.get().strip()
        end = self.end_entry.get().strip()
        activity = self.activity_entry.get().strip()
        
        if not all([start, end, activity]):
            return
        
        block = TimeBlock(
            start_time=start,
            end_time=end,
            activity=activity
        )
        
        self.plan.add_time_block(block)
        self.storage.save_daily_plan(self.plan)
        
        self.destroy()
        self.on_save()
