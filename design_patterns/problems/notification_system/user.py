# User Class
class User:
    def __init__(self, preferences=[]):
        self.name = None
        self.email = None
        self.phone = None
        self.preferences = preferences  # A list of preferred notification methods

    def add_preference(self, preference):
        if preference not in self.preferences:
            self.preferences.append(preference)
            print(f"You will now be notified through {preference}!")
        else:
            print(f"You already have {preference} notifications on!")
        
    def remove_preference(self, preference):
        if preference in self.preferences:
            self.preferences.remove(preference)
            print(f"You will now not be notified through {preference}!")
        else:
            print(f"You already have {preference} notifications off!")
        
class UserBuilder:
    def __init__(self):
        self.user = User()
    
    def set_name(self, name):
        self.user.name = name
        return self
        
    def set_email(self, email):
        self.user.email = email
        return self
        
    def set_phone_number(self, number):
        self.user.phone = number
        return self
        
    def set_preferences(self, preference):
        self.user.preferences = preference
        return self
    
    def add_preference(self, preference):
        self.user.add_preference(preference)
        return self
        
    def build(self):
        # Validation can be added here to ensure essential parts are included
        if not self.user.name:
            raise ValueError("User must have a name.")
        if not self.user.email:
            raise ValueError("User must have an email.")
        if not self.user.phone:
            raise ValueError("User must have a phone number.")
        return self.user    

class UserCreator:
    def __init__(self, builder: UserBuilder):
        self.builder = builder
    
    
    
    def construct_user_all(self, name, email, phone):
        return (self.builder
                .set_name(name)
                .set_email(email)
                .set_phone_number(phone)
                .add_preference("sms")
                .add_preference("push")
                .add_preference("email")
                .build())
        
    def construct_user(self, name, email, phone):
        return (self.builder
                .set_name(name)
                .set_email(email)
                .set_phone_number(phone)
                .build())