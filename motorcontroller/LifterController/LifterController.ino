#include "AiEsp32RotaryEncoder.h"
#include "Arduino.h"
#include <TFT_eSPI.h> // Graphics and font library for ST7735 driver chip
#include <SPI.h>
#include <WiFi.h>
#include <ESPAsyncWebServer.h>

#define ROTARY_ENCODER_A_PIN 21
#define ROTARY_ENCODER_B_PIN 32
#define ROTARY_ENCODER_BUTTON_PIN 25
AiEsp32RotaryEncoder rotaryEncoder = AiEsp32RotaryEncoder(ROTARY_ENCODER_A_PIN, ROTARY_ENCODER_B_PIN, ROTARY_ENCODER_BUTTON_PIN, -1);

TFT_eSPI tft = TFT_eSPI();  // Invoke library, pins defined in User_Setup.h

// Set your access point network credentials
const char* ssid = "x";
const char* password = "y";
int ConnectionTries = 0;
unsigned long previousMillis = 0;
const long interval = 2000; 
bool online = 0;

const char* nameforClient = "LifterController";
const String nameforDisplay = "Lifter";

// Create AsyncWebServer object on port 80
AsyncWebServer server(80);

// Motor
int motor1Pin1 = 27; 
int motor1Pin2 = 26; 
int enable1Pin = 12; 
int MinimalPWDNumber = 170;

int MotorSpeed = 5;
String MotorMode = "OFF";
String ClientMode = "BOOT..";
int LastSpeed = MotorSpeed;
String LastMode = "OFF";

// Setting PWM properties
const int freq = 30000;
const int pwmChannel = 0;
const int resolution = 8;
int dutyCycle = 100;

//TFT
char PrintoutNew[9];
char PrintoutOld[9];

void setup() {
  //we must initialize rotary encoder
  rotaryEncoder.begin();
  rotaryEncoder.setup([]{rotaryEncoder.readEncoder_ISR();});
  //optionally we can set boundaries and if values should cycle or not
  rotaryEncoder.setBoundaries(0, 101, false); //minValue, maxValue, cycle values (when max go to min and vice versa)
  rotaryEncoder.reset(MotorSpeed);
  // sets the pins as outputs:
  pinMode(motor1Pin1, OUTPUT);
  pinMode(motor1Pin2, OUTPUT);
  pinMode(enable1Pin, OUTPUT);
  
  // configure LED PWM functionalitites
  ledcSetup(pwmChannel, freq, resolution);
  // attach the channel to the GPIO to be controlled
  ledcAttachPin(enable1Pin, pwmChannel);

  tft.init();
  tft.setRotation(0);
  initializeTftScreen();
  Serial.begin(115200);
  Serial.println(String(nameforClient) + " v0.9 ready"); 


  connectWifi();

  server.on("/clientmode", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send_P(200, "text/plain", getClientMode().c_str());
  });

  server.on("/status", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send_P(200, "text/plain", getStatus().c_str());
  });

  server.on("/", HTTP_GET, [](AsyncWebServerRequest *request){
    request->redirect("http://legosorter:3000/");
  });

  server.on("/alterspeed", HTTP_PUT, [](AsyncWebServerRequest *request){
    String message = """updated"" : {";
    //Serial.println("Update Request received");
    if(request->hasParam("speedchange")){
      int speedchange = request->arg("speedchange").toInt();
      if(MotorSpeed + speedchange != MotorSpeed){
        setNewSpeed(MotorSpeed + speedchange);
        message += """speed"" :" + String(MotorSpeed) + " ";
        }   
      }
    request->send(200, "text/plain", message + "}");
  });

   server.on("/update", HTTP_PUT, [](AsyncWebServerRequest *request){
    String message = """updated"" : {";
    //Serial.println("Update Request received");
    if(request->hasParam("speed")){
      int speed = request->arg("speed").toInt();
      if(speed != MotorSpeed){
        setNewSpeed(speed);
        rotaryEncoder.reset(speed);
        message += """speed"" :" + String(speed) + ", ";
      }
    }
    if(request->hasParam("motormode")){
      String motormode = request->arg("motormode");
      if(motormode != MotorMode){
        setNewMotorMode(motormode);
        message += """motormode"" : """ + motormode + """, ";
      }
    }
    if(request->hasParam("clientmode")){
      String clientmode = request->arg("clientmode");
      if(clientmode != ClientMode) {
        setNewClientMode(clientmode);
        message += """clientmode"" : """ + clientmode + """";
      }
    }
    request->send(200, "text/plain", message + "}");
  });

  
  // Start server
  server.begin();
}

