from unittest import TestCase
from unittest.mock import patch, call
from app.core.models import User, Role
from app.cli_tree.utils import ask_body_data, cli_get_all_user, cli_patch_user, cli_post_user, cli_delete_user, \
    cli_get_all_customer, cli_patch_related_customer, cli_post_customer, cli_get_all_event, cli_get_no_support_event, \
    cli_get_related_event, cli_patch_event, cli_patch_related_event, cli_post_event, cli_get_all_contract, \
    cli_get_not_signed_contract, cli_get_not_paid_contract, cli_patch_contract, cli_patch_related_contract, \
    cli_post_contract
from app.core.schemas import UserSchema


class UtilsTests(TestCase):
    def setUp(self):
        self.test_user = User(id=12345, name="test_user", role=Role.commercial)

    # ask_body_data()

    @patch("app.cli_tree.utils.typer.prompt")
    def test_ask_body_data(self, prompt):
        prompt.side_effect = ["John", "1 street", "Toulouse"]
        data = ["name", "address", "city"]
        result = {"name": "John", "address": "1 street", "city": "Toulouse"}

        self.assertEqual(ask_body_data(*data), result)

        prompt_calls = [
            call(text='Propriété NAME ', default='', show_default=False),
            call(text='Propriété ADDRESS ', default='', show_default=False),
            call(text='Propriété CITY ', default='', show_default=False)
        ]
        prompt.assert_has_calls(prompt_calls)

    @patch("app.cli_tree.utils.typer.prompt")
    def test_ask_body_data_empty_args(self, prompt):
        data = []
        result = {}

        self.assertEqual(ask_body_data(*data), result)

        prompt.assert_not_called()

    # cli_get_all_user()

    @patch("app.cli_tree.utils.rprint")
    @patch("app.cli_tree.utils.get_all_user_flow")
    def test_cli_get_all_user(self, get_all_user_flow, rprint):
        cli_get_all_user(self.test_user)
        get_all_user_flow.assert_called_once_with(
            UserSchema(id=12345, password=None, name='test_user', role='commercial', creation_date=None, last_update=None)
        )
        rprint.assert_called()

    # cli_patch_user()

    @patch("app.cli_tree.utils.ask_body_data")
    @patch("app.cli_tree.utils.typer.prompt")
    @patch("app.cli_tree.utils.rprint")
    @patch("app.cli_tree.utils.patch_user_flow")
    def test_cli_patch_user(self, patch_user_flow, rprint, prompt, ask_body_data):
        prompt.return_value = 99999
        ask_body_data.return_value = {"name": "Test name"}
        cli_patch_user(self.test_user)
        patch_user_flow.assert_called_once_with(
            UserSchema(
                id=12345, password=None, name='test_user', role='commercial', creation_date=None, last_update=None
            ),
            99999,
            {"name": "Test name"}
        )
        rprint.assert_called()

    # cli_post_user()

    @patch("app.cli_tree.utils.rprint")
    @patch("app.cli_tree.utils.post_user_flow")
    @patch("app.cli_tree.utils.ask_body_data")
    def test_cli_post_user(self, ask_body_data, post_user_flow, rprint):
        ask_body_data.return_value = {"name": "Test name", "password": "esgsegse", "role": "commercial"}
        cli_post_user(self.test_user)
        post_user_flow.assert_called_once_with(
            UserSchema(
                id=12345, password=None, name='test_user', role='commercial', creation_date=None, last_update=None
            ),
            {"name": "Test name", "password": "esgsegse", "role": "commercial"}
        )
        rprint.assert_called()

    # cli_delete_user()

    @patch("app.cli_tree.utils.rprint")
    @patch("app.cli_tree.utils.delete_user_flow")
    @patch("app.cli_tree.utils.typer.prompt")
    def test_cli_delete_user(self, prompt, delete_user_flow, rprint):
        prompt.return_value = 99999
        cli_delete_user(self.test_user)
        delete_user_flow.assert_called_once_with(
            UserSchema(
                id=12345, password=None, name='test_user', role='commercial', creation_date=None, last_update=None
            ),
            99999
        )
        rprint.assert_called()

    # cli_get_all_customer()

    @patch("app.cli_tree.utils.rprint")
    @patch("app.cli_tree.utils.get_all_customer_flow")
    def test_cli_get_all_customer(self, get_all_customer_flow, rprint):
        cli_get_all_customer(self.test_user)
        get_all_customer_flow.assert_called_once_with(
            UserSchema(
                id=12345, password=None, name='test_user', role='commercial', creation_date=None, last_update=None
            )
        )
        rprint.assert_called()

    # cli_patch_related_customer()

    @patch("app.cli_tree.utils.rprint")
    @patch("app.cli_tree.utils.patch_related_customer_flow")
    @patch("app.cli_tree.utils.ask_body_data")
    @patch("app.cli_tree.utils.typer.prompt")
    def test_cli_patch_related_customer(self, prompt, ask_body_data, patch_related_customer_flow, rprint):
        prompt.return_value = 99999
        body = {"salesman_id": "88888", "name": "John", "email": "test@test.com", "phone": "0606060606", "company_name": "Fake company"}
        ask_body_data.return_value = body
        cli_patch_related_customer(self.test_user)
        patch_related_customer_flow.assert_called_once_with(
            UserSchema(
                id=12345, password=None, name='test_user', role='commercial', creation_date=None, last_update=None
            ),
            99999,
            body
        )
        rprint.assert_called()

    # cli_post_customer()

    @patch("app.cli_tree.utils.rprint")
    @patch("app.cli_tree.utils.post_customer_flow")
    @patch("app.cli_tree.utils.ask_body_data")
    def test_cli_post_customer(self, ask_body_data, post_customer_flow, rprint):
        body = {"salesman_id": "88888", "name": "John", "email": "test@test.com", "phone": "0606060606",
                "company_name": "Fake company"}
        ask_body_data.return_value = body
        cli_post_customer(self.test_user)
        post_customer_flow.assert_called_once_with(
            UserSchema(
                id=12345, password=None, name='test_user', role='commercial', creation_date=None, last_update=None
            ),
            body
        )
        rprint.assert_called()

    # cli_get_all_event()

    @patch("app.cli_tree.utils.rprint")
    @patch("app.cli_tree.utils.get_all_event_flow")
    def test_cli_get_all_event(self, get_all_event_flow, rprint):
        cli_get_all_event(self.test_user)
        get_all_event_flow.assert_called_once_with(
            UserSchema(
                id=12345, password=None, name='test_user', role='commercial', creation_date=None, last_update=None
            ),
        )
        rprint.assert_called()

    # cli_get_no_support_event()

    @patch("app.cli_tree.utils.rprint")
    @patch("app.cli_tree.utils.get_no_support_event_flow")
    def test_cli_get_no_support_event(self, get_no_support_event_flow, rprint):
        cli_get_no_support_event(self.test_user)
        get_no_support_event_flow.assert_called_once_with(
            UserSchema(
                id=12345, password=None, name='test_user', role='commercial', creation_date=None, last_update=None
            ),
        )
        rprint.assert_called()

    # cli_get_related_event()

    @patch("app.cli_tree.utils.rprint")
    @patch("app.cli_tree.utils.get_related_event_flow")
    def test_cli_get_related_event(self, get_related_event_flow, rprint):
        cli_get_related_event(self.test_user)
        get_related_event_flow.assert_called_once_with(
            UserSchema(
                id=12345, password=None, name='test_user', role='commercial', creation_date=None, last_update=None
            ),
        )
        rprint.assert_called()

    # cli_patch_event()

    @patch("app.cli_tree.utils.rprint")
    @patch("app.cli_tree.utils.patch_event_flow")
    @patch("app.cli_tree.utils.ask_body_data")
    @patch("app.cli_tree.utils.typer.prompt")
    def test_cli_patch_event(self, prompt, ask_body_data, patch_event_flow, rprint):
        prompt.return_value = 77777
        body = {"name": "Test event name", "contract_id": "12345", "customer_id": "56789", "support_contact_id": "22222", "location": "Toulouse", "attendees": "38", "notes": "My personnal notes"}
        ask_body_data.return_value = body
        cli_patch_event(self.test_user)
        patch_event_flow.assert_called_once_with(
            UserSchema(
                id=12345, password=None, name='test_user', role='commercial', creation_date=None, last_update=None
            ),
            77777,
            body
        )
        rprint.assert_called()

    # cli_patch_related_event()

    @patch("app.cli_tree.utils.rprint")
    @patch("app.cli_tree.utils.patch_related_event_flow")
    @patch("app.cli_tree.utils.ask_body_data")
    @patch("app.cli_tree.utils.typer.prompt")
    def test_cli_patch_related_event(self, prompt, ask_body_data, patch_related_event_flow, rprint):
        prompt.return_value = 77777
        body = {"name": "Test event name", "contract_id": "12345", "customer_id": "56789",
                "support_contact_id": "22222", "location": "Toulouse", "attendees": "38", "notes": "My personnal notes"}
        ask_body_data.return_value = body
        cli_patch_related_event(self.test_user)
        patch_related_event_flow.assert_called_once_with(
            UserSchema(
                id=12345, password=None, name='test_user', role='commercial', creation_date=None, last_update=None
            ),
            77777,
            body
        )
        rprint.assert_called()

    # cli_post_event()

    @patch("app.cli_tree.utils.rprint")
    @patch("app.cli_tree.utils.post_event_flow")
    @patch("app.cli_tree.utils.ask_body_data")
    def test_cli_post_event(self, ask_body_data, post_event_flow, rprint):
        body = {"name": "Test event name", "contract_id": "12345", "customer_id": "56789",
                "support_contact_id": "22222", "location": "Toulouse", "attendees": "38", "notes": "My personnal notes"}
        ask_body_data.return_value = body
        cli_post_event(self.test_user)
        post_event_flow.assert_called_once_with(
            UserSchema(
                id=12345, password=None, name='test_user', role='commercial', creation_date=None, last_update=None
            ),
            body
        )
        rprint.assert_called()

    # cli_get_all_contract()

    @patch("app.cli_tree.utils.rprint")
    @patch("app.cli_tree.utils.get_all_contract_flow")
    def test_cli_get_all_contract(self, get_all_contract_flow, rprint):
        cli_get_all_contract(self.test_user)
        get_all_contract_flow.assert_called_once_with(
            UserSchema(
                id=12345, password=None, name='test_user', role='commercial', creation_date=None, last_update=None
            ),
        )
        rprint.assert_called()

    # cli_get_not_signed_contract()

    @patch("app.cli_tree.utils.rprint")
    @patch("app.cli_tree.utils.get_not_signed_contract_flow")
    def test_cli_get_not_signed_contract(self, get_not_signed_contract_flow, rprint):
        cli_get_not_signed_contract(self.test_user)
        get_not_signed_contract_flow.assert_called_once_with(
            UserSchema(
                id=12345, password=None, name='test_user', role='commercial', creation_date=None, last_update=None
            ),
        )
        rprint.assert_called()

    # cli_get_not_paid_contract()

    @patch("app.cli_tree.utils.rprint")
    @patch("app.cli_tree.utils.get_not_paid_contract_flow")
    def test_cli_get_not_paid_contract(self, get_not_paid_contract_flow, rprint):
        cli_get_not_paid_contract(self.test_user)
        get_not_paid_contract_flow.assert_called_once_with(
            UserSchema(
                id=12345, password=None, name='test_user', role='commercial', creation_date=None, last_update=None
            ),
        )
        rprint.assert_called()

    # cli_patch_contract()

    @patch("app.cli_tree.utils.rprint")
    @patch("app.cli_tree.utils.patch_contract_flow")
    @patch("app.cli_tree.utils.ask_body_data")
    @patch("app.cli_tree.utils.typer.prompt")
    def test_cli_patch_contract(self, prompt, ask_body_data, patch_contract_flow, rprint):
        prompt.return_value = 66666
        body = {"customer_id": "22222", "salesman_id": "12345", "amount_total": "25.35", "amount_outstanding": "20.21", "state": "signed"}
        ask_body_data.return_value = body
        cli_patch_contract(self.test_user)
        patch_contract_flow.assert_called_once_with(
            UserSchema(
                id=12345, password=None, name='test_user', role='commercial', creation_date=None, last_update=None
            ),
            66666,
            body
        )
        rprint.assert_called()

    # cli_patch_related_contract()

    @patch("app.cli_tree.utils.rprint")
    @patch("app.cli_tree.utils.patch_related_contract_flow")
    @patch("app.cli_tree.utils.ask_body_data")
    @patch("app.cli_tree.utils.typer.prompt")
    def test_cli_patch_related_contract(self, prompt, ask_body_data, patch_related_contract_flow, rprint):
        prompt.return_value = 66666
        body = {"customer_id": "22222", "salesman_id": "12345", "amount_total": "25.35", "amount_outstanding": "20.21",
                "state": "signed"}
        ask_body_data.return_value = body
        cli_patch_related_contract(self.test_user)
        patch_related_contract_flow.assert_called_once_with(
            UserSchema(
                id=12345, password=None, name='test_user', role='commercial', creation_date=None, last_update=None
            ),
            66666,
            body
        )
        rprint.assert_called()

    # cli_post_contract()

    @patch("app.cli_tree.utils.rprint")
    @patch("app.cli_tree.utils.post_contract_flow")
    @patch("app.cli_tree.utils.ask_body_data")
    def test_cli_post_contract(self, ask_body_data, post_contract_flow, rprint):
        body = {"customer_id": "22222", "salesman_id": "12345", "amount_total": "25.35", "amount_outstanding": "20.21",
                "state": "signed"}
        ask_body_data.return_value = body
        cli_post_contract(self.test_user)
        post_contract_flow.assert_called_once_with(
            UserSchema(
                id=12345, password=None, name='test_user', role='commercial', creation_date=None, last_update=None
            ),
            body
        )
        rprint.assert_called()
