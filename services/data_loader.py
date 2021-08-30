import csv
from models import trips, locations


class DataLoader:
    @staticmethod
    def delete_entries_in_locations_trips(db=None):
        """
        deletes everything from the locations and trips tables
        :param db:
        :return:
        """
        trips_num_rows_deleted, locations_num_rows_deleted, error = 0, 0, ''
        try:
            trips_num_rows_deleted = db.query(trips.Trips).delete()
            locations_num_rows_deleted = db.query(locations.Locations).delete()
            db.commit()
        except Exception as ex:
            error = repr(ex)
        return locations_num_rows_deleted, trips_num_rows_deleted, error


    @staticmethod
    def load_locations_trips_into_db(db=None):
        """
        This method reads the trips locations CSV files and loads into the DB
        :param db:
        :return: location_count, trips_count, error_str
        """
        location_list, trips_list, error_str = [], [], ""
        with open('data/locations.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')

            for idx, row in enumerate(csv_reader):
                if idx == 0:
                    continue
                location_list.append(locations.Locations(
                    LocationCode=row[0],
                    Latitude=row[1],
                    Longitude=row[2],
                    FacilityOwnedByCarvana=row[3]
                ))
        try:
            location_count = len(location_list)
            db.bulk_save_objects(location_list)
            db.commit()
        except Exception as ex:
            error_str = repr(ex)
            location_count = 0

        with open('data/trips.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for idx, row in enumerate(csv_reader):
                if idx == 0:
                    continue
                trips_list.append(trips.Trips(
                    Route=row[0],
                    Origin=row[1],
                    Destination=row[2],
                    WeeklyCapacity=row[3]
                ))
        try:
            trips_count = len(trips_list)
            db.bulk_save_objects(trips_list)
            db.commit()
        except Exception as ex:
            error_str = error_str + " " + repr(ex)
            trips_count = 0
        return location_count, trips_count, error_str
