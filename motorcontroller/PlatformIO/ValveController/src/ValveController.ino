#include "Arduino.h"
#include <ArduinoOTA.h>
#include <ESPAsyncWebServer.h>
#include <CircularBuffer.h>
#include <ezTime.h>
#include <ArduinoJson.h>
#include "OTA.h"
#include "boardinfo.h"
#include <credentials.h>
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
const String Version = VERSION;

// Create AsyncWebServer object on port 80 
AsyncWebServer Server(80);

// Valves
float PressureReading = 0;
const int NumberOfValves = 8;
//const int valvePins[NumberOfValves] = {13,18,14,27,26,25,33,32}; // define pins
//const int valvePins[NumberOfValves] = {27,26,14,25,18,33,13,32}; // define pins
const int valvePins[NumberOfValves] = {25,18,14,33,26,13,27,32}; // define pins
#define ONBOARD_LED  2

String ClientMode = "BOOT..";

//TFT
char PrintoutNew[9];
char PrintoutOld[9];

//Timed Event Handling 
Timezone myLocalTime;

//CircularBuffer
typedef struct {
  long actiontime;
  bool openValve;
  int bucket;
} BrickAction;
const int NumberofElementsInQueue = 20;
CircularBuffer<BrickAction,NumberofElementsInQueue> BickActionBuffers[NumberOfValves];

void setup() {
  SetupOTA(NameforClient, mySSID, myPASSWORD);
 
  pinMode(ONBOARD_LED,OUTPUT);
  myLocalTime.setLocation(F("de")); // set your time zone
  Serial.begin(115200);
  SerialPrint(String(NameforClient) + " " + Version + " ready"); 
  
  Server.on("/", HTTP_GET, [](AsyncWebServerRequest *request){
    request->redirect("http://legosorter:3000/");
  });

  Server.on("/getstatus", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send(200, "text/plain", GetStatus());
  });

  Server.on("/getpressure", HTTP_GET, [](AsyncWebServerRequest *request){
     request->send_P(200, "text/plain", GetPressure().c_str());
  });

  Server.on("/selftest", HTTP_PUT, [](AsyncWebServerRequest *request){
    StaticJsonDocument<768> SelfTestResponsedoc;
    SelfTestResponsedoc["client"] = NameforClient;
    SerialPrint("Selftest is running...");
    for(int i=0; i<NumberOfValves+1; i++)
      {
        JsonObject Valve = SelfTestResponsedoc.createNestedObject("Valve" + String(i+1));
        Valve["ON"] = UTC.dateTime("H:i:s.v");
        ChangeValvePosition(i,1);
        delay(500);
        ChangeValvePosition(i,0);
        Valve["OFF"] = UTC.dateTime("H:i:s.v");
      }
    String message;
    serializeJsonPretty(SelfTestResponsedoc, message);
    request->send(200, "text/plain", message);
  });

  Server.on("/pushBrick", HTTP_PUT, [](AsyncWebServerRequest *request){
    SerialPrint("Update Request received");
    StaticJsonDocument<256> PushBrickResponsedoc;
    PushBrickResponsedoc["client"] = NameforClient;
    String message = "";
    JsonObject pushBrick  = PushBrickResponsedoc.createNestedObject("pushBrick");
    pushBrick.remove("error");

    // GUARDS
    if(!request->hasParam("time") || !request->hasParam("bucket")) {
      pushBrick["error"] = "Missing information about time or bucket!";
      request->send(500, "text/plain", message ); 
    }

    int bucket = request->arg("bucket").toInt();
    int bucketindex = bucket -1;
    if (bucket < 0 && bucket >= NumberOfValves) {
        pushBrick["error"] = "Error: bucketnumber not suppported!";
        request->send(500, "text/plain", message ); 
      }
      
    if(BickActionBuffers[bucketindex].isFull()) {
      pushBrick["error"] = "Error: Buffer is full!";
      request->send(500, "text/plain", message ); 
    }
    
    BrickAction action = {};
    // BUCKET
    action.bucket = bucket;
    pushBrick["bucket"] =  String(bucket);
    
    // DURATION
    int duration = 20; 
    if(request->hasParam("duration")){
      duration = request->arg("duration").toInt();
    }
    pushBrick["duration"] = String(duration);

    // TIME 
    long requesttime = CutTimeStampTolong(request->arg("time"));
    //SerialPrint("\r\nRequesttime:\t" + String(requesttime)); 
    long opentime = 0;
    if(requesttime < 15000) {
      opentime = CutTimeStampTolong(GetUnixTimeStamp()) + requesttime;
    } else {
      opentime = requesttime;
    }
    //SerialPrint("opentime:\t" + String(opentime)); 
    pushBrick["time"] = String(opentime);   
    
    if(opentime != 0 ) {
      //open valve
      action.openValve = 1;
      action.actiontime = opentime;
      BickActionBuffers[bucketindex].push(action);
      
      //close valve
      action.openValve = 0;
      action.actiontime = opentime + duration;
      BickActionBuffers[bucketindex].push(action);
    }
    PushBrickResponsedoc["datetime"] = UTC.dateTime(RFC3339_EXT);
    serializeJsonPretty(PushBrickResponsedoc, message);
    request->send(200, "text/plain", message);
  });

  Server.on("/update", HTTP_PUT, [](AsyncWebServerRequest *request){
    StaticJsonDocument<128> StatusResponsedoc;
    SerialPrint("Update Request received");
    if(request->hasParam("clientmode")){
      String clientmode = request->arg("clientmode");
      if(clientmode != ClientMode) {
        SetNewClientMode(clientmode);
      }
      StatusResponsedoc["clientmode"] = ClientMode;
    }

    if(request->hasParam("ntp")){
      String ntp = request->arg("ntp");
      if(ntp == "1") {
        updateNTP();
        StatusResponsedoc["lastNtpUpdateTime"] = String(lastNtpUpdateTime());
      }
    }
    StatusResponsedoc["datetime"] = UTC.dateTime(RFC3339_EXT);
    String message;
    serializeJsonPretty(StatusResponsedoc, message);
    request->send(200, "text/plain", message);
  });
  
  // Start server
  Server.begin();
  SetNewClientMode("Searching");  

  // sets the pins as outputs:
  for(int i=0; i<NumberOfValves; i++)
  {
    pinMode(valvePins[i], OUTPUT);// set pin as output
    digitalWrite(valvePins[i], HIGH); // set initial state OFF for low trigger relay
    SerialPrint("ValvePin " + String(valvePins[i]) + " was set to HIGH"); 
  }
  setInterval(60); // every minute ntp update
  waitForSync();

  Init();
}

