# tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from .models import Tasks
from goals.models import Goals


class TestTasksModel(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
                username='testuser', password='12345')
        # Create a test goal
        self.goal = Goals.objects.create(owner=self.user, name="Test Goal")

    def test_create_task(self):
        task = Tasks.objects.create(
            owner=self.user,
            goals=self.goal,
            task_title="Test Task",
            task_details="This is a test task"
        )
        self.assertEqual(task.task_title, "Test Task")
        self.assertEqual(task.task_details, "This is a test task")
        self.assertEqual(task.owner, self.user)
        self.assertEqual(task.goals, self.goal)
        self.assertIsNotNone(task.created_at)
        self.assertIsNotNone(task.updated_at)
        self.assertTrue(task.active)
        self.assertFalse(task.completed)
        self.assertFalse(task.children)

    def test_task_str_method(self):
        task = Tasks.objects.create(owner=self.user, task_title="Test Task")
        self.assertEqual(str(task), f'{task.id} Test Task')

    def test_task_ordering(self):
        task1 = Tasks.objects.create(owner=self.user, task_title="Task 1")
        task2 = Tasks.objects.create(owner=self.user, task_title="Task 2")
        tasks = Tasks.objects.all()
        self.assertEqual(tasks[0], task2)
        self.assertEqual(tasks[1], task1)

    def test_max_length_fields(self):
        # Test task_title field max length
        with self.assertRaises(ValidationError):
            task = Tasks(
                owner=self.user,
                task_title="A" * 51,  # Exceeds max_length of 50
            )
            task.full_clean()

        # Test task_details field max length
        with self.assertRaises(ValidationError):
            task = Tasks(
                owner=self.user,
                task_title="Test Task",
                task_details="A" * 151,  # Exceeds max_length of 150
            )
            task.full_clean()

    def test_blank_and_null_fields(self):
        # Test that blank task_title is not allowed
        with self.assertRaises(ValidationError):
            task = Tasks(owner=self.user, task_title="")
            task.full_clean()

        # Test that blank and null are allowed for certain fields
        task = Tasks.objects.create(
            owner=self.user,
            task_title="Test Task",
            task_details="",
            value=None,
            criteria=None,
            deadline=None
        )
        task.full_clean()  # This should not raise a ValidationError

    def test_nested_tasks(self):
        parent_task = Tasks.objects.create(
                owner=self.user, task_title="Parent Task")
        child_task = Tasks.objects.create(
            owner=self.user,
            task_title="Child Task",
            parent=parent_task
        )
        self.assertEqual(child_task.parent, parent_task)
        self.assertTrue(Tasks.objects.filter(nested_tasks=child_task).exists())

    def test_cascade_delete(self):
        Tasks.objects.create(owner=self.user, task_title="Test Task")
        self.assertEqual(Tasks.objects.count(), 1)
        self.user.delete()
        self.assertEqual(Tasks.objects.count(), 0)

    def test_goal_relationship(self):
        task = Tasks.objects.create(
            owner=self.user, task_title="Test Task", goals=self.goal)
        self.assertEqual(task.goals, self.goal)
        self.assertTrue(self.goal.tasks_for_goals.filter(id=task.id).exists())

    def test_updated_at_auto_update(self):
        task = Tasks.objects.create(owner=self.user, task_title="Test Task")
        original_updated_at = task.updated_at

        # Update the task
        task.task_title = "Updated Task"
        task.save()

        # Refresh from database
        task.refresh_from_db()

        # Check that updated_at has changed
        self.assertGreater(task.updated_at, original_updated_at)

    def test_deadline(self):
        future_date = timezone.now() + timedelta(days=7)
        task = Tasks.objects.create(
            owner=self.user,
            task_title="Test Task",
            deadline=future_date
        )
        self.assertEqual(task.deadline, future_date)

    def test_toggle_completion(self):
        task = Tasks.objects.create(owner=self.user, task_title="Test Task")
        self.assertFalse(task.completed)
        task.completed = True
        task.save()
        task.refresh_from_db()
        self.assertTrue(task.completed)

    def test_model_fields(self):
        task = Tasks.objects.create(owner=self.user, task_title="Test Task")
        expected_fields = [
            'id', 'owner', 'goals', 'children', 'parent', 'created_at',
            'updated_at', 'active', 'deadline', 'task_title', 'task_details',
            'value', 'criteria', 'completed'
        ]
        for field in expected_fields:
            self.assertTrue(hasattr(task, field))
