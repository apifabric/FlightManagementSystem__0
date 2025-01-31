# using resolved_model self.resolved_model FIXME
# created from response, to create create_db_models.sqlite, with test data
#    that is used to create project
# should run without error in manager 
#    if not, check for decimal, indent, or import issues

import decimal
import logging
import sqlalchemy
from sqlalchemy.sql import func 
from decimal import Decimal
from logic_bank.logic_bank import Rule
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date, DateTime, Numeric, Boolean, Text, DECIMAL
from sqlalchemy.types import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from datetime import date   
from datetime import datetime
from typing import List


logging.getLogger('sqlalchemy.engine.Engine').disabled = True  # remove for additional logging

Base = declarative_base()  # from system/genai/create_db_models_inserts/create_db_models_prefix.py


from sqlalchemy.dialects.sqlite import *

class Airport(Base):
    """description: Model representing airports with basic information such as name, city, and country."""
    __tablename__ = 'airport'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    city = Column(String)
    country = Column(String)
    iata_code = Column(String)
    icao_code = Column(String)

class Runway(Base):
    """description: Model representing airport runways with details like length, width, and surface type."""
    __tablename__ = 'runway'
    id = Column(Integer, primary_key=True)
    airport_id = Column(Integer, ForeignKey('airport.id'))
    length_ft = Column(Integer)
    width_ft = Column(Integer)
    surface = Column(String)

class Flight(Base):
    """description: Model representing flights, including details about the airline, flight number, and scheduled times."""
    __tablename__ = 'flight'
    id = Column(Integer, primary_key=True)
    airline = Column(String)
    flight_number = Column(String)
    origin_airport_id = Column(Integer, ForeignKey('airport.id'))
    destination_airport_id = Column(Integer, ForeignKey('airport.id'))
    departure_time = Column(DateTime)
    arrival_time = Column(DateTime)

class BaggageClaim(Base):
    """description: Model representing baggage claim areas at airports with location and capacity details."""
    __tablename__ = 'baggage_claim'
    id = Column(Integer, primary_key=True)
    airport_id = Column(Integer, ForeignKey('airport.id'))
    location = Column(String)
    capacity = Column(Integer)

class Customer(Base):
    """description: Model representing customers/passengers with personal contact information."""
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    phone_number = Column(String)

class Booking(Base):
    """description: Model representing flight bookings made by customers, including seat type and booking date."""
    __tablename__ = 'booking'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    flight_id = Column(Integer, ForeignKey('flight.id'))
    seat_type = Column(String)
    booking_date = Column(DateTime)

class Gate(Base):
    """description: Model representing gates at airports where flights embark and disembark."""
    __tablename__ = 'gate'
    id = Column(Integer, primary_key=True)
    airport_id = Column(Integer, ForeignKey('airport.id'))
    gate_number = Column(String)

class Airline(Base):
    """description: Model representing airlines with basic identification and country of origin."""
    __tablename__ = 'airline'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    country_of_origin = Column(String)
    iata_code = Column(String)
    icao_code = Column(String)

class Cargo(Base):
    """description: Model representing cargo items loaded on flights with weight and descriptive details."""
    __tablename__ = 'cargo'
    id = Column(Integer, primary_key=True)
    airway_bill_number = Column(String)
    flight_id = Column(Integer, ForeignKey('flight.id'))
    weight = Column(Integer)
    description = Column(String)

class Maintenance(Base):
    """description: Model representing maintenance activities performed on runways with description and date."""
    __tablename__ = 'maintenance'
    id = Column(Integer, primary_key=True)
    runway_id = Column(Integer, ForeignKey('runway.id'))
    maintenance_date = Column(DateTime)
    description = Column(String)

class Terminal(Base):
    """description: Model representing airport terminals with an identifier linked to an airport."""
    __tablename__ = 'terminal'
    id = Column(Integer, primary_key=True)
    airport_id = Column(Integer, ForeignKey('airport.id'))
    terminal_number = Column(String)

class Lounge(Base):
    """description: Model representing lounges within airport terminals, including amenities like capacity."""
    __tablename__ = 'lounge'
    id = Column(Integer, primary_key=True)
    terminal_id = Column(Integer, ForeignKey('terminal.id'))
    name = Column(String)
    capacity = Column(Integer)


# end of model classes


try:
    
    
    # ALS/GenAI: Create an SQLite database
    import os
    mgr_db_loc = True
    if mgr_db_loc:
        print(f'creating in manager: sqlite:///system/genai/temp/create_db_models.sqlite')
        engine = create_engine('sqlite:///system/genai/temp/create_db_models.sqlite')
    else:
        current_file_path = os.path.dirname(__file__)
        print(f'creating at current_file_path: {current_file_path}')
        engine = create_engine(f'sqlite:///{current_file_path}/create_db_models.sqlite')
    Base.metadata.create_all(engine)
    
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # ALS/GenAI: Prepare for sample data
    
    
    session.commit()
    airport1 = Airport(name="John F. Kennedy International Airport", city="New York", country="USA", iata_code="JFK", icao_code="KJFK")
    airport2 = Airport(name="Los Angeles International Airport", city="Los Angeles", country="USA", iata_code="LAX", icao_code="KLAX")
    airport3 = Airport(name="Heathrow Airport", city="London", country="UK", iata_code="LHR", icao_code="EGLL")
    airport4 = Airport(name="Changi Airport", city="Singapore", country="Singapore", iata_code="SIN", icao_code="WSSS")
    
    
    
    session.add_all([airport1, airport2, airport3, airport4])
    session.commit()
    # end of test data
    
    
except Exception as exc:
    print(f'Test Data Error: {exc}')
