

gps_d = [
    '$GPRMC,183701.00,A,4739.454136,N,11717.264615,W,0.0,0.0,241024,16.6,W,A*02',
    '$GPGGA,183701.00,4739.454136,N,11717.264615,W,1,06,1.6,594.4,M,-17.3,M,,*5C'
]

gps = GPSData()
for data in gps_d:
    if data.startswith('$'):
            gps.parseData(data)

print(gps.getLatitude(), gps.getLongitude(), gps.getAltitude(), gps.getSpeed())


    