"""
Analytics data aggregation utilities.
"""
from typing import Dict, List, Tuple
from datetime import datetime, timedelta
from collections import defaultdict, Counter

from models.project import Project
from models.task import Task


def get_project_status_distribution(projects: List[Project]) -> Dict[str, int]:
    """Get count of projects by status."""
    distribution = defaultdict(int)
    for project in projects:
        distribution[project.status] += 1
    return dict(distribution)


def get_tasks_by_status(tasks: List[Task]) -> Dict[str, int]:
    """Get count of tasks by status."""
    distribution = defaultdict(int)
    for task in tasks:
        distribution[task.status] += 1
    return dict(distribution)


def get_tasks_completed_per_day(tasks: List[Task], days: int = 30) -> Dict[str, int]:
    """Get tasks completed per day for the last N days."""
    today = datetime.now().date()
    start_date = today - timedelta(days=days - 1)
    
    # Initialize all dates with 0
    date_counts = {}
    for i in range(days):
        date = start_date + timedelta(days=i)
        date_counts[date.strftime("%Y-%m-%d")] = 0
    
    # Count completed tasks by date
    for task in tasks:
        if task.completed_at:
            try:
                completed_date = datetime.fromisoformat(task.completed_at).date()
                if start_date <= completed_date <= today:
                    date_counts[completed_date.strftime("%Y-%m-%d")] += 1
            except:
                pass
    
    return date_counts


def get_time_by_project(projects: List[Project], tasks: List[Task]) -> Dict[str, float]:
    """Get total actual hours logged by project."""
    project_time = defaultdict(float)
    
    # Create project ID to name mapping
    project_names = {p.id: p.name for p in projects}
    
    for task in tasks:
        if task.actual_hours and task.project_id:
            project_name = project_names.get(task.project_id, "Unknown")
            project_time[project_name] += task.actual_hours
    
    # Sort by time spent (descending) and return top 10
    sorted_projects = sorted(project_time.items(), key=lambda x: x[1], reverse=True)
    return dict(sorted_projects[:10])


def get_priority_distribution(tasks: List[Task]) -> Dict[str, int]:
    """Get count of tasks by priority."""
    distribution = defaultdict(int)
    for task in tasks:
        distribution[task.priority] += 1
    return dict(distribution)


def calculate_completion_rate(tasks: List[Task], days: int = 7) -> float:
    """Calculate task completion rate for the last N days."""
    cutoff_date = datetime.now() - timedelta(days=days)
    
    total_tasks = 0
    completed_tasks = 0
    
    for task in tasks:
        # Check if task was created in the time period
        try:
            created = datetime.fromisoformat(task.created_at)
            if created >= cutoff_date:
                total_tasks += 1
                if task.status == "completed":
                    completed_tasks += 1
        except:
            pass
    
    if total_tasks == 0:
        return 0.0
    
    return (completed_tasks / total_tasks) * 100


def get_best_productivity_day(tasks: List[Task]) -> str:
    """Get the day of week with most task completions."""
    day_counts = defaultdict(int)
    
    for task in tasks:
        if task.completed_at:
            try:
                completed = datetime.fromisoformat(task.completed_at)
                day_name = completed.strftime("%A")
                day_counts[day_name] += 1
            except:
                pass
    
    if not day_counts:
        return "Not enough data"
    
    best_day = max(day_counts.items(), key=lambda x: x[1])
    return best_day[0]


def get_most_used_tags(tasks: List[Task], limit: int = 10) -> List[Tuple[str, int]]:
    """Get most frequently used tags."""
    tag_counts = Counter()
    
    for task in tasks:
        for tag in task.tags:
            tag_counts[tag] += 1
    
    return tag_counts.most_common(limit)


def get_average_tasks_per_day(tasks: List[Task], days: int = 30) -> float:
    """Calculate average tasks completed per day."""
    completed_per_day = get_tasks_completed_per_day(tasks, days)
    total_completed = sum(completed_per_day.values())
    
    if days == 0:
        return 0.0
    
    return total_completed / days


def get_blocked_tasks_frequency(tasks: List[Task]) -> List[Tuple[str, int]]:
    """Get tasks that are frequently blocked (number of times status was 'blocked')."""
    # For now, just return currently blocked tasks
    # In a real implementation, you'd track status change history
    blocked_tasks = []
    
    for task in tasks:
        if task.status == "blocked":
            blocked_tasks.append((task.title, 1))
    
    return blocked_tasks[:10]
