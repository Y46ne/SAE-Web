from Espece import Espece

class EspeceHypothetique(Espece):
    def __init__(self, nom, espece_fille1, espece_fille2):
        super().__init__(nom)
        self.especes_filles = [espece_fille1, espece_fille2]