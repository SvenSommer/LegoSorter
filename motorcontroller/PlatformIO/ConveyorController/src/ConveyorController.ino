#include "AiEsp32RotaryEncoder.h"
#include "Arduino.h"
#include <ArduinoOTA.h>
#include <TFT_eSPI.h> // Graphics and font library for ST7735 driver chip
#include <SPI.h>
#include <WiFi.h>
#include <ESPAsyncWebServer.h>
#include <AccelStepper.h>
#include <ezTime.h>
#include <ArduinoJson.h>
#include "ota.h"
#include "boardinfo.h"
#include <credentials.h>

#define ROTARY_ENCODER_A_PIN 21
#define ROTARY_ENCODER_B_PIN 32
#define ROTARY_ENCODER_BUTTON_PIN 25
AiEsp32RotaryEncoder RotaryEncoder = AiEsp32RotaryEncoder(ROTARY_ENCODER_A_PIN, ROTARY_ENCODER_B_PIN, ROTARY_ENCODER_BUTTON_PIN, -1);

TFT_eSPI tft = TFT_eSPI();  // Invoke library, pins defined in User_Setup.h

//DEBUG
const bool Debug = true;

// Set your access point network credentials
const char* ssid = mySSID;
const char* password = myPASSWORD;
int ConnectionTries = 0;
unsigned long PreviousMillis = 0;
const long Interval = 2000; 
bool Online = 0;

const char* NameforClient = CONTROLLERNAME;
const String NameforDisplay = "Conveyor";
const String Version = VERSION;

AsyncWebServer Server(80);

// Motor
int MotorPulsePin = 27; 
int MotorDirPin = 26; 
int EnableMotorPin = 12; 
int MinimalSpeed = 0;
int MaxSpeed = 2000;
AccelStepper Stepper(1,MotorPulsePin,MotorDirPin);


String MotorMode = "OFF";
int MotorSpeed = 20;
String ClientMode = "SEARCH..";
int LastSpeed = 0;
String LastMode = "OFF";

//TFT
char PrintoutNew[9];
char PrintoutOld[9];

//Timed Event Handling 
Timezone myLocalTime;

void setup() {
  SetupOTA(NameforClient, mySSID, myPASSWORD);

  myLocalTime.setLocation(F("de")); // set your time zone
  //we must initialize rotary encoder
  RotaryEncoder.begin();
  RotaryEncoder.setup([]{RotaryEncoder.readEncoder_ISR();});
  //optionally we can set boundaries and if values should cycle or not
  RotaryEncoder.setBoundaries(0, 101, false); //minValue, maxValue, cycle values (when max go to min and vice versa)
  RotaryEncoder.reset(MotorSpeed);
  
  tft.init();
  tft.setRotation(2);
  InitializeTftScreen();
  
  Serial.begin(115200);
  SerialPrint(String(NameforClient) + " " + Version + " ready"); 

  Stepper.setMaxSpeed(MaxSpeed);
  Stepper.setAcceleration(2000);
  Stepper.disableOutputs();

  Server.on("/", HTTP_GET, [](AsyncWebServerRequest *request){
    request->redirect("http://legosorter:3000/");
  });

  Server.on("/getstatus", HTTP_GET, [](AsyncWebServerRequest *request){
    //SerialPrint("status Request received");
    request->send(200, "text/plain", GetStatus());
  });

  Server.on("/alterspeed", HTTP_PUT, [](AsyncWebServerRequest *request){
    SerialPrint("alterspeed Request received");
    if(request->hasParam("speedchange")){
      int speedchange = request->arg("speedchange").toInt();
      if(MotorSpeed + speedchange != MotorSpeed){
        SetNewSpeed(MotorSpeed + speedchange);
        }   
      }
    request->send(200, "text/plain", GetStatus());
  });

  Server.on("/togglemotormode", HTTP_PUT, [](AsyncWebServerRequest *request){
    SerialPrint("togglemotormode Request received");
    if(request->hasParam("toogle")){
      int toogle = request->arg("toogle").toInt();
      if(toogle == 1){
        ToggleMotorMode();
        }   
      }
    request->send(200, "text/plain", GetStatus());
  });


  Server.on("/update", HTTP_PUT, [](AsyncWebServerRequest *request){
    SerialPrint("Update Request received");
    if(request->hasParam("speed")){
      int speed = request->arg("speed").toInt();
      if(speed != MotorSpeed){
        SetNewSpeed(speed);
      }
    }
    if(request->hasParam("motormode")){
      String motormode = request->arg("motormode");
      if(motormode != MotorMode){
        SetNewMotorMode(motormode);
      }
    }
    if(request->hasParam("clientmode")){
      String clientmode = request->arg("clientmode");
      if(clientmode != ClientMode) {
        SetNewClientMode(clientmode);
      }
    }
    request->send(200, "text/plain", GetStatus());
  });

  
  // Start server
  Server.begin();
  setInterval(60); // every minute ntp update
  waitForSync();
  Init();
}

