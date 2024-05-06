from unittest import TestCase
from app.core.models import (
    Role,
    Permission,
    User,
    Customer,
    Contract,
    Event,
    Base,
    AbstractBaseModel
)
from freezegun import freeze_time


class RoleTests(TestCase):
    def setUp(self):
        self.role = Role()

    def test_role_inherits(self):
        self.assertIsInstance(self.role, Role)
        self.assertIsInstance(self.role, AbstractBaseModel)
        self.assertIsInstance(self.role, Base)

    def test_role_tablename(self):
        self.assertEqual(self.role.__tablename__, "role")

    def test_role_primary_key(self):
        self.assertTrue(self.role.__table__.columns["id"].primary_key)

    def test_role_declarated_fields(self):
        self.assertEqual(
            self.role.__table__.columns.keys(),
            ["id", "name"]
        )

    def test_role_required_fields(self):
        self.assertFalse(self.role.__table__.columns["name"].nullable)

    def test_role_autoincrement(self):
        self.assertTrue(self.role.__table__.columns["id"].autoincrement)

    def test_role_index_values(self):
        self.assertTrue(self.role.__table__.columns["name"].index)


@freeze_time("2024-04-29")
class UserTests(TestCase):
    def setUp(self):
        self.user = User()

    def test_user_inherits(self):
        self.assertIsInstance(self.user, User)
        self.assertIsInstance(self.user, AbstractBaseModel)
        self.assertIsInstance(self.user, Base)

    def test_user_tablename(self):
        self.assertEqual(self.user.__tablename__, "user")

    def test_user_primary_key(self):
        self.assertTrue(self.user.__table__.columns["id"].primary_key)

    def test_user_foreign_keys(self):
        self.assertTrue(self.user.__table__.columns["role_id"].foreign_keys)

    def test_user_declarated_fields(self):
        self.assertEqual(
            self.user.__table__.columns.keys(),
            ["id", "name", "password", "role_id", "creation_date", "last_update"]
        )

    def test_user_required_fields(self):
        self.assertFalse(self.user.__table__.columns["name"].nullable)
        self.assertFalse(self.user.__table__.columns["password"].nullable)
        self.assertFalse(self.user.__table__.columns["role_id"].nullable)

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
        self.assertIsInstance(self.customer, AbstractBaseModel)
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
        self.assertIsInstance(self.contract, AbstractBaseModel)
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

    def test_contract_required_fields(self):
        self.assertFalse(self.contract.__table__.columns["customer_id"].nullable)
        self.assertFalse(self.contract.__table__.columns["salesman_id"].nullable)
        self.assertFalse(self.contract.__table__.columns["state"].nullable)

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
        self.assertIsInstance(self.event, AbstractBaseModel)
        self.assertIsInstance(self.event, Base)

    def test_event_tablename(self):
        self.assertEqual(self.event.__tablename__, "event")

    def test_event_primary_key(self):
        self.assertTrue(self.event.__table__.columns["id"].primary_key)

    def test_event_foreign_keys(self):
        self.assertTrue(self.event.__table__.columns["contract_id"].foreign_keys)
        self.assertTrue(self.event.__table__.columns["customer_name"].foreign_keys)
        self.assertTrue(self.event.__table__.columns["customer_phone"].foreign_keys)
        self.assertTrue(self.event.__table__.columns["customer_email"].foreign_keys)
        self.assertTrue(self.event.__table__.columns["support_contact_name"].foreign_keys)
        self.assertTrue(self.event.__table__.columns["support_contact_id"].foreign_keys)

    def test_event_declarated_fields(self):
        self.assertEqual(
            self.event.__table__.columns.keys(),
            ["id", "name", "contract_id", "customer_name", "customer_phone", "customer_email",
             "start_date", "end_date", "support_contact_name", "support_contact_id", "location", "attendees", "notes"]
        )

    def test_event_required_fields(self):
        self.assertFalse(self.event.__table__.columns["name"].nullable)
        self.assertFalse(self.event.__table__.columns["contract_id"].nullable)
        self.assertFalse(self.event.__table__.columns["customer_name"].nullable)
        self.assertFalse(self.event.__table__.columns["customer_phone"].nullable)
        self.assertFalse(self.event.__table__.columns["customer_email"].nullable)
        self.assertFalse(self.event.__table__.columns["support_contact_name"].nullable)
        self.assertFalse(self.event.__table__.columns["support_contact_id"].nullable)

    def test_event_autoincrement(self):
        self.assertTrue(self.event.__table__.columns["id"].autoincrement)

    def test_event_index_values(self):
        self.assertTrue(self.event.__table__.columns["name"].index)
        self.assertTrue(self.event.__table__.columns["start_date"].index)
# backref
