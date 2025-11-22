"""
Advanced chart generators for additional analytics visualizations.
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.figure import Figure
import tempfile
from pathlib import Path
from typing import List, Dict, Tuple
from datetime import datetime, timedelta
from collections import Counter


temp_dir = Path(tempfile.gettempdir()) / "deskflow_charts"
temp_dir.mkdir(exist_ok=True)


# Color mapping
STATUS_COLORS = {
    "planning": "#3498db",
    "active": "#2ecc71",
    "paused": "#f39c12",
    "completed": "#95a5a6",
    "archived": "#7f8c8d",
    "todo": "#3498db",
    "in_progress": "#f39c12",
    "blocked": "#e74c3c",
   "completed": "#2ecc71"
}

PRIORITY_COLORS = {
    "low": "#95a5a6",
    "medium": "#f39c12",
    "high": "#e74c3c"
}


def generate_weekly_heatmap(data: Dict[str, int], filename: str = "weekly_heatmap.png") -> str:
    """
    Generate weekly productivity heatmap showing tasks completed per day.
    
    Args:
        data: Dict with date strings as keys and task count as values
        filename: Output filename
    
    Returns:
        Path to saved image
    """
    fig, ax = plt.subplots(figsize=(10, 4))
    fig.patch.set_facecolor('#FAFAFA')
    ax.set_facecolor('#FAFAFA')
    
    # Prepare data - group by week
    if not data:
        # Empty state
        ax.text(0.5, 0.5, 'No data available', ha='center', va='center',
                transform=ax.transAxes, fontsize=14, color='gray')
        ax.axis('off')
    else:
        # Convert to datetime and group by week
        dates = sorted([datetime.fromisoformat(d) for d in data.keys()])
        
        # Get week range
        weeks = {}
        for date in dates:
            week_start = date - timedelta(days=date.weekday())
            week_key = week_start.strftime("%Y-W%W")
            day_name = date.strftime("%a")
            
            if week_key not in weeks:
                weeks[week_key] = {d: 0 for d in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]}
            
            day_abbr = date.strftime("%a")
            weeks[week_key][day_abbr] += data[date.strftime("%Y-%m-%d")]
        
        # Prepare matrix
        week_labels = list(weeks.keys())
        day_labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        
        matrix = []
        for week in week_labels:
            matrix.append([weeks[week][day] for day in day_labels])
        
        # Create heatmap
        im = ax.imshow(matrix, cmap='YlOrRd', aspect='auto')
        
        # Set ticks
        ax.set_xticks(range(len(day_labels)))
        ax.set_xticklabels(day_labels)
        ax.set_yticks(range(len(week_labels)))
        ax.set_yticklabels([f"Week {i+1}" for i in range(len(week_labels))])
        
        # Add text annotations
        for i in range(len(week_labels)):
            for j in range(len(day_labels)):
                text = ax.text(j, i, matrix[i][j],
                             ha="center", va="center", color="black", fontsize=10)
        
        # Colorbar
        plt.colorbar(im, ax=ax, label='Tasks Completed')
        
        ax.set_title('Weekly Productivity Heatmap', fontsize=14, pad=15)
    
    plt.tight_layout()
    output_path = temp_dir / filename
    plt.savefig(output_path, dpi=100, bbox_inches='tight', facecolor='#FAFAFA')
    plt.close()
    
    return str(output_path)


def generate_trend_area_chart(dates: List[str], values: List[int], 
                               filename: str = "trend_area.png") -> str:
    """
    Generate area chart showing cumulative task completion trend.
    
    Args:
        dates: List of date strings
        values: List of task counts per date
        filename: Output filename
    
    Returns:
        Path to saved image
    """
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor('#FAFAFA')
    ax.set_facecolor('#FAFAFA')
    
    if not dates or not values:
        ax.text(0.5, 0.5, 'No data available', ha='center', va='center',
                transform=ax.transAxes, fontsize=14, color='gray')
        ax.axis('off')
    else:
        # Calculate cumulative
        cumulative = []
        total = 0
        for v in values:
            total += v
            cumulative.append(total)
        
        # Plot area chart
        ax.fill_between(range(len(dates)), cumulative, alpha=0.3, color='#2ecc71')
        ax.plot(range(len(dates)), cumulative, color='#27ae60', linewidth=2)
        
        # Format
        ax.set_xlabel('Date', fontsize=11)
        ax.set_ylabel('Cumulative Tasks Completed', fontsize=11)
        ax.set_title('Task Completion Trend', fontsize=14, pad=15)
        
        # X-axis labels (show every few dates)
        step = max(1, len(dates) // 10)
        ax.set_xticks(range(0, len(dates), step))
        ax.set_xticklabels([dates[i] for i in range(0, len(dates), step)], rotation=45)
        
        ax.grid(True, alpha=0.3, linestyle='--')
    
    plt.tight_layout()
    output_path = temp_dir / filename
    plt.savefig(output_path, dpi=100, bbox_inches='tight', facecolor='#FAFAFA')
    plt.close()
    
    return str(output_path)


def generate_priority_matrix(data: Dict[str, Dict[str, int]], 
                             filename: str = "priority_matrix.png") -> str:
    """
    Generate stacked bar chart showing priority vs completion status.
    
    Args:
        data: Dict like {"high": {"completed": 10, "incomplete": 5}, ...}
        filename: Output filename
    
    Returns:
        Path to saved image
    """
    fig, ax = plt.subplots(figsize=(8, 5))
    fig.patch.set_facecolor('#FAFAFA')
    ax.set_facecolor('#FAFAFA')
    
    if not data:
        ax.text(0.5, 0.5, 'No data available', ha='center', va='center',
                transform=ax.transAxes, fontsize=14, color='gray')
        ax.axis('off')
    else:
        priorities = list(data.keys())
        completed = [data[p].get("completed", 0) for p in priorities]
        incomplete = [data[p].get("incomplete", 0) for p in priorities]
        
        x = range(len(priorities))
        width = 0.5
        
        # Stacked bars
        ax.bar(x, completed, width, label='Completed', color='#2ecc71')
        ax.bar(x, incomplete, width, bottom=completed, label='Incomplete', color='#e74c3c')
        
        ax.set_xlabel('Priority', fontsize=11)
        ax.set_ylabel('Number of Tasks', fontsize=11)
        ax.set_title('Priority vs Completion Status', fontsize=14, pad=15)
        ax.set_xticks(x)
        ax.set_xticklabels([p.capitalize() for p in priorities])
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y', linestyle='--')
    
    plt.tight_layout()
    output_path = temp_dir / filename
    plt.savefig(output_path, dpi=100, bbox_inches='tight', facecolor='#FAFAFA')
    plt.close()
    
    return str(output_path)


def generate_tag_usage_chart(tags: Dict[str, int], filename: str = "tag_usage.png", 
                             top_n: int = 10) -> str:
    """
    Generate horizontal bar chart of most used tags.
    
    Args:
        tags: Dict with tag names as keys and usage count as values
        filename: Output filename
        top_n: Show top N tags
    
    Returns:
        Path to saved image
    """
    fig, ax = plt.subplots(figsize=(8, 6))
    fig.patch.set_facecolor('#FAFAFA')
    ax.set_facecolor('#FAFAFA')
    
    if not tags:
        ax.text(0.5, 0.5, 'No tags used yet', ha='center', va='center',
                transform=ax.transAxes, fontsize=14, color='gray')
        ax.axis('off')
    else:
        # Sort and get top N
        sorted_tags = sorted(tags.items(), key=lambda x: x[1], reverse=True)[:top_n]
        tag_names = [t[0] for t in sorted_tags]
        tag_counts = [t[1] for t in sorted_tags]
        
        # Horizontal bar chart
        y_pos = range(len(tag_names))
        ax.barh(y_pos, tag_counts, color='#3498db')
        
        ax.set_yticks(y_pos)
        ax.set_yticklabels(tag_names)
        ax.invert_yaxis()  # Top tag at top
        ax.set_xlabel('Usage Count', fontsize=11)
        ax.set_title(f'Top {len(tag_names)} Most Used Tags', fontsize=14, pad=15)
        ax.grid(True, alpha=0.3, axis='x', linestyle='--')
        
        # Add value labels
        for i, v in enumerate(tag_counts):
            ax.text(v + 0.5, i, str(v), va='center')
    
    plt.tight_layout()
    output_path = temp_dir / filename
    plt.savefig(output_path, dpi=100, bbox_inches='tight', facecolor='#FAFAFA')
    plt.close()
    
    return str(output_path)
