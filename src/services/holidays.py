import os
import pandas as pd

HOLIDAY_TYPES = [
    "Public holiday",
    "Observance",
    "Local holiday",
    "Local observance",
    "Special holiday"
]

class HolidaysService:
    """
    Class service pour gérer les datas des jours fériés
    """

    def __init__(self):
        """
        Initialisation de la classe HolidaysService
        """
        self.file_path = os.path.join('data', 'global_holidays.csv')
        try:
            self.df = pd.read_csv(self.file_path)
        except ImportError as error:
            raise ImportError(f"Erreur lors de la lecture du fichier: {str(error)}") from error

    def get_holidays_by_country(self, holiday_type):
        """
        Retourne le nombre de jours fériés par pays
        """
        if holiday_type:
            filtered_df = self.df[self.df['Type'] == holiday_type]
        else:
            filtered_df = self.df

        holidays_count = filtered_df.groupby('ADM_name').size()
        return holidays_count.to_dict()

    def get_holidays_for_one_country(self, iso3, holiday_type):
        """
        Retourne le nombre de jours fériés pour un seul pays
        """
        filtered_df = self.df[self.df['ISO3'] == iso3.upper()]

        if filtered_df.empty:
            return {}

        if holiday_type:
            filtered_df = filtered_df[filtered_df['Type'] == holiday_type]

        holiday_count = len(filtered_df)

        return {
            "country": iso3.upper(),
            "data": holiday_count
        }

    def get_min_max_holidays(self, holiday_type):
        """
        Retourne le pays avec le moins de jours fériés et
        le pays avec le plus de jours fériés
        """
        if holiday_type:
            filtered_df = self.df[self.df['Type'] == holiday_type]
        else:
            filtered_df = self.df

        holiday_counts = filtered_df.groupby('ADM_name').size()

        min_holidays_country = holiday_counts.idxmin()

        min_holidays_data = filtered_df[filtered_df['ADM_name'] == min_holidays_country]

        max_holidays_country = holiday_counts.idxmax()

        max_holidays_data = filtered_df[filtered_df['ADM_name'] == max_holidays_country]

        return {
            "min": {
                "country": min_holidays_country,
                "data": len(min_holidays_data[['Date', 'Name']].to_dict(orient='records'))
            },
            "max": {
                "country": max_holidays_country,
                "data": len(max_holidays_data[['Date', 'Name']].to_dict(orient='records'))
            }
        }

    def get_holidays_repartition_by_type(self, country):
        """
        Fonction qui renvoi un dictionnaire avec en clé
        le type de jour férie et en valeur le nombre de jours fériés
        de ce type
        """
        if country:
            filtered_df = self.df[self.df['ADM_name'] == country.capitalize()]
        else:
            filtered_df = self.df

        if country and country.capitalize() not in filtered_df['ADM_name'].values:
            return {}

        df_filtered = filtered_df[filtered_df['Type'].isin(HOLIDAY_TYPES)]
        holidays_repartition = df_filtered['Type'].value_counts().to_dict()

        for holiday_type in HOLIDAY_TYPES:
            if holiday_type not in holidays_repartition:
                holidays_repartition[holiday_type] = 0

        return holidays_repartition

    def get_holidays_by_year(self, country):
        """
        Fonction qui renvoi le nombre de jours
        fériés par année
        """

        if country:
            filtered_df = self.df[self.df['ADM_name'] == country.capitalize()]
        else:
            filtered_df = self.df

        if country and country.capitalize() not in filtered_df['ADM_name'].values:
            return {}

        filtered_df['Date'] = pd.to_datetime(filtered_df['Date'])

        filtered_df['Year'] = filtered_df['Date'].dt.year

        holiday_count_per_year = filtered_df.groupby('Year').size()

        return holiday_count_per_year.to_dict()

    def get_holidays_by_month(self, country):
        """
        Fonction qui renvoi le nombre de jours
        fériés par mois
        """

        if country:
            filtered_df = self.df[self.df['ADM_name'] == country.capitalize()]
        else:
            filtered_df = self.df

        if country and country.capitalize() not in filtered_df['ADM_name'].values:
            return {}

        filtered_df['Date'] = pd.to_datetime(filtered_df['Date'])

        filtered_df['YearMonth'] = filtered_df['Date'].dt.to_period('M').astype(str)

        holiday_count_per_month = filtered_df.groupby('YearMonth').size().to_dict()

        return holiday_count_per_month

    def get_total_holidays(self, holiday_type):
        """
        Fonction qui renvoie le nombre total de jours fériés
        dans le monde
        """

        if holiday_type:
            filtered_df = self.df[self.df['Type'] == holiday_type]
        else:
            filtered_df = self.df

        return {"total": len(filtered_df)}