void Init(){
  SetNewSpeed(20);
  SetNewMotorMode("OFF");
}


void loop() {
  ArduinoOTA.handle();
  CheckForEncoderChanges();
  RunMotor();
  checkWifiConnection(); 
}

void ConnectWifi() {
   //Wifi
  WiFi.config(INADDR_NONE, INADDR_NONE, INADDR_NONE);
  WiFi.begin(ssid, password);
  WiFi.setHostname(NameforClient);
 SerialPrint("Connecting...");
}

void checkWifiConnection() {
  unsigned long currentMillis = millis();
  if(currentMillis - PreviousMillis >= Interval) {
    if(WiFi.status()== WL_CONNECTED ) {
      if(Online == 0) {// was disconnected, now connected
       SerialPrint("Wifi connection established");
        //SerialPrint("IP " + WiFi.localIP());
        waitForSync();
        SerialPrint("Done. Current time is " + myLocalTime.dateTime("d.m.Y H:i:s.v T"));
        Online = 1;
        SetNewClientMode(ClientMode); //update Display to show correct color 
      }
    } else{
      if(Online == 1){ //was online, now disconnected
       SerialPrint("Wifi connection lost");
        Online = 0;
        SetNewClientMode(ClientMode); //update Display to show correct color 
      }
     SerialPrint("Trying to Reconnect to Wifi.");
      ConnectWifi();
    }
     PreviousMillis = currentMillis;
  }
}

String GetStatus(){
  StaticJsonDocument<192> StatusResponsedoc;
  StatusResponsedoc["client"] = NameforClient;
  StatusResponsedoc["ip"] = WiFi.localIP().toString();
  StatusResponsedoc["version"] = Version;
  StatusResponsedoc["clientmode"] = ClientMode;
  StatusResponsedoc["motormode"] = MotorMode;
  StatusResponsedoc["speed"] = MotorSpeed;
  StatusResponsedoc["datetime"] = myLocalTime.dateTime("d.m.Y H:i:s.v T");
  String message = "";
  serializeJsonPretty(StatusResponsedoc, message);
  return message; 
}

void CheckForEncoderChanges(){
 if (RotaryEncoder.currentButtonState() == BUT_RELEASED) {
    //we can process it here or call separate function like:
    Rotary_onButtonClick();
  }
  
  int16_t encoderDelta = RotaryEncoder.encoderChanged();
  if (encoderDelta != 0 ) {
    SetNewSpeed(RotaryEncoder.readEncoder());
    SetNewClientMode("MANUAL");  
  }
}
  
void Rotary_onButtonClick() {
  ToggleMotorMode();
  SetNewClientMode("MANUAL");
}

void ToggleMotorMode(){
    if(MotorMode == "ON") {
      SetNewMotorMode("OFF");
     SerialPrint("Motor stopped");
    }
    else
    {
      SetNewMotorMode("ON");
     SerialPrint("Motor started");
   }
 }
 
void RunMotor() {
  if(MotorMode == "ON"){
    if(LastMode == "OFF"){
      Stepper.enableOutputs();
      Stepper.run();
      LastSpeed = LastSpeed -1;
      LastMode = "ON";
    }
    if(MotorSpeed != LastSpeed){
      LastSpeed = MotorSpeed;
      
      int mappedSpeed = map(MotorSpeed, 0, 100, MinimalSpeed, MaxSpeed);
      Stepper.setSpeed(mappedSpeed);  
      SerialPrint("new motor speed set to: " + String(MotorSpeed) + " ("+ String(mappedSpeed) + ")");
    }
    Stepper.runSpeed();
  } else if(LastMode == "ON"){
    Stepper.stop();
    Stepper.disableOutputs();
    LastMode = "OFF";
  }     
}
  
