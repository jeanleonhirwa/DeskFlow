"""
Project data model for Desk Flow.
"""
import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any


class Milestone:
    """Represents a project milestone."""
    
    def __init__(
        self,
        name: str,
        description: str = "",
        target_date: Optional[str] = None,
        completed: bool = False,
        completed_at: Optional[str] = None,
        milestone_id: Optional[str] = None
    ):
        self.id = milestone_id or str(uuid.uuid4())
        self.name = name
        self.description = description
        self.target_date = target_date
        self.completed = completed
        self.completed_at = completed_at
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert milestone to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "target_date": self.target_date,
            "completed": self.completed,
            "completed_at": self.completed_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Milestone":
        """Create milestone from dictionary."""
        return cls(
            name=data["name"],
            description=data.get("description", ""),
            target_date=data.get("target_date"),
            completed=data.get("completed", False),
            completed_at=data.get("completed_at"),
            milestone_id=data.get("id")
        )


class Project:
    """Represents a software development project."""
    
    def __init__(
        self,
        name: str,
        description: str = "",
        status: str = "planning",
        priority: str = "medium",
        color: str = "#E07B53",
        start_date: Optional[str] = None,
        target_date: Optional[str] = None,
        completion_date: Optional[str] = None,
        repository_url: Optional[str] = None,
        tech_stack: Optional[List[str]] = None,
        team_members: Optional[List[str]] = None,
        milestones: Optional[List[Milestone]] = None,
        notes: str = "",
        tags: Optional[List[str]] = None,
        project_id: Optional[str] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None
    ):
        self.id = project_id or str(uuid.uuid4())
        self.name = name
        self.description = description
        self.status = status
        self.priority = priority
        self.color = color
        self.created_at = created_at or datetime.now().isoformat()
        self.updated_at = updated_at or datetime.now().isoformat()
        self.start_date = start_date
        self.target_date = target_date
        self.completion_date = completion_date
        self.repository_url = repository_url
        self.tech_stack = tech_stack or []
        self.team_members = team_members or []
        self.milestones = milestones or []
        self.notes = notes
        self.tags = tags or []
        self._progress_percentage = 0.0
    
    @property
    def progress_percentage(self) -> float:
        """Calculate progress based on completed milestones."""
        if not self.milestones:
            return 0.0
        completed = sum(1 for m in self.milestones if m.completed)
        return (completed / len(self.milestones)) * 100
    
    def update(self, **kwargs):
        """Update project fields."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now().isoformat()
    
    def add_milestone(self, milestone: Milestone):
        """Add a milestone to the project."""
        self.milestones.append(milestone)
        self.updated_at = datetime.now().isoformat()
    
    def remove_milestone(self, milestone_id: str):
        """Remove a milestone from the project."""
        self.milestones = [m for m in self.milestones if m.id != milestone_id]
        self.updated_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert project to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,
            "color": self.color,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "start_date": self.start_date,
            "target_date": self.target_date,
            "completion_date": self.completion_date,
            "progress_percentage": self.progress_percentage,
            "repository_url": self.repository_url,
            "tech_stack": self.tech_stack,
            "team_members": self.team_members,
            "milestones": [m.to_dict() for m in self.milestones],
            "notes": self.notes,
            "tags": self.tags
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Project":
        """Create project instance from dictionary."""
        milestones = [
            Milestone.from_dict(m) for m in data.get("milestones", [])
        ]
        
        return cls(
            name=data["name"],
            description=data.get("description", ""),
            status=data.get("status", "planning"),
            priority=data.get("priority", "medium"),
            color=data.get("color", "#E07B53"),
            start_date=data.get("start_date"),
            target_date=data.get("target_date"),
            completion_date=data.get("completion_date"),
            repository_url=data.get("repository_url"),
            tech_stack=data.get("tech_stack", []),
            team_members=data.get("team_members", []),
            milestones=milestones,
            notes=data.get("notes", ""),
            tags=data.get("tags", []),
            project_id=data.get("id"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
    
    def validate(self) -> tuple[bool, Optional[str]]:
        """Validate project data."""
        if not self.name or not self.name.strip():
            return False, "Project name is required"
        
        valid_statuses = ["planning", "active", "paused", "completed", "archived"]
        if self.status not in valid_statuses:
            return False, f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
        
        valid_priorities = ["low", "medium", "high"]
        if self.priority not in valid_priorities:
            return False, f"Invalid priority. Must be one of: {', '.join(valid_priorities)}"
        
        return True, None
