#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file Light.py
 @brief ModuleDescription
 @date $Date$


"""
import sys
import time
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist
import spidev

# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
light_spec = ["implementation_id", "Light", 
		 "type_name",         "Light", 
		 "description",       "ModuleDescription", 
		 "version",           "1.0.0", 
		 "vendor",            "VenderName", 
		 "category",          "Category", 
		 "activity_type",     "STATIC", 
		 "max_instance",      "1", 
		 "language",          "Python", 
		 "lang_type",         "SCRIPT",
		 "conf.default.Analog_port", "0",

		 "conf.__widget__.Analog_port", "text",

         "conf.__type__.Analog_port", "short",

		 ""]
# </rtc-template>

##
# @class Light
# @brief ModuleDescription
# 
# 109_Light Brick Compornent use on Raspberry Pi.
# sensor get analog value of illuminance.(range 0 to 1023)
# 
# Out: Illuminance level (0 to 1023)
# 
# 
class Light(OpenRTM_aist.DataFlowComponentBase):
	
	##
	# @brief constructor
	# @param manager Maneger Object
	# 
	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

		#level_arg = [None] * ((len(RTC._d_TimedShort) - 4) / 2)
		#self._d_level = RTC.TimedShort(*level_arg)
		
		self._d_level = RTC.TimedShort(RTC.Time(0,0),0)
		"""
		Data: level has value of illuminance.(range : 0 to 1023)
		"""
		self._IlluminanceOut = OpenRTM_aist.OutPort("Illuminance", self._d_level)


		


		# initialize of configuration-data.
		# <rtc-template block="init_conf_param">
		"""
		
		 - Name:  Analog_port
		 - DefaultValue: 0
		"""
		self._Analog_port = [0]
		
		# </rtc-template>

		self._spi = spidev.SpiDev()
		 
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
		self.bindParameter("Analog_port", self._Analog_port, "0")
		
		# Set InPort buffers
		
		# Set OutPort buffers
		self.addOutPort("Illuminance",self._IlluminanceOut)
		
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
		self._spi.open(0,0)
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
		self.spi.close()
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
		self._d_level.data = self.readadc(self._Analog_port[0])
		print("Illuminance : {:8}".format(self._d_level.data))
		
		self._IlluminanceOut.write()
		time.sleep(0.01)
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
	def readadc(self, channel):
		adc = self._spi.xfer2([1,(8+channel)<<4,0])
		data = ((adc[1]&3) << 8) + adc[2]
		return data



def LightInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=light_spec)
    manager.registerFactory(profile,
                            Light,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    LightInit(manager)

    # Create a component
    comp = manager.createComponent("Light")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
	main()

