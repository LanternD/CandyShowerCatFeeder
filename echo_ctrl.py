"""
    This is the demo code for the Candy Shower Cat Feeder.
    Fauxmo lib will help you to set your device in a UPnP mode, which will turn the device running this code into an
    Amazon Echo enabled deivce. Discover the device in "Smart Home" Tab in Amazon
    Alexa app on the cellphone.

    The Turn On / Off request will be sent to device_handler.
"""

import fauxmo
import logging
import time
import RPi.GPIO as GPIO


from basic_device_handler import basic_device_handler

logging.basicConfig(level=logging.DEBUG)

class device_handler(basic_device_handler):
    """Rewrite the act() function to perform our task
    """

    TRIGGERS = {"Candy Shower": 52001} # add more devices if you like
    
    def act(self, client_address, state, name):
        print "State", state, "on", name, "from client @", client_address

        if state == True:
            GPIO.output(18, GPIO.HIGH)
            self.time_stamp = time.time() # update the time stamp, which is the starting time
            print self.time_stamp
        else: # Turn Off request
            GPIO.output(18, GPIO.LOW)
            
        return True # tell Amazon Echo everything works well.

def run():
    # Startup the fauxmo server

    fauxmo.DEBUG = True
    poller1 = fauxmo.poller() # poller listen to the channel for request
    upnp1 = fauxmo.upnp_broadcast_responder() # the UPnP broadcast model
    upnp1.init_socket() 
    poller1.add(upnp1)

    print 'GPIO Initialization.'
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(18, GPIO.OUT)

    # Register the device callback as a fauxmo handler
    device1 = device_handler()
    for trig, port in device1.TRIGGERS.items():
        fauxmo.fauxmo(trig, upnp1, poller1, None, port, device1)

    # Loop and poll for incoming Echo requests
    logging.debug("Entering fauxmo polling loop")
    while True:
        try:
            # Allow time for a ctrl-c to stop the process
            poller1.poll(100)
            time.sleep(0.1)
            '''
                If the time lapses for 10 seconds, turn off the feeder, that is enough for your cat
            '''
            current_time = time.time()
            if current_time >= (device1.time_stamp + 10):
                # print 'ts', d.time_stamp
                # print 'ct', current_time
                GPIO.output(18, GPIO.LOW)
            if current_time >= (device1.time_stamp + 86400):
                # you haven't told the Alexa to feed your cat for one day! Feed some automatically
                GPIO.output(18, GPIO.HIGH)
                device1.time_stamp = current_time
                
        except Exception, e:
            logging.critical("Critical exception: " + str(e))
            GPIO.cleanup()
            break


if __name__ == "__main__":
    run()
    GPIO.cleanup()
