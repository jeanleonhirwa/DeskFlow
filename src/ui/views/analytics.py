"""
Analytics dashboard view with metrics and charts.
"""
import customtkinter as ctk
from typing import Optional
from PIL import Image
import sys
sys.path.append('..')

from ui.components.common import IconButton
from utils.analytics_data import (
    get_project_status_distribution,
    get_tasks_by_status,
    get_tasks_completed_per_day,
    get_time_by_project,
    get_priority_distribution,
    calculate_completion_rate,
    get_best_productivity_day,
    get_most_used_tags,
    get_average_tasks_per_day
)
from utils.chart_generator import (
    generate_pie_chart,
    generate_donut_chart,
    generate_bar_chart,
    generate_horizontal_bar
)


class MetricCard(ctk.CTkFrame):
    """Metric display card."""
    
    def __init__(self, parent, title: str, value: str, subtitle: str = "", **kwargs):
        super().__init__(parent, fg_color=("white", "#2D2D2D"), corner_radius=12, **kwargs)
        
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=20, pady=16)
        
        # Title
        ctk.CTkLabel(
            content,
            text=title,
            font=("Segoe UI", 12),
            text_color="gray60"
        ).pack(anchor="w")
        
        # Value
        ctk.CTkLabel(
            content,
            text=value,
            font=("Segoe UI", 32, "bold")
        ).pack(anchor="w", pady=(4, 0))
        
        # Subtitle
        if subtitle:
            ctk.CTkLabel(
                content,
                text=subtitle,
                font=("Segoe UI", 11),
                text_color="gray60"
            ).pack(anchor="w", pady=(4, 0))


class ChartCard(ctk.CTkFrame):
    """Chart display card."""
    
    def __init__(self, parent, title: str, chart_path: Optional[str] = None, **kwargs):
        super().__init__(parent, fg_color=("white", "#2D2D2D"), corner_radius=12, **kwargs)
        
        # Title
        ctk.CTkLabel(
            self,
            text=title,
            font=("Segoe UI", 14, "bold")
        ).pack(anchor="w", padx=16, pady=(16, 8))
        
        # Chart container
        self.chart_container = ctk.CTkFrame(self, fg_color="transparent")
        self.chart_container.pack(fill="both", expand=True, padx=16, pady=(0, 16))
        
        if chart_path:
            self.display_chart(chart_path)
        else:
            self.show_no_data()
    
    def display_chart(self, chart_path: str):
        """Display chart image."""
        try:
            # Clear container
            for widget in self.chart_container.winfo_children():
                widget.destroy()
            
            # Load and display image
            image = Image.open(chart_path)
            # Resize to fit
            image.thumbnail((800, 400), Image.Resampling.LANCZOS)
            photo = ctk.CTkImage(light_image=image, dark_image=image, size=image.size)
            
            label = ctk.CTkLabel(self.chart_container, image=photo, text="")
            label.image = photo  # Keep reference
            label.pack()
        except Exception as e:
            print(f"Error displaying chart: {e}")
            self.show_no_data()
    
    def show_no_data(self):
        """Show no data message."""
        for widget in self.chart_container.winfo_children():
            widget.destroy()
        
        ctk.CTkLabel(
            self.chart_container,
            text="No data available",
            font=("Segoe UI", 12),
            text_color="gray60"
        ).pack(pady=40)


