class Signup():
    def __init__(self, name, email, password):
        self.name= name
        self.email =email
        self.password = password

    def toDBcollection(self):
        return{
            'name': self.name,
            'email' : self.email,
            'password': self.password
            }