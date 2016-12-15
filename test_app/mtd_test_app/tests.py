from django.test import TestCase
from .models import DegenerateModel, DegenerateTimestampedModel, ContactPerson, DeliveryRecord, Person


class DegenerateTestCase(TestCase):
    def setUp(self):
        DegenerateModel.objects.create()

    def test_degenerate_model_to_dict(self):
        """This test tests the simplest case"""
        degenerate_model_instance = DegenerateModel.objects.get()
        self.assertEqual(degenerate_model_instance.to_dict(), {
            'id': degenerate_model_instance.id,
        })


class DegenerateTimestampedModelTestCase(TestCase):
    def setUp(self):
        DegenerateTimestampedModel.objects.create()

    def test_degenerate_model_to_dict(self):
        """This test tests skipping fields"""
        degenerate_timestamped_model_instance = DegenerateTimestampedModel.objects.get()
        self.assertEqual(degenerate_timestamped_model_instance.to_dict(), {
            'id': degenerate_timestamped_model_instance.id,
        })


class ContactTestCase(TestCase):
    def setUp(self):
        ContactPerson.objects.create(name="Name", tel="555-55-55", email="name@example.com")

    def test_contact_to_dict(self):
        """This test tests manual field grouping"""
        contact_person = ContactPerson.objects.get()

        self.assertEqual(contact_person.to_dict(), {
            'id': contact_person.id,
            'name': contact_person.name,
            'contacts': {
                'tel': contact_person.tel,
                'email': contact_person.email
            },
        })

        self.assertEqual(contact_person.to_dict(compress_groups=False), {
            'id': contact_person.id,
            'name': contact_person.name,
            'contacts': {
                'tel': contact_person.tel,
                'email': contact_person.email,
                'website': None
            },
        })


class DeliveryRecordTestCase(TestCase):
    def setUp(self):
        DeliveryRecord.objects.create(address_country="Russia", address_city="Moscow", address_street="Red Square")

    def test_delivery_to_dict(self):
        """This test tests prefix field grouping"""

        delivery = DeliveryRecord.objects.get()

        self.assertEqual(delivery.to_dict(), {
            'id': delivery.id,
            'address': {
                'country': delivery.address_country,
                'city': delivery.address_city,
                'street': delivery.address_street,
            }
        })

        self.assertEqual(delivery.to_dict(compress_prefixes=False), {
            'id': delivery.id,
            'address': {
                'country': delivery.address_country,
                'state': None,
                'city': delivery.address_city,
                'street': delivery.address_street
            }
        })


class PersonTestCase(TestCase):
    def setUp(self):
        Person.objects.create(first_name="Ivo", nickname="Super", last_name="Bobul", middle_name="Tarasovich",
                              actually_exists=False, has_superpowers=True,
                              tel="333-55-55", email="super.ivo@bobul.com", website="https://super.ivo.bobul.com",
                              address_country="Ukraine", address_city="Kiev", address_street="Tarasa Shevchenko")

    def test_person_to_dict(self):
        """This test tests both prefix and manual field grouping, as well as field skipping"""

        person = Person.objects.get()

        self.assertEqual(person.to_dict(), {
            'name': {
                'first_name': person.first_name,
                'middle_name': person.middle_name,
                'last_name': person.last_name,
            },
            'nickname': person.nickname,
            'has_superpowers': person.has_superpowers,
            'contacts': {
                'tel': person.tel,
                'email': person.email,
                'website': person.website
            },
            'address': {
                'country': person.address_country,
                'city': person.address_city,
                'street': person.address_street
            }
        })