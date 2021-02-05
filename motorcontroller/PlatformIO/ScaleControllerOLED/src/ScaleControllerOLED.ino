#include <Wire.h>  // Only needed for Arduino 1.6.5 and earlier
#include "SSD1306Wire.h" // legacy include: `#include "SSD1306.h"`
#include "HX711.h"
#include <WiFi.h>
#include <ESPAsyncWebServer.h>
#include <HTTPClient.h>
#include <SPI.h>
#include <ezTime.h>
#include <CircularBuffer.h>
#include "ota.h"
#include "boardinfo.h"
#include <credentials.h>
#include <ArduinoJson.h>
#include <ArduinoOTA.h>

// Initialize the OLED display using Wire library
SSD1306Wire  display(0x3c, 5, 4);

// Set your access point network credentials
const char* Ssid = mySSID;
const char* Password = myPASSWORD;
int ConnectionTries = 0;
unsigned long PreviousMillis = 0;
const long Interval = 2000; 
bool Online = 0;
const String ScaleNumber = BOARDNUMBER;
const char* NameforClient = CONTROLLERNAME;
const String NameforDisplay = "Scale " + ScaleNumber;
const String Version = VERSION;
String ClientMode = "AWAIT";

// HX711 circuit wiring
const int LOADCELL_DOUT_PIN = 13;
const int LOADCELL_SCK_PIN = 15;
double Treshold = 4;
int Cooldown_cycles = -1;
double Oldvalue = 0.00;
double Newvalue = 0.00;
double Delta = 0.00;
double Rausch_max = 0.000;
int Counter = 0;
int Cooldown = 1;
double Lastbrickweight = 0;

String SetNo = "?";
String CompletePartCount = "?";

bool Debug = true;
bool Success = false;
bool Blocked = false;


AsyncWebServer Server(80);

HX711 Scale;

//Timed Event Handling 
Timezone myLocalTime;
CircularBuffer<long,50> BricktimeBuffer;
CircularBuffer<long,50> BrickIdBuffer;

//TFT
char PrintoutNew[9];
char PrintoutOld[9];

//LegoServer for BrickResponse
String ServerName = "http://192.168.178.46:3000/bricksortedresponse";

