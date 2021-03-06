#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file Axis3.py
 @brief ModuleDescription
 @date $Date$


"""
import sys
import time
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist
import FaBo3Axis_ADXL345

# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
axis3_spec = ["implementation_id", "Axis3", 
		 "type_name",         "Axis3", 
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
# @class Axis3
# @brief ModuleDescription
# 
# FaBo 201 3Axis sensor RTC. Get 3 Axis (x, y, and z ) and Tap
#	information(Single or Double Tap)
# 
# Out: 3 Axis Data and Tap information
# 
# 
class Axis3(OpenRTM_aist.DataFlowComponentBase):
	
	##
	# @brief constructor
	# @param manager Maneger Object
	# 
	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

		#axis_arg = [None] * ((len(RTC._d_TimedShortSeq) - 4) / 2)
		#self._d_axis = RTC.TimedShortSeq(*axis_arg)
		self._d_axis = RTC.TimedShortSeq(RTC.Time(0,0),0)
                """
		value of Axis : x, y and z.
		 - Type: short
		 - Number: 3
		"""
		self._AxisOut = OpenRTM_aist.OutPort("Axis", self._d_axis)
		
                #tap_arg = [None] * ((len(RTC._d_TimedShort) - 4) / 2)
		#self._d_tap = RTC.TimedShort(*tap_arg)
		self._d_tap = RTC.TimedShort(RTC.Time(0,0),0)
                """
		value of tap: if value 1 > get Single Tap. if value 2 > Double Tap. value 0
		is not Tap (Default)
		 - Type: short
		 - Number: 1
		"""
		self._TapOut = OpenRTM_aist.OutPort("Tap", self._d_tap)


		


		# initialize of configuration-data.
		# <rtc-template block="init_conf_param">
		
		# </rtc-template>
                self.adxl345 = FaBo3Axis_ADXL345.ADXL345()
		 
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
		self.addOutPort("Axis",self._AxisOut)
		self.addOutPort("Tap",self._TapOut)
		
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
	
		##
		#
		# The activated action (Active state entry action)
		# former rtc_active_entry()
		#
		# @param ec_id target ExecutionContext Id
		# 
		# @return RTC::ReturnCode_t
		#
		#
	def onActivated(self, ec_id):
	        self.adxl345.enableTap()
                self._d_tap.data = 0
		return RTC.RTC_OK
	
		##
		#
		# The deactivated action (Active state exit action)
		# former rtc_active_exit()
		#
		# @param ec_id target ExecutionContext Id
		#
		# @return RTC::ReturnCode_t
		#
		#
	def onDeactivated(self, ec_id):
	
		return RTC.RTC_OK
	
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
                
	        tap = self.adxl345.readIntStatus()
                axes = self.adxl345.read()
                shortSeq = []


                if self.adxl345.isDoubleTap(tap):
                    print "get DoubleTap"
                    self._d_tap.data = 2
                elif self.adxl345.isSingleTap(tap):
                    print "get SingleTap"
                    self._d_tap.data = 1
                else:
                    print "no Tap"
                    self._d_tap.data = 0
                
                shortSeq.append(axes['x'])
                shortSeq.append(axes['y'])
                shortSeq.append(axes['z'])

                print ("x :{}, y :{}, z :{}").format(axes['x'], axes['y'], axes['z'])
                
                self._d_axis.data = shortSeq
                self._AxisOut.write()
                self._TapOut.write()
                
                time.sleep(0.5)
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
	



def Axis3Init(manager):
    profile = OpenRTM_aist.Properties(defaults_str=axis3_spec)
    manager.registerFactory(profile,
                            Axis3,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    Axis3Init(manager)

    # Create a component
    comp = manager.createComponent("Axis3")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
	main()