void loop() {
  checkForEncoderChanges();
  runMotor();
  checkWifiConnection();  
}


void connectWifi() {
   //Wifi
  WiFi.config(INADDR_NONE, INADDR_NONE, INADDR_NONE);
  WiFi.begin(ssid, password);
  WiFi.setHostname(nameforClient);
  Serial.println("Connecting...");
}

void checkWifiConnection() {
  unsigned long currentMillis = millis();
  if(currentMillis - previousMillis >= interval) {
    if(WiFi.status()== WL_CONNECTED ) {
      if(online == 0) {// was disconnected, now connected
        Serial.println("Wifi connection established");
        online = 1;
        setNewClientMode(ClientMode); //update Display to show correct color 
      }
    } else{
      if(online == 1){ //was online, now disconnected
        Serial.println("Wifi connection lost");
        online = 0;
        setNewClientMode(ClientMode); //update Display to show correct color 
      }
      Serial.println("Trying to Reconnect to Wifi.");
      connectWifi();
    }
     previousMillis = currentMillis;
  }
}

String getClientMode(){
  return ClientMode;
}

String getStatus(){
  return"{\"speed\":" + String(MotorSpeed) + ",\"motormode\":\"" + String(MotorMode) + "\",\"clientmode\":\"" + String(ClientMode) + "\"}"; 
}

void checkForEncoderChanges(){
  if (rotaryEncoder.currentButtonState() == BUT_RELEASED) {
    //we can process it here or call separate function like:
    rotary_onButtonClick();
  }
  
  int16_t encoderDelta = rotaryEncoder.encoderChanged();
  if (encoderDelta == 0) return;
  int newSpeed = MotorSpeed;
  if (encoderDelta>0) newSpeed++;
  if (encoderDelta<0) newSpeed--;
  setNewSpeed(newSpeed);
  setNewClientMode("MANUAL");  
  Serial.println("updated ActualSpeed via Encoder to " + String(MotorSpeed));
}
  
void rotary_onButtonClick() {
  toggleMotorMode();
  setNewClientMode("MANUAL");
}

void toggleMotorMode(){
    //Serial.println("Motor currently: " + MotorMode);
    if(MotorMode == "ON") {
      setNewMotorMode("OFF");

      Serial.println("Motor stopped");
    }
    else
    {
      setNewMotorMode("ON");
      Serial.println("Motor started");
   }
}
 
void runMotor() {
    if(MotorMode == "ON") {
      if(LastMode == "OFF"){
        digitalWrite(motor1Pin1, HIGH);
        digitalWrite(motor1Pin2, LOW); 
        LastSpeed = LastSpeed -1;
        LastMode = "ON";
      }
      if(MotorSpeed != LastSpeed){
        LastSpeed = MotorSpeed;
        
        int mappedSpeed = map(MotorSpeed, 0, 100, MinimalPWDNumber, 255);
        ledcWrite(pwmChannel, mappedSpeed); 
        Serial.println("new motor speed set to: " + String(MotorSpeed) + " ("+ String(mappedSpeed) + ")");
      }
    }
     else if(LastMode == "ON"){
        digitalWrite(motor1Pin1, LOW);
        digitalWrite(motor1Pin2, LOW); 
        LastMode = "OFF";
    }   
}
  