void setup() {
  SetupOTA(NameforClient, mySSID, myPASSWORD);

  myLocalTime.setLocation(F("de")); // set your time zone

  Scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);

  // Initialising the UI will init the display too.
  display.init();
  display.flipScreenVertically();
  display.setFont(ArialMT_Plain_10);
  DrawLoadingDisplay();

  Serial.begin(115200);
  SerialPrint(String(NameforClient) + " v0.9"); 
  SerialPrint("Connecting...");

  Server.on("/", HTTP_GET, [](AsyncWebServerRequest *request){
    request->redirect("http://legosorter:3000/");
  });
  
  Server.on("/getstatus", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send(200, "text/plain", GetStatus());
  });

   Server.on("/initialize", HTTP_PUT, [](AsyncWebServerRequest *request){
    StaticJsonDocument<128> responsedoc;
    //SerialPrint("Update Request received");
    responsedoc["client"] = NameforClient;
    if(request->hasParam("setNo")){
      String setNo = request->arg("setNo");
      if(setNo != SetNo){
        SetNo = setNo;
        SetNewClientMode(setNo);
        responsedoc["setNo"] = String(setNo);
      }
    }
    if(request->hasParam("completePartCount")){
      String completePartCount = request->arg("completePartCount");
      if(completePartCount != CompletePartCount){
        CompletePartCount = completePartCount;
        SetNewPartsCounter(Counter);
        responsedoc["completePartCount"] = String(completePartCount);
      }
    }
    String message;
    serializeJsonPretty(responsedoc, message);
    request->send(200, "text/plain", message);
  });

  Server.on("/tare", HTTP_PUT, [](AsyncWebServerRequest *request){
    StaticJsonDocument<64> responsedoc;
    responsedoc["client"] = NameforClient;
    Scale.tare();  
    SetNewWeight(0);
    responsedoc["tared"] = "completed";
    String message;
    serializeJsonPretty(responsedoc, message);
    request->send(200, "text/plain", message);
  });

  Server.on("/reset", HTTP_PUT, [](AsyncWebServerRequest *request){
    Scale.tare(); 
    SetNo = "?";
    SetNewClientMode("AWAIT");
    SetNewWeight(0);
    CompletePartCount = "?";
    InitializeTftScreen();
    SetNewPartsCounter(0);
    request->send(200, "text/plain", GetStatus());
  });

  Server.on("/expectBrick", HTTP_PUT, [](AsyncWebServerRequest *request){
     StaticJsonDocument<128> responsedoc;
     responsedoc["client"] = NameforClient;
     JsonObject expectBrick = responsedoc.createNestedObject("expectBrick");
     String message;
     //SerialPrint("Update Request received");
    if(request->hasParam("time")){
      long bricktime_org = CutTimeStampTolong(request->arg("time"));
      //long bricktime_org = CutTimeStampTolong(GetUnixTimeStamp() + 2000);
      if(BricktimeBuffer.isFull()) {
      expectBrick["error"] = "Error: Buffer is full!";
      expectBrick["errorcode"] = "400";
      serializeJsonPretty(responsedoc, message);
      request->send(500, "text/plain", message);
      return;
      }

      BricktimeBuffer.push(bricktime_org);
      SerialPrint("received bricktime_str: " + String(BricktimeBuffer.last()));
      expectBrick["time"] =  String(BricktimeBuffer.last());
    }

    if(request->hasParam("weight")){
      double weight = request->arg("weight").toDouble();
      expectBrick["weight"] = String(weight);
    }

    if(request->hasParam("brickId")){
      long brickId = request->arg("brickId").toInt();
      BrickIdBuffer.push(brickId);
      expectBrick["brickId"] = String(BrickIdBuffer.last());
    } else {
        BrickIdBuffer.push(0);
        expectBrick["brickId"] = String(BrickIdBuffer.last());
    }
    serializeJsonPretty(responsedoc, message);
    request->send(200, "text/plain", message);
  });

  
  // Start server
  Server.begin();

  
  SerialPrint("Initializing the scale. Waiting for Wifi and NTP Server Connection");
  Scale.set_scale(2280.f);    // this value is obtained by calibrating the scale with known weights; see the README for details
  Scale.tare();    // reset the scale to 0 
  
  setInterval(60); // every minute ntp update
  waitForSync();
  Recalibrate();

}

void loop() {
  ArduinoOTA.handle();
  CheckWifiConnection(); 
  CheckEvents();
   // clear the display
  display.clear();
  // draw the current demo method
  DrawStatusDisplay();
  display.setTextAlignment(TEXT_ALIGN_RIGHT);
  display.drawString(10, 128, String(millis()));
  // write the buffer to the display
  display.display();
}

void DrawStatusDisplay() {
    display.setTextAlignment(TEXT_ALIGN_LEFT);
    display.setFont(ArialMT_Plain_10);
    display.drawString(0, 0, String(NameforDisplay));
    display.setFont(ArialMT_Plain_16);
    display.drawString(0, 10, ClientMode);
    display.setFont(ArialMT_Plain_10);
    display.drawString(0, 26, "Parts");
    display.setFont(ArialMT_Plain_16);
    display.drawString(0, 36, String(Counter) + "/" + CompletePartCount);
    display.setFont(ArialMT_Plain_10);
    display.drawString(0, 52, String(Lastbrickweight,2));
}

void DrawLoadingDisplay() {
    display.setTextAlignment(TEXT_ALIGN_LEFT);
    display.setFont(ArialMT_Plain_16);
    display.drawString(0, 0, "LOADING....");
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
        SerialPrint("Wifi connection established. Getting Current Time from NTP Server");
        waitForSync();
        SerialPrint("Done. Current time is " + myLocalTime.dateTime("d.m.Y H:i:s.v T") + "\t|\t" +  GetUnixTimeStamp());
        SetNewClientMode("AWAIT");
        Online = 1;
        SetNewClientMode(ClientMode); //update Display to show correct color 
      }
    } else{
      if(Online == 1){ //was Online, now disconnected
        SerialPrint("Wifi connection lost");
        Online = 0;
        SerialPrint("Wifi connection lost");
        SetNewClientMode(ClientMode); //update Display to show correct color 
      }
      SerialPrint("Trying to Reconnect to Wifi.");
      while(WiFi.status() != WL_CONNECTED) {
        ConnectWifi();
        delay(500);
        Serial.print(".");
        SerialPrint("Reconnecting...");
        SetNewClientMode("RECONNECTING");
      }
    }
     PreviousMillis = currentMillis;
  }
}

