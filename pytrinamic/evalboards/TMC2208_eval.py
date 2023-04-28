from pytrinamic.evalboards import TMCLEval
from pytrinamic.ic import TMC2208
from pytrinamic.features import MotorControlModule


class TMC2208_eval(TMCLEval):
    """
    This class represents a TMC2208 Evaluation board.

    Communication is done over the TMCL commands writeDRV and readDRV. An
    implementation without TMCL may still use this class if these two functions
    are provided properly. See __init__ for details on the function
    requirements.
    """
    def __init__(self, connection, module_id=1):
        """
        Parameters:
            connection:
                Type: class
                A class that provides the necessary functions for communicating
                with a TMC2208. The required functions are
                    connection.writeDRV(registerAddress, value, moduleID)
                    connection.readDRV(registerAddress, moduleID, signed)
                for writing/reading to registers of the TMC2208.
            module_id:
                Type: int, optional, default value: 1
                The TMCL module ID of the TMC2208. This ID is used as a
                parameter for the writeDRV and readDRV functions.
        """
        TMCLEval.__init__(self, connection, module_id)
        self.motors = [self._MotorTypeA(self, 0)]
        self.ics = [TMC2208()]

    # Use the driver controller functions for register access

    def write_register(self, register_address, value):
        return self._connection.write_drv(register_address, value, self._module_id)

    def read_register(self, register_address, signed=False):
        return self._connection.read_drv(register_address, self._module_id, signed)

    # Motion control functions

    def rotate(self, axis, value):
        self._connection.rotate(axis, value)
    
    def stop(self, axis):
        self._connection.stop(axis)
    
    def move_to(self, axis, position, velocity=None):
        if velocity and velocity != 0:
            self.motors[axis].set_axis_parameter(self.motors[axis].AP.MaxVelocity, velocity)
        self._connection.move_to(axis, position, self._module_id)

    def move_by(self, axis, difference, velocity=None):
        if velocity:
            self.motors[axis].set_axis_parameter(self.motors[axis].AP.MaxVelocity, velocity)
        self._connection.move_by(axis, difference, self._module_id)

    class _MotorTypeA(MotorControlModule):
        def __init__(self, eval_board, axis):
            MotorControlModule.__init__(self, eval_board, axis, self.AP)

        class AP:
            TargetPosition                 = 0
            ActualPosition                 = 1
            TargetVelocity                 = 2
            ActualVelocity                 = 3
            MaxVelocity                    = 4
            MaxAcceleration                = 5
