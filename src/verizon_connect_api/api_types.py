from typing import TypedDict, Optional


class Vehicle(TypedDict):
    Name: str
    VehicleNumber: Optional[str]
    RegistrationNumber: Optional[str]
    VIN: Optional[str]
    Make: Optional[str]
    Year: Optional[int]
    Model: Optional[str]
    TankCapacity: Optional[float]
    HighwayMPG: Optional[float]
    CityMPG: Optional[float]
    FuelType: int
    VehicleSize: int
    HasNavigationDevice: bool
    HasTachograph: bool


class PartialVehicle(TypedDict):
    Name: str
    Number: Optional[str]


class ActiveDiagnosticTroubleCodes(TypedDict):
    VehicleNumber: str
    VehicleName: str
    ActiveDTCs: str
    LastUpdatedDateTime: str


class DiagnosticTroubleCode(TypedDict):
    DTC: str
    IsActive: bool
    LastUpdatedDateTime: str


class DiagnosticTroubleCodeHistory(TypedDict):
    VehicleNumber: str
    VehicleName: str
    DTCs: list[DiagnosticTroubleCode]


class EngineControlModuleStatus(TypedDict):
    CurrentOdometer: float
    DeviceTimeZoneOffset: Optional[int]
    DeviceTimeZoneUseDST: bool
    DisplayState: str
    DriverName: Optional[str]
    DriverNumber: Optional[str]
    DTCs: Optional[list[str]]
    # haha typo in production
    EngineMintutes: int
    FuelLevelPercentage: float
    IdleTime: int
    Speed: float
    SensorValues: list[str]
    UpdateUTC: str
    TotalFuelUsed: float
    TotalIdleFuel: float
    TotalPTOFuel: float
    TotalPTOTime: int
    VIN: str
    BatteryLevel: Optional[float]
    TractionBatteryChargingLastStartUtc: Optional[str]
    TractionBatteryChargingUtc: Optional[str]


class Address(TypedDict):
    AddressLine1: str
    AddressLine2: str
    Locality: str
    AdministrativeArea: str
    PostalCode: str
    Country: str


class Coordinates(TypedDict):
    Longitude: float
    Latitude: float


class AddressWithCoordinates(Address, Coordinates):
    pass


class VehicleGPSLocation(Coordinates, TypedDict):
    VehicleNumber: str
    VehicleName: str
    OdometerInKM: float
    UpdateUtc: str
    IsPrivate: bool
    DriverNumber: Optional[str]
    FirstName: Optional[str]
    LastName: Optional[str]
    Address: Address
    Speed: float
    BatteryLevel: Optional[float]
    TractionBatteryChargingLastStartUtc: Optional[str]
    TractionBatteryChargingUtc: Optional[str]


class LocationStatus(Coordinates, TypedDict):
    Address: Address
    DeltaDistance: float
    DeltaTime: int
    DeviceTimeZoneOffset: Optional[int]
    DeviceTimeZoneUseDST: bool
    DisplayState: str
    Direction: int
    Heading: str
    DriverNumber: Optional[str]
    GeoFenceName: Optional[str]
    Speed: float
    UpdateUTC: str
    IsPrivate: bool


class Segment(TypedDict):
    StartDateUtc: str
    StartLocation: AddressWithCoordinates
    StartLocationIsPrivate: bool
    EndLocation: AddressWithCoordinates
    EndDateUtc: str
    EndLocationIsPrivate: bool
    IsComplete: bool
    DistanceKilometers: float


class SegmentHistory(TypedDict):
    Driver: Optional[str]
    Vehicle: PartialVehicle
    Segments: list[Segment]


class VehicleStatus(TypedDict):
    DeviceTimeZoneOffset: Optional[int]
    DeviceTimeZoneUseDST: bool
    DisplayState: str
    DriverNumber: Optional[str]
    Speed: float
    UpdateUTC: str
    DriverName: Optional[str]
    EngineMinutes: int
    CurrentOdometer: float
    IdleTime: int
    SensorValues: list[str]
    BatteryLevel: Optional[float]
    TractionBatteryChargingUtc: Optional[str]
    TractionBatteryChargingLastStartUtc: Optional[str]
