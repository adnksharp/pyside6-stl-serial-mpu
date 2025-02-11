#include <Adafruit_MPU6050.h>
#include <Wire.h>
#define l LED_BUILTIN

float alpha = 0.96, dtime;

struct {
	float accel, gyro, filter;
} Roll, Pitch, Yaw;

unsigned long gtime, ctime;

Adafruit_MPU6050 mpu;

void setup(void) {
	Serial.begin(115200);
	pinMode(l, OUTPUT);

	while (!mpu.begin()) 
	{
		digitalWrite(l, !digitalRead(l));
		delay(10);
	}
	gtime = millis();
}

void loop(void) 
{
	sensors_event_t a, g, temp;
	mpu.getEvent(&a, &g, &temp);

	Roll.accel = atan2(a.acceleration.y, a.acceleration.z) * 180 / M_PI;
	Pitch.accel = atan2(-a.acceleration.x, sqrt(a.acceleration.y * a.acceleration.y + a.acceleration.z * a.acceleration.z)) * 180 / M_PI;

	ctime = millis();
	dtime = (ctime - gtime) / 1000.0;
	gtime = ctime;

	Roll.gyro = g.gyro.x * dtime;
	Pitch.gyro = g.gyro.y * dtime;
	Yaw.gyro = g.gyro.z * dtime;

	Roll.filter = alpha * (Roll.filter + Roll.gyro) + (1 - alpha) * Roll.accel;
	Pitch.filter = alpha * (Pitch.filter + Pitch.gyro) + (1 - alpha) * Pitch.accel;
	Yaw.filter += (Yaw.gyro * 180 / M_PI);

	Serial.println(String(Roll.filter) + ',' + String(Pitch.filter) + ',' + String(Yaw.filter));
	delay(50);
}