void CheckEvents(){
  if(!BricktimeBuffer.isEmpty()) {
  long currentTime =  CutTimeStampTolong(GetUnixTimeStamp());
  if(currentTime - BricktimeBuffer.first() >=  0) {
      long brickid = BrickIdBuffer.first();
      Serial.print("currentTime: \t" + String(currentTime) + " \t Bricktime: \t " + String(BricktimeBuffer.first())  + "\t id: \t" + String(brickid));
      SerialPrint("\t Event was due before " + String(currentTime - BricktimeBuffer.first())  + "ms");
      BricktimeBuffer.shift();
      BrickIdBuffer.shift();
      AwaitBrick(brickid);
    }
/*     else {
      Serial.print("currentTime: \t" + String(currentTime) + "ms \t Bricktime: \t " + String(BricktimeBuffer.first())  + "");
      SerialPrint("\t Event is due in" + String(currentTime - BricktimeBuffer.first()));
    } */
  }
}

void AwaitBrick(long brickid){
  Success = false;
  if(!Blocked) {
    Blocked = true;
    SerialPrint("Awaiting Brick!");
    MarkScreenForIncommingPart();
    for (int i = 1; i <= 3; i++) {
      Serial.print("Round -> " + String(i));
      if(CheckScale()) {
        if (Debug){
          SerialPrint("Brick added!");
        }
        Recalibrate();
 
        SendoutStatusMessage(brickid, true);
        Success = true;
        Blocked = false;
        break;
      }
    }
    if(!Success) {
           if (Debug){
              SerialPrint("No Brick found!");
            }
        MarkScreenForIncommingPartFailue();
        SendoutStatusMessage(brickid, false);
        }
      Blocked = false;
  } else {
    SerialPrint("ERROR! Scale currently blocked!");
  }
}

void SendoutStatusMessage(long brickid, bool success) {
  String serverPath  = ServerName + "?brickid=" + String(brickid) + "&status=" + String(success);
  SerialPrint("Sending to " + serverPath);
  // Your Domain name with URL path or IP address with path
  HTTPClient http;
  http.begin(serverPath.c_str());
  
  // Send HTTP GET request
  int httpResponseCode = http.GET();
  
  if (httpResponseCode>0) {
    Serial.print("HTTP Response code: ");
    SerialPrint(String(httpResponseCode));
    String payload = http.getString();
    SerialPrint(payload);
  }
  else {
    Serial.print("Error code: ");
    SerialPrint(String(httpResponseCode));
  }
  // Free resources
  http.end();
}

long CutTimeStampTolong(String timestamp){
  String tmp = timestamp.substring(4);
  //SerialPrint("tmp: " + tmp);
  return tmp.toInt();
}

String GetUnixTimeStamp(){
   String milliEpoch = String(now()) + ms();
   //SerialPrint("\t | \t" + milliEpoch +"\t|\t"+ String(ms_time));
   return milliEpoch;
   
}

bool CheckScale(){
  Oldvalue = Newvalue;
  Newvalue = Scale.get_units(10)*-100;
  Delta = Newvalue - Oldvalue; 
  if (Cooldown >= 1) {  
    if (abs(Delta) > Treshold && Delta > 0 ){
      SetNewPartsCounter(Counter + 1);
      SetNewWeight(Newvalue);
      Cooldown = Cooldown_cycles;
      if (Debug){
        SerialPrint("\tSuccess\tCounter:\t" + String(Counter) + "/" + String(Cooldown) 
        + "\t| Newvalue:\t" + String(Newvalue , 2) + "(" +  String(Delta,2)  +  ")" 
        + "\t| Lastbrickweight:\t" + String(Lastbrickweight , 2)
        + "\t| Rausch (max):\t" + String(Rausch_max,2));
      }
      return true;
    } else if (abs(Delta) > Rausch_max) {
      Rausch_max = abs(Delta);
      
    }
  }
  Cooldown +=1;
  if (Debug){
        SerialPrint("\tFailure\t Counter:\t" + String(Counter) + "/" + String(Cooldown) 
        + "\t| Newvalue:\t" + String(Newvalue , 2) + "(" +  String(Delta,2)  +  ")" 
        + "\t| Lastbrickweight:\t" + String(Lastbrickweight , 2)
        + "\t| Rausch (max):\t" + String(Rausch_max,2));
  }
  return false;
}


