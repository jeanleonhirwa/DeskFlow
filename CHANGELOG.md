# Changelog

All notable changes to Desk Flow will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-11-22

### Added

**Phase 1 - MVP**
- Project management with custom colors and milestones
- Task management with Kanban board (4 columns)
- Basic CRUD operations for projects and tasks
- Light and dark theme support
- JSON-based local data storage
- Automatic backup system (7-day retention)
- Corrupted file recovery
- Settings panel

**Phase 2 - Core Features**
- Daily Planner module with calendar integration
- Focus goal setting
- Time blocks for scheduling
- Task scheduling in Daily Planner
- Weekly overview
- Mood tracking
- Enhanced project features (milestones, progress tracking)
- Search and filter functionality for tasks

**Phase 3 - Enhanced Features**
- Analytics Dashboard with 5 chart types
- Key productivity metrics (completion rates, project stats)
- Date range filtering (7/30/90 days, all time)
- Productivity insights (best day, avg tasks/day, top tags)
- Export functionality (CSV for projects/tasks, JSON for all data)
- Import functionality (JSON restore)
- Data & Backup management in Settings

**Phase 3.5 - Skipped Features**
- Task Dependencies UI with multi-select
- Circular dependency validation
- Completion blocking based on dependencies
- Visual dependency badges on task cards
- Time Tracking system with persistent timer
- Timer widget (Start/Stop/Reset)
- Automatic hour logging
- Timer running indicators

**Phase 4 - Polish**
- Comprehensive keyboard shortcuts (Ctrl+1-4, Ctrl+N, Ctrl+F, etc.)
- Context-aware actions (Ctrl+N creates different items per view)
- Quick navigation shortcuts
- Centralized error handling with logging
- User-friendly error dialogs
- Success notifications
- Error logs in `~/.deskflow/logs/error.log`

### Technical Improvements
- Atomic file writes to prevent data corruption
- Background timer updates
- Optimized chart generation
- Matplotlib integration for analytics
- Type hints throughout codebase
- Modular architecture with clean separation

### Documentation
- Comprehensive USER_GUIDE.md
- KEYBOARD_SHORTCUTS.md reference
- Updated README.md
- Inline code documentation

## [Unreleased]

### Planned
- Notifications and reminders system
- Enhanced dark mode aesthetics
- Drag & Drop for Kanban board
- Project templates
- Daily plan templates
- Performance optimizations
- Packaging for distribution (Windows .exe, macOS .app, Linux AppImage)

---

## Version History

### v1.0.0 (Initial Release)
Complete desktop task management application with projects, tasks, daily planning, analytics, time tracking, and dependencies management.

---

*For detailed feature documentation, see [USER_GUIDE.md](USER_GUIDE.md)*
