import csv
from models import trips, locations


class DataLoader:

    @staticmethod
    def generate_reports(location_codes=None, db=None):
        output, error_str = [], ''
        try:
            for code in location_codes:
                temp_dict = {}
                location_from_db = db.query(locations.Locations).filter_by(LocationCode=code).first()
                if not location_from_db:
                    raise Exception("Not a valid location code")
                temp_dict["LocationCode"] = location_from_db.LocationCode
                temp_dict["Latitude"] = location_from_db.Latitude
                temp_dict["Longitude"] = location_from_db.Longitude
                temp_dict["FacilityOwnedByCarvana"] = True if location_from_db.FacilityOwnedByCarvana else False

                trip_origin_from_db = db.query(trips.Trips).filter_by(Origin=code).all()
                if trip_origin_from_db:
                    origin = []
                    for item in trip_origin_from_db:
                        origin.append(f"{item.Origin} to {item.Destination} ({item.WeeklyCapacity} Weekly Capacity)")
                    temp_dict["OriginTrips"] = origin
                trip_destination_from_db = db.query(trips.Trips).filter_by(Destination=code).all()
                if trip_destination_from_db:
                    destination = []
                    for item in trip_destination_from_db:
                        destination.append(f"{item.Origin} to {item.Destination} ({item.WeeklyCapacity} Weekly Capacity)")
                    temp_dict["DestinationTrips"] = destination
                output.append(temp_dict)
        except Exception as ex:
            error_str = repr(ex)
        return output, error_str

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

