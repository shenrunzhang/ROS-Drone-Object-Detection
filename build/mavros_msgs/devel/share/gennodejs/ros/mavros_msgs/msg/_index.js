
"use strict";

let ESCStatus = require('./ESCStatus.js');
let MagnetometerReporter = require('./MagnetometerReporter.js');
let ESCTelemetryItem = require('./ESCTelemetryItem.js');
let CamIMUStamp = require('./CamIMUStamp.js');
let ESCInfo = require('./ESCInfo.js');
let Thrust = require('./Thrust.js');
let GPSINPUT = require('./GPSINPUT.js');
let Mavlink = require('./Mavlink.js');
let RTKBaseline = require('./RTKBaseline.js');
let VFR_HUD = require('./VFR_HUD.js');
let StatusText = require('./StatusText.js');
let TimesyncStatus = require('./TimesyncStatus.js');
let LandingTarget = require('./LandingTarget.js');
let WaypointList = require('./WaypointList.js');
let RadioStatus = require('./RadioStatus.js');
let FileEntry = require('./FileEntry.js');
let WaypointReached = require('./WaypointReached.js');
let Vibration = require('./Vibration.js');
let ParamValue = require('./ParamValue.js');
let RCOut = require('./RCOut.js');
let GlobalPositionTarget = require('./GlobalPositionTarget.js');
let ExtendedState = require('./ExtendedState.js');
let ManualControl = require('./ManualControl.js');
let State = require('./State.js');
let DebugValue = require('./DebugValue.js');
let BatteryStatus = require('./BatteryStatus.js');
let ESCTelemetry = require('./ESCTelemetry.js');
let LogData = require('./LogData.js');
let ESCInfoItem = require('./ESCInfoItem.js');
let HilSensor = require('./HilSensor.js');
let ActuatorControl = require('./ActuatorControl.js');
let RCIn = require('./RCIn.js');
let CameraImageCaptured = require('./CameraImageCaptured.js');
let CompanionProcessStatus = require('./CompanionProcessStatus.js');
let ADSBVehicle = require('./ADSBVehicle.js');
let GPSRTK = require('./GPSRTK.js');
let HilGPS = require('./HilGPS.js');
let ESCStatusItem = require('./ESCStatusItem.js');
let TerrainReport = require('./TerrainReport.js');
let LogEntry = require('./LogEntry.js');
let MountControl = require('./MountControl.js');
let CommandCode = require('./CommandCode.js');
let OpticalFlowRad = require('./OpticalFlowRad.js');
let HilStateQuaternion = require('./HilStateQuaternion.js');
let CellularStatus = require('./CellularStatus.js');
let HomePosition = require('./HomePosition.js');
let Altitude = require('./Altitude.js');
let VehicleInfo = require('./VehicleInfo.js');
let Param = require('./Param.js');
let AttitudeTarget = require('./AttitudeTarget.js');
let HilControls = require('./HilControls.js');
let NavControllerOutput = require('./NavControllerOutput.js');
let Waypoint = require('./Waypoint.js');
let Tunnel = require('./Tunnel.js');
let RTCM = require('./RTCM.js');
let GPSRAW = require('./GPSRAW.js');
let OverrideRCIn = require('./OverrideRCIn.js');
let WheelOdomStamped = require('./WheelOdomStamped.js');
let EstimatorStatus = require('./EstimatorStatus.js');
let PlayTuneV2 = require('./PlayTuneV2.js');
let Trajectory = require('./Trajectory.js');
let PositionTarget = require('./PositionTarget.js');
let OnboardComputerStatus = require('./OnboardComputerStatus.js');
let HilActuatorControls = require('./HilActuatorControls.js');

module.exports = {
  ESCStatus: ESCStatus,
  MagnetometerReporter: MagnetometerReporter,
  ESCTelemetryItem: ESCTelemetryItem,
  CamIMUStamp: CamIMUStamp,
  ESCInfo: ESCInfo,
  Thrust: Thrust,
  GPSINPUT: GPSINPUT,
  Mavlink: Mavlink,
  RTKBaseline: RTKBaseline,
  VFR_HUD: VFR_HUD,
  StatusText: StatusText,
  TimesyncStatus: TimesyncStatus,
  LandingTarget: LandingTarget,
  WaypointList: WaypointList,
  RadioStatus: RadioStatus,
  FileEntry: FileEntry,
  WaypointReached: WaypointReached,
  Vibration: Vibration,
  ParamValue: ParamValue,
  RCOut: RCOut,
  GlobalPositionTarget: GlobalPositionTarget,
  ExtendedState: ExtendedState,
  ManualControl: ManualControl,
  State: State,
  DebugValue: DebugValue,
  BatteryStatus: BatteryStatus,
  ESCTelemetry: ESCTelemetry,
  LogData: LogData,
  ESCInfoItem: ESCInfoItem,
  HilSensor: HilSensor,
  ActuatorControl: ActuatorControl,
  RCIn: RCIn,
  CameraImageCaptured: CameraImageCaptured,
  CompanionProcessStatus: CompanionProcessStatus,
  ADSBVehicle: ADSBVehicle,
  GPSRTK: GPSRTK,
  HilGPS: HilGPS,
  ESCStatusItem: ESCStatusItem,
  TerrainReport: TerrainReport,
  LogEntry: LogEntry,
  MountControl: MountControl,
  CommandCode: CommandCode,
  OpticalFlowRad: OpticalFlowRad,
  HilStateQuaternion: HilStateQuaternion,
  CellularStatus: CellularStatus,
  HomePosition: HomePosition,
  Altitude: Altitude,
  VehicleInfo: VehicleInfo,
  Param: Param,
  AttitudeTarget: AttitudeTarget,
  HilControls: HilControls,
  NavControllerOutput: NavControllerOutput,
  Waypoint: Waypoint,
  Tunnel: Tunnel,
  RTCM: RTCM,
  GPSRAW: GPSRAW,
  OverrideRCIn: OverrideRCIn,
  WheelOdomStamped: WheelOdomStamped,
  EstimatorStatus: EstimatorStatus,
  PlayTuneV2: PlayTuneV2,
  Trajectory: Trajectory,
  PositionTarget: PositionTarget,
  OnboardComputerStatus: OnboardComputerStatus,
  HilActuatorControls: HilActuatorControls,
};
