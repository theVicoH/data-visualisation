import os
from http import HTTPStatus
import pandas as pd

class PassengersService:
    """
    Class service pour gérer les datas des passengers
    """

    def __init__(self):
        """
        Initialisation de la classe PassengerService
        """
        self.file_path = os.path.join('data', 'monthly_passengers.csv')
        try:
            self.df = pd.read_csv(self.file_path)
        except ImportError as error:
            raise ImportError(f"Erreur lors de la lecture du fichier: {str(error)}") from error

    def get_totals_group_by_country(self, column):
        """
        Retourne le volume total de passagers par pays selon la colonne de donnée
        """
        totals = (self.df[self.df[column].notna()][column] * 1000).groupby(self.df['ISO3']).sum()
        return totals.to_dict()

    def get_all_totals_by_country(self, iso3):
        """
        Retourne le total des passagers domestiques et internationaux pour un pays
        """
        country_data = self.df[self.df['ISO3'] == iso3.upper()]
        if country_data.empty:
            return {
                "error": "Entrez un iso3 valide"
            }, HTTPStatus.BAD_REQUEST

        domestic_totals = self.get_totals_group_by_country('Domestic')
        international_totals = self.get_totals_group_by_country('International')
        total_totals = self.get_totals_group_by_country('Total')

        iso3 = iso3.upper()
        return {
            "country": iso3,
            "domestic_total": domestic_totals.get(iso3, 0),
            "international_total": international_totals.get(iso3, 0),
            "total": total_totals.get(iso3, 0)
        }

    def get_totals_by_year(self, year):
        """
        Retourne les totaux de passagers domestiques et internationaux pour une année donnée
        """
        year_data = self.df[self.df['Year'] == year]

        if year_data.empty:
            return None

        domestic_total = (
                year_data['Domestic'].sum() * 1000
            ) if not year_data['Domestic'].empty else 0
        international_total = (
                year_data['International'].sum() * 1000
            ) if not year_data['International'].empty else 0
        total = (
                year_data['Total'].sum() * 1000
            ) if not year_data['Total'].empty else 0

        return {
            "year": year,
            "domestic_total": domestic_total,
            "international_total": international_total,
            "total": total
        }