void setNewSpeed(int newSpeed){
      if(newSpeed > 0 && newSpeed < 101) {
        int oldSpeed = MotorSpeed;
        MotorSpeed = newSpeed;
        updateTftSpeed(oldSpeed, MotorSpeed);
      }
}

void setNewMotorMode(String newMode){
      String oldMode = MotorMode;
      MotorMode = newMode;
      Serial.println("Updating Motor from " + oldMode + " to " + MotorMode);
      updateTftMode(oldMode, MotorMode);
}

void setNewClientMode(String newClientMode){
        String oldStatus = ClientMode;
        ClientMode = newClientMode;
        updateTftClientMode(oldStatus, ClientMode);
      
}
void initializeTftScreen(){
    tft.fillScreen(TFT_BLACK);
    tft.setCursor(0, 0, 2);
    tft.setTextColor(TFT_WHITE,TFT_BLACK);  
    tft.setTextSize(1);
    tft.println(nameforDisplay);
    tft.setTextSize(2); 
    if(online == 0){
      tft.setTextColor(TFT_BLUE,TFT_BLACK); // blue is red 
    } else {
      tft.setTextColor(TFT_WHITE,TFT_BLACK);
    }
    tft.println(ClientMode);
    tft.setTextSize(1);
    tft.setTextColor(TFT_WHITE,TFT_BLACK); 
    tft.println("Motor Mode");
    tft.setTextSize(2); 
    tft.println(MotorMode);
    tft.setTextSize(1);
    tft.println("Motor Speed");
    tft.setTextSize(2);
    tft.println(MotorSpeed);
  }

void updateTftSpeed(int oldSpeed, int newSpeed){
      String newSpeedString = String(newSpeed);
      newSpeedString.toCharArray(PrintoutNew, 4);
      String oldSpeedString = String(oldSpeed);
      oldSpeedString.toCharArray(PrintoutOld, 4);
      int mappedOldSpeed = map(oldSpeed, 0, 100, 0, tft.width());
      int mappednewSpeed = map(newSpeed, 0, 100, 0, tft.width());

      tft.setTextSize(2); 
      //erase old Printout
      tft.setCursor(0, 112, 2);
      tft.setTextColor(TFT_BLACK,TFT_BLACK);
      tft.println(PrintoutOld);
      //print new Printout
      tft.setCursor(0, 112, 2);
      tft.setTextColor(TFT_WHITE,TFT_BLACK);
      tft.println(PrintoutNew);
      
}

void updateTftMode(String oldMode, String newMode){
      newMode.toCharArray(PrintoutNew, 4);
      oldMode.toCharArray(PrintoutOld, 4);
     
      tft.setTextSize(2); 
      //erase old Printout
      tft.setCursor(0, 64, 2);
      tft.setTextColor(TFT_BLACK,TFT_BLACK);
      tft.println(PrintoutOld);
      //print new Printout
      tft.setCursor(0, 64, 2);
      tft.setTextColor(TFT_WHITE,TFT_BLACK);
      tft.println(PrintoutNew);
}

void updateTftClientMode(String oldStatus, String newStatus){
      newStatus.toCharArray(PrintoutNew, 9);
      oldStatus.toCharArray(PrintoutOld, 9);
     
      tft.setTextSize(2); 
      //erase old Printout
      tft.setCursor(0, 16, 2);
      tft.setTextColor(TFT_BLACK,TFT_BLACK);
      tft.println(PrintoutOld);
      //print new Printout
      tft.setCursor(0, 16, 2);
      if(online == 0){
        tft.setTextColor(TFT_BLUE,TFT_BLACK); // blue is red 
      } else {
        tft.setTextColor(TFT_WHITE,TFT_BLACK);
      }
      tft.println(PrintoutNew);
}
