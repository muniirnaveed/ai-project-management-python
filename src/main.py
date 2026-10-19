"""Run: python -m src.main"""
import json
from .project_manager import Project, Task


def main():
    project = Project('Website Launch')
    project.add_task(Task('T-001', 'Design homepage', 'Ayesha', 'done', 5, 4.5))
    project.add_task(Task('T-002', 'Build API', 'Ali', 'in_progress', 8, 3))
    project.add_task(Task('T-003', 'Review launch checklist', 'Sara', 'blocked', 2))
    print(json.dumps(project.daily_status_report(), indent=2))


if __name__ == '__main__':
    main()
