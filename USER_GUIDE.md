# Desk Flow - User Guide

## Table of Contents
1. [Getting Started](#getting-started)
2. [Projects](#projects)
3. [Tasks](#tasks)
4. [Daily Planner](#daily-planner)
5. [Analytics](#analytics)
6. [Time Tracking](#time-tracking)
7. [Task Dependencies](#task-dependencies)
8. [Keyboard Shortcuts](#keyboard-shortcuts)
9. [Settings](#settings)
10. [Data Management](#data-management)
11. [Troubleshooting](#troubleshooting)

---

## Getting Started

### First Launch
1. Launch Desk Flow
2. You'll see the Projects view (empty on first run)
3. Click **"+ New Project"** to create your first project
4. Fill in project details and click **"Save Project"**

### Navigation
Use the top navigation bar to switch between views:
- **Projects** - Manage all your projects
- **Tasks** - Kanban board for tasks
- **Daily Planner** - Plan your day with time blocks
- **Analytics** - View productivity metrics

---

## Projects

### Creating a Project
1. Click **"+ New Project"**
2. Fill in:
   - **Name** (required)
   - **Description**
   - **Status** (Planning, Active, Paused, Completed, Archived)
   - **Color** (pick from palette)
   - **Due Date** (YYYY-MM-DD)
   - **Tech Stack** (comma-separated)
   - **Tags** (comma-separated)
3. Click **"Save Project"**

### Managing Milestones
1. Open a project
2. Scroll to **Milestones** section
3. Enter milestone name and target date
4. Click **"Add Milestone"**
5. Check off completed milestones

### Editing/Deleting
- Click any project card to edit
- Click **"Delete"** to remove (with confirmation)

---

## Tasks

### Kanban Board
Tasks are organized in 4 columns:
- **To Do** - Not started
- **In Progress** - Currently working
- **Blocked** - Waiting on something
- **Completed** - Done

### Creating a Task
1. Click **"+ New Task"**
2. Fill in details:
   - **Title** (required)
   - **Project** (optional)
   - **Status & Priority**
   - **Description**
   - **Due Date**
   - **Tags**
   - **Blocked Reason** (if status is Blocked)
   - **Dependencies** (tasks that must complete first)
3. Click **"Save Task"**

### Search & Filter
- **Search bar** - Type to filter by title/description
- **Priority filter** - Show only High/Medium/Low
- **Project filter** - Show tasks for specific project

---

## Daily Planner

### Focus Goal
Set your main goal for the day at the top of the planner.

### Scheduled Tasks
- Select a date from calendar
- Click **"Schedule Task"** 
- Choose from your tasks
- Task appears in scheduled section

### Time Blocks
1. Click **"Add Time Block"**
2. Enter:
   - **Title** (e.g., "Team Meeting")
   - **Start Time** (HH:MM)
   - **End Time** (HH:MM)
3. Click **"Add Block"**

### Notes & Mood
- **Notes section** - Jot down thoughts for the day
- **Mood tracker** - Rate your day (1-5 stars)

---

## Analytics

### Metrics Cards
Top row shows:
- **Total Projects** with active count
- **Active Tasks** with total count
- **Completion Rate** for date range
- **Projects Completed** in period

### Charts
- **Project Status Distribution** - Pie chart
- **Daily Task Completion** - Bar chart by date
- **Task Status** - Donut chart
- **Time Logged by Project** - Horizontal bars
- **Priority Distribution** - Bar chart

### Date Ranges
Change timeframe:
- Last 7 days
- Last 30 days (default)
- Last 90 days
- All time

### Productivity Insights
- **Best Day** - Day of week with most completions
- **Avg Tasks/Day** - Your daily average
- **Most Used Tags** - Your top 5 tags

---

## Time Tracking

### Starting Timer
1. Open any task
2. Scroll to **Time Tracking** section
3. Click **"▶ Start"**
4. Timer starts counting
5. Task card shows "⏱️ Timer running"

### Stopping Timer
1. Open task with running timer
2. Click **"⏸ Stop"**
3. Time is added to **Total Logged**
4. Timer resets to 00:00:00

### Timer Persistence
- Timer runs even if dialog is closed
- Timer survives app restart
- Time is auto-saved every update

### Viewing Logged Time
- **In task form**: See "Total Logged: X.XX hours"
- **In analytics**: See time by project chart

---

## Task Dependencies

### Adding Dependencies
1. Create/edit a task
2. Scroll to **Dependencies** section
3. Check tasks that must complete first
4. Save task

### Visual Indicators
- Task card shows "🔗 2 dependencies"
- Dependencies list shown in task form

### Completion Blocking
- Cannot mark task complete if dependencies incomplete
- Dialog shows which tasks are blocking
- Complete dependencies first

### Circular Dependency Prevention
- System detects circular references (A→B→A)
- Shows error: "Would create circular dependency"
- Fix by choosing different dependency

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl + 1-4` | Switch between views |
| `Ctrl + N` | New item (context-aware) |
| `Ctrl + F` | Focus search |
| `Ctrl + ,` | Open Settings |
| `Ctrl + T` | Toggle theme |
| `Ctrl + Q` | Quit app |
| `Escape` | Close dialog |

See [KEYBOARD_SHORTCUTS.md](KEYBOARD_SHORTCUTS.md) for full list.

---

## Settings

### Appearance
- **Theme**: Light, Dark, or System
- **Project Color**: Default color for new projects

### General
- **Work Hours**: Start and end times
- **Notifications**: Enable/disable (when implemented)

### Data & Backup
- **Manual Backup**: Create backup now
- **Auto Backup**: Toggle automatic backups
- **Clear All Data**: Delete all data (with backup)
- **Export**: Save data to CSV or JSON
- **Import**: Restore from JSON backup

### About
- Version number
- Data storage location

---

## Data Management

### Automatic Backups
- Backs up daily to `~/.deskflow/backups/`
- Keeps last 7 days of backups
- Runs on app launch if > 24h since last backup

### Manual Export
1. Open Settings (Ctrl+,)
2. Go to **Data & Backup** tab
3. Choose export format:
   - **Export All (JSON)** - Complete backup
   - **Export Projects (CSV)** - Spreadsheet format
   - **Export Tasks (CSV)** - Spreadsheet format
4. Choose save location

### Import Data
1. Settings → Data & Backup
2. Click **"Import from JSON"**
3. Select previously exported JSON file
4. Data is merged with existing

### Data Location
All data stored in:
- **Windows**: `C:\Users\<username>\.deskflow\`
- **Mac**: `/Users/<username>/.deskflow/`
- **Linux**: `/home/<username>/.deskflow/`

---

## Troubleshooting

### App Won't Start
- Check if Python is installed (if running from source)
- Verify all dependencies installed: `pip install -r requirements.txt`
- Check error logs in `~/.deskflow/logs/error.log`

### Data Not Saving
- Ensure write permissions to `~/.deskflow/` directory
- Check disk space available
- Review error.log for details

### Charts Not Showing
- Ensure matplotlib is installed: `pip install matplotlib`
- Create some tasks/projects first (charts need data)
- Check date range filter

### Timer Not Resuming
- Check `tasks.json` for timer_running: true
- Verify timer_start_time is valid ISO timestamp
- Restart app to recover timer state

### Corrupted Data
- Automatic backups in `~/.deskflow/backups/`
- Rename current JSON file
- Copy backup file to data directory
- Restart app

### Search Not Working
- Check spelling
- Search looks in title AND description
- Case-insensitive matching
- Clear filters if applied

---

## Tips & Best Practices

### Productivity Tips
1. **Set Daily Focus Goal** - Start each day with one main objective
2. **Use Time Tracking** - Track where time actually goes
3. **Dependencies** - Break down complex tasks with dependencies
4. **Tags** - Use consistent tags for easy filtering
5. **Regular Backups** - Export data weekly for safety

### Organization Tips
1. **Archive Old Projects** - Keep active list clean
2. **Clear Completed** - Move done tasks to completed
3. **Color Coding** - Use consistent colors per project type
4. **Milestones** - Break projects into milestones
5. **Analytics** - Review weekly to spot patterns

### Keyboard Workflow
Power user workflow:
1. `Ctrl + 2` - Jump to Tasks
2. `Ctrl + F` - Search for task
3. `Ctrl + N` - Create new task
4. Fill form and save
5. `Ctrl + 4` - Check Analytics

---

## Getting Help

### Resources
- **Keyboard Shortcuts**: KEYBOARD_SHORTCUTS.md
- **Error Logs**: ~/.deskflow/logs/error.log
- **Data Files**: ~/.deskflow/data/

### Common Questions

**Q: Can I sync across devices?**
A: Currently local-only. Export/import JSON to transfer manually.

**Q: Is my data private?**
A: Yes, all data stored locally on your computer.

**Q: Can I customize colors?**
A: Project colors selectable from predefined palette.

**Q: Does it work offline?**
A: Yes, fully offline application.

---

*Desk Flow v1.0.0 - Built for productivity*
