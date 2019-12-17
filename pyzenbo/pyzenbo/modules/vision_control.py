import pyzenbo.modules.zenbo_command as commands
from pyzenbo.modules.inter_communication import DESTINATION
from pyzenbo.modules.wait_for import WaitForDetectFace, WaitForRecognizeFace


class VisionControl:
    def __init__(self, inter_comm):
        self._inter_comm = inter_comm

    def cancel_detect_face(self):
        """
        Cancel the running detect face process.

        :return: serial number of the command, if command is blocking also
            return a dict, it include two key, 'state' indicate execute
            result and 'error' will contain error code
        """
        des = DESTINATION["vision"]
        cmd = commands.VISION_CANCEL_DETECT_FACE
        data = {}
        serial, error = self._inter_comm.send_command(
            des, cmd, data, False, None)
        return serial, error

    def cancel_detect_person(self):
        """
        Cancel the running detect person process.

        :return: serial number of the command, if command is blocking also
            return a dict, it include two key, 'state' indicate execute
            result and 'error' will contain error code
        """
        des = DESTINATION["vision"]
        cmd = commands.VISION_CANCEL_DETECT_PERSON
        data = {}
        serial, error = self._inter_comm.send_command(
            des, cmd, data, False, None)
        return serial, error

    def cancel_recognize_person(self):
        """
        Cancel the running recognize person process.

        :return: serial number of the command, if command is blocking also
            return a dict, it include two key, 'state' indicate execute
            result and 'error' will contain error code
        """
        des = DESTINATION["vision"]
        cmd = commands.VISION_CANCEL_RECOGNIZE_PERSON
        data = {}
        serial, error = self._inter_comm.send_command(
            des, cmd, data, False, None)
        return serial, error

    def request_detect_face(
            self,
            interval=1,
            enable_debug_preview=False,
            enable_detect_head=False,
            enable_face_posture=False,
            enable_candidate_obj=False,
            enable_head_gaze_classifier=False,
            sync=False,
            timeout=None):
        """
        Request detect faces, and the result is returned by
        vision_callback. A face list will be returned as detecting faces.
        user's face with trackID with respect to Robot Base Coordinates
        (in meters), x axis means robot to user depth, y means left/right
        shift, z means user height above ground.

        :param interval: face detect interval accept only positive integer in
            seconds, default is 1
        :param enable_debug_preview: enable debug preview, default is False
        :param enable_detect_head: turn on the head detection, when head
            detection off, default is False
        :param enable_face_posture: turn on detect head orientation,
            default is False
        :param enable_candidate_obj: turn on report bounding box on possible
            person region, default is False
        :param enable_head_gaze_classifier: turn on head direction classifier
            mostly used tf previous head orientation, beyond detection
            limit and cannot report value, default is False
        :param sync: True if this command is blocking
        :param timeout: maximum blocking time in second, None means infinity
        :return: serial number of the command, if command is blocking also
            return a dict, it include two key, 'state' indicate execute
            result and 'error' will contain error code
        """
        des = DESTINATION["vision"]
        cmd = commands.VISION_REQUEST_DETECT_FACE
        data = {
            'interval': int(interval * 1000),
            'enableDebugPreview': bool(enable_debug_preview),
            'enableDetectHead': bool(enable_detect_head),
            'enableFacePosture': bool(enable_face_posture),
            'enableCandidateObj': bool(enable_candidate_obj),
            'enableHeadGazeClassifier': bool(enable_head_gaze_classifier),
        }
        serial, error = self._inter_comm.send_command(
            des, cmd, data, sync, timeout)
        return serial, error

    def request_detect_person(
            self,
            interval=1,
            enable_debug_preview=False,
            enable_detect_head=False,
            sync=False,
            timeout=None):
        """
        Request detect a person, and the result is returned by vision_callback.
        The body tracking function now only supports tracking an individual
        person.

        :param interval: detect person interval accept only positive integer
            in seconds, default is 1.
        :param enable_debug_preview: enable debug preview, default is False.
        :param enable_detect_head: turn on the head detection, when head
            detection off, default is False
        :param sync: True if this command is blocking
        :param timeout: maximum blocking time in second, None means infinity
        :return: serial number of the command, if command is blocking also
            return a dict, it include two key, 'state' indicate execute
            result and 'error' will contain error code
        """
        des = DESTINATION["vision"]

        cmd = commands.VISION_REQUEST_DETECT_PERSON
        data = {
            'interval': int(interval * 1000),
            'enableDebugPreview': bool(enable_debug_preview),
            'enableDetectHead': bool(enable_detect_head),
        }
        serial, error = self._inter_comm.send_command(
            des, cmd, data, sync, timeout)
        return serial, error

    def request_recognize_person(
            self,
            interval=1,
            enable_debug_preview=False,
            enable_detect_head=False,
            enable_face_posture=False,
            enable_candidate_obj=False,
            enable_head_gaze_classifier=False,
            sync=False,
            timeout=None):
        """
        Request robot to recognize person who has enrolled, and the result is
        returned by vision_callback.

        :param interval: recognize person interval accept only positive integer
            in seconds, default is 1
        :param enable_debug_preview: enable debug preview, default is False
        :param enable_detect_head: turn on the head detection, when head
            detection off, default is False
        :param enable_face_posture: turn on detect head orientation,
            default is False
        :param enable_candidate_obj: turn on report bounding box on possible
            person region, default is False
        :param enable_head_gaze_classifier: turn on head direction classifier
            mostly used tf previous head orientation, beyond detection
            limit and cannot report value, default is False
        :param sync: True if this command is blocking
        :param timeout: maximum blocking time in second, None means infinity
        :return: serial number of the command, if command is blocking also
            return a dict, it include two key, 'state' indicate execute
            result and 'error' will contain error code
        """
        des = DESTINATION["vision"]
        cmd = commands.VISION_REQUEST_RECOGNIZE_PERSON
        data = {
            'interval': int(interval * 1000),
            'enableDebugPreview': bool(enable_debug_preview),
            'enableDetectHead': bool(enable_detect_head),
            'enableFacePosture': bool(enable_face_posture),
            'enableCandidateObj': bool(enable_candidate_obj),
            'enableHeadGazeClassifier': bool(enable_head_gaze_classifier),
        }
        serial, error = self._inter_comm.send_command(
            des, cmd, data, sync, timeout)
        return serial, error

    def wait_for_detect_face(self,
                             interval=1,
                             enable_debug_preview=False,
                             enable_detect_head=False,
                             enable_face_posture=False,
                             enable_candidate_obj=False,
                             enable_head_gaze_classifier=False,
                             timeout=10):
        """
        Wait for detect faces execute completed and return the detect faces
        result.

        :param interval: face detect interval accept only positive integer in
            seconds, default is 1
        :param enable_debug_preview: enable debug preview, default is False
        :param enable_detect_head: turn on the head detection, when head
            detection off, default is False
        :param enable_face_posture: turn on detect head orientation,
            default is False
        :param enable_candidate_obj: turn on report bounding box on possible
            person region, default is False
        :param enable_head_gaze_classifier: turn on head direction classifier
            mostly used tf previous head orientation, beyond detection
            limit and cannot report value, default is False
        :param timeout: maximum blocking time in second, None means infinity
        :return: detect face result, if timeout will return None
        """
        self.request_detect_face(interval,
                                 enable_debug_preview,
                                 enable_detect_head,
                                 enable_face_posture,
                                 enable_candidate_obj,
                                 enable_head_gaze_classifier)
        wait_for_detect_face = WaitForDetectFace(self._inter_comm)
        wait_for_result = wait_for_detect_face.start(timeout)
        self.cancel_detect_face()
        return wait_for_result

    def wait_for_recognize_person(self,
                                  user_id,
                                  interval=1,
                                  enable_debug_preview=False,
                                  enable_detect_head=False,
                                  enable_face_posture=False,
                                  enable_candidate_obj=False,
                                  enable_head_gaze_classifier=False,
                                  timeout=10):
        """
        Wait for recognize person execute completed and return the recognize
        result.

        :param user_id: given an specified name to wait for recognize
        :param interval: face detect interval accept only positive integer in
            seconds, default is 1
        :param enable_debug_preview: enable debug preview, default is False
        :param enable_detect_head: turn on the head detection, when head
            detection off, default is False
        :param enable_face_posture: turn on detect head orientation,
            default is False
        :param enable_candidate_obj: turn on report bounding box on possible
            person region, default is False
        :param enable_head_gaze_classifier: turn on head direction classifier
            mostly used tf previous head orientation, beyond detection
            limit and cannot report value, default is False
        :param timeout: maximum blocking time in second, None means infinity
        :return: recognize result, if timeout will return None
        """
        self.request_recognize_person(interval,
                                      enable_debug_preview,
                                      enable_detect_head,
                                      enable_face_posture,
                                      enable_candidate_obj,
                                      enable_head_gaze_classifier)
        wait_for_recognize_face = WaitForRecognizeFace(self._inter_comm)
        wait_for_result = wait_for_recognize_face.start(user_id, timeout)
        self.cancel_recognize_person()
        return wait_for_result
