"""
Chart generation utilities using matplotlib.
"""
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from typing import Dict, List
import os
from pathlib import Path


# Chart styling
CHART_STYLE = 'seaborn-v0_8-darkgrid'
COLORS = {
    'primary': '#E07B53',
    'secondary': '#F4A261',
    'success': '#4CAF50',
    'warning': '#FFA726',
    'error': '#EF5350',
    'info': '#2196F3',
    'purple': '#9C27B0',
    'cyan': '#00BCD4'
}

STATUS_COLORS = {
    'planning': '#2196F3',
    'active': '#4CAF50',
    'paused': '#FFA726',
    'completed': '#66BB6A',
    'archived': '#9E9E9E',
    'todo': '#2196F3',
    'in_progress': '#FFA726',
    'blocked': '#EF5350',
    'low': '#4CAF50',
    'medium': '#FFA726',
    'high': '#EF5350'
}


def get_temp_chart_path(chart_name: str) -> str:
    """Get path for saving temporary chart image."""
    temp_dir = Path(os.environ.get('TEMP', '/tmp')) / 'deskflow_charts'
    temp_dir.mkdir(parents=True, exist_ok=True)
    return str(temp_dir / f"{chart_name}.png")


def generate_pie_chart(data: Dict[str, int], title: str, chart_name: str) -> str:
    """Generate a pie chart."""
    if not data or sum(data.values()) == 0:
        return None
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    labels = list(data.keys())
    sizes = list(data.values())
    colors = [STATUS_COLORS.get(label.lower(), COLORS['primary']) for label in labels]
    
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
           startangle=90, textprops={'fontsize': 10})
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    ax.axis('equal')
    
    filepath = get_temp_chart_path(chart_name)
    plt.tight_layout()
    plt.savefig(filepath, dpi=100, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    
    return filepath


def generate_donut_chart(data: Dict[str, int], title: str, chart_name: str) -> str:
    """Generate a donut chart."""
    if not data or sum(data.values()) == 0:
        return None
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    labels = list(data.keys())
    sizes = list(data.values())
    colors = [STATUS_COLORS.get(label.lower(), COLORS['primary']) for label in labels]
    
    wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors,
                                       autopct='%1.1f%%', startangle=90,
                                       textprops={'fontsize': 10},
                                       pctdistance=0.85)
    
    # Draw circle for donut
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    ax.add_artist(centre_circle)
    
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    ax.axis('equal')
    
    filepath = get_temp_chart_path(chart_name)
    plt.tight_layout()
    plt.savefig(filepath, dpi=100, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    
    return filepath


def generate_bar_chart(data: Dict[str, int], title: str, xlabel: str, ylabel: str, chart_name: str) -> str:
    """Generate a vertical bar chart."""
    if not data:
        return None
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    labels = list(data.keys())
    values = list(data.values())
    
    bars = ax.bar(labels, values, color=COLORS['primary'], alpha=0.8)
    
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel(xlabel, fontsize=11)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.grid(axis='y', alpha=0.3)
    
    # Rotate x labels if too many
    if len(labels) > 10:
        plt.xticks(rotation=45, ha='right')
    
    filepath = get_temp_chart_path(chart_name)
    plt.tight_layout()
    plt.savefig(filepath, dpi=100, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    
    return filepath


def generate_horizontal_bar(data: Dict[str, float], title: str, xlabel: str, chart_name: str) -> str:
    """Generate a horizontal bar chart."""
    if not data:
        return None
    
    fig, ax = plt.subplots(figsize=(10, max(6, len(data) * 0.5)))
    
    labels = list(data.keys())
    values = list(data.values())
    
    y_pos = range(len(labels))
    bars = ax.barh(y_pos, values, color=COLORS['secondary'], alpha=0.8)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=10)
    ax.set_xlabel(xlabel, fontsize=11)
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    ax.grid(axis='x', alpha=0.3)
    
    # Add value labels on bars
    for i, (bar, value) in enumerate(zip(bars, values)):
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height()/2, 
                f'{value:.1f}h',
                ha='left', va='center', fontsize=9, color='black')
    
    filepath = get_temp_chart_path(chart_name)
    plt.tight_layout()
    plt.savefig(filepath, dpi=100, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    
    return filepath


def generate_line_chart(data: Dict[str, int], title: str, xlabel: str, ylabel: str, chart_name: str) -> str:
    """Generate a line chart."""
    if not data:
        return None
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    labels = list(data.keys())
    values = list(data.values())
    
    ax.plot(labels, values, marker='o', linewidth=2, markersize=6,
            color=COLORS['primary'], markerfacecolor=COLORS['secondary'])
    ax.fill_between(range(len(values)), values, alpha=0.2, color=COLORS['primary'])
    
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel(xlabel, fontsize=11)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.grid(True, alpha=0.3)
    
    # Rotate x labels
    if len(labels) > 15:
        plt.xticks(rotation=45, ha='right')
        # Show every nth label to avoid crowding
        nth = max(1, len(labels) // 15)
        for i, label in enumerate(ax.get_xticklabels()):
            if i % nth != 0:
                label.set_visible(False)
    
    filepath = get_temp_chart_path(chart_name)
    plt.tight_layout()
    plt.savefig(filepath, dpi=100, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    
    return filepath
