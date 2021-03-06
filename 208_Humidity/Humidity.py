#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file Humidity.py
 @brief ModuleDescription
 @date $Date$


"""
import sys
import time
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist

#import FaBo Humidity module http://www.fabo.io/208.html
import FaBoHumidity_HTS221

# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
humidity_spec = ["implementation_id", "Humidity", 
		 "type_name",         "Humidity", 
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
# @class Humidity
# @brief ModuleDescription
# 
# RTC get temperature and float data by FaBo sensor unit 208 Humidity.
# 
# Humidity sensor get data humidity and temperature(Data type : float).
#	RTC send those data to other RTC.
# 
# 
class Humidity(OpenRTM_aist.DataFlowComponentBase):
	
	##
	# @brief constructor
	# @param manager Maneger Object
	# 
	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)
		#fix to run outport.write()
		#humidity_arg = [None] * ((len(RTC._d_TimedFloat) - 4) / 2)
		#self._d_humidity = RTC.TimedFloat(*humidity_arg)
		
		self._d_humidity = RTC.TimedFloat(RTC.Time(0,0),0)
		"""
		208 Humidity sensor by FaBo
		Humidiy OutPort send humidity data to other RTC
		 - Type: float
		 - Number: 1
		 - Unit: %
		 - Frequency: 1sec
		 - Operation Cycle: 1sec
		"""
		self._HumidityOut = OpenRTM_aist.OutPort("Humidity", self._d_humidity)
		
		#fix 
		#temperature_arg = [None] * ((len(RTC._d_TimedFloat) - 4) / 2)
		#self._d_temperature = RTC.TimedFloat(*temperature_arg)
		
		self._d_temperature = RTC.TimedFloat(RTC.Time(0,0),0)
		"""
		Send temperature data to other RTC
		 - Type: float
		 - Number: 1
		 - Semantics: Temperature
		 - Unit: Celsius
		 - Frequency: 1sec
		 - Operation Cycle: 1sec
		"""
		self._TemperatureOut = OpenRTM_aist.OutPort("Temperature", self._d_temperature)


		


		# initialize of configuration-data.
		# <rtc-template block="init_conf_param">
		
		# </rtc-template>

		self._hts221 = FaBoHumidity_HTS221.HTS221()
		 
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
		self.addOutPort("Humidity",self._HumidityOut)
		self.addOutPort("Temperature",self._TemperatureOut)
		
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
		self._d_humidity.data = self._hts221.readHumi()
		self._d_temperature.data = self._hts221.readTemp()
		
		#check data
		#print "Humidity = ", self._d_humidity.data
		#print "Temperature = ", self._d_temperature.data
		
		self._HumidityOut.write()
		self._TemperatureOut.write()
		
		time.sleep(1)
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
	



def HumidityInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=humidity_spec)
    manager.registerFactory(profile,
                            Humidity,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    HumidityInit(manager)

    # Create a component
    comp = manager.createComponent("Humidity")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
	main()

