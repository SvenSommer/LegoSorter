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

#define ROTARY_ENCODER_A_PIN 32
#define ROTARY_ENCODER_B_PIN 21
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
const String NameforDisplay = "Lifter";
const String Version = VERSION;

// Create AsyncWebServer object on port 80
AsyncWebServer Server(80);

// Motor
const int MOTOR_PWM_PIN = 16;
const int MOTOR_VINA_PIN = 27;
const int MOTOR_VINB_PIN = 26;
int MinimalPWDNumber = 80;

int MotorSpeed = 5;
String MotorMode = "OFF";
String ClientMode = "BOOT..";
int LastSpeed = 0;
String LastMode = "OFF";

// Setting PWM properties
const int Freq = 18000;
const int PwmChannel = 0;
const int Resolution = 8;
int DutyCycle = 100;

//TFT
char PrintoutNew[9];
char PrintoutOld[9];

//Timed Event Handling 
Timezone myLocalTime;

bool _handlingOTA;

void setup() {
  SetupOTA(NameforClient, mySSID, myPASSWORD);

  myLocalTime.setLocation(F("de")); // set your time zone
  //we must initialize rotary encoder
  RotaryEncoder.begin();
  RotaryEncoder.setup([]{RotaryEncoder.readEncoder_ISR();});
  //optionally we can set boundaries and if values should cycle or not
  RotaryEncoder.setBoundaries(0, 101, false); //minValue, maxValue, cycle values (when max go to min and vice versa)
  RotaryEncoder.reset(MotorSpeed);
  // sets the pins as outputs:
  // pinMode(MOTOR_PWM_PIN, OUTPUT); // ist das korrekt? - wird evtl. von ledcAttachPin gesetzt
  pinMode(MOTOR_VINA_PIN, OUTPUT);
  pinMode(MOTOR_VINB_PIN, OUTPUT);
  
  // configure LED PWM functionalitites
  ledcSetup(PwmChannel, Freq, Resolution);
  // attach the channel to the GPIO to be controlled
  ledcAttachPin(MOTOR_PWM_PIN, PwmChannel);

  tft.init();
  tft.setRotation(2);
  InitializeTftScreen();
  Serial.begin(115200);
  SerialPrint(String(NameforClient) + " v0.9 ready"); 

  Server.on("/", HTTP_GET, [](AsyncWebServerRequest *request){
    request->redirect("http://legosorter:3000/");
  });

  Server.on("/getstatus", HTTP_GET, [](AsyncWebServerRequest *request){
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

void loop() {
  ArduinoOTA.handle();
  if(!_handlingOTA)
  {
    CheckForEncoderChanges();
    RunMotor();
    CheckWifiConnection();  
  }
}

void Init(){
  SetNewSpeed(50);
  SetNewMotorMode("OFF");
}

void ConnectWifi() {
   //Wifi
  WiFi.config(INADDR_NONE, INADDR_NONE, INADDR_NONE);
  WiFi.begin(ssid, password);
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
      while(WiFi.status() != WL_CONNECTED) {
        ConnectWifi();
        delay(500);
        Serial.print("Reconnecting...");
      }
    }
     PreviousMillis = currentMillis;
  }
}

String GetStatus(){
  StaticJsonDocument<128> StatusResponsedoc;
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
    //SerialPrint("Motor currently: " + MotorMode);
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
    if(MotorMode == "ON") {
      if(LastMode == "OFF"){
        digitalWrite(MOTOR_VINA_PIN, HIGH);
        digitalWrite(MOTOR_VINB_PIN, LOW); 
        LastSpeed = LastSpeed -1;
        LastMode = "ON";
      }
      if(MotorSpeed != LastSpeed){
        LastSpeed = MotorSpeed;
        
        int mappedSpeed = map(MotorSpeed, 0, 100, MinimalPWDNumber, 255);
        ledcWrite(PwmChannel, mappedSpeed); 
        SerialPrint("new motor speed set to: " + String(MotorSpeed) + " ("+ String(mappedSpeed) + ")");
      }
    }
     else if(LastMode == "ON"){
        digitalWrite(MOTOR_VINA_PIN, LOW);
        digitalWrite(MOTOR_VINB_PIN, LOW); 
        LastMode = "OFF";
    }   
}
  
void SetNewSpeed(int newSpeed){
  if (newSpeed > 100)
  {
    newSpeed = 100;
  }
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
      tft.setTextColor(TFT_RED,TFT_BLACK); 
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
