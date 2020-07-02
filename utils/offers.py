from utils import dbhandler

class Offers():
    """docstring for Offers"""
    def __init__(self):
        self.db = dbhandler.Dbhandler()

    """
        Provides list of all the offers configured in db
        Params:
            -
        Returns:
            - List Obj with all details of offer
            - Empty list if none found
    """
    def get_all_offer(self):
        # Fetch all offers
        query = 'SELECT * FROM offers;'
        output = self.db.fetch(query)
        return output

    """
        Provides offer details for provided offerid
        Params:
            - offerid
        Returns:
            - Obj with all details of offer
            - False
    """
    def get_offer_by_id(self, offerid):
        query = "SELECT * FROM offers WHERE `offerid`={}".format(offerid)
        output = self.db.fetch(query)

        if len(output) == 1:
            return output[0]
        return False

    """
        Add a new offer with all the details provided
        Params:
            - productid
            - addedby
            - discount
            - description
            - fromd
            - tod
        Returns:
            - List Obj with all details the newly created offer
            - False
    """
    def add_new_offer(self, productid, addedby, discount, description, fromd, tod):
        # TODO: Validate duplicate offer before create
        # Create offer
        query = "INSERT INTO offers (`productid`, `addedby`, `discount`, `description`, `from`, `to`) VALUES('{}', '{}', '{}', '{}', '{}', '{}')".format(
                    productid,
                    addedby,
                    discount,
                    description,
                    fromd,
                    tod)
        res = self.db.execute(query)
        if res:
            # Verify the offer got created
            getquery = "SELECT * FROM offers WHERE `productid`='{}' AND `addedby`='{}' AND `description`='{}' AND `discount`='{}' AND `from`='{}' AND `to`='{}'".format(
                    productid,
                    addedby,
                    description,
                    discount,
                    fromd,
                    tod)
            output = self.db.fetch(getquery)
            if len(output) == 1:
                return output[0]
        return False

    """
        Modifies an existing offer
        Params:
            - productid
            - addedby
            - discount
            - description
            - fromd
            - tod
            - offerid
        Returns:
            - List Obj with the details of modified offer
            - False
    """
    def modify_offer(self, productid, addedby, discount, description, fromd, tod, offerid):
        # TODO: Validate if offer exists
        # Modify offer
        query = "UPDATE offers SET `productid`={}, `addedby`='{}', `discount`='{}', `description`='{}', `from`='{}', `to`='{}' WHERE offerid={}".format(
                    productid,
                    addedby,
                    discount,
                    description,
                    fromd,
                    tod,
                    offerid)
        res = self.db.execute(query)
        if res:
            # Verify that the product modified
            getquery = "SELECT * FROM offers WHERE `productid`='{}' AND `addedby`='{}' AND `discount`='{}' AND `description`='{}' AND `from`='{}' AND `to`='{}'".format(
                    productid,
                    addedby,
                    discount,
                    description,
                    fromd,
                    tod)
            output = self.db.fetch(getquery)
            if len(output) == 1:
                return output[0]
        return False

    """
        Deletes an existing offer
        Params:
            - offerid
        Returns:
            - True
            - False
    """
    def delete_offer_by_id(self, offerid):
        # Validate if offer exists
        # Delete offer
        query = "DELETE FROM offers WHERE `offerid`='{}'".format(
                        offerid)
        res = self.db.execute(query)
        if res:
            # Verify that the offer deleted
            getquery = "SELECT * FROM offers WHERE `offerid`='{}'".format(
                        offerid)
            output = self.db.fetch(getquery)
            if len(output) == 0:
                return True
        return False
