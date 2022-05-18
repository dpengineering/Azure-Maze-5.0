/*
   THIS IS FOR TESTING BOTH BALL PUMPS
*/

#include "SpeedyStepper.h"

SpeedyStepper BallPump1;
SpeedyStepper BallPump2;

const long BALL_PUMP_1_STEPS_PER_REV = 200 * 76.766;
const long BALL_PUMP_1_MICROSTEPPING = 8;
const long BALL_PUMP_1_STEPS_PER_REV_INCLUDING_MICROSTEPPING = (BALL_PUMP_1_STEPS_PER_REV * BALL_PUMP_1_MICROSTEPPING);
const long BALL_PUMP_1_SPEED_IN_SPS = 7500; // 5000; // 750;
const long BALL_PUMP_1_ACCELERATION_IN_RPSS = 5000;
const byte BALL_PUMP_1_HOME_SENSOR = 26;          // barrel sensor
const byte BALL_PUMP_1_SENSOR = 28;               // Optical Ball sensor
const long BALL_PUMP_1_DIRECTION_TOWARD_HOME = -1; // -1 is CCW
const long BALL_PUMP_1_DIRECTION = -1;             // -1 is CCW
const long BALL_PUMP_1_MAX_STEPS = 1500000;
const long BALL_PUMP_1_GATE = 23;

const long BALL_PUMP_2_STEPS_PER_REV = 200 * 76.766;
const long BALL_PUMP_2_MICROSTEPPING = 8;
const long BALL_PUMP_2_STEPS_PER_REV_INCLUDING_MICROSTEPPING = (BALL_PUMP_1_STEPS_PER_REV * BALL_PUMP_1_MICROSTEPPING);
const long BALL_PUMP_2_SPEED_IN_SPS = 7500; // 5000; // 750;
const long BALL_PUMP_2_ACCELERATION_IN_RPSS = 5000;
const byte BALL_PUMP_2_HOME_SENSOR = 27;           // barrel sensor
const byte BALL_PUMP_2_SENSOR = 29;                // Optical ball sensor
const long BALL_PUMP_2_DIRECTION_TOWARD_HOME = 1; // -1 is CCW
const long BALL_PUMP_2_DIRECTION = 1;             // -1 is CCW
const long BALL_PUMP_2_MAX_STEPS = 1500000;
const long BALL_PUMP_2_GATE = 24;

bool pump1ready;
bool pump2ready;

// BALL PUMPS SETUP HERE//
void PumpOneSetup()
{
  
  int ballPump1HomeSensorState = 0;
   Serial.println("Start Homing Ball Pump 1");
  BallPump1.enableStepper();
  // Don't Assume the Ball Pump Is correctly homed, offset and ready to accept a ball - so rotate some first then home
  BallPump1.moveRelativeInSteps(10000 * BALL_PUMP_1_DIRECTION_TOWARD_HOME);

  BallPump1.moveToHomeInSteps(BALL_PUMP_1_DIRECTION_TOWARD_HOME, BALL_PUMP_1_SPEED_IN_SPS,
                              BALL_PUMP_1_MAX_STEPS, BALL_PUMP_1_HOME_SENSOR);
  BallPump1.disableStepper();
   ballPump1HomeSensorState = digitalRead(BALL_PUMP_1_HOME_SENSOR);
  Serial.print("BALL_PUMP#1_HOME_SENSOR_STATE = ");
  Serial.println(ballPump1HomeSensorState);
  Serial.println("Ball Pump 1 Homed");
  Serial.println("Moving to allow ball to enter gate");
  // Homing sensor is located such that ball will not enter gate - at home so we have to rotate it - to allow ball to enter gate.
  BallPump1.enableStepper();
  BallPump1.moveRelativeInSteps(3500 * BALL_PUMP_1_DIRECTION_TOWARD_HOME);
  BallPump1.disableStepper();
  Serial.println("Ball Pump 1 Ready for Ball");
}

void PumpTwoSetup()
{
  int ballPump2HomeSensorState = 0;
  Serial.println("Start Homing Ball Pump 2");
  BallPump2.enableStepper();
  // Don't Assume the Ball Pump Is correctly homed, offset and ready to accept a ball - so rotate some first then home
  BallPump2.moveRelativeInSteps(10000 * BALL_PUMP_2_DIRECTION_TOWARD_HOME);
  BallPump2.moveToHomeInSteps(BALL_PUMP_2_DIRECTION_TOWARD_HOME, BALL_PUMP_2_SPEED_IN_SPS,
                              BALL_PUMP_2_MAX_STEPS, BALL_PUMP_2_HOME_SENSOR);
  BallPump2.disableStepper();
  ballPump2HomeSensorState = digitalRead(BALL_PUMP_2_HOME_SENSOR);
  Serial.print("BALL_PUMP#2_HOME_SENSOR_STATE = ");
  Serial.println(ballPump2HomeSensorState);
  Serial.println("Ball Pump 2 Homed");
  Serial.println("Moving to allow ball to enter gate");
  // Homing sensor is located such that ball will not enter gate - at home so we have to rotate it - to allow ball to enter gate.
  BallPump2.enableStepper();
  BallPump2.moveRelativeInSteps(3000 * BALL_PUMP_2_DIRECTION_TOWARD_HOME); //original 3500
  BallPump2.disableStepper();
  Serial.println("Ball Pump 2 Ready for Ball");
}


