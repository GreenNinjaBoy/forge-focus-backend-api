# tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Goals


class TestGoalsModel(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser', password='12345')

    def test_create_goal(self):
        goal = Goals.objects.create(
            owner=self.user,
            name="Test Goal",
            reason="This is a test reason"
        )
        self.assertEqual(goal.name, "Test Goal")
        self.assertEqual(goal.reason, "This is a test reason")
        self.assertEqual(goal.owner, self.user)
        self.assertIsNotNone(goal.created_at)
        self.assertIsNotNone(goal.updated_at)

    def test_goal_str_method(self):
        goal = Goals.objects.create(owner=self.user, name="Test Goal")
        self.assertEqual(str(goal), f'{goal.id} Test Goal')

    def test_goal_ordering(self):
        goal1 = Goals.objects.create(owner=self.user, name="Goal 1")
        goal2 = Goals.objects.create(owner=self.user, name="Goal 2")
        goals = Goals.objects.all()
        self.assertEqual(goals[0], goal2)
        self.assertEqual(goals[1], goal1)

    def test_max_length_name(self):
        # Test name field max length
        with self.assertRaises(ValidationError):
            goal = Goals(
                owner=self.user,
                name="A" * 51,  # Exceeds max_length of 50
                reason="Test reason"
            )
            goal.full_clean()

    def test_blank_fields(self):
        # Test that blank name is not allowed
        with self.assertRaises(ValidationError):
            goal = Goals(owner=self.user, name="", reason="Test reason")
            goal.full_clean()

        # Test that blank reason is allowed
        goal = Goals(owner=self.user, name="Test Goal", reason="")
        goal.full_clean()  # This should not raise a ValidationError

    def test_null_reason(self):
        goal = Goals.objects.create(
            owner=self.user, name="Test Goal", reason=None)
        self.assertIsNone(goal.reason)

    def test_image_upload(self):
        # Create a simple image file
        image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'',  # Empty content for this test
            content_type='image/jpeg'
        )

        goal = Goals.objects.create(
            owner=self.user,
            name="Test Goal",
            image=image
        )
        self.assertTrue(goal.image.name.startswith('images/'))

    def test_default_image(self):
        goal = Goals.objects.create(owner=self.user, name="Test Goal")
        self.assertEqual(goal.image.name, '../default_post_pdrfdn')

    def test_cascade_delete(self):
        Goals.objects.create(owner=self.user, name="Test Goal")
        self.assertEqual(Goals.objects.count(), 1)
        self.user.delete()
        self.assertEqual(Goals.objects.count(), 0)

    def test_updated_at_auto_update(self):
        goal = Goals.objects.create(owner=self.user, name="Test Goal")
        original_updated_at = goal.updated_at

        # Update the goal
        goal.name = "Updated Goal"
        goal.save()

        # Refresh from database
        goal.refresh_from_db()

        # Check that updated_at has changed
        self.assertNotEqual(goal.updated_at, original_updated_at)

    def test_model_fields(self):
        goal = Goals.objects.create(owner=self.user, name="Test Goal")
        self.assertTrue(hasattr(goal, 'id'))
        self.assertTrue(hasattr(goal, 'owner'))
        self.assertTrue(hasattr(goal, 'created_at'))
        self.assertTrue(hasattr(goal, 'updated_at'))
        self.assertTrue(hasattr(goal, 'name'))
        self.assertTrue(hasattr(goal, 'reason'))
        self.assertTrue(hasattr(goal, 'image'))
