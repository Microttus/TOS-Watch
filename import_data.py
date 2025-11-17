import requests
from typing import Optional, Union
from pydantic import BaseModel, ValidationError


# ==== Nested Models ====

class MedicalDeviceInformation(BaseModel):
    manufacturer: str
    modelNumber: str
    hardwareRevision: Optional[str] = None
    firmwareRevision: Optional[str] = None
    systemId: Optional[str] = None
    pnpId: Optional[str] = None
    deviceSerialNumber: str


class CGMInfo(BaseModel):
    sensorType: str


class TherapyAlgorithmState(BaseModel):
    autoModeShieldState: str
    autoModeReadinessState: str
    plgmLgsState: str
    waitToCalibrateDuration: int
    safeBasalDuration: int


class LastAlarmAdditionalInfo(BaseModel):
    sg: Optional[int] = None
    pumpDeliverySuspendState: Optional[bool] = None
    pnpId: Optional[str] = None
    alertSilenced: Optional[bool] = None
    unitsRemaining: Optional[float] = None  # now optional


class LastAlarm(BaseModel):
    faultId: str
    version: str
    GUID: str
    dateTime: str
    type: str
    additionalInfo: Optional[LastAlarmAdditionalInfo] = None


class ActiveInsulin(BaseModel):
    amount: float
    datetime: Optional[str] = None
    kind: str
    version: int
    precision: Optional[str] = None


class LastSG(BaseModel):
    kind: str
    version: int
    sg: int
    sensorState: Optional[str] = None
    timestamp: Optional[str] = None


# ==== Main Root Model ====

class DeviceData(BaseModel):
    clientTimeZoneName: str
    lastName: str
    firstName: str
    appModelType: str
    appModelNumber: str
    currentServerTime: int
    conduitSerialNumber: str
    conduitBatteryLevel: int
    conduitBatteryStatus: str
    lastConduitDateTime: str
    lastConduitUpdateServerDateTime: int
    medicalDeviceFamily: str
    medicalDeviceInformation: MedicalDeviceInformation
    medicalDeviceTime: int
    lastMedicalDeviceDataUpdateServerTime: int
    cgmInfo: CGMInfo
    calFreeSensor: bool
    calibStatus: str
    timeToNextEarlyCalibrationMinutes: int
    timeToNextCalibrationMinutes: int
    timeToNextCalibrationRecommendedMinutes: int
    timeToNextCalibHours: int
    finalCalibration: bool
    sensorDurationMinutes: int
    sensorDurationHours: int
    transmitterPairedTime: str
    systemStatusTimeRemaining: int
    gstBatteryLevel: int
    pumpBannerState: Optional[Union[str, list]] = None  # fixed type union
    therapyAlgorithmState: TherapyAlgorithmState
    reservoirLevelPercent: int
    reservoirAmount: int
    pumpSuspended: bool
    pumpBatteryLevelPercent: int
    reservoirRemainingUnits: float
    conduitInRange: bool
    conduitMedicalDeviceInRange: bool
    conduitSensorInRange: bool
    systemStatusMessage: Optional[str] = None
    sensorState: str
    gstCommunicationState: bool
    pumpCommunicationState: bool
    timeFormat: str
    bgUnits: str
    maxAutoBasalRate: float
    maxBolusAmount: float
    sgBelowLimit: int
    approvedForTreatment: bool
    lastAlarm: Optional[LastAlarm] = None
    activeInsulin: ActiveInsulin
    basal: Optional[dict] = None
    lastSensorTime: int
    lastSG: LastSG
    lastSGTrend: str
    belowHypoLimit: int
    aboveHyperLimit: int
    timeInRange: int
    averageSGFloat: float
    averageSG: int
    sensorLifeText: str
    sensorLifeIcon: str



# ==== Fetch + Parse JSON ====

def retrive_updated_data() -> DeviceData:
    try:
        response = requests.get("http://localhost:8081/carelink/nohistory", timeout=5)
        response.raise_for_status()
        updated_data = DeviceData.model_validate_json(response.text)
        return updated_data
    except (requests.RequestException, ValidationError) as e:
        print(f"Error retrieving device data: {e}")
        return None


if __name__ == "__main__":

    data = retrive_updated_data()

    print(f"Device serial: {data.medicalDeviceInformation.deviceSerialNumber}")
    print(f"Last name: {data.lastName}")
    print(f"Algorithm state: {data.therapyAlgorithmState.autoModeShieldState}")
