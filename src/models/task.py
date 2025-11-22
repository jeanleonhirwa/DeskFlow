"""
Task data model for Desk Flow.
"""
import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any


class ChecklistItem:
    """Represents a checklist item within a task."""
    
    def __init__(
        self,
        text: str,
        completed: bool = False,
        item_id: Optional[str] = None
    ):
        self.id = item_id or str(uuid.uuid4())
        self.text = text
        self.completed = completed
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert checklist item to dictionary."""
        return {
            "id": self.id,
            "text": self.text,
            "completed": self.completed
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ChecklistItem":
        """Create checklist item from dictionary."""
        return cls(
            text=data["text"],
            completed=data.get("completed", False),
            item_id=data.get("id")
        )


class Task:
    """Represents a development task."""
    
    def __init__(
        self,
        title: str,
        project_id: Optional[str] = None,
        description: str = "",
        status: str = "todo",
        priority: str = "medium",
        due_date: Optional[str] = None,
        estimated_hours: Optional[float] = None,
        actual_hours: Optional[float] = None,
        tags: Optional[List[str]] = None,
        checklist: Optional[List[ChecklistItem]] = None,
        blocked_reason: Optional[str] = None,
        dependencies: Optional[List[str]] = None,
        timer_running: bool = False,
        timer_start_time: Optional[str] = None,
        timer_elapsed_seconds: int = 0,
        task_id: Optional[str] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
        completed_at: Optional[str] = None
    ):
        self.id = task_id or str(uuid.uuid4())
        self.project_id = project_id
        self.title = title
        self.description = description
        self.status = status
        self.priority = priority
        self.created_at = created_at or datetime.now().isoformat()
        self.updated_at = updated_at or datetime.now().isoformat()
        self.due_date = due_date
        self.completed_at = completed_at
        self.estimated_hours = estimated_hours
        self.actual_hours = actual_hours
        self.tags = tags or []
        self.checklist = checklist or []
        self.blocked_reason = blocked_reason
        self.dependencies = dependencies or []
        self.timer_running = timer_running
        self.timer_start_time = timer_start_time
        self.timer_elapsed_seconds = timer_elapsed_seconds
    
    @property
    def checklist_progress(self) -> tuple[int, int]:
        """Get checklist completion progress (completed, total)."""
        if not self.checklist:
            return 0, 0
        completed = sum(1 for item in self.checklist if item.completed)
        return completed, len(self.checklist)
    
    @property
    def is_overdue(self) -> bool:
        """Check if task is overdue."""
        if not self.due_date or self.status == "completed":
            return False
        try:
            due = datetime.fromisoformat(self.due_date)
            return datetime.now() > due
        except:
            return False
    
    def update(self, **kwargs):
        """Update task fields."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now().isoformat()
        
        # Auto-set completed_at when status changes to completed
        if kwargs.get("status") == "completed" and not self.completed_at:
            self.completed_at = datetime.now().isoformat()
        elif kwargs.get("status") != "completed":
            self.completed_at = None
    
    def add_checklist_item(self, item: ChecklistItem):
        """Add a checklist item to the task."""
        self.checklist.append(item)
        self.updated_at = datetime.now().isoformat()
    
    def remove_checklist_item(self, item_id: str):
        """Remove a checklist item from the task."""
        self.checklist = [item for item in self.checklist if item.id != item_id]
        self.updated_at = datetime.now().isoformat()
    
    def start_timer(self):
        """Start the task timer."""
        if not self.timer_running:
            self.timer_running = True
            self.timer_start_time = datetime.now().isoformat()
            self.updated_at = datetime.now().isoformat()
    
    def stop_timer(self, elapsed_seconds: int):
        """Stop the timer and add elapsed time to actual hours."""
        if self.timer_running:
            self.timer_running = False
            self.timer_start_time = None
           
            # Add elapsed time to actual hours
            hours_worked = elapsed_seconds / 3600
            if self.actual_hours:
                self.actual_hours += hours_worked
            else:
                self.actual_hours = hours_worked
            
            # Reset elapsed seconds
            self.timer_elapsed_seconds = 0
            self.updated_at = datetime.now().isoformat()
    
    def get_timer_display(self) -> str:
        """Get formatted timer display (HH:MM:SS)."""
        hours = self.timer_elapsed_seconds // 3600
        minutes = (self.timer_elapsed_seconds % 3600) // 60
        seconds = self.timer_elapsed_seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    def get_total_time_seconds(self) -> int:
        """Get total time including running timer."""
        total = self.timer_elapsed_seconds
        if self.timer_running and self.timer_start_time:
            try:
                start = datetime.fromisoformat(self.timer_start_time)
                elapsed_now = (datetime.now() - start).total_seconds()
                total += int(elapsed_now)
            except:
                pass
        return total
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "project_id": self.project_id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "due_date": self.due_date,
            "completed_at": self.completed_at,
            "estimated_hours": self.estimated_hours,
            "actual_hours": self.actual_hours,
            "tags": self.tags,
            "checklist": [item.to_dict() for item in self.checklist],
            "blocked_reason": self.blocked_reason,
            "dependencies": self.dependencies,
            "timer_running": self.timer_running,
            "timer_start_time": self.timer_start_time,
            "timer_elapsed_seconds": self.timer_elapsed_seconds
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Task":
        """Create task instance from dictionary."""
        checklist = [
            ChecklistItem.from_dict(item) for item in data.get("checklist", [])
        ]
        
        return cls(
            title=data["title"],
            project_id=data.get("project_id"),
            description=data.get("description", ""),
            status=data.get("status", "todo"),
            priority=data.get("priority", "medium"),
            due_date=data.get("due_date"),
            estimated_hours=data.get("estimated_hours"),
            actual_hours=data.get("actual_hours"),
            tags=data.get("tags", []),
            checklist=checklist,
            blocked_reason=data.get("blocked_reason"),
            dependencies=data.get("dependencies", []),
            timer_running=data.get("timer_running", False),
            timer_start_time=data.get("timer_start_time"),
            timer_elapsed_seconds=data.get("timer_elapsed_seconds", 0),
            task_id=data.get("id"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            completed_at=data.get("completed_at")
        )
    
    def validate(self) -> tuple[bool, Optional[str]]:
        """Validate task data."""
        if not self.title or not self.title.strip():
            return False, "Task title is required"
        
        valid_statuses = ["todo", "in_progress", "blocked", "completed"]
        if self.status not in valid_statuses:
            return False, f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
        
        valid_priorities = ["low", "medium", "high"]
        if self.priority not in valid_priorities:
            return False, f"Invalid priority. Must be one of: {', '.join(valid_priorities)}"
        
        if self.status == "blocked" and not self.blocked_reason:
            return False, "Blocked reason is required when status is 'blocked'"
        
        return True, None
