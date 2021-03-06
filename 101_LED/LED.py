#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file LED.py
 @brief ModuleDescription
 @date $Date$


"""
import sys
import time
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist

#Import to use GPIO
import RPi.GPIO as GPIO


# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
led_spec = ["implementation_id", "LED", 
		 "type_name",         "LED", 
		 "description",       "ModuleDescription", 
		 "version",           "1.0.0", 
		 "vendor",            "VenderName", 
		 "category",          "Category", 
		 "activity_type",     "STATIC", 
		 "max_instance",      "1", 
		 "language",          "Python", 
		 "lang_type",         "SCRIPT",
		 "conf.default.LEDPIN", "4",

		 "conf.__widget__.LEDPIN", "text",

         "conf.__type__.LEDPIN", "short",

		 ""]
# </rtc-template>


#add mycodes

GPIO.setwarnings(False)
GPIO.setmode( GPIO.BCM)
GPIO.setup( 4, GPIO.OUT)

LIGHT = GPIO.PWM(4, 100)


def arduino_map(x,in_min, in_max, out_min, out_max):
	return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min


##
# @class LED
# @brief ModuleDescription
# 
# FaBoLEDユニットを点灯させるRTC。真理値を用いて点灯、消灯のみで制御する方法もある
#	が、ここでは照度制御なども考え、データをFloatで取得し汎用的に点灯させられるRTCを
#	考慮する
# 
# InPortよりLED照度情報(数値)を取得し、それに応じた照度でLEDを点灯させる。
# 
# 
class LED(OpenRTM_aist.DataFlowComponentBase):
	
	##
	# @brief constructor
	# @param manager Maneger Object
	# 
	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

		signal_arg = [None] * ((len(RTC._d_TimedShort) - 4) / 2)
		self._d_signal = RTC.TimedShort(*signal_arg)
		"""
		LED点灯を制御する信号をInPortより取得し、LEDを制御する
		 - Type: Short
		"""
		self._SignalPortIn = OpenRTM_aist.InPort("SignalPort", self._d_signal)


		


		# initialize of configuration-data.
		# <rtc-template block="init_conf_param">
		"""
		LEDユニットを接続したGPIOピンの番号を指定する。
		 - Name: LEDPIN LEDPIN
		 - DefaultValue: 4
		"""
		self._LEDPIN = [4]
		

		 
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
		self.bindParameter("LEDPIN", self._LEDPIN, "4")
		
		# Set InPort buffers
		self.addInPort("SignalPort",self._SignalPortIn)
		
		# Set OutPort buffers
		
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
	def onFinalize(self):
		GPIO.cleanup()
		print"Finish GPIO cleanup"
		return RTC.RTC_OK
	
		##
		#
		# The startup action when ExecutionContext startup
		# former rtc_starting_entry()
		# 
		# @param ec_id target ExecutionContext Id
		#
		# @return RTC::ReturnCode_t
		#
		#
	def onStartup(self, ec_id):
	
		return RTC.RTC_OK
	
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
	def onActivated(self, ec_id):
		
		LIGHT.start(0)
		print"LED Start"	
		return RTC.RTC_OK
	
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
	def onDeactivated(self, ec_id):
		LIGHT.stop()
		print"LED STOP"	
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
		if(self._SignalPortIn.isNew()):
			self._d_signal = self._SignalPortIn.read()
			value = arduino_map(self._d_signal.data, 0, 1023,0, 100)		
			LIGHT.ChangeDutyCycle(value)
			
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
	



def LEDInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=led_spec)
    manager.registerFactory(profile,
                            LED,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    LEDInit(manager)

    # Create a component
    comp = manager.createComponent("LED")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
	main()

