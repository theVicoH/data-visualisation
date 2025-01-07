import os
from http import HTTPStatus
import pandas as pd
from flask import jsonify

class HolidaysService:
    """
    Class service pour gérer les datas des jours fériés
    """

    def __init__(self):
        """
        Initialisation de la classe HolidaysService
        """
        self.file_path = os.path.join('data', 'global_holidays.csv')

    def get_holidays_by_country(self):
        """
        Retourne le nombre de jours fériés par pays
        """
        try:
            df = pd.read_csv(self.file_path)
            holidays_count = df.groupby('ADM_name').size()
            return jsonify({"data": holidays_count.to_dict()}), HTTPStatus.OK

        except ImportError as error:
            return jsonify({"error": error}), HTTPStatus.INTERNAL_SERVER_ERROR

    def double_holidays(self):
        """
        Retourne un double coucou holidays
        """
        return jsonify("double coucou"), HTTPStatus.OK
