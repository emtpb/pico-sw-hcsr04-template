"""Python interface for the ultasonic sensor HC-SR04."""
from machine import Pin, time_pulse_us
import time


class HCSR04:
    """Interface for ultrasonic sensor HC-SR04."""

    def __init__(self, trigger_pin, echo_pin, timeout=70000):
        """Initialize sensor pins.

        Args:
            trigger_pin (int): GPIO number trigger is connected to
            echo_pin (int): GPIO number echo is connected to
            timeout (int): Timeout in microseconds
        """
        # Initialize pins
        self.trigger = Pin(trigger_pin, mode=Pin.OUT)
        self.trigger.off()

        # Enable pull down resistor to ensure input is stable when there is a
        # wiring error (pin would float otherwise)
        self.echo = Pin(echo_pin, mode=Pin.IN, pull=Pin.PULL_DOWN)

        # Timeout in microseconds
        self.timeout = timeout

    def get_distance_cm(self):
        """Trigger measurement and return distance in cm.

        Returns:
            * distance in cm if measurement is valid
            * -2 if rising edge was not detected within time
            * -1 if falling edge was not detected within time
        """
        # Start measurement by sending 10 us pulse on trigger pin
        self.trigger.on()
        time.sleep_us(10)
        self.trigger.off()

        # Get time and convert to us to s -> Divide by 1000000
        t_pulse = time_pulse_us(self.echo, 1, self.timeout) / 1000000

        # Check if timeout occured, see
        # https://docs.micropython.org/en/latest/library/machine.html#machine.time_pulse_us
        if t_pulse < 0:
            return t_pulse

        # Calculate distance:
        # Sound velocity in air: 343 m/s at room temperature (20 °C)
        c_air = 343
        # Ultrasonic wave travels distance two times -> Divide by 2
        # Distance in cm -> Multiply by 100
        distance = c_air * t_pulse / 2 * 100

        return distance
