"""
Notification and reminder management system.
"""
from datetime import datetime, timedelta
from typing import List, Callable, Optional
import threading
import time


class NotificationManager:
    """Manages task reminders and notifications."""
    
    def __init__(self, storage_manager, show_notification_callback: Callable):
        self.storage = storage_manager
        self.show_notification = show_notification_callback
        self.running = False
        self.check_interval = 300  # Check every 5 minutes
        self.thread = None
        
        # Get notification settings
        settings = self.storage.get_settings()
        self.settings = settings.notification_settings if hasattr(settings, 'notification_settings') else {}
        
        # Default settings if not defined
        if not self.settings:
            self.settings = {
                "enabled": True,
                "task_due_soon": True,
                "task_overdue": True,
                "daily_summary": True,
                "daily_summary_time": "09:00",
                "notification_duration": 5000
            }
        
        self.daily_summary_shown_today = False
    
    def start(self):
        """Start the notification manager."""
        if not self.settings.get("enabled", True):
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._check_loop, daemon=True)
        self.thread.start()
    
    def stop(self):
        """Stop the notification manager."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=1)
    
    def _check_loop(self):
        """Main loop to check for notifications."""
        while self.running:
            try:
                # Check daily summary
                if self.settings.get("daily_summary", True):
                    self._check_daily_summary()
                
                # Check due soon tasks
                if self.settings.get("task_due_soon", True):
                    self._check_due_soon_tasks()
                
                # Check overdue tasks
                if self.settings.get("task_overdue", True):
                    self._check_overdue_tasks()
                
                # Sleep for interval
                time.sleep(self.check_interval)
                
            except Exception as e:
                print(f"Notification check error: {e}")
                time.sleep(self.check_interval)
    
    def _check_daily_summary(self):
        """Check if daily summary should be shown."""
        now = datetime.now()
        summary_time = self.settings.get("daily_summary_time", "09:00")
        
        try:
            hour, minute = map(int, summary_time.split(":"))
            target_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            
            # Show if within 5 minutes of target time and not shown today
            if abs((now - target_time).total_seconds()) < 300 and not self.daily_summary_shown_today:
                tasks = self.storage.get_all_tasks()
                today_tasks = [
                    t for t in tasks 
                    if t.due_date and t.due_date.startswith(now.strftime("%Y-%m-%d"))
                    and t.status != "completed"
                ]
                
                if today_tasks:
                    self.show_notification(
                        "Daily Summary",
                        f"You have {len(today_tasks)} task{'s' if len(today_tasks) != 1 else ''} due today",
                        self.settings.get("notification_duration", 5000),
                        lambda: self._open_tasks_view()
                    )
                    self.daily_summary_shown_today = True
            
            # Reset flag at midnight
            if now.hour == 0 and now.minute == 0:
                self.daily_summary_shown_today = False
                
        except Exception as e:
            print(f"Daily summary check error: {e}")
    
    def _check_due_soon_tasks(self):
        """Check for tasks due within 24 hours."""
        now = datetime.now()
        tomorrow = now + timedelta(days=1)
        
        try:
            tasks = self.storage.get_all_tasks()
        except:
            return
        
        for task in tasks:
            if task.status == "completed" or not task.due_date:
                continue
            
            try:
                due = datetime.fromisoformat(task.due_date)
                hours_until_due = (due - now).total_seconds() / 3600
                
                # Notify if due within 24 hours but not yet overdue
                if 0 < hours_until_due < 24:
                    # Check if we already notified (simple check - could be improved)
                    if not hasattr(task, '_notified_due_soon'):
                        self.show_notification(
                            "Task Due Soon",
                            f"'{task.title}' is due in {int(hours_until_due)} hour{'s' if int(hours_until_due) != 1 else ''}",
                            self.settings.get("notification_duration", 5000),
                            lambda t=task: self._open_task(t)
                        )
                        task._notified_due_soon = True
            except Exception:
                # Silently skip tasks with validation or parsing errors
                continue
    
    def _check_overdue_tasks(self):
        """Check for overdue tasks."""
        now = datetime.now()
        
        try:
            tasks = self.storage.get_all_tasks()
        except:
            return
        
        for task in tasks:
            if task.status == "completed" or not task.due_date:
                continue
            
            try:
                due = datetime.fromisoformat(task.due_date)
                if now > due:
                    # Check if we already notified (every 24 hours)
                    if not hasattr(task, '_notified_overdue') or \
                       (now - task._notified_overdue).total_seconds() > 86400:
                        
                        days_overdue = (now - due).days
                        self.show_notification(
                            "Task Overdue",
                            f"'{task.title}' is {days_overdue} day{'s' if days_overdue != 1 else ''} overdue",
                            self.settings.get("notification_duration", 5000),
                            lambda t=task: self._open_task(t)
                        )
                        task._notified_overdue = now
            except Exception:
                # Silently skip tasks with validation or parsing errors
                continue
    
    def _open_tasks_view(self):
        """Callback to open tasks view."""
        # This will be implemented by main window
        pass
    
    def _open_task(self, task):
        """Callback to open specific task."""
        # This will be implemented by main window
        pass
    
    def update_settings(self, settings: dict):
        """Update notification settings."""
        self.settings.update(settings)
        
        # Restart if enabled status changed
        was_running = self.running
        if settings.get("enabled", True) and not was_running:
            self.start()
        elif not settings.get("enabled", True) and was_running:
            self.stop()
