from pydantic_extra_types.phone_numbers import PhoneNumber


class PhoneNumberUser(PhoneNumber):
    max_length = 12
    min_length = 11
    phone_format = "E164"
