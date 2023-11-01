'''
Forza UDP test

'''

import socket, struct, time

localIp = "127.0.0.1"
localPort = 1337
bufferSize = 331


#Create a datagram socket.
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

#Bind to address and ip, then display message.

UDPServerSocket.bind((localIp, localPort))
print("UDP Server up and listening!")

#Listen for incoming datagrams.
dataFormat = '<iIfffffffffffffffffffffffffffiiiiffffffffffffffffffffiiiiifffffffffffffffffHBBBBBBbbbffffi'
ForzaTelemetryVariables = ['isRaceOn','TimestampMS','EngineMaxRPM','EngineIdleRPM','CurrentEngineRPM','AccelerationX','AccelerationY','AccelerationZ','VelocityX','VelocityY','VelocityZ','AngularVelocityX','AngularVelocityY','AngularVelocityZ','Yaw','Pitch','Roll','NormalizedSuspensionTravelFrontLeft','NormalizedSuspensionTravelFrontRight','NormalizedSuspensionTravelRearLeft','NormalizedSuspensionTravelRearRight','TireSlipRatioFrontLeft','TireSlipRatioFrontRight','TireSlipRatioRearLeft','TireSlipRatioRearRight','WheelRotationSpeedFrontLeft','WheelRotationSpeedFrontRight','WheelRotationSpeedRearLeft','WheelRotationSpeedRearRight','WheelOnRumbleStripFrontLeft','WheelOnRumbleStripFrontRight','WheelOnRumbleStripRearLeft','WheelOnRumbleStripRearRight','WheelInPuddleDepthFrontLeft','WheelInPuddleDepthFrontRight','WheelInPuddleDepthRearLeft','WheelInPuddleDepthRearRight','SurfaceRumbleFrontLeft','SurfaceRumbleFrontRight','SurfaceRumbleRearLeft','SurfaceRumbleRearRight','TireSlipAngleFrontLeft','TireSlipAngleFrontRight','TireSlipAngleRearLeft','TireSlipAngleRearRight','TireCombinedSlipFrontLeft','TireCombinedSlipFrontRight','TireCombinedSlipRearLeft','TireCombinedSlpRearRight','SuspensionTravelMetersFrontLeft','SuspensionTravelMetersFrontRight','SuspensionTravelMetersRearLeft','SuspensionTravelMetersRearRight','CarMake/Model','CarClass','CarPerformanceIndex','DrivetrainType','NumberOfCylinders','PositionX','PositionY','PositionZ','Speed','Power','Torque','TireTempFrontLeft','TireTempFrontRight','TireTempRearLeft','TireTempRearRight','Boost','Fuel','DistanceTraveled','BestLap','LastLap','CurrentLap','CurrentRaceTime','LapNumber','RacePosition','Accel','Brake','Clutch','Steer','NormalisedDrivingLine','NormalisedAiBrakeDifference','TireWearFrontLeft','TireWearFrontRight','TireWearRearLeft','TireWearRearRight','TrackId']

dataExpectedSize = struct.calcsize(dataFormat)
bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)    
message = bytesAddressPair[0]
print("Expected message length: "+ str(dataExpectedSize))
print('Received message length: '+ str(len(message)))
while(True):
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPServerSocket.bind((localIp, localPort))
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)    
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]
    if len(bytesAddressPair[0]) == dataExpectedSize:

        unpackedData = struct.unpack(dataFormat, message)
        zippedData = zip(ForzaTelemetryVariables,unpackedData)
        freshList = list(zippedData)
        if freshList[0][1] == 1:
            print("Structured dump from forza: ")
            print(freshList)
        else:
            print('Game in Menu')
    else:
        print("Received data does not match the expected format. Are you on Dash or Sled?")
    time.sleep(4)


