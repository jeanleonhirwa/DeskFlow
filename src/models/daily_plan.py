"""
Daily Plan data model for Desk Flow.
"""
import uuid
from datetime import datetime, date
from typing import Optional, List, Dict, Any


class TimeBlock:
    """Represents a time block in a daily plan."""
    
    def __init__(
        self,
        start_time: str,
        end_time: str,
        activity: str,
        task_id: Optional[str] = None,
        completed: bool = False,
        block_id: Optional[str] = None
    ):
        self.id = block_id or str(uuid.uuid4())
        self.start_time = start_time  # HH:MM format
        self.end_time = end_time  # HH:MM format
        self.activity = activity
        self.task_id = task_id
        self.completed = completed
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert time block to dictionary."""
        return {
            "id": self.id,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "activity": self.activity,
            "task_id": self.task_id,
            "completed": self.completed
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TimeBlock":
        """Create time block from dictionary."""
        return cls(
            start_time=data["start_time"],
            end_time=data["end_time"],
            activity=data["activity"],
            task_id=data.get("task_id"),
            completed=data.get("completed", False),
            block_id=data.get("id")
        )


class DailyPlan:
    """Represents a daily plan."""
    
    def __init__(
        self,
        plan_date: str,  # ISO date string (YYYY-MM-DD)
        focus_goal: str = "",
        tasks: Optional[List[str]] = None,  # List of task UUIDs
        time_blocks: Optional[List[TimeBlock]] = None,
        notes: str = "",
        mood: Optional[str] = None,  # excellent, good, neutral, tired, stressed
        completed: bool = False,
        plan_id: Optional[str] = None
    ):
        self.id = plan_id or str(uuid.uuid4())
        self.date = plan_date
        self.focus_goal = focus_goal
        self.tasks = tasks or []
        self.time_blocks = time_blocks or []
        self.notes = notes
        self.mood = mood
        self.completed = completed
    
    @property
    def tasks_progress(self) -> tuple[int, int]:
        """Get task completion progress (completed, total)."""
        # This will be calculated by checking actual task completion status
        # For now, return the count
        return 0, len(self.tasks)
    
    @property
    def time_blocks_progress(self) -> tuple[int, int]:
        """Get time block completion progress."""
        if not self.time_blocks:
            return 0, 0
        completed = sum(1 for block in self.time_blocks if block.completed)
        return completed, len(self.time_blocks)
    
    def add_task(self, task_id: str):
        """Add a task to the daily plan."""
        if task_id not in self.tasks:
            self.tasks.append(task_id)
    
    def remove_task(self, task_id: str):
        """Remove a task from the daily plan."""
        if task_id in self.tasks:
            self.tasks.remove(task_id)
    
    def add_time_block(self, time_block: TimeBlock):
        """Add a time block to the plan."""
        self.time_blocks.append(time_block)
    
    def remove_time_block(self, block_id: str):
        """Remove a time block from the plan."""
        self.time_blocks = [b for b in self.time_blocks if b.id != block_id]
    
    def update(self, **kwargs):
        """Update daily plan fields."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert daily plan to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "date": self.date,
            "focus_goal": self.focus_goal,
            "tasks": self.tasks,
            "time_blocks": [b.to_dict() for b in self.time_blocks],
            "notes": self.notes,
            "mood": self.mood,
            "completed": self.completed
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DailyPlan":
        """Create daily plan instance from dictionary."""
        time_blocks = [
            TimeBlock.from_dict(b) for b in data.get("time_blocks", [])
        ]
        
        return cls(
            plan_date=data["date"],
            focus_goal=data.get("focus_goal", ""),
            tasks=data.get("tasks", []),
            time_blocks=time_blocks,
            notes=data.get("notes", ""),
            mood=data.get("mood"),
            completed=data.get("completed", False),
            plan_id=data.get("id")
        )
    
    def validate(self) -> tuple[bool, Optional[str]]:
        """Validate daily plan data."""
        # Date validation
        try:
            datetime.fromisoformat(self.date)
        except:
            return False, "Invalid date format. Use YYYY-MM-DD"
        
        # Mood validation
        if self.mood and self.mood not in ["excellent", "good", "neutral", "tired", "stressed"]:
            return False, "Invalid mood value"
        
        # Time block validation
        for block in self.time_blocks:
            try:
                # Validate time format HH:MM
                datetime.strptime(block.start_time, "%H:%M")
                datetime.strptime(block.end_time, "%H:%M")
            except:
                return False, f"Invalid time format in time block: {block.activity}"
        
        return True, None
