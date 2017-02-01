#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file Axis9.py
 @brief ModuleDescription
 @date $Date$


"""
import sys
import time
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist
import FaBo9Axis_MPU9250

# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
axis9_spec = ["implementation_id", "Axis9", 
		 "type_name",         "Axis9", 
		 "description",       "ModuleDescription", 
		 "version",           "1.0.0", 
		 "vendor",            "VenderName", 
		 "category",          "Category", 
		 "activity_type",     "STATIC", 
		 "max_instance",      "1", 
		 "language",          "Python", 
		 "lang_type",         "SCRIPT",
		 ""]
# </rtc-template>

##
# @class Axis9
# @brief ModuleDescription
# 
# 202 9Axis sensor, Get 3 Axis, 3 Gyro, 3 Mag
# 
# 
class Axis9(OpenRTM_aist.DataFlowComponentBase):
	
	##
	# @brief constructor
	# @param manager Maneger Object
	# 
	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

		#axis_arg = [None] * ((len(RTC._d_TimedFloatSeq) - 4) / 2)
		#self._d_axis = RTC.TimedFloatSeq(*axis_arg)
		self._d_axis = RTC.TimedFloatSeq(RTC.Time(0,0),0)
                """
		"""
		self._3AxisOut = OpenRTM_aist.OutPort("3Axis", self._d_axis)
		
                #gyro_arg = [None] * ((len(RTC._d_TimedFloatSeq) - 4) / 2)
		#self._d_gyro = RTC.TimedFloatSeq(*gyro_arg)
		self._d_gyro = RTC.TimedFloatSeq(RTC.Time(0,0),0)
                """
		"""
		self._3GyroOut = OpenRTM_aist.OutPort("3Gyro", self._d_gyro)
		
                #mag_arg = [None] * ((len(RTC._d_TimedFloatSeq) - 4) / 2)
		#self._d_mag = RTC.TimedFloatSeq(*mag_arg)
		self._d_mag = RTC.TimedFloatSeq(RTC.Time(0,0),0)
                """
		"""
		self._3MagOut = OpenRTM_aist.OutPort("3Mag", self._d_mag)


		


		# initialize of configuration-data.
		# <rtc-template block="init_conf_param">
		
		# </rtc-template>

                self.mpu = FaBo9Axis_MPU9250.MPU9250()
		 
	##
	#
	# The initialize action (on CREATED->ALIVE transition)
	# formaer rtc_init_entry() 
	# 
	# @return RTC::ReturnCode_t
	# 
	#
	def onInitialize(self):
		# Bind variables and configuration variable
		
		# Set InPort buffers
		
		# Set OutPort buffers
		self.addOutPort("3Axis",self._3AxisOut)
		self.addOutPort("3Gyro",self._3GyroOut)
		self.addOutPort("3Mag",self._3MagOut)
		
		# Set service provider to Ports
		
		# Set service consumers to Ports
		
		# Set CORBA Service Ports
		
		return RTC.RTC_OK
	
	#	##
	#	# 
	#	# The finalize action (on ALIVE->END transition)
	#	# formaer rtc_exiting_entry()
	#	# 
	#	# @return RTC::ReturnCode_t
	#
	#	# 
	#def onFinalize(self):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The startup action when ExecutionContext startup
	#	# former rtc_starting_entry()
	#	# 
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onStartup(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The shutdown action when ExecutionContext stop
	#	# former rtc_stopping_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onShutdown(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The activated action (Active state entry action)
	#	# former rtc_active_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	# 
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onActivated(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The deactivated action (Active state exit action)
	#	# former rtc_active_exit()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onDeactivated(self, ec_id):
	#
	#	return RTC.RTC_OK
	
		##
		#
		# The execution action that is invoked periodically
		# former rtc_active_do()
		#
		# @param ec_id target ExecutionContext Id
		#
		# @return RTC::ReturnCode_t
		#
		#
	def onExecute(self, ec_id):
	    
                axisSeq = []
                gyroSeq = []
                magSeq = []
                
                accel = self.mpu.readAccel()
                gyro =self.mpu.readGyro()
                mag = self.mpu.readMagnet()

                axisSeq.append(accel['x'])
                axisSeq.append(accel['y'])
                axisSeq.append(accel['z'])

                gyroSeq.append(gyro['x'])
                gyroSeq.append(gyro['y'])
                gyroSeq.append(gyro['z'])

                magSeq.append(mag['x'])
                magSeq.append(mag['y'])
                magSeq.append(mag['z'])
                

                self._d_axis.data = axisSeq
                self._d_gyro.data = gyroSeq
                self._d_mag.data = magSeq
                
                self._3AxisOut.write()
                self._3GyroOut.write()
                self._3MagOut.write()


		return RTC.RTC_OK
	
	#	##
	#	#
	#	# The aborting action when main logic error occurred.
	#	# former rtc_aborting_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onAborting(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The error action in ERROR state
	#	# former rtc_error_do()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onError(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The reset action that is invoked resetting
	#	# This is same but different the former rtc_init_entry()
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onReset(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The state update action that is invoked after onExecute() action
	#	# no corresponding operation exists in OpenRTm-aist-0.2.0
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#

	#	#
	#def onStateUpdate(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	#	##
	#	#
	#	# The action that is invoked when execution context's rate is changed
	#	# no corresponding operation exists in OpenRTm-aist-0.2.0
	#	#
	#	# @param ec_id target ExecutionContext Id
	#	#
	#	# @return RTC::ReturnCode_t
	#	#
	#	#
	#def onRateChanged(self, ec_id):
	#
	#	return RTC.RTC_OK
	



def Axis9Init(manager):
    profile = OpenRTM_aist.Properties(defaults_str=axis9_spec)
    manager.registerFactory(profile,
                            Axis9,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    Axis9Init(manager)

    # Create a component
    comp = manager.createComponent("Axis9")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
	main()