void Recalibrate() {
  Newvalue = Scale.get_units(10)*-100;
  if (Newvalue > 0) {
    SetNewWeight(Newvalue);
  }
  else {
    SetNewWeight(0);
  }  
  Cooldown +=1;
  SerialPrint("recalibrated to :\t" + String(Newvalue)); 
}

String GetStatus(){
  StaticJsonDocument<256> Responsedoc;
  Responsedoc["client"] = NameforClient;
  Responsedoc["ip"] = WiFi.localIP().toString();
  Responsedoc["version"] = Version;
  Responsedoc["setNo "] = SetNo;
  Responsedoc["completePartCount "] = CompletePartCount;
  Responsedoc["currentPartCount "] = String(Counter);
  Responsedoc["weight "] = String(Lastbrickweight) ;
  Responsedoc["datetime"] = myLocalTime.dateTime("d.m.Y H:i:s.v T");
  String message;
  serializeJsonPretty(Responsedoc, message);
  return message;
}

void SetNewPartsCounter(int newCounter){
  int oldCounter = newCounter;
  Counter = newCounter;
  String textToOverwrite = String(oldCounter) + "/" + CompletePartCount;
  String textToWrite = String(Counter) + "/" + CompletePartCount;        
  UpdateTftPartsSuccess(textToOverwrite,textToWrite);
}

void SetNewWeight(double newWeight){
  //Convert Weight to grams
  newWeight = newWeight / 36.68627451;
  if(Counter > 0) {
    double oldWeight = Lastbrickweight;
    Lastbrickweight = newWeight;
    UpdateTftWeight(String(oldWeight,2),String(Lastbrickweight,2));
  }
}

void SetNewClientMode(String newClientMode){
  String oldStatus = ClientMode;
  ClientMode = newClientMode;
  UpdateTftClientMode(oldStatus, ClientMode);
}

void MarkScreenForIncommingPart(){
  updateTftPartsExspecting(String(Counter) + "/" + CompletePartCount, String(Counter) + "/" + CompletePartCount);
}

void MarkScreenForIncommingPartFailue(){
    UpdateTftPartsFailure(String(Counter) + "/" + CompletePartCount, String(Counter) + "/" + CompletePartCount);
  }

void InitializeTftScreen(){
    // clear the display
    display.clear();
    display.setTextAlignment(TEXT_ALIGN_LEFT);
    display.setFont(ArialMT_Plain_10);
    display.drawString(0, 0, NameforDisplay);
  }

void UpdateTftClientMode(String oldStatus, String newStatus){
      newStatus.toCharArray(PrintoutNew, 9);
      oldStatus.toCharArray(PrintoutOld, 9);
}

void updateTftParts(String oldParts, String newParts){
      newParts.toCharArray(PrintoutNew, 9);
      oldParts.toCharArray(PrintoutOld, 9);
}

void updateTftPartsExspecting(String oldParts, String newParts){
      newParts.toCharArray(PrintoutNew, 9);
      oldParts.toCharArray(PrintoutOld, 9);
}

void UpdateTftPartsSuccess(String oldParts, String newParts){
      newParts.toCharArray(PrintoutNew, 9);
      oldParts.toCharArray(PrintoutOld, 9);
}

void UpdateTftPartsFailure(String oldParts, String newParts){
      newParts.toCharArray(PrintoutNew, 9);
      oldParts.toCharArray(PrintoutOld, 9);
}

void UpdateTftWeight(String oldWeight, String newWeight){
      newWeight.toCharArray(PrintoutNew, 9);
      oldWeight.toCharArray(PrintoutOld, 9);
}


void SerialPrint(String message){
  if(Debug){
    TelnetStream.println(message);
  } 
}

