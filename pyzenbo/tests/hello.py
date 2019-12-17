import pyzenbo
from pyzenbo.modules.dialog_system import RobotFace

host = '192.168.0.186'
sdk = pyzenbo.connect(host)

sdk.robot.set_expression(RobotFace.DEFAULT, 'Hello World')
sdk.robot.set_expression(RobotFace.HIDEFACE)

sdk.release()
