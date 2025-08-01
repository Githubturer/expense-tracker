class DuplicateEmailError(Exception):
    def __init__(self, email: str):
        self.email = email
        self.message = f"The email {email} is already in use."
        super().__init__(self.message)


class InvalidCredentialsError(Exception):
    def __init__(self, message: str = "Invalid credentials"):
        self.message = message
        super().__init__(self.message)


class UserNotFoundError(Exception):
    def __init__(self):
        self.message = "User not found"
        super().__init__(self.message)


class NewPasswordError(Exception):
    def __init__(
        self, message: str = "New password cannot be the same as the old password"
    ):
        self.message = message
        super().__init__(self.message)
