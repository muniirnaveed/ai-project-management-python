"""Small, dependency-free educational project management model."""
from dataclasses import dataclass, field
from datetime import date
from typing import Dict, List

VALID_STATUSES = {'todo', 'in_progress', 'blocked', 'done'}

@dataclass
class Task:
    id: str
    title: str
    assignee: str
    status: str = 'todo'
    estimated_hours: float = 0.0
    logged_hours: float = 0.0

    def __post_init__(self):
        if not self.id or not self.title or not self.assignee:
            raise ValueError('Task ID, title and assignee are required')
        if self.status not in VALID_STATUSES:
            raise ValueError('Invalid status')
        if self.estimated_hours < 0 or self.logged_hours < 0:
            raise ValueError('Hours cannot be negative')

@dataclass
class Project:
    name: str
    tasks: Dict[str, Task] = field(default_factory=dict)

    def add_task(self, task: Task):
        if task.id in self.tasks:
            raise ValueError('Duplicate task ID')
        self.tasks[task.id] = task

    def update_status(self, task_id: str, status: str):
        if status not in VALID_STATUSES:
            raise ValueError('Invalid status')
        self.tasks[task_id].status = status

    def log_time(self, task_id: str, hours: float):
        if hours <= 0:
            raise ValueError('Logged hours must be positive')
        self.tasks[task_id].logged_hours += hours

    def summary(self) -> dict:
        counts = {status: 0 for status in sorted(VALID_STATUSES)}
        for task in self.tasks.values():
            counts[task.status] += 1
        return {
            'project': self.name,
            'total_tasks': len(self.tasks),
            'statuses': counts,
            'total_logged_hours': round(sum(t.logged_hours for t in self.tasks.values()), 2),
            'completion_percentage': round(100 * counts['done'] / len(self.tasks), 1) if self.tasks else 0.0,
        }

    def daily_status_report(self, report_date: date = None) -> dict:
        report_date = report_date or date.today()
        return {
            'date': report_date.isoformat(),
            **self.summary(),
            'blocked_tasks': [t.title for t in self.tasks.values() if t.status == 'blocked'],
            'completed_tasks': [t.title for t in self.tasks.values() if t.status == 'done'],
        }
