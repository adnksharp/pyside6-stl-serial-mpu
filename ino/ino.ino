#include <Adafruit_MPU6050.h>
#include <Wire.h>
#define l LED_BUILTIN
Adafruit_MPU6050 mpu;

void setup(void) {
	Serial.begin(115200);
	pinMode(l, OUTPUT);

	while (!mpu.begin()) 
	{
		digitalWrite(l, !digitalRead(l));
		delay(10);
	}
}

void loop(void) 
{
	sensors_event_t a, g, temp;
	mpu.getEvent(&a, &g, &temp);

	float roll = atan2(a.acceleration.y, a.acceleration.z) * 180 / M_PI;
	float pitch = atan2(-a.acceleration.x, sqrt(a.acceleration.y * a.acceleration.y + a.acceleration.z * a.acceleration.z)) * 180 / M_PI;

	Serial.println(String(roll) + ',' + String(pitch));
	delay(100);
}
