# coding: utf-8
from sqlalchemy import DECIMAL, DateTime  # API Logic Server GenAI assist
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

########################################################################################################################
# Classes describing database for SqlAlchemy ORM, initially created by schema introspection.
#
# Alter this file per your database maintenance policy
#    See https://apilogicserver.github.io/Docs/Project-Rebuild/#rebuilding
#
# Created:  January 31, 2025 14:11:30
# Database: sqlite:////tmp/tmp.YMbzSbVGx8-01JJYB6WJMHM1YBCX8G4S70MCA/FlightManagementSystem/database/db.sqlite
# Dialect:  sqlite
#
# mypy: ignore-errors
########################################################################################################################
 
from database.system.SAFRSBaseX import SAFRSBaseX, TestBase
from flask_login import UserMixin
import safrs, flask_sqlalchemy, os
from safrs import jsonapi_attr
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.sqltypes import NullType
from typing import List

db = SQLAlchemy() 
Base = declarative_base()  # type: flask_sqlalchemy.model.DefaultMeta
metadata = Base.metadata

#NullType = db.String  # datatype fixup
#TIMESTAMP= db.TIMESTAMP

from sqlalchemy.dialects.sqlite import *

if os.getenv('APILOGICPROJECT_NO_FLASK') is None or os.getenv('APILOGICPROJECT_NO_FLASK') == 'None':
    Base = SAFRSBaseX   # enables rules to be used outside of Flask, e.g., test data loading
else:
    Base = TestBase     # ensure proper types, so rules work for data loading
    print('*** Models.py Using TestBase ***')



class Airline(Base):  # type: ignore
    """
    description: Model representing airlines with basic identification and country of origin.
    """
    __tablename__ = 'airline'
    _s_collection_name = 'Airline'  # type: ignore

    id = Column(Integer, primary_key=True)
    name = Column(String)
    country_of_origin = Column(String)
    iata_code = Column(String)
    icao_code = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)



class Airport(Base):  # type: ignore
    """
    description: Model representing airports with basic information such as name, city, and country.
    """
    __tablename__ = 'airport'
    _s_collection_name = 'Airport'  # type: ignore

    id = Column(Integer, primary_key=True)
    name = Column(String)
    city = Column(String)
    country = Column(String)
    iata_code = Column(String)
    icao_code = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)
    BaggageClaimList : Mapped[List["BaggageClaim"]] = relationship(back_populates="airport")
    FlightList : Mapped[List["Flight"]] = relationship(foreign_keys='[Flight.destination_airport_id]', back_populates="destination_airport")
    originFlightList : Mapped[List["Flight"]] = relationship(foreign_keys='[Flight.origin_airport_id]', back_populates="origin_airport")
    GateList : Mapped[List["Gate"]] = relationship(back_populates="airport")
    RunwayList : Mapped[List["Runway"]] = relationship(back_populates="airport")
    TerminalList : Mapped[List["Terminal"]] = relationship(back_populates="airport")



class Customer(Base):  # type: ignore
    """
    description: Model representing customers/passengers with personal contact information.
    """
    __tablename__ = 'customer'
    _s_collection_name = 'Customer'  # type: ignore

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    phone_number = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)
    BookingList : Mapped[List["Booking"]] = relationship(back_populates="customer")



class BaggageClaim(Base):  # type: ignore
    """
    description: Model representing baggage claim areas at airports with location and capacity details.
    """
    __tablename__ = 'baggage_claim'
    _s_collection_name = 'BaggageClaim'  # type: ignore

    id = Column(Integer, primary_key=True)
    airport_id = Column(ForeignKey('airport.id'))
    location = Column(String)
    capacity = Column(Integer)

    # parent relationships (access parent)
    airport : Mapped["Airport"] = relationship(back_populates=("BaggageClaimList"))

    # child relationships (access children)



class Flight(Base):  # type: ignore
    """
    description: Model representing flights, including details about the airline, flight number, and scheduled times.
    """
    __tablename__ = 'flight'
    _s_collection_name = 'Flight'  # type: ignore

    id = Column(Integer, primary_key=True)
    airline = Column(String)
    flight_number = Column(String)
    origin_airport_id = Column(ForeignKey('airport.id'))
    destination_airport_id = Column(ForeignKey('airport.id'))
    departure_time = Column(DateTime)
    arrival_time = Column(DateTime)

    # parent relationships (access parent)
    destination_airport : Mapped["Airport"] = relationship(foreign_keys='[Flight.destination_airport_id]', back_populates=("FlightList"))
    origin_airport : Mapped["Airport"] = relationship(foreign_keys='[Flight.origin_airport_id]', back_populates=("originFlightList"))

    # child relationships (access children)
    BookingList : Mapped[List["Booking"]] = relationship(back_populates="flight")
    CargoList : Mapped[List["Cargo"]] = relationship(back_populates="flight")



