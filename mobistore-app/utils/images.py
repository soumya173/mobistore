from utils import dbhandler

class Images():
    """docstring for Images"""
    def __init__(self):
        self.db = dbhandler.Dbhandler()

    """
        Provides list of all the images configured in db
        Params:
            -
        Returns:
            - List Obj with all details of offer
            - Empty list if none found
    """
    def get_all_image(self):
        # Fetch all images
        query = 'SELECT * FROM images;'
        output = self.db.fetch(query)
        return output

    """
        Provides image details for provided imageid
        Params:
            - imageid
        Returns:
            - Obj with all details of image
            - False
    """
    def get_image_by_id(self, imageid):
        query = "SELECT * FROM images WHERE `imageid`={}".format(imageid)
        output = self.db.fetch(query)

        if len(output) == 1:
            return output[0]
        return False

    """
        Add a new image with all the details provided
        Params:
            - productid
            - url
        Returns:
            - List Obj with all details the newly created image
            - False
    """
    def add_new_image(self, productid, url):
        # Create image
        query = "INSERT INTO images (`productid`, `url`) VALUES('{}', '{}')".format(
                    productid,
                    url)
        res = self.db.execute(query)
        if res:
            # Verify the image got created
            getquery = "SELECT * FROM images WHERE `productid`='{}' AND `url`='{}'".format(
                    productid,
                    url)
            output = self.db.fetch(getquery)
            if len(output) == 1:
                return output[0]
        return False

    """
        Modifies an existing image
        Params:
            - productid
            - url
            - imageid
        Returns:
            - List Obj with the details of modified image
            - False
    """
    def modify_image(self, productid, url, imageid):
        # TODO: Validate if image exists
        # Modify image
        query = "UPDATE images SET `productid`='{}', `url`='{}' WHERE imageid={}".format(
                    productid,
                    url,
                    imageid)
        res = self.db.execute(query)
        if res:
            # Verify that the image modified
            getquery = "SELECT * FROM images WHERE `productid`='{}' AND `url`='{}' AND `imageid`='{}'".format(
                    productid,
                    url,
                    imageid)
            output = self.db.fetch(getquery)
            if len(output) == 1:
                return output[0]
        return False

    """
        Deletes an existing image
        Params:
            - imageid
        Returns:
            - True
            - False
    """
    def delete_image_by_id(self, imageid):
        # Validate if image exists
        # Delete image
        query = "DELETE FROM images WHERE `imageid`='{}'".format(
                        imageid)
        res = self.db.execute(query)
        if res:
            # Verify that the image deleted
            getquery = "SELECT * FROM images WHERE `imageid`='{}'".format(
                        imageid)
            output = self.db.fetch(getquery)
            if len(output) == 0:
                return True
        return False
