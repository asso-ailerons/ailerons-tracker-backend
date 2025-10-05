""" Article Model """


class Article:
    """ Model for a news article. """

    def __init__(self, form, image_url: str, published: bool = False, archived: bool = False):
        self.title = form['newsTitle']
        self.content = form["newsContent"]
        self.image_url = image_url
        self.published = published
        self.archived = archived
        self.publication_date = form["newsDate"]

    def upload(self):
        """ Insert the object as a new row in table 'individual' """

        data = supabase.upsert(self, 'article')
        return data