class AnalyticsView(ctk.CTkScrollableFrame):
    """Analytics dashboard view."""
    
    def __init__(self, parent, storage_manager, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        
        self.storage = storage_manager
        self.date_range = 30  # Default to last 30 days
        
        self._create_ui()
        self.refresh()
    
    def _create_ui(self):
        """Create analytics UI."""
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(20, 10))
        
        # Title
        ctk.CTkLabel(
            header,
            text="Analytics",
            font=("Segoe UI", 24, "bold")
        ).pack(side="left")
        
        # Date range selector
        range_frame = ctk.CTkFrame(header, fg_color="transparent")
        range_frame.pack(side="right")
        
        ctk.CTkLabel(range_frame, text="Date Range:", font=("Segoe UI", 13)).pack(side="left", padx=(0, 8))
        
        self.range_menu = ctk.CTkOptionMenu(
            range_frame,
            values=["Last 7 days", "Last 30 days", "Last 90 days", "All time"],
            command=self._on_range_change,
            width=150,
            font=("Segoe UI", 13)
        )
        self.range_menu.set("Last 30 days")
        self.range_menu.pack(side="left")
        
        IconButton(
            range_frame,
            text="🔄 Refresh",
            command=self.refresh,
            width=100,
            font=("Segoe UI", 13)
        ).pack(side="left", padx=(8, 0))
        
        # Content container
        self.content = ctk.CTkFrame(self, fg_color="transparent")
        self.content.pack(fill="both", expand=True, padx=20, pady=(10, 20))
    
    def refresh(self):
        """Refresh analytics data and charts."""
        # Clear content
        for widget in self.content.winfo_children():
            widget.destroy()
        
        # Load data
        projects = self.storage.get_all_projects()
        tasks = self.storage.get_all_tasks()
        
        if not projects and not tasks:
            self._show_empty_state()
            return
        
        # Render metrics and charts
        self._render_metrics(projects, tasks)
        self._render_charts(projects, tasks)
        self._render_insights(tasks)
    
    def _show_empty_state(self):
        """Show empty state when no data."""
        from ui.components.common import EmptyState
        empty = EmptyState(
            self.content,
            message="No data yet. Create some projects and tasks to see analytics!"
        )
        empty.pack(fill="both", expand=True, pady=100)
    
    def _render_metrics(self, projects, tasks):
        """Render key metrics cards."""
        metrics_frame = ctk.CTkFrame(self.content, fg_color="transparent")
        metrics_frame.pack(fill="x", pady=(0, 16))
        
        # Calculate metrics
        total_projects = len(projects)
        active_projects = len([p for p in projects if p.status == "active"])
        total_tasks = len(tasks)
        active_tasks = len([t for t in tasks if t.status in ["todo", "in_progress"]])
        completion_rate = calculate_completion_rate(tasks, self.date_range)
        completed_this_month = len([p for p in projects if p.status == "completed"])
        
        # Create metric cards in grid
        MetricCard(
            metrics_frame,
            title="Total Projects",
            value=str(total_projects),
            subtitle=f"{active_projects} active"
        ).pack(side="left", fill="both", expand=True, padx=(0, 8))
        
        MetricCard(
            metrics_frame,
            title="Active Tasks",
            value=str(active_tasks),
            subtitle=f"{total_tasks} total"
        ).pack(side="left", fill="both", expand=True, padx=8)
        
        MetricCard(
            metrics_frame,
            title="Completion Rate",
            value=f"{completion_rate:.1f}%",
            subtitle=f"Last {self.date_range} days"
        ).pack(side="left", fill="both", expand=True, padx=8)
        
        MetricCard(
            metrics_frame,
            title="Projects Completed",
            value=str(completed_this_month),
            subtitle="This period"
        ).pack(side="left", fill="both", expand=True, padx=(8, 0))
    
    def _render_charts(self, projects, tasks):
        """Render analytics charts."""
        # Project status distribution
        project_status = get_project_status_distribution(projects)
        if project_status:
            chart_path = generate_pie_chart(
                project_status,
                "Project Status Distribution",
                "project_status"
            )
            chart = ChartCard(self.content, "Project Status Distribution", chart_path)
            chart.pack(fill="x", pady=(0, 16))
        
        # Tasks completed per day
        tasks_per_day = get_tasks_completed_per_day(tasks, self.date_range)
        if tasks_per_day:
            chart_path = generate_bar_chart(
                tasks_per_day,
                f"Tasks Completed - Last {self.date_range} Days",
                "Date",
                "Tasks Completed",
                "tasks_per_day"
            )
            chart = ChartCard(self.content, "Daily Task Completion", chart_path)
            chart.pack(fill="x", pady=(0, 16))
        
        # Tasks by status
        tasks_by_status = get_tasks_by_status(tasks)
        if tasks_by_status:
            chart_path = generate_donut_chart(
                tasks_by_status,
                "Tasks by Status",
                "tasks_status"
            )
            chart = ChartCard(self.content, "Task Status Distribution", chart_path)
            chart.pack(fill="x", pady=(0, 16))
        
        # Time logged by project
        time_by_project = get_time_by_project(projects, tasks)
        if time_by_project:
            chart_path = generate_horizontal_bar(
                time_by_project,
                "Time Logged by Project (Top 10)",
                "Hours",
                "time_by_project"
            )
            chart = ChartCard(self.content, "Time by Project", chart_path)
            chart.pack(fill="x", pady=(0, 16))
        
        # Priority distribution
        priority_dist = get_priority_distribution(tasks)
        if priority_dist:
            chart_path = generate_bar_chart(
                priority_dist,
                "Task Priority Distribution",
                "Priority",
                "Number of Tasks",
                "priority_dist"
            )
            chart = ChartCard(self.content, "Priority Distribution", chart_path)
            chart.pack(fill="x", pady=(0, 16))
    
    def _render_insights(self, tasks):
        """Render productivity insights."""
        insights_frame = ctk.CTkFrame(self.content, fg_color=("white", "#2D2D2D"), corner_radius=12)
        insights_frame.pack(fill="x")
        
        ctk.CTkLabel(
            insights_frame,
            text="📊 Productivity Insights",
            font=("Segoe UI", 16, "bold")
        ).pack(anchor="w", padx=16, pady=(16, 12))
        
        insights_content = ctk.CTkFrame(insights_frame, fg_color="transparent")
        insights_content.pack(fill="x", padx=16, pady=(0, 16))
        
        # Best productivity day
        best_day = get_best_productivity_day(tasks)
        self._add_insight(insights_content, "Best Productivity Day", best_day)
        
        # Average tasks per day
        avg_tasks = get_average_tasks_per_day(tasks, self.date_range)
        self._add_insight(insights_content, "Average Tasks/Day", f"{avg_tasks:.1f}")
        
        # Most used tags
        top_tags = get_most_used_tags(tasks, 5)
        if top_tags:
            tags_str = ", ".join([f"#{tag} ({count})" for tag, count in top_tags])
            self._add_insight(insights_content, "Most Used Tags", tags_str)
    
    def _add_insight(self, parent, label: str, value: str):
        """Add an insight row."""
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", pady=4)
        
        ctk.CTkLabel(
            row,
            text=f"{label}:",
            font=("Segoe UI", 12, "bold"),
            width=200,
            anchor="w"
        ).pack(side="left")
        
        ctk.CTkLabel(
            row,
            text=value,
            font=("Segoe UI", 12),
            text_color="gray60"
        ).pack(side="left")
    
    def _on_range_change(self, value: str):
        """Handle date range change."""
        range_map = {
            "Last 7 days": 7,
            "Last 30 days": 30,
            "Last 90 days": 90,
            "All time": 365 * 10  # 10 years
        }
        self.date_range = range_map.get(value, 30)
        self.refresh()
