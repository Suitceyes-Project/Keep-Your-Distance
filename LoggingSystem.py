import csv
import time
import config as cfg

class LoggingSystem:
    
    def __init__(self, marker_service):
        if cfg.isLogEnabled == False:
            return
        
        self._marker_service = marker_service
        self._name_logfile = 'logfile_{}.csv'.format(self.get_time_stamp("init"))
            
    def __enter__(self):
        if cfg.isLogEnabled == False:
            return self
        
        self._logfile = open(self._name_logfile, mode='w')
        self._writer = csv.writer(self._logfile)            
        self._writer.writerow(['timestamp', 'marker nr', 'distance', 'angle'])
        self._write_row('init', 'init', 'init')
        return self
        
    def __exit__(self, exc_type, exc_value, traceback):
        self._dispose()
        
    def _write_row(self, marker, distance, angle):
        self._writer.writerow([self.get_time_stamp(), marker, distance, angle])
    
    def update(self):
        if cfg.isLogEnabled == False:
            return
        
        markers = self._marker_service.get_markers()        
        if markers is None:
            return
        
        for i in range(0, len(markers)):
            distance = self._marker_service.get_distance(markers[i])
            angle = self._marker_service.get_angle(markers[i])
            self._write_row(str(markers[i]), str(distance), str(angle))
                
    def _dispose(self):
        if cfg.isLogEnabled == False:
            return
        self._write_row('end', 'end', 'end')
        self._logfile.close()
        
    
    # ----------------------------------------------------------------------------------------------------------------------
    # returns current time stamp in format: 2019-04-20 12:25:25
    @staticmethod
    def get_time_stamp(S=""):
        ts = time.gmtime()

        if S != "":
            # returns current time stamp for naming the logfile: 04-20_12-25
            timestamp = time.strftime("%m-%d_%H-%M", ts)
        else:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S", ts)

        return timestamp