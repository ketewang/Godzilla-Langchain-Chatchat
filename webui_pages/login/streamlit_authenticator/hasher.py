import bcrypt

class Hasher:

    salt = "$2b$12$bkLM9PdtFzG74MDqSSpUnO"

    """
    This class will hash plain text passwords.
    """
    def __init__(self, passwords: list):
        """
        Create a new instance of "Hasher".

        Parameters
        ----------
        passwords: list
            The list of plain text passwords to be hashed.
        """

        self.passwords = passwords

    def _hash(self, password: str) -> str:
        """
        Hashes the plain text password.

        Parameters
        ----------
        password: str
            The plain text password to be hashed.
        Returns
        -------
        str
            The hashed password.
        """
        #return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode('utf-8')
        return bcrypt.hashpw(password.encode(), self.salt.encode()).decode('utf-8')

    @classmethod
    def hash(cls,password:str) -> str:
        return bcrypt.hashpw(password.encode(), cls.salt.encode()).decode('utf-8')


    def generate(self) -> list:
        """
        Hashes the list of plain text passwords.

        Returns
        -------
        list
            The list of hashed passwords.
        """
        return [self._hash(password) for password in self.passwords]


if __name__ == '__main__':
    #ret=bcrypt.gensalt().decode('utf-8')
    ret = Hasher.hash("123")
    a =Hasher(["123"]).generate()[0]
    print(ret)
    print(a)