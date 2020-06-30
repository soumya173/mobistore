from utils import dbhandler

class Users():
    """docstring for Users"""
    def __init__(self):
        self.db = dbhandler.Dbhandler()

    """
        Provides list of all the users configured in db
        Params:
            -
        Returns:
            - List Obj with all details of user
            - Empty list if none found
    """
    def get_all_user(self):
        # Fetch all users
        query = 'SELECT `userid`, `firstname`, `lastname`, `email`, `mobile`, `type`, `created`, `modified` FROM users;'
        output = self.db.fetch(query)
        return output

    """
        Authenticate user by email and password
        Params:
            - email
            - password
        Returns:
            - Obj with all details of user
            - False
    """
    def authenticate_user(self, email, password):
        user_details = self.get_user_by_email(email)
        if user_details != False:
            if password == user_details['password']:
                return user_details

        return False

    """
        Provides user details for provided userid
        Params:
            - userid
        Returns:
            - Obj with all details of user
            - False
    """
    def get_user_by_id(self, userid):
        query = "SELECT `userid`, `firstname`, `lastname`, `email`, `mobile`, `type`, `created`, `modified` FROM users WHERE `userid`={}".format(userid)
        output = self.db.fetch(query)

        if len(output) == 1:
            return output[0]
        return False

    """
        Provides user details for provided email
        Params:
            - email
        Returns:
            - Obj with all details of user
            - False
    """
    def get_user_by_email(self, email):
        query = "SELECT * FROM users WHERE `email`='{}'".format(email)
        output = self.db.fetch(query)

        if len(output) == 1:
            return output[0]
        return False

    """
        Add a new user with all the details provided
        Params:
            - password
            - firstname
            - lastname
            - email
            - mobile
            - type
        Returns:
            - List Obj with all details the newly created user
            - False
    """
    def add_new_user(self, password, firstname, lastname, email, mobile, type):
        # TODO: Validate duplicate user before create
        # Create user
        query = "INSERT INTO users (`password`, `firstname`, `lastname`, `email`, `mobile`, `type`, `created`, `modified`) VALUES('{}', '{}', '{}', '{}', '{}', '{}', now(), now())".format(
                        password,
                        firstname,
                        lastname,
                        email,
                        mobile,
                        type)
        res = self.db.execute(query)
        if res:
            # Verify the user got created
            getquery = "SELECT `userid`, `firstname`, `lastname`, `email`, `mobile`, `type`, `created`, `modified` FROM users WHERE `firstname`='{}' AND `lastname`='{}' AND `email`='{}' AND `mobile`='{}' AND `type`='{}'".format(
                        firstname,
                        lastname,
                        email,
                        mobile,
                        type)
            output = self.db.fetch(getquery)
            if len(output) == 1:
                return output[0]
        return False

    """
        Modifies an existing user
        Params:
            - password
            - firstname
            - lastname
            - email
            - mobile
            - type
            - userid
        Returns:
            - List Obj with the details of modified user
            - False
    """
    def modify_user(self, password, firstname, lastname, mobile, type, userid):
        # TODO: Validate if user exists
        # Modify user
        query = "UPDATE users SET `password`='{}', `firstname`='{}', `lastname`='{}', `mobile`='{}', `type`='{}', `modified`=now() WHERE userid={}".format(
                        password,
                        firstname,
                        lastname,
                        mobile,
                        type,
                        userid)
        res = self.db.execute(query)
        if res:
            # Verify that the user modified
            getquery = "SELECT `userid`, `firstname`, `lastname`, `email`, `mobile`, `type`, `created`, `modified` FROM users WHERE `userid`='{}' AND `firstname`='{}' AND `lastname`='{}' AND `email`='{}' AND `mobile`='{}' AND `type`='{}'".format(
                        userid,
                        firstname,
                        lastname,
                        email,
                        mobile,
                        type)
            output = self.db.fetch(getquery)
            if len(output) == 1:
                return output[0]
        return False

    """
        Deletes an existing user
        Params:
            - userid
        Returns:
            - True
            - False
    """
    def delete_user_by_id(self, userid):
        # Validate if user exists
        # Delete user
        query = "DELETE FROM users WHERE `userid`='{}'".format(
                        userid)
        res = self.db.execute(query)
        if res:
            # Verify that the user deleted
            getquery = "SELECT `userid`, `firstname`, `lastname`, `email`, `mobile`, `type`, `created`, `modified` FROM users WHERE `userid`='{}'".format(
                        userid)
            output = self.db.fetch(getquery)
            if len(output) == 0:
                return True
        return False
