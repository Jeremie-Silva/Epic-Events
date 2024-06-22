from unittest import TestCase
from sqlalchemy import Enum as SQLEnum
from app.core.models import (
    Role,
    User,
    Customer,
    Contract,
    Event,
    Base,
)
from freezegun import freeze_time


@freeze_time("2024-04-29")
class UserTests(TestCase):
    def setUp(self):
        self.user = User()

    def test_user_inherits(self):
        self.assertIsInstance(self.user, User)
        self.assertIsInstance(self.user, Base)

    def test_user_tablename(self):
        self.assertEqual(self.user.__tablename__, "user")

    def test_user_primary_key(self):
        self.assertTrue(self.user.__table__.columns["id"].primary_key)

    def test_user_role_enum(self):
        self.assertIsInstance(self.user.__table__.columns["role"].type, SQLEnum)

    def test_user_declarated_fields(self):
        self.assertEqual(
            self.user.__table__.columns.keys(),
            ["id", "name", "password", "role", "creation_date", "last_update"]
        )

    def test_user_required_fields(self):
        self.assertFalse(self.user.__table__.columns["name"].nullable)
        self.assertFalse(self.user.__table__.columns["password"].nullable)

    def test_user_unique_fields(self):
        self.assertTrue(self.user.__table__.columns["name"].unique)

    def test_user_autoincrement(self):
        self.assertTrue(self.user.__table__.columns["id"].autoincrement)

    def test_user_index_values(self):
        self.assertTrue(self.user.__table__.columns["name"].index)


@freeze_time("2024-04-29")
class CustomerTests(TestCase):
    def setUp(self):
        self.customer = Customer()

    def test_customer_inherits(self):
        self.assertIsInstance(self.customer, Customer)
        self.assertIsInstance(self.customer, Base)

    def test_customer_tablename(self):
        self.assertEqual(self.customer.__tablename__, "customer")

    def test_customer_primary_key(self):
        self.assertTrue(self.customer.__table__.columns["id"].primary_key)

    def test_customer_foreign_keys(self):
        self.assertTrue(self.customer.__table__.columns["salesman_id"].foreign_keys)

    def test_customer_declarated_fields(self):
        self.assertEqual(
            self.customer.__table__.columns.keys(),
            ["id", "salesman_id", "name", "email", "phone", "company_name", "creation_date", "last_update"]
        )

    def test_customer_required_fields(self):
        self.assertFalse(self.customer.__table__.columns["name"].nullable)

    def test_customer_unique_fields(self):
        self.assertTrue(self.customer.__table__.columns["name"].unique)

    def test_customer_autoincrement(self):
        self.assertTrue(self.customer.__table__.columns["id"].autoincrement)

    def test_customer_index_values(self):
        self.assertTrue(self.customer.__table__.columns["name"].index)


@freeze_time("2024-04-29")
class ContractTests(TestCase):
    def setUp(self):
        self.contract = Contract()

    def test_contract_inherits(self):
        self.assertIsInstance(self.contract, Contract)
        self.assertIsInstance(self.contract, Base)

    def test_contract_tablename(self):
        self.assertEqual(self.contract.__tablename__, "contract")

    def test_contract_primary_key(self):
        self.assertTrue(self.contract.__table__.columns["id"].primary_key)

    def test_contract_foreign_keys(self):
        self.assertTrue(self.contract.__table__.columns["customer_id"].foreign_keys)
        self.assertTrue(self.contract.__table__.columns["salesman_id"].foreign_keys)

    def test_contract_declarated_fields(self):
        self.assertEqual(
            self.contract.__table__.columns.keys(),
            ["id", "customer_id", "salesman_id", "amount_total", "amount_outstanding", "creation_date", "last_update", "state"]
        )

    def test_contract_state_enum(self):
        self.assertIsInstance(self.contract.__table__.columns["state"].type, SQLEnum)

    def test_contract_autoincrement(self):
        self.assertTrue(self.contract.__table__.columns["id"].autoincrement)

    def test_contract_index_values(self):
        self.assertTrue(self.contract.__table__.columns["state"].index)


@freeze_time("2024-04-29")
class EventTests(TestCase):
    def setUp(self):
        self.event = Event()

    def test_event_inherits(self):
        self.assertIsInstance(self.event, Event)
        self.assertIsInstance(self.event, Base)

    def test_event_tablename(self):
        self.assertEqual(self.event.__tablename__, "event")

    def test_event_primary_key(self):
        self.assertTrue(self.event.__table__.columns["id"].primary_key)

    def test_event_foreign_keys(self):
        self.assertTrue(self.event.__table__.columns["contract_id"].foreign_keys)
        self.assertTrue(self.event.__table__.columns["customer_id"].foreign_keys)
        self.assertTrue(self.event.__table__.columns["support_contact_id"].foreign_keys)

    def test_event_declarated_fields(self):
        self.assertEqual(
            self.event.__table__.columns.keys(),
            ["id", "name", "contract_id", "customer_id", "start_date", "end_date", "support_contact_id", "location", "attendees", "notes"]
        )

    def test_event_required_fields(self):
        self.assertFalse(self.event.__table__.columns["name"].nullable)

    def test_event_autoincrement(self):
        self.assertTrue(self.event.__table__.columns["id"].autoincrement)

    def test_event_index_values(self):
        self.assertTrue(self.event.__table__.columns["name"].index)
        self.assertTrue(self.event.__table__.columns["start_date"].index)
