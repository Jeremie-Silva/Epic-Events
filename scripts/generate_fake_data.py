from random import randint
from app.core.database import db, AnyModels
from app.core.models import User, Role, Customer, Contract, Event
from faker import Faker


fake = Faker("fr_FR")


def generate_fake_instance(model: AnyModels, generate_fields: list[str], **kwargs):
    if "id" in generate_fields:
        kwargs["id"] = randint(100000000, 999999999)
    if "name" in generate_fields:
        kwargs["name"] = ":::" + fake.name() + ":::"
    if "password" in generate_fields:
        kwargs["password"] = "test"
    if "email" in generate_fields:
        kwargs["email"] = fake.email()
    if "phone" in generate_fields:
        kwargs["phone"] = fake.phone_number()
    if "company_name" in generate_fields:
        kwargs["company_name"] = fake.name()
    if "amount_total" in generate_fields:
        kwargs["amount_total"] = randint(1, 100)
    if "amount_outstanding" in generate_fields:
        kwargs["amount_outstanding"] = randint(1, 1000)
    if "start_date" in generate_fields:
        kwargs["start_date"] = fake.date()
    if "end_date" in generate_fields:
        kwargs["end_date"] = fake.date()
    if "location" in generate_fields:
        kwargs["location"] = fake.address()
    if "attendees" in generate_fields:
        kwargs["attendees"] = randint(1, 100)
    if "notes" in generate_fields:
        kwargs["notes"] = fake.street_address()
    return model(**kwargs)


def generate_users():
    fake_user_gestion: User = generate_fake_instance(
        User, generate_fields=["id", "name", "password"], role=Role.gestion
    )
    fake_user_commercial: User = generate_fake_instance(
        User, generate_fields=["id", "name", "password"], role=Role.commercial
    )
    fake_user_support: User = generate_fake_instance(
        User, generate_fields=["id", "name", "password"],  role=Role.support
    )
    db.add_objs(fake_user_gestion, fake_user_commercial, fake_user_support)


def generate_customers():
    salesman: User = db.get_obj(model=User, role=Role.commercial)
    fake_customer: User = generate_fake_instance(
        Customer, generate_fields=["id", "name", "email", "phone", "company_name"],
        salesman=salesman, salesman_id=salesman.id
    )
    db.add_objs(fake_customer)


def generate_contracts():
    customer: Customer = db.get_obj(model=Customer)
    salesman: User = db.get_obj(model=User, role=Role.commercial)
    fake_contract_waiting: Contract = generate_fake_instance(
        Contract, generate_fields=["id", "amount_total", "amount_outstanding"],
        customer=customer, customer_id=customer.id, salesman=salesman, salesman_id=salesman.id
    )
    fake_contract_signed: Contract = generate_fake_instance(
        Contract, generate_fields=["id", "amount_total", "amount_outstanding"],
        customer=customer, customer_id=customer.id, salesman=salesman, salesman_id=salesman.id,
        state="signed"
    )
    db.add_objs(fake_contract_waiting, fake_contract_signed)


def generate_events():
    contract: Contract = db.get_obj(model=Contract)
    customer: Customer = db.get_obj(model=Customer)
    support: User = db.get_obj(model=User, role=Role.support)
    fake_event: Event = generate_fake_instance(
        Event, generate_fields=["id", "name", "start_date", "end_date", "location", "attendees", "notes"],
        contract=contract, contract_id=contract.id, customer=customer, customer_id=customer.id,
        support=support, support_contact_id=support.id
    )
    db.add_objs(fake_event)


if __name__ == "__main__":
    generate_users()
    generate_customers()
    generate_contracts()
    generate_events()
