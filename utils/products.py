from utils import dbhandler

class Products():
    """docstring for Products"""
    def __init__(self):
        self.db = dbhandler.Dbhandler()

    """
        Provides list of all the products configured in db
        Params:
            -
        Returns:
            - List Obj with all details of product
            - Empty list if none found
    """
    def get_all_product(self):
        # Fetch all products
        query = 'SELECT * FROM products;'
        output = self.db.fetch(query)
        return output

    """
        Provides product details for provided productid
        Params:
            - productid
        Returns:
            - Obj with all details of product
            - False
    """
    def get_product_by_id(self, productid):
        query = "SELECT * FROM products WHERE `productid`={}".format(productid)
        output = self.db.fetch(query)

        if len(output) == 1:
            return output[0]
        return False

    """
        Add a new product with all the details provided
        Params:
            - name
            - type
            - price
            - description
            - instock
            - addedby
        Returns:
            - List Obj with all details the newly created product
            - False
    """
    def add_new_product(self, name, type, price, description, instock, addedby, labels):
        # TODO: Validate duplicate product before create
        # Create product
        query = "INSERT INTO products (`name`, `type`, `price`, `description`, `instock`, `created`, `modified`, `addedby`, `labels`) VALUES('{}', '{}', '{}', '{}', '{}', now(), now(), '{}', '{}')".format(
                    name,
                    type,
                    price,
                    description,
                    instock,
                    addedby,
                    labels)
        res = self.db.execute(query)
        if res:
            # Verify the product got created
            getquery = "SELECT * FROM products WHERE `name`='{}' AND `price`='{}' AND `description`='{}' AND `instock`='{}' AND `type`='{}' AND `addedby`='{}' AND `labels`='{}'".format(
                    name,
                    price,
                    description,
                    instock,
                    type,
                    addedby,
                    labels)
            output = self.db.fetch(getquery)
            if len(output) == 1:
                return output[0]
        return False

    """
        Modifies an existing product
        Params:
            - name
            - type
            - price
            - description
            - instock
            - addedby
            - productid
        Returns:
            - List Obj with the details of modified product
            - False
    """
    def modify_product(self, name, type, price, description, instock, addedby, labels, productid):
        # TODO: Validate if product exists
        # Modify product
        query = "UPDATE products SET `name`='{}', `type`='{}', `price`='{}', `description`='{}', `instock`={}, `modified`=now(), `addedby`={}, `labels`='{}' WHERE productid={}".format(
                    name,
                    type,
                    price,
                    description,
                    instock,
                    addedby,
                    labels,
                    productid)
        res = self.db.execute(query)
        if res:
            # Verify that the product modified
            getquery = "SELECT * FROM products WHERE `name`='{}' AND `type`='{}' AND `price`='{}' AND `description`='{}' AND `instock`='{}' AND `addedby`='{}' AND `productid`={}  AND `labels`='{}'".format(
                    name,
                    type,
                    price,
                    description,
                    instock,
                    addedby,
                    productid,
                    labels)
            output = self.db.fetch(getquery)
            if len(output) == 1:
                return output[0]
        return False

    """
        Deletes an existing product
        Params:
            - productid
        Returns:
            - True
            - False
    """
    def delete_product_by_id(self, productid):
        # Validate if product exists
        # Delete product
        query = "DELETE FROM products WHERE `productid`='{}'".format(
                        productid)
        res = self.db.execute(query)
        if res:
            # Verify that the product deleted
            getquery = "SELECT * FROM products WHERE `productid`='{}'".format(
                        productid)
            output = self.db.fetch(getquery)
            if len(output) == 0:
                return True
        return False