void loop() {
  ArduinoOTA.handle();
  CheckWifiConnection();  
  CheckEvents();
}

void Init(){
  SetNewClientMode("Searching");  
}

void ConnectWifi() {
   //Wifi
  WiFi.config(INADDR_NONE, INADDR_NONE, INADDR_NONE);
  WiFi.begin(Ssid, Password);
  WiFi.setHostname(NameforClient);
  Serial.println("Connecting...");
}

void CheckWifiConnection() {
  unsigned long currentMillis = millis();
  if(currentMillis - PreviousMillis >= Interval) {
    if(WiFi.status()== WL_CONNECTED ) {
      if(Online == 0) {// was disconnected, now connected
        SerialPrint("Wifi connection established");
        waitForSync();
        SerialPrint("Done. Current time is " + myLocalTime.dateTime("d.m.Y H:i:s.v T") + "\t|\t" +  GetUnixTimeStamp());
        Online = 1;
        SetNewClientMode("Online"); 
        digitalWrite(ONBOARD_LED,HIGH);
      }
    } else{
      if(Online == 1){ //was Online, now disconnected
        SerialPrint("Wifi connection lost");
        Online = 0;
        SetNewClientMode("Offline");
        digitalWrite(ONBOARD_LED,LOW);
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
  StaticJsonDocument<192> StatusResponsedoc;
  String message = "";
  StatusResponsedoc["client"] = NameforClient;
  StatusResponsedoc["ip"] = WiFi.localIP().toString();
  StatusResponsedoc["version"] = Version;
  StatusResponsedoc["clientmode"] = ClientMode;
  StatusResponsedoc["lastNtpUpdateTime"] = lastNtpUpdateTime();
  StatusResponsedoc["timestamp"] = GetUnixTimeStamp();
  StatusResponsedoc["datetime"] = myLocalTime.dateTime("d.m.Y H:i:s.v T");
  serializeJsonPretty(StatusResponsedoc, message);
  return message; 
}

String GetPressure(){
  StaticJsonDocument<192> PressureResponsedoc;
  String message = "";
  PressureReading = analogRead(34);
  float voltage = (PressureReading * 0.0008) + 0.1754;
  float pressure_bar = (PressureReading * 0.0022) - 1.0257;
  SerialPrint("Reading: " + String(PressureReading) + "\t|\tVoltage: "+ String(voltage) + "v\t|\tPressure: " + String(pressure_bar) + "bar");
  PressureResponsedoc["client"] = NameforClient;
  JsonObject pressure = PressureResponsedoc.createNestedObject("pressureRecord");
  pressure["voltage"] = voltage;
  pressure["pressureBar"] = pressure_bar;
  pressure["datetime"] = myLocalTime.dateTime("d.m.Y H:i:s.v T");
  
  serializeJsonPretty(PressureResponsedoc, message);
  return message;
}

void CheckEvents(){
  //SerialPrint("CurrentTime:\t" + String(currentTime));
  for (int i = 0; i <= NumberOfValves-1; i++) {
    if(!BickActionBuffers[i].isEmpty()) {
      BrickAction currentBrickaction = BickActionBuffers[i].first();
      long currentTime =  CutTimeStampTolong(GetUnixTimeStamp());
       if(currentTime - currentBrickaction.actiontime >=  0) {
          SerialPrint("CurrentTime:\t" + String(currentTime) + " \t Actiontime: \t " + String(currentBrickaction.actiontime)  + "\t Bucketnumber: \t" + String(currentBrickaction.bucket)+ "\t OpenValve: \t" + String(currentBrickaction.openValve));
          SerialPrint("\t Event was due before " + String(currentTime - currentBrickaction.actiontime)  + "ms");
          BickActionBuffers[i].shift();
          ChangeValvePosition(currentBrickaction.bucket, currentBrickaction.openValve);
        } else {
          SerialPrint("Bucket\t" + String(currentBrickaction.bucket)+  " will push in " + String(currentTime - currentBrickaction.actiontime)  + " ms");
        }
    }
  }
}

void ChangeValvePosition(int valvenumber, bool openValve){
  if (openValve) {
    digitalWrite(valvePins[valvenumber-1], LOW); 
    SerialPrint("ValvePin " + String(valvePins[valvenumber-1]) + " was set to LOW"); 
  } else {
    digitalWrite(valvePins[valvenumber-1], HIGH); 
    SerialPrint("ValvePin " + String(valvePins[valvenumber-1]) + " was set to HIGH"); 
  }
}

void SetNewClientMode(String newClientMode){
    String oldStatus = ClientMode;
    ClientMode = newClientMode;
    SerialPrint("Updating Clientmode from " + oldStatus + " to " + newClientMode);
}

long CutTimeStampTolong(String timestamp){
  if(timestamp.length() < 9) {
    return timestamp.toInt();
  }
  String tmp = timestamp.substring(4,13);
  return tmp.toInt();
}

String GetUnixTimeStamp(){
  String milliEpoch = "";
  int tries = 1;
  do {
     char buffer [3];
     unsigned long ms_time = ms();
     sprintf(buffer,"%03d",ms_time);
     milliEpoch = String(now()) + buffer;
     if(tries > 1) {
      delay(1);
      SerialPrint("getting unix timestamp. Try: " + String(tries) + " Length: " + String(milliEpoch.length()));
     }
     tries += 1;
    } while (milliEpoch.length() != 13);
    
    return milliEpoch.substring(0,13);
}

void SerialPrint(String message){
  if(Debug){
    TelnetStream.println(message);
  } 
}
