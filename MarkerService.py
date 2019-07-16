class MarkerService:
    
    def __init__(self):
        self._markers = [] # contains an array of all markers
        self._corners = { } # maps marker id to an array of corners
        self._forward = { } 
        self._marker_centers = { } # maps marker id to its marker center
        self._distances = { } # maps the distance between the camera and a marker id
        self._angles = { } 
        self._frame = None
        self._corners_array = None
        
    def get_markers(self):
        """
        Returns an array of all detected marker ids
        """
        return self._markers
    
    def update_marker(self, marker_id, corners, marker_center, distance, angle):
        """
        Updates the properties for a single marker
        """
        self._markers.append(marker_id)
        self._corners[marker_id] = corners
        self._marker_centers[marker_id] = marker_center
        self._distances[marker_id] = distance
        self._angles[marker_id] = angle
        return
    
    def get_angle(self, marker_id):
        return self._angles[marker_id]
    
    def get_corners(self, marker_id):
        if marker_id in self._corners:
            return self._corners[marker_id]
        return None
    
    def get_distance(self, marker_id):
        return self._distances[marker_id]
    
    def set_forward(self, marker_id, forward):
        self._forward[marker_id] = forward
    
    def get_forward(self, marker_id):
        if marker_id in self._forward:
            return self._forward[marker_id]
        return None
    
    def set_corners_array(self, corners):
        self._corners_array = corners
        
    def get_corners_array(self):
        return self._corners_array;

    def clear(self):
        self._markers.clear()
        self._corners.clear()
        self._forward.clear()
        self._marker_centers.clear()
        self._distances.clear()
        self._angles.clear()
        return