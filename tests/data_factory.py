from factory import DictFactory, Faker
from faker import Faker as FakeIt

FAKER = FakeIt(seed=0)


class DataFactory(DictFactory):
    phone = Faker("phone_number")
    address = Faker("address")
    car_plate = Faker("license_plate")
    ip_address = FAKER.ipv4()
