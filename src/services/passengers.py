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

    def get_totals_by_date(self, year, month=None):
        """
        Retourne les totaux de passagers domestiques et internationaux pour une année 
        et optionnellement un mois spécifique
        """
        year_data = self.df[self.df['Year'] == year]

        if year_data.empty:
            return None

        if month is not None:
            year_data = year_data[year_data['Month'] == month]
            if year_data.empty:
                return None

        domestic_total = round(
            year_data['Domestic'].sum() * 1000
        ) if not year_data['Domestic'].empty else 0
        international_total = round(
            year_data['International'].sum() * 1000
        ) if not year_data['International'].empty else 0
        total = round(
            year_data['Total'].sum() * 1000
        ) if not year_data['Total'].empty else 0

        result = {
            "year": year,
            "domestic_total": domestic_total,
            "international_total": international_total,
            "total": total
        }

        if month is not None:
            result["month"] = month

        return result

    def get_totals_by_date_range(self, start_year, start_month, end_year, end_month):
        """
        Retourne les totaux entre deux dates
        """

        for col in ['Domestic', 'International', 'Total']:
            self.df[col] = pd.to_numeric(self.df[col], errors='coerce')

        mask = (
            ((self.df['Year'] > start_year) |
             ((self.df['Year'] == start_year) &
              (self.df['Month'] >= start_month))) &
            ((self.df['Year'] < end_year) |
             ((self.df['Year'] == end_year) &
              (self.df['Month'] <= end_month)))
        )

        date_range_data = self.df[mask]

        if date_range_data.empty:
            return None

        return {
            "period": {
                "start": {"year": start_year, "month": start_month},
                "end": {"year": end_year, "month": end_month}
            },
            "domestic_total": round(date_range_data['Domestic'].fillna(0).sum() * 1000),
            "international_total": round(date_range_data['International'].fillna(0).sum() * 1000),
            "total": round(date_range_data['Total'].fillna(0).sum() * 1000),
            "countries": date_range_data['ISO3'].nunique()
        }
    def get_world_totals(self):
        """
        Retourne les totaux mondiaux
        """
        for col in ['Domestic', 'International', 'Total']:
            self.df[col] = pd.to_numeric(self.df[col], errors='coerce')

        return {
            "domestic_total": round(self.df['Domestic'].fillna(0).sum() * 1000),
            "international_total": round(self.df['International'].fillna(0).sum() * 1000),
            "total": round(self.df['Total'].fillna(0).sum() * 1000),
            "countries": self.df['ISO3'].nunique()
        }

    def get_monthly_data_by_country(self, iso3):
        """
        Retourne les données mensuelles pour un pays spécifique
        """
        country_data = self.df[self.df['ISO3'] == iso3.upper()]
        if country_data.empty:
            return None

        result = []
        for _, row in country_data.iterrows():
            result.append({
                "year": int(row['Year']),
                "month": int(row['Month']),
                "domestic": round(
                        row['Domestic'] * 1000) if pd.notna(row['Domestic']
                    ) else 0,
                "international": round(
                        row['International'] * 1000) if pd.notna(row['International']
                    ) else 0,
                "total": round(row['Total'] * 1000) if pd.notna(row['Total']) else 0
            })

        return sorted(result, key=lambda x: (x['year'], x['month']))
