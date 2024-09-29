# tests.py
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.forms import modelform_factory
from .models import Contact


class TestContactModel(TestCase):
    def test_create_contact(self):
        contact = Contact.objects.create(
            name="John Doe",
            email="john@example.com",
            message="This is a test message"
        )
        self.assertEqual(contact.name, "John Doe")
        self.assertEqual(contact.email, "john@example.com")
        self.assertEqual(contact.message, "This is a test message")
        self.assertIsNotNone(contact.created_at)

    def test_contact_str_method(self):
        contact = Contact.objects.create(
            name="Jane Doe",
            email="jane@example.com",
            message="Another test message"
        )
        self.assertEqual(str(contact), "Another test message")

    def test_contact_ordering(self):
        contact1 = Contact.objects.create(
            name="User1",
            email="user1@example.com",
            message="Message 1"
        )
        contact2 = Contact.objects.create(
            name="User2",
            email="user2@example.com",
            message="Message 2"
        )
        contacts = Contact.objects.all()
        self.assertEqual(contacts[0], contact2)
        self.assertEqual(contacts[1], contact1)

        def test_max_length_fields(self):
            ContactForm = modelform_factory(Contact, fields='__all__')

            # Test name field
            form = ContactForm(data={
                'name': 'A' * 51,  # Exceeds max_length of 50
                'email': 'test@example.com',
                'message': 'Test message'
            })
            self.assertFalse(form.is_valid())
            self.assertIn('name', form.errors)

            # Test email field
            form = ContactForm(data={
                'name': 'Test Name',
                'email': 'A' * 241 + '@example.com',  # Exceeds max_length
                'message': 'Test message'
            })
            self.assertFalse(form.is_valid())
            self.assertIn('email', form.errors)

            # Test message field
            form = ContactForm(data={
                'name': 'Test Name',
                'email': 'test@example.com',
                'message': 'A' * 251  # Exceeds max_length of 250
            })
            self.assertFalse(form.is_valid())
            self.assertIn('message', form.errors)

            # Test that valid lengths don't raise any validation errors
            form = ContactForm(data={
                'name': 'A' * 50,
                'email': 'A' * 240 + '@example.com',
                'message': 'A' * 250
            })
            if not form.is_valid():
                print("Form errors:", form.errors)
                for field, errors in form.errors.items():
                    print(f"Field '{field}' errors:", errors)
                print("Form data:", form.data)
            self.assertTrue(form.is_valid())

    def test_blank_fields(self):
        contact = Contact(name="", email="", message="")
        with self.assertRaises(ValidationError):
            contact.full_clean()

    def test_invalid_email(self):
        contact = Contact(
            name="Test", email="invalid_email", message="Test message")
        with self.assertRaises(ValidationError):
            contact.full_clean()

    def test_model_fields(self):
        contact = Contact.objects.create(
            name="Test User",
            email="test@example.com",
            message="Test message"
        )
        self.assertTrue(hasattr(contact, 'id'))
        self.assertTrue(hasattr(contact, 'name'))
        self.assertTrue(hasattr(contact, 'email'))
        self.assertTrue(hasattr(contact, 'message'))
        self.assertTrue(hasattr(contact, 'created_at'))

    def test_created_at_auto_now_add(self):
        contact = Contact.objects.create(
            name="Test User",
            email="test@example.com",
            message="Test message"
        )
        self.assertIsNotNone(contact.created_at)
        original_created_at = contact.created_at

        # Update the contact
        contact.name = "Updated Name"
        contact.save()

        # Refresh from database
        contact.refresh_from_db()

        # Check that created_at hasn't changed
        self.assertEqual(contact.created_at, original_created_at)