class Gate(Base):  # type: ignore
    """
    description: Model representing gates at airports where flights embark and disembark.
    """
    __tablename__ = 'gate'
    _s_collection_name = 'Gate'  # type: ignore

    id = Column(Integer, primary_key=True)
    airport_id = Column(ForeignKey('airport.id'))
    gate_number = Column(String)

    # parent relationships (access parent)
    airport : Mapped["Airport"] = relationship(back_populates=("GateList"))

    # child relationships (access children)



class Runway(Base):  # type: ignore
    """
    description: Model representing airport runways with details like length, width, and surface type.
    """
    __tablename__ = 'runway'
    _s_collection_name = 'Runway'  # type: ignore

    id = Column(Integer, primary_key=True)
    airport_id = Column(ForeignKey('airport.id'))
    length_ft = Column(Integer)
    width_ft = Column(Integer)
    surface = Column(String)

    # parent relationships (access parent)
    airport : Mapped["Airport"] = relationship(back_populates=("RunwayList"))

    # child relationships (access children)
    MaintenanceList : Mapped[List["Maintenance"]] = relationship(back_populates="runway")



class Terminal(Base):  # type: ignore
    """
    description: Model representing airport terminals with an identifier linked to an airport.
    """
    __tablename__ = 'terminal'
    _s_collection_name = 'Terminal'  # type: ignore

    id = Column(Integer, primary_key=True)
    airport_id = Column(ForeignKey('airport.id'))
    terminal_number = Column(String)

    # parent relationships (access parent)
    airport : Mapped["Airport"] = relationship(back_populates=("TerminalList"))

    # child relationships (access children)
    LoungeList : Mapped[List["Lounge"]] = relationship(back_populates="terminal")



class Booking(Base):  # type: ignore
    """
    description: Model representing flight bookings made by customers, including seat type and booking date.
    """
    __tablename__ = 'booking'
    _s_collection_name = 'Booking'  # type: ignore

    id = Column(Integer, primary_key=True)
    customer_id = Column(ForeignKey('customer.id'))
    flight_id = Column(ForeignKey('flight.id'))
    seat_type = Column(String)
    booking_date = Column(DateTime)

    # parent relationships (access parent)
    customer : Mapped["Customer"] = relationship(back_populates=("BookingList"))
    flight : Mapped["Flight"] = relationship(back_populates=("BookingList"))

    # child relationships (access children)



class Cargo(Base):  # type: ignore
    """
    description: Model representing cargo items loaded on flights with weight and descriptive details.
    """
    __tablename__ = 'cargo'
    _s_collection_name = 'Cargo'  # type: ignore

    id = Column(Integer, primary_key=True)
    airway_bill_number = Column(String)
    flight_id = Column(ForeignKey('flight.id'))
    weight = Column(Integer)
    description = Column(String)

    # parent relationships (access parent)
    flight : Mapped["Flight"] = relationship(back_populates=("CargoList"))

    # child relationships (access children)



class Lounge(Base):  # type: ignore
    """
    description: Model representing lounges within airport terminals, including amenities like capacity.
    """
    __tablename__ = 'lounge'
    _s_collection_name = 'Lounge'  # type: ignore

    id = Column(Integer, primary_key=True)
    terminal_id = Column(ForeignKey('terminal.id'))
    name = Column(String)
    capacity = Column(Integer)

    # parent relationships (access parent)
    terminal : Mapped["Terminal"] = relationship(back_populates=("LoungeList"))

    # child relationships (access children)



class Maintenance(Base):  # type: ignore
    """
    description: Model representing maintenance activities performed on runways with description and date.
    """
    __tablename__ = 'maintenance'
    _s_collection_name = 'Maintenance'  # type: ignore

    id = Column(Integer, primary_key=True)
    runway_id = Column(ForeignKey('runway.id'))
    maintenance_date = Column(DateTime)
    description = Column(String)

    # parent relationships (access parent)
    runway : Mapped["Runway"] = relationship(back_populates=("MaintenanceList"))

    # child relationships (access children)
