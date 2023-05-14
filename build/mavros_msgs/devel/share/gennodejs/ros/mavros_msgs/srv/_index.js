
"use strict";

let VehicleInfoGet = require('./VehicleInfoGet.js')
let FileRemove = require('./FileRemove.js')
let LogRequestList = require('./LogRequestList.js')
let CommandLong = require('./CommandLong.js')
let FileRemoveDir = require('./FileRemoveDir.js')
let FileClose = require('./FileClose.js')
let WaypointPull = require('./WaypointPull.js')
let MountConfigure = require('./MountConfigure.js')
let CommandTOL = require('./CommandTOL.js')
let CommandInt = require('./CommandInt.js')
let WaypointSetCurrent = require('./WaypointSetCurrent.js')
let FileChecksum = require('./FileChecksum.js')
let ParamGet = require('./ParamGet.js')
let ParamSet = require('./ParamSet.js')
let LogRequestData = require('./LogRequestData.js')
let WaypointClear = require('./WaypointClear.js')
let SetMode = require('./SetMode.js')
let CommandAck = require('./CommandAck.js')
let WaypointPush = require('./WaypointPush.js')
let MessageInterval = require('./MessageInterval.js')
let ParamPush = require('./ParamPush.js')
let CommandBool = require('./CommandBool.js')
let ParamPull = require('./ParamPull.js')
let CommandTriggerControl = require('./CommandTriggerControl.js')
let CommandTriggerInterval = require('./CommandTriggerInterval.js')
let StreamRate = require('./StreamRate.js')
let FileRead = require('./FileRead.js')
let CommandVtolTransition = require('./CommandVtolTransition.js')
let CommandHome = require('./CommandHome.js')
let LogRequestEnd = require('./LogRequestEnd.js')
let FileList = require('./FileList.js')
let FileRename = require('./FileRename.js')
let SetMavFrame = require('./SetMavFrame.js')
let FileWrite = require('./FileWrite.js')
let FileOpen = require('./FileOpen.js')
let FileTruncate = require('./FileTruncate.js')
let FileMakeDir = require('./FileMakeDir.js')

module.exports = {
  VehicleInfoGet: VehicleInfoGet,
  FileRemove: FileRemove,
  LogRequestList: LogRequestList,
  CommandLong: CommandLong,
  FileRemoveDir: FileRemoveDir,
  FileClose: FileClose,
  WaypointPull: WaypointPull,
  MountConfigure: MountConfigure,
  CommandTOL: CommandTOL,
  CommandInt: CommandInt,
  WaypointSetCurrent: WaypointSetCurrent,
  FileChecksum: FileChecksum,
  ParamGet: ParamGet,
  ParamSet: ParamSet,
  LogRequestData: LogRequestData,
  WaypointClear: WaypointClear,
  SetMode: SetMode,
  CommandAck: CommandAck,
  WaypointPush: WaypointPush,
  MessageInterval: MessageInterval,
  ParamPush: ParamPush,
  CommandBool: CommandBool,
  ParamPull: ParamPull,
  CommandTriggerControl: CommandTriggerControl,
  CommandTriggerInterval: CommandTriggerInterval,
  StreamRate: StreamRate,
  FileRead: FileRead,
  CommandVtolTransition: CommandVtolTransition,
  CommandHome: CommandHome,
  LogRequestEnd: LogRequestEnd,
  FileList: FileList,
  FileRename: FileRename,
  SetMavFrame: SetMavFrame,
  FileWrite: FileWrite,
  FileOpen: FileOpen,
  FileTruncate: FileTruncate,
  FileMakeDir: FileMakeDir,
};
