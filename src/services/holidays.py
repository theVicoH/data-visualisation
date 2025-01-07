import os
from http import HTTPStatus
import pandas as pd
from flask import jsonify, request

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
            valid_holiday_types = [
                "Public holiday",
                "Observance",
                "Local holiday",
                "Local observance",
                "Special holiday"
            ]
            df = pd.read_csv(self.file_path)

            holiday_type = request.args.get('holiday-type')

            if holiday_type:
                if holiday_type not in valid_holiday_types:
                    return jsonify({
                        "error": "holiday-type non valide"
                    }), HTTPStatus.BAD_REQUEST

                df = df[df['Type'] == holiday_type]

            holidays_count = df.groupby('ADM_name').size()
            return jsonify({"data": holidays_count.to_dict()}), HTTPStatus.OK

        except ImportError as error:
            return jsonify({"error": error}), HTTPStatus.INTERNAL_SERVER_ERROR

    def get_holidays_for_one_country(self, iso3):
        """
        Retourne le nombre de jours fériés pour un seul pays

        :param iso3: iso3 du pays dont vous voulez savoir les jours fériés
        :type iso3: str
        """
        try:
            valid_holiday_types = [
                "Public holiday",
                "Observance",
                "Local holiday",
                "Local observance",
                "Special holiday"
            ]
            df = pd.read_csv(self.file_path)
            filtered_df = df[df['ISO3'] == iso3.upper()]

            if filtered_df.empty:
                return jsonify({
                    "error": "iso3 non valide"
                }), HTTPStatus.BAD_REQUEST

            holiday_type = request.args.get('holiday-type')

            if holiday_type:
                if holiday_type not in valid_holiday_types:
                    return jsonify({
                        "error": "holiday-type non valide"
                    }), HTTPStatus.BAD_REQUEST

                filtered_df = filtered_df[filtered_df['Type'] == holiday_type]
                holiday_count = len(filtered_df)
                return jsonify({
                    "country": iso3,
                    "data": holiday_count
                }), HTTPStatus.OK

            holiday_count = len(filtered_df)

            return jsonify({
                "country": iso3,
                "data": holiday_count
            }), HTTPStatus.OK

        except ImportError as error:
            return jsonify({"error": error}), HTTPStatus.INTERNAL_SERVER_ERROR

    def get_min_max_holidays(self):
        """
        Retourne le pays avec le moins de jours fériés et
        le pays avec le plus de jours fériés
        """
        try:
            valid_holiday_types = [
                "Public holiday",
                "Observance",
                "Local holiday",
                "Local observance",
                "Special holiday"
            ]
            df = pd.read_csv(self.file_path)

            holiday_type = request.args.get('holiday-type')

            if holiday_type:
                if holiday_type not in valid_holiday_types:
                    return jsonify({
                        "error": "holiday-type non valide"
                    }), HTTPStatus.BAD_REQUEST

                df = df[df['Type'] == holiday_type]

            holiday_counts = df.groupby('ADM_name').size()

            min_holidays_country = holiday_counts.idxmin()

            min_holidays_data = df[df['ADM_name'] == min_holidays_country]

            max_holidays_country = holiday_counts.idxmax()

            max_holidays_data = df[df['ADM_name'] == max_holidays_country]

            return jsonify({
                "min": {
                    "country": min_holidays_country,
                    "data": len(min_holidays_data[['Date', 'Name']].to_dict(orient='records'))
                },
                "max": {
                    "country": max_holidays_country,
                    "data": len(max_holidays_data[['Date', 'Name']].to_dict(orient='records'))
                }
            }), HTTPStatus.OK

        except ImportError as error:
            return jsonify({"error": error}), HTTPStatus.INTERNAL_SERVER_ERROR

    def get_holidays_repartition_by_type(self):
        """
        Fonction qui renvoi un dictionnaire avec en clé
        le type de jour férie et en valeur le nombre de jours fériés
        de ce type
        """
        try:
            valid_holiday_types = [
                "Public holiday",
                "Observance",
                "Local holiday",
                "Local observance",
                "Special holiday"
            ]
            df = pd.read_csv(self.file_path)
            country = request.args.get('country')

            if country:
                if country.capitalize() not in df['ADM_name'].values:
                    return jsonify({
                        "error": "country non valide"
                    }), HTTPStatus.BAD_REQUEST

                df = df[df['ADM_name'] == country.capitalize()]

            df_filtered = df[df['Type'].isin(valid_holiday_types)]
            holidays_repartition = df_filtered['Type'].value_counts().to_dict()

            for holiday_type in valid_holiday_types:
                if holiday_type not in holidays_repartition:
                    holidays_repartition[holiday_type] = 0

            return jsonify(
                holidays_repartition
            ), HTTPStatus.OK

        except ImportError as error:
            return jsonify({"error": error}), HTTPStatus.INTERNAL_SERVER_ERROR

    def get_holidays_by_year(self):
        """
        Fonction qui renvoi le nombre de jours
        fériés par année
        """

        try:
            df = pd.read_csv(self.file_path)

            df['Date'] = pd.to_datetime(df['Date'])

            df['Year'] = df['Date'].dt.year

            holiday_count_per_year = df.groupby('Year').size()

            return jsonify(holiday_count_per_year.to_dict()), HTTPStatus.OK

        except ImportError as error:
            return jsonify({"error": error}), HTTPStatus.INTERNAL_SERVER_ERROR
