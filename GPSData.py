from Constants import Constants

class GPSData():

    utc_time    = ''
    pos_status  = ''
    lat         = ''
    lat_dir     = ''
    lon         = ''
    lon_dir     = ''
    speed       = ''
    track       = ''
    date        = ''
    mag_var     = ''
    var_dir     = ''
    mode_ind    = ''

    quality     = ''
    sat_num     = ''
    hdop        = ''
    alt         = ''
    a_units     = ''
    undulation  = ''
    u_units     = ''
    age         = ''
    station_id  = ''

    def parseData(self, data):
        gps_arr = data.split(',')
        gps_sentence = gps_arr[0]
        gps_data = gps_arr[1:]

        if gps_sentence == Constants.gps_sentences[0]:
            self.utc_time    = gps_data[0]
            self.pos_status  = gps_data[1]
            self.lat         = gps_data[2]
            self.lat_dir     = gps_data[3]
            self.lon         = gps_data[4]
            self.lon_dir     = gps_data[5]
            self.speed       = gps_data[6]
            self.track       = gps_data[7]
            self.date        = gps_data[8]
            self.mag_var     = gps_data[9]
            self.var_dir     = gps_data[10]
            self.mode_ind    = gps_data[11].split('*')[0]

        elif gps_sentence == Constants.gps_sentences[1]:
            self.utc_time    = gps_data[0]
            self.lat         = gps_data[1]
            self.lat_dir     = gps_data[2]
            self.lon         = gps_data[3]
            self.lon_dir     = gps_data[4]
            self.quality     = gps_data[5]
            self.sat_num     = gps_data[6]
            self.hdop        = gps_data[7]
            self.alt         = gps_data[8]
            self.a_units     = gps_data[9]
            self.undulation  = gps_data[10]
            self.u_units     = gps_data[11]
            self.age         = gps_data[12]
            self.station_id  = gps_data[13].split('*')[0]

    def isValid(self) -> bool:
        return self.pos_status == 'A'
    
    def getLatitude(self):
        if len(self.lat) == 0: return ''
        s = ''
        if self.lat_dir == 'S':
            s += '-'

        l_arr = self.lat.split('.')
        s += l_arr[0][:-2] + ' ' + l_arr[0][-2:] + '.' + l_arr[1]
        return s
    
    def getLongitude(self):
        if len(self.lon) == 0: return ''
        s = ''
        if self.lon_dir == 'W':
            s += '-'

        l_arr = self.lon.split('.')
        s += l_arr[0][:-2] + ' ' + l_arr[0][-2:] + '.' + l_arr[1]
        return s
    
    def getAltitude(self, format='I'):
        if len(self.alt) == 0: return '0'
        if format == 'I':
            return '{:.2f}'.format(float(self.alt) * 3.28084)
        else:
            return self.alt
        
    def getSpeed(self, format='I'):
        if len(self.speed) == 0: return '0'
        if format == 'I':
            return '{:.0f}'.format(float(self.speed) * 1.15078)
        else:
            return self.speed