import csv
import time
import config as cfg

class LoggingSystem:
    
    def __init__(self, marker_service):
        if cfg.isLogEnabled == False:
            return
        
        self._marker_service = marker_service
        self.name_logfile = 'logfile_{}.csv'.format(self.get_time_stamp("init"))
        with open(self.name_logfile, mode='w') as logfile:
            writer = csv.writer(logfile)
            writer.writerow(['timestamp', 'marker nr', 'distance', 'angle'])
            writer.writerow([self.get_time_stamp(), 'init', 'init', 'init'])
    
    def update(self):
        if cfg.isLogEnabled == False:
            return
        
        markers = self._marker_service.get_markers()        
        if markers is None:
            return
        
        for i in range(0, len(markers)):
            with open(self.name_logfile, mode='a') as logfile:
                writer = csv.writer(logfile)
                distance = self._marker_service.get_distance(markers[i])
                angle = self._marker_service.get_angle(markers[i])
                writer.writerow([self.get_time_stamp(), str(markers[i]), str(distance), str(angle)])
                
    def dispose(self):
        if cfg.isLogEnabled == False:
            return
        with open(self.name_logfile, mode='a') as logfile:
            writer = csv.writer(logfile)
            writer.writerow([self.get_time_stamp(),'end', 'end', 'end'])
    
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