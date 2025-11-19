# Desk Flow

A clean, offline-first desktop application for software developers to manage projects, track tasks, and plan daily activities.

## Features

- **Project Management**: Create, organize, and track software development projects
- **Task Management**: Kanban board with drag-and-drop functionality
- **Dark/Light Themes**: Beautiful Claude-inspired interface with theme switching
- **Offline-First**: All data stored locally with automatic backups
- **Cross-Platform**: Works on Windows, macOS, and Linux

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd DeskFlow
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
- Windows: `venv\Scripts\activate`
- macOS/Linux: `source venv/bin/activate`

4. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python src/main.py
```

## Data Storage

All data is stored locally in:
- Windows: `C:\Users\<username>\.deskflow\`
- macOS/Linux: `~/.deskflow/`

## Development Status

Currently in Phase 1 (MVP) development:
- ✅ Project structure
- 🚧 Core data layer
- 🚧 UI framework
- 🚧 Project management module
- 🚧 Task management module

## Technology Stack

- **UI Framework**: CustomTkinter
- **Data Storage**: JSON (local files)
- **Python**: 3.8+

## License

TBD
