"""
Export and import utilities for data management.
"""
import json
import csv
from pathlib import Path
from typing import List
from datetime import datetime

from models.project import Project
from models.task import Task
from models.daily_plan import DailyPlan


def export_projects_csv(projects: List[Project], filepath: str) -> bool:
    """Export projects to CSV file."""
    try:
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            if not projects:
                return True
            
            # Define CSV headers
            headers = [
                'ID', 'Name', 'Description', 'Status', 'Priority', 'Color',
                'Created At', 'Updated At', 'Start Date', 'Target Date',
                'Completion Date', 'Progress %', 'Repository URL',
                'Tech Stack', 'Team Members', 'Notes', 'Tags'
            ]
            
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            
            for project in projects:
                writer.writerow({
                    'ID': project.id,
                    'Name': project.name,
                    'Description': project.description,
                    'Status': project.status,
                    'Priority': project.priority,
                    'Color': project.color,
                    'Created At': project.created_at,
                    'Updated At': project.updated_at,
                    'Start Date': project.start_date or '',
                    'Target Date': project.target_date or '',
                    'Completion Date': project.completion_date or '',
                    'Progress %': project.progress_percentage,
                    'Repository URL': project.repository_url or '',
                    'Tech Stack': ', '.join(project.tech_stack),
                    'Team Members': ', '.join(project.team_members),
                    'Notes': project.notes,
                    'Tags': ', '.join(project.tags)
                })
        
        return True
    except Exception as e:
        print(f"Error exporting projects CSV: {e}")
        return False


def export_tasks_csv(tasks: List[Task], filepath: str) -> bool:
    """Export tasks to CSV file."""
    try:
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            if not tasks:
                return True
            
            headers = [
                'ID', 'Project ID', 'Title', 'Description', 'Status', 'Priority',
                'Created At', 'Updated At', 'Due Date', 'Completed At',
                'Estimated Hours', 'Actual Hours', 'Tags', 'Blocked Reason'
            ]
            
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            
            for task in tasks:
                writer.writerow({
                    'ID': task.id,
                    'Project ID': task.project_id or '',
                    'Title': task.title,
                    'Description': task.description,
                    'Status': task.status,
                    'Priority': task.priority,
                    'Created At': task.created_at,
                    'Updated At': task.updated_at,
                    'Due Date': task.due_date or '',
                    'Completed At': task.completed_at or '',
                    'Estimated Hours': task.estimated_hours or '',
                    'Actual Hours': task.actual_hours or '',
                    'Tags': ', '.join(task.tags),
                    'Blocked Reason': task.blocked_reason or ''
                })
        
        return True
    except Exception as e:
        print(f"Error exporting tasks CSV: {e}")
        return False


def export_daily_plans_csv(plans: List[DailyPlan], filepath: str) -> bool:
    """Export daily plans to CSV file."""
    try:
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            if not plans:
                return True
            
            headers = [
                'ID', 'Date', 'Focus Goal', 'Tasks', 'Time Blocks',
                'Notes', 'Mood', 'Completed'
            ]
            
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            
            for plan in plans:
                time_blocks_str = '; '.join([
                    f"{b.start_time}-{b.end_time}: {b.activity}"
                    for b in plan.time_blocks
                ])
                
                writer.writerow({
                    'ID': plan.id,
                    'Date': plan.date,
                    'Focus Goal': plan.focus_goal,
                    'Tasks': ', '.join(plan.tasks),
                    'Time Blocks': time_blocks_str,
                    'Notes': plan.notes,
                    'Mood': plan.mood or '',
                    'Completed': plan.completed
                })
        
        return True
    except Exception as e:
        print(f"Error exporting daily plans CSV: {e}")
        return False


def export_all_data_json(storage, filepath: str) -> bool:
    """Export all data to JSON file."""
    try:
        data = {
            'export_date': datetime.now().isoformat(),
            'projects': [p.to_dict() for p in storage.get_all_projects()],
            'tasks': [t.to_dict() for t in storage.get_all_tasks()],
            'daily_plans': []  # Daily plans export
        }
        
        # Get all daily plans (last 90 days)
        from datetime import timedelta
        start_date = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
        end_date = datetime.now().strftime("%Y-%m-%d")
        
        daily_plans = storage.get_daily_plans_range(start_date, end_date)
        data['daily_plans'] = [p.to_dict() for p in daily_plans]
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return True
    except Exception as e:
        print(f"Error exporting JSON: {e}")
        return False


def export_projects_json(projects: List[Project], filepath: str) -> bool:
    """Export projects only to JSON file."""
    try:
        data = {
            'export_date': datetime.now().isoformat(),
            'projects': [p.to_dict() for p in projects]
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return True
    except Exception as e:
        print(f"Error exporting projects JSON: {e}")
        return False


def export_tasks_json(tasks: List[Task], filepath: str) -> bool:
    """Export tasks only to JSON file."""
    try:
        data = {
            'export_date': datetime.now().isoformat(),
            'tasks': [t.to_dict() for t in tasks]
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return True
    except Exception as e:
        print(f"Error exporting tasks JSON: {e}")
        return False


def import_projects_json(filepath: str, storage) -> tuple[bool, str]:
    """Import projects from JSON file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        projects_data = data.get('projects', [])
        count = 0
        
        for project_dict in projects_data:
            project = Project.from_dict(project_dict)
            storage.save_project(project)
            count += 1
        
        return True, f"Imported {count} projects successfully"
    except Exception as e:
        return False, f"Error importing projects: {str(e)}"


def import_tasks_json(filepath: str, storage) -> tuple[bool, str]:
    """Import tasks from JSON file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        tasks_data = data.get('tasks', [])
        count = 0
        
        for task_dict in tasks_data:
            task = Task.from_dict(task_dict)
            storage.save_task(task)
            count += 1
        
        return True, f"Imported {count} tasks successfully"
    except Exception as e:
        return False, f"Error importing tasks: {str(e)}"


def import_all_data_json(filepath: str, storage) -> tuple[bool, str]:
    """Import all data from JSON file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Import projects
        projects_data = data.get('projects', [])
        for project_dict in projects_data:
            project = Project.from_dict(project_dict)
            storage.save_project(project)
        
        # Import tasks
        tasks_data = data.get('tasks', [])
        for task_dict in tasks_data:
            task = Task.from_dict(task_dict)
            storage.save_task(task)
        
        # Import daily plans
        plans_data = data.get('daily_plans', [])
        for plan_dict in plans_data:
            plan = DailyPlan.from_dict(plan_dict)
            storage.save_daily_plan(plan)
        
        total = len(projects_data) + len(tasks_data) + len(plans_data)
        return True, f"Imported {total} items successfully"
    except Exception as e:
        return False, f"Error importing data: {str(e)}"
