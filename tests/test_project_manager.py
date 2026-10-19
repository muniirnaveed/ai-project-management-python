import unittest
from datetime import date
from src.project_manager import Project, Task


class ProjectManagerTests(unittest.TestCase):
    def setUp(self):
        self.project = Project('Demo')
        self.project.add_task(Task('1', 'Write docs', 'Ayesha'))

    def test_add_task(self):
        self.assertEqual(self.project.summary()['total_tasks'], 1)

    def test_duplicate_task_rejected(self):
        with self.assertRaises(ValueError):
            self.project.add_task(Task('1', 'Other', 'Ali'))

    def test_invalid_status_rejected(self):
        with self.assertRaises(ValueError):
            Task('2', 'Invalid', 'Ali', 'unknown')

    def test_update_status(self):
        self.project.update_status('1', 'done')
        self.assertEqual(self.project.summary()['completion_percentage'], 100.0)

    def test_log_time(self):
        self.project.log_time('1', 1.25)
        self.assertEqual(self.project.summary()['total_logged_hours'], 1.25)

    def test_negative_time_rejected(self):
        with self.assertRaises(ValueError):
            self.project.log_time('1', -1)

    def test_daily_report(self):
        self.project.update_status('1', 'blocked')
        report = self.project.daily_status_report(date(2026, 10, 19))
        self.assertEqual(report['date'], '2026-10-19')
        self.assertEqual(report['blocked_tasks'], ['Write docs'])

    def test_empty_project(self):
        self.assertEqual(Project('Empty').summary()['completion_percentage'], 0)


if __name__ == '__main__':
    unittest.main()