void SetNewSpeed(int newSpeed){
  if(newSpeed > 0 && newSpeed < 101) {
    int oldSpeed = MotorSpeed;
    MotorSpeed = newSpeed;
    UpdateTftSpeed(oldSpeed, MotorSpeed);
  }
}

void SetNewMotorMode(String newMode){
  String oldMode = MotorMode;
  MotorMode = newMode;
  SerialPrint("Updating Motor from " + oldMode + " to " + MotorMode);
  UpdateTftMode(oldMode, MotorMode);
}

void SetNewClientMode(String newClientMode){
    String oldStatus = ClientMode;
    ClientMode = newClientMode;
    SerialPrint("Updating Clientmode from " + oldStatus + " to " + newClientMode);
    UpdateTftClientMode(oldStatus, ClientMode);
}

void InitializeTftScreen(){
    tft.fillScreen(TFT_BLACK);
    tft.setCursor(0, 0, 2);
    tft.setTextColor(TFT_LIGHTGREY,TFT_BLACK);  
    tft.setTextSize(1);
    tft.println(NameforDisplay);
    tft.setTextSize(2); 
    if(Online == 0){
      tft.setTextColor(TFT_RED,TFT_BLACK); // blue is red 
    } else {
      tft.setTextColor(TFT_LIGHTGREY,TFT_BLACK);
    }
    tft.println(ClientMode);
    tft.setTextSize(1);
    tft.setTextColor(TFT_LIGHTGREY,TFT_BLACK); 
    tft.println("Motor Mode");
    tft.setTextSize(2); 
    tft.println(MotorMode);
    tft.setTextSize(1);
    tft.println("Motor Speed");
    tft.setTextSize(2);
    tft.println(MotorSpeed);
  }

void UpdateTftSpeed(int oldSpeed, int newSpeed){
      String newSpeedString = String(newSpeed);
      newSpeedString.toCharArray(PrintoutNew, 4);
      String oldSpeedString = String(oldSpeed);
      oldSpeedString.toCharArray(PrintoutOld, 4);
      tft.setTextSize(2); 
      //erase old Printout
      tft.setCursor(0, 112, 2);
      tft.setTextColor(TFT_BLACK,TFT_BLACK);
      tft.println(PrintoutOld);
      //print new Printout
      tft.setCursor(0, 112, 2);
      tft.setTextColor(TFT_LIGHTGREY,TFT_BLACK);
      tft.println(PrintoutNew);
}

void UpdateTftMode(String oldMode, String newMode){
      newMode.toCharArray(PrintoutNew, 4);
      oldMode.toCharArray(PrintoutOld, 4);
     
      tft.setTextSize(2); 
      //erase old Printout
      tft.setCursor(0, 64, 2);
      tft.setTextColor(TFT_BLACK,TFT_BLACK);
      tft.println(PrintoutOld);
      //print new Printout
      tft.setCursor(0, 64, 2);
      tft.setTextColor(TFT_LIGHTGREY,TFT_BLACK);
      tft.println(PrintoutNew);
}

void UpdateTftClientMode(String oldStatus, String newStatus){
      newStatus.toCharArray(PrintoutNew, 9);
      oldStatus.toCharArray(PrintoutOld, 9);
     
      tft.setTextSize(2); 
      //erase old Printout
      tft.setCursor(0, 16, 2);
      tft.setTextColor(TFT_BLACK,TFT_BLACK);
      tft.println(PrintoutOld);
      //print new Printout
      tft.setCursor(0, 16, 2);
      if(Online == 0){
        tft.setTextColor(TFT_RED,TFT_BLACK); 
      } else {
        tft.setTextColor(TFT_LIGHTGREY,TFT_BLACK);
      }
      tft.println(PrintoutNew);
}

void SerialPrint(String message){
  if(Debug){
    Serial.println(message);
  } 
}
