from fastapi import FastAPI, Query, Depends
from typing import List
from services.data_loader import DataLoader
from sqlalchemy.orm import Session
from fastapi import Depends
from models import trips, locations
from services.database import SessionLocal, engine


app = FastAPI()

trips.Base.metadata.create_all(bind=engine)
locations.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get('/reports')
def get_reports(location_codes: List[str] = Query(None), db: Session = Depends(get_db)):
    """
    API call to generate detailed reports for given location codes
    :return:
    """
    if not location_codes:
        return {"error_msg": "Location code missing"}
    dl = DataLoader()
    output_reports, error_msg = dl.generate_reports(location_codes, db)
    return {
        "report": output_reports,
        "error_msg": error_msg
    }


@app.post("/records")
def populate_records(db: Session = Depends(get_db)):
    """
    API to populate records into the DB (reads from CSV)
    Throws exception if entries already exists in the DB

    :return:
    """
    dl = DataLoader()
    location_count, trips_count, error_message = dl.load_locations_trips_into_db(db)
    return {
        "locations_added": location_count,
        "trips_added": trips_count,
        "error_message": error_message
    }


@app.delete("/records")
def delete_all_records(db: Session = Depends(get_db)):
    """
    API to delete every records in the trips & location tables (if exists)
    :return:
    """
    dl = DataLoader()
    locations_num_rows_deleted, trips_num_rows_deleted, error = dl.delete_entries_in_locations_trips(db)
    return {
        "locations_num_rows_deleted": locations_num_rows_deleted,
        "trips_num_rows_deleted": trips_num_rows_deleted,
        "error_message": error
    }


