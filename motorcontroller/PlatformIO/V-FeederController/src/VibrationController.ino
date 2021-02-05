#include "AiEsp32RotaryEncoder.h"
#include "Arduino.h"
#include <ArduinoOTA.h>
#include <TFT_eSPI.h> // Graphics and font library for ST7735 driver chip
#include <SPI.h>
#include <WiFi.h>
#include <ESPAsyncWebServer.h>
#include <ezTime.h>
#include <ArduinoJson.h>
#include "ota.h"
#include "boardinfo.h"
#include <credentials.h>

#define ROTARY_ENCODER_A_PIN 21
#define ROTARY_ENCODER_B_PIN 32
#define ROTARY_ENCODER_BUTTON_PIN 25
AiEsp32RotaryEncoder RotaryEncoder = AiEsp32RotaryEncoder(ROTARY_ENCODER_A_PIN, ROTARY_ENCODER_B_PIN, ROTARY_ENCODER_BUTTON_PIN, -1);

TFT_eSPI Tft = TFT_eSPI();  // Invoke library, pins defined in User_Setup.h

//DEBUG
const bool Debug = true;

// Set your access point network credentials
const char* Ssid = mySSID;
const char* Password = myPASSWORD;
int ConnectionTries = 0;
unsigned long PreviousMillis = 0;
const long Interval = 2000; 
bool Online = 0;

const char* NameforClient = CONTROLLERNAME;
const String NameforDisplay = "V-Feeder";
const String Version = VERSION;

// Create AsyncWebServer object on port 80
AsyncWebServer Server(80);

// Motor A
int Motor1Pin1 = 27; 
int Motor1Pin2 = 26; 
int Enable1Pin = 12; 
int MinimalPWDNumber = 140;
int MaximalPWDNumber = 210;

int MotorSpeed = 0;
String MotorMode = "";
String ClientMode = "SEARCH..";
int LastSpeed = 0;
String LastMode = "OFF";

// Setting PWM properties
const int Freq = 30000;
const int PwmChannel = 0;
const int Resolution = 8;
int DutyCycle = 100;

//TFT
char PrintoutNew[9];
char PrintoutOld[9];

//Double Click
unsigned long PreviousMillisDoubleClick = 0;
const long IntervalDoubleClick = 500; 

//Burst Mode
int BurstPhase = 1;
int BurstRestartCounter = 0;
int BurstSpeed = 30;
unsigned long PreviousMillisBurst = 0;
const long IntervalBurst = 50; 

//Timed Event Handling 
Timezone myLocalTime;

void setup() {
  SetupOTA(NameforClient, mySSID, myPASSWORD);

  myLocalTime.setLocation(F("de")); // set your time zone
  //we must initialize rotary encoder
  RotaryEncoder.begin();
  RotaryEncoder.setup([]{RotaryEncoder.readEncoder_ISR();});
  //optionally we can set boundaries and if values should cycle or not
  RotaryEncoder.setBoundaries(1, 100, false); //minValue, maxValue, cycle values (when max go to min and vice versa)
  RotaryEncoder.reset(MotorSpeed);
  // sets the pins as outputs:
  pinMode(Motor1Pin1, OUTPUT);
  pinMode(Motor1Pin2, OUTPUT);
  pinMode(Enable1Pin, OUTPUT);
  
  // configure LED PWM functionalitites
  ledcSetup(PwmChannel, Freq, Resolution);
  // attach the channel to the GPIO to be controlled
  ledcAttachPin(Enable1Pin, PwmChannel);

  Tft.init();
  Tft.setRotation(2);
  InitializeTftScreen();
  Serial.begin(115200);
  SerialPrint(String(NameforClient) + " v0.9 ready"); 

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
  Init();
  setInterval(60); // every minute ntp update
  waitForSync();

}

void loop() {
  ArduinoOTA.handle();
  CheckForEncoderChanges();
  RunMotor();
  CheckWifiConnection(); 

}

void Init(){
  SetNewSpeed(50);
  SetNewMotorMode("OFF");
}

void ConnectWifi() {
   //Wifi
  WiFi.config(INADDR_NONE, INADDR_NONE, INADDR_NONE);
  WiFi.begin(Ssid, Password);
  WiFi.setHostname(NameforClient);
  SerialPrint("Connecting...");
}