//Setup Begins//
void setup()
{

  Serial.begin(9600);
  Serial.println("Setup begins");

//  pinMode(BALL_PUMP_SELECTOR_POT, INPUT_PULLUP);

  BallPump1.connectToPort(1);
  BallPump1.setStepsPerRevolution(BALL_PUMP_1_STEPS_PER_REV * BALL_PUMP_1_MICROSTEPPING);
  BallPump1.setSpeedInStepsPerSecond(BALL_PUMP_1_SPEED_IN_SPS);
  BallPump1.setAccelerationInStepsPerSecondPerSecond(BALL_PUMP_1_ACCELERATION_IN_RPSS);
  BallPump1.disableStepper();

  pinMode(BALL_PUMP_1_SENSOR, INPUT_PULLUP);
  pinMode(BALL_PUMP_1_HOME_SENSOR, INPUT_PULLUP);
  pinMode(BALL_PUMP_1_GATE, INPUT);
  
  BallPump2.connectToPort(2);
  BallPump2.setStepsPerRevolution(BALL_PUMP_2_STEPS_PER_REV * BALL_PUMP_2_MICROSTEPPING);
  BallPump2.setSpeedInStepsPerSecond(BALL_PUMP_2_SPEED_IN_SPS);
  BallPump2.setAccelerationInStepsPerSecondPerSecond(BALL_PUMP_2_ACCELERATION_IN_RPSS);
  BallPump2.disableStepper();

  pinMode(BALL_PUMP_2_SENSOR, INPUT_PULLUP);
  pinMode(BALL_PUMP_2_HOME_SENSOR, INPUT_PULLUP);
  pinMode(BALL_PUMP_2_GATE, INPUT);

  int ballPumpSelector = 0;

  pump1ready = false;
  pump2ready = false;

  delay(1000);
}

//Loop Begins//
void loop()
{
    Serial.print("Port 23 status ");
    Serial.println(digitalRead(BALL_PUMP_1_GATE));
    Serial.print("Port 24 status ");
    Serial.println(digitalRead(BALL_PUMP_2_GATE));
    Serial.println(digitalRead(" "));
    Serial.print("Pump 1 Homed? ");
    Serial.println(pump1ready);
    Serial.print("Pump 2 Homed? ");
    Serial.println(pump2ready);


    if(digitalRead(23) == HIGH && !pump1ready)
    {
      PumpOneSetup();
      pump1ready = true;
    }
    

    if(digitalRead(24)==HIGH && !pump2ready)
    {
      PumpTwoSetup();
      pump2ready = true;
    }

    

    if(pump2ready && pump1ready)
    {
      
      int ballPumpHomeSensorState = 1;
      if (digitalRead(BALL_PUMP_1_SENSOR) == HIGH && digitalRead(23) == HIGH)
      {
    
        Serial.println("Pump 1");
        // Move Ball Pump 1
       
        if ((digitalRead(BALL_PUMP_1_SENSOR) == HIGH)) // LOW for an active LOW sensor
        {                                              // Ball Detected - Pump ball
          Serial.println("Move Ball pump #1, one Rotation");
          BallPump1.enableStepper();
          BallPump1.moveRelativeInSteps(BALL_PUMP_1_STEPS_PER_REV * 8 * BALL_PUMP_1_DIRECTION);
  
          BallPump1.disableStepper();
          Serial.println("Moved Ball pump #1, one Rotation");
        }
        else
        {
        
          Serial.println("No ball detected in ball pump #1");
          ballPumpHomeSensorState = digitalRead(BALL_PUMP_1_HOME_SENSOR);
          Serial.print("BALL_PUMP#1_HOME_SENSOR_STATE = ");
          Serial.println(ballPumpHomeSensorState);
        }
      }
    
      if (digitalRead(BALL_PUMP_2_SENSOR) == HIGH && digitalRead(24)==HIGH) 
      {
        // Move Ball Pump 2
  
        Serial.println("Pump 2");
    
        if ((digitalRead(BALL_PUMP_2_SENSOR)) == HIGH) // HIGH for an active HIGH sensor
        {
          Serial.println("Move Ball pump #2, one Rotation");
          BallPump2.enableStepper();
          BallPump2.moveRelativeInSteps(BALL_PUMP_2_STEPS_PER_REV * 8 * BALL_PUMP_2_DIRECTION); //
          BallPump2.disableStepper();
          Serial.println("Moved Ball pump #2, one Rotation");
        }
        else
        {
          Serial.println("No ball detected in ball pump #2");
          ballPumpHomeSensorState = digitalRead(BALL_PUMP_2_HOME_SENSOR);
          Serial.print("BALL_PUMP#2_HOME_SENSOR_STATE = ");
          Serial.println(ballPumpHomeSensorState);
        }
      }
    }

    else
    {
      Serial.println("Nothing happens");
    }
  delay(500);
}
