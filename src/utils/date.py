from http import HTTPStatus

class DateUtils:
    """
    Class utils pour gérer verifier les paramètres de date
    """

    @staticmethod
    def validate_year(year_param):
        """
        Valide le paramètre année
        """
        if not year_param:
            return None, ({"error": "Le paramètre 'year' est requis"}, HTTPStatus.BAD_REQUEST)

        try:
            return int(year_param), None
        except ValueError:
            return None, ({"error": "L'année doit être un nombre entier"}, HTTPStatus.BAD_REQUEST)

    @staticmethod
    def validate_month(month_param):
        """
        Valide le paramètre mois
        """
        if not month_param:
            return None, None

        try:
            month = int(month_param)
            if not 1 <= month <= 12:
                return None, (
                      {"error": "Le mois doit être compris entre 1 et 12"}, HTTPStatus.BAD_REQUEST
                    )
            return month, None
        except ValueError:
            return None, (
                    {"error": "Le mois doit être un nombre entier"}, HTTPStatus.BAD_REQUEST
                  )