void CheckWifiConnection() {
  unsigned long currentMillis = millis();
  if(currentMillis - PreviousMillis >= Interval) {
    if(WiFi.status()== WL_CONNECTED ) {
      if(Online == 0) {// was disconnected, now connected
        SerialPrint("Wifi connection established");
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
     ArduinoOTA.handle();
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
    if(ClientMode != "BURST"){
      SetNewClientMode("MANUAL");  
    }
  }
}
  
void Rotary_onButtonClick() {
  if(CheckForDoubleClick()){
    ToogleBurstMode();
    return;
  } 
  ToggleMotorMode();
  if(ClientMode != "BURST") {
    SetNewClientMode("MANUAL");
  }
}

void ToogleBurstMode(){
  if(ClientMode != "BURST")
    SetNewClientMode("BURST");
  else
    SetNewClientMode("MANUAL");
}

bool CheckForDoubleClick(){
  unsigned long currentMillis = millis();
  SerialPrint("Interval DB:  " + String(currentMillis - PreviousMillisDoubleClick));
  if(currentMillis - PreviousMillisDoubleClick <= IntervalDoubleClick) {
    PreviousMillisDoubleClick = 0;
    return true;
  }
  PreviousMillisDoubleClick = millis();
  return false;
}

void ToggleMotorMode(){
    SerialPrint("Motor currently: " + MotorMode);
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
  ArduinoOTA.handle();
  if(ClientMode == "BURST") {
    CheckForBurstStep();
  }
  if(MotorMode == "ON") {
    if(LastMode == "OFF" && ClientMode != "BURST"){
      if(MotorSpeed < 50 )
        SetNewSpeed(50);

      SendStartCommand();
      LastSpeed = LastSpeed -1;
      LastMode = "ON";
    }
    if(MotorSpeed != LastSpeed){
      LastSpeed = MotorSpeed;
      SendSpeedCommand(MotorSpeed);         
    }
  }
    else if(LastMode == "ON"){
      SendStopCommand();
      LastMode = "OFF";
  }   
}

void SendStartCommand(){
  digitalWrite(Motor1Pin1, HIGH);
  digitalWrite(Motor1Pin2, LOW); 
}

void SendStopCommand(){
  digitalWrite(Motor1Pin1, LOW);
  digitalWrite(Motor1Pin2, LOW); 
}

void SendSpeedCommand(int speed) {
  int mappedSpeed = map(speed, 0, 100, MinimalPWDNumber, MaximalPWDNumber);
  ledcWrite(PwmChannel, mappedSpeed); 
  SerialPrint("new motor speed set to: " + String(MotorSpeed) + " ("+ String(mappedSpeed) + ")");
}
  
void SetNewSpeed(int newSpeed){
  if (newSpeed > 100)
  {
    newSpeed = 100;
  }
  
  if((newSpeed > 0) && (newSpeed != MotorSpeed)) {
    int oldSpeed = MotorSpeed;
    MotorSpeed = newSpeed;
    SerialPrint("Updating Speed from " + String(oldSpeed) + " to " + String(newSpeed));
    UpdateTftSpeed(oldSpeed, MotorSpeed);
    RotaryEncoder.reset(newSpeed);
  }
}

void SetNewMotorMode(String newMode){
  if(newMode != MotorMode) {
    String oldMode = MotorMode;
    MotorMode = newMode;
    SerialPrint("Updating Motor from " + oldMode + " to " + MotorMode);
    UpdateTftMode(oldMode, MotorMode);
  }
}

void SetNewClientMode(String newClientMode){
    String oldStatus = ClientMode;
    ClientMode = newClientMode;
    SerialPrint("Updating Clientmode from " + oldStatus + " to " + newClientMode);
    UpdateTftClientMode(oldStatus, ClientMode);
}

void CheckForBurstStep(){
  if(MotorMode != "OFF"){
    //SerialPrint("Checking for Burst Step");
    unsigned long currentMillis = millis();
    if(currentMillis - PreviousMillisBurst >= IntervalBurst) {
      //SerialPrint("Executing next Burst Step");
      ExecuteBurstStep();
      PreviousMillisBurst = currentMillis;
    }
  }else {
    SendStopCommand();
  }
}

void ExecuteBurstStep(){
  if (BurstSpeed >= 100){
    BurstPhase = 2;
  }
  int rotaryValue = RotaryEncoder.readEncoder();
  int timer = -0.1 * rotaryValue + 11;
  if(BurstRestartCounter >= timer)
  {
    SerialPrint("Burst: Phase 0 - Restart");
    BurstPhase = 1;
    BurstSpeed = 50;
    BurstRestartCounter = 0;
    SendSpeedCommand(BurstSpeed);
    SendStartCommand();

  }
  if(BurstPhase == 1){
    SerialPrint("Burst: Phase 1 - Inreasing");
    double delta = 0.1 * rotaryValue;
    BurstSpeed = BurstSpeed + delta;
    SerialPrint("delta: " + String(delta) + " Burstspeed:  " + String(BurstSpeed));
    SendSpeedCommand(BurstSpeed);
  }
  if(BurstPhase == 2){
    SerialPrint("Burst: Phase 2 - Waiting");
    SendStopCommand();
    BurstRestartCounter++;
  } 
}

void InitializeTftScreen(){
    Tft.fillScreen(TFT_BLACK);
    Tft.setCursor(0, 0, 2);
    Tft.setTextColor(TFT_LIGHTGREY,TFT_BLACK);  
    Tft.setTextSize(1);
    Tft.println(NameforDisplay);
    Tft.setTextSize(2); 
    if(Online == 0){
      Tft.setTextColor(TFT_RED,TFT_BLACK);
    } else {
      Tft.setTextColor(TFT_LIGHTGREY,TFT_BLACK);
    }
    Tft.println(ClientMode);
    Tft.setTextSize(1);
    Tft.setTextColor(TFT_LIGHTGREY,TFT_BLACK); 
    Tft.println("Motor Mode");
    Tft.setTextSize(2); 
    Tft.println(MotorMode);
    Tft.setTextSize(1);
    Tft.println("Motor Speed");
    Tft.setTextSize(2);
    Tft.println(MotorSpeed);
  }

void UpdateTftSpeed(int oldSpeed, int newSpeed){
      String newSpeedString = String(newSpeed);
      newSpeedString.toCharArray(PrintoutNew, 4);
      String oldSpeedString = String(oldSpeed);
      oldSpeedString.toCharArray(PrintoutOld, 4);

      Tft.setTextSize(2); 
      //erase old Printout
      Tft.setCursor(0, 112, 2);
      Tft.setTextColor(TFT_BLACK,TFT_BLACK);
      Tft.println(PrintoutOld);
      //print new Printout
      Tft.setCursor(0, 112, 2);
      Tft.setTextColor(TFT_LIGHTGREY,TFT_BLACK);
      Tft.println(PrintoutNew);
      
}

void UpdateTftMode(String oldMode, String newMode){
      newMode.toCharArray(PrintoutNew, 4);
      oldMode.toCharArray(PrintoutOld, 4);
     
      Tft.setTextSize(2); 
      //erase old Printout
      Tft.setCursor(0, 64, 2);
      Tft.setTextColor(TFT_BLACK,TFT_BLACK);
      Tft.println(PrintoutOld);
      //print new Printout
      Tft.setCursor(0, 64, 2);
      Tft.setTextColor(TFT_LIGHTGREY,TFT_BLACK);
      Tft.println(PrintoutNew);
}

void UpdateTftClientMode(String oldStatus, String newStatus){
      newStatus.toCharArray(PrintoutNew, 9);
      oldStatus.toCharArray(PrintoutOld, 9);
     
      Tft.setTextSize(2); 
      //erase old Printout
      Tft.setCursor(0, 16, 2);
      Tft.setTextColor(TFT_BLACK,TFT_BLACK);
      Tft.println(PrintoutOld);
      //print new Printout
      Tft.setCursor(0, 16, 2);
      if(Online == 0){
        Tft.setTextColor(TFT_RED,TFT_BLACK); 
      } else {
        Tft.setTextColor(TFT_LIGHTGREY,TFT_BLACK);
      }
      Tft.println(PrintoutNew);
}

void SerialPrint(String message){
  if(Debug){
    Serial.println(message);
  } 
}
