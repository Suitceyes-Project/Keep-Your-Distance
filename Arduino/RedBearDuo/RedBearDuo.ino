/*
 Name:    VibeGlove_Controller_Redbear.ino
 Created: 05.02.2017 10:03:06
 Author:  Jan
*/


#if defined(ARDUINO) 
SYSTEM_MODE(SEMI_AUTOMATIC); 
#endif

#include <CmdMessenger.h>  // CmdMessenger


#define MIN_CONN_INTERVAL          0x0028 // 50ms.
#define MAX_CONN_INTERVAL          0x0190 // 500ms.
#define SLAVE_LATENCY              0x0000 // No slave latency.
#define CONN_SUPERVISION_TIMEOUT   0x03E8 // 10s.

// Learn about appearance: http://developer.bluetooth.org/gatt/characteristics/Pages/CharacteristicViewer.aspx?u=org.bluetooth.characteristic.gap.appearance.xml
#define BLE_PERIPHERAL_APPEARANCE  BLE_APPEARANCE_UNKNOWN

#define BLE_DEVICE_NAME            "Simple Chat"

#define CHARACTERISTIC1_MAX_LEN    15
#define CHARACTERISTIC2_MAX_LEN    15
#define TXRX_BUF_LEN               15

/******************************************************
 *               Variable Definitions
 ******************************************************/
static uint8_t service1_uuid[16]    = { 0x71,0x3d,0x00,0x00,0x50,0x3e,0x4c,0x75,0xba,0x94,0x31,0x48,0xf1,0x8d,0x94,0x1e };
static uint8_t service1_tx_uuid[16] = { 0x71,0x3d,0x00,0x03,0x50,0x3e,0x4c,0x75,0xba,0x94,0x31,0x48,0xf1,0x8d,0x94,0x1e };
static uint8_t service1_rx_uuid[16] = { 0x71,0x3d,0x00,0x02,0x50,0x3e,0x4c,0x75,0xba,0x94,0x31,0x48,0xf1,0x8d,0x94,0x1e };

// GAP and GATT characteristics value
static uint8_t  appearance[2] = { 
  LOW_BYTE(BLE_PERIPHERAL_APPEARANCE), 
  HIGH_BYTE(BLE_PERIPHERAL_APPEARANCE) 
};

static uint8_t  change[4] = {
  0x00, 0x00, 0xFF, 0xFF
};

static uint8_t  conn_param[8] = {
  LOW_BYTE(MIN_CONN_INTERVAL), HIGH_BYTE(MIN_CONN_INTERVAL), 
  LOW_BYTE(MAX_CONN_INTERVAL), HIGH_BYTE(MAX_CONN_INTERVAL), 
  LOW_BYTE(SLAVE_LATENCY), HIGH_BYTE(SLAVE_LATENCY), 
  LOW_BYTE(CONN_SUPERVISION_TIMEOUT), HIGH_BYTE(CONN_SUPERVISION_TIMEOUT)
};

/* 
 * BLE peripheral advertising parameters:
 *     - advertising_interval_min: [0x0020, 0x4000], default: 0x0800, unit: 0.625 msec
 *     - advertising_interval_max: [0x0020, 0x4000], default: 0x0800, unit: 0.625 msec
 *     - advertising_type: 
 *           BLE_GAP_ADV_TYPE_ADV_IND 
 *           BLE_GAP_ADV_TYPE_ADV_DIRECT_IND 
 *           BLE_GAP_ADV_TYPE_ADV_SCAN_IND 
 *           BLE_GAP_ADV_TYPE_ADV_NONCONN_IND
 *     - own_address_type: 
 *           BLE_GAP_ADDR_TYPE_PUBLIC 
 *           BLE_GAP_ADDR_TYPE_RANDOM
 *     - advertising_channel_map: 
 *           BLE_GAP_ADV_CHANNEL_MAP_37 
 *           BLE_GAP_ADV_CHANNEL_MAP_38 
 *           BLE_GAP_ADV_CHANNEL_MAP_39 
 *           BLE_GAP_ADV_CHANNEL_MAP_ALL
 *     - filter policies: 
 *           BLE_GAP_ADV_FP_ANY 
 *           BLE_GAP_ADV_FP_FILTER_SCANREQ 
 *           BLE_GAP_ADV_FP_FILTER_CONNREQ 
 *           BLE_GAP_ADV_FP_FILTER_BOTH
 *     
 * Note:  If the advertising_type is set to BLE_GAP_ADV_TYPE_ADV_SCAN_IND or BLE_GAP_ADV_TYPE_ADV_NONCONN_IND, 
 *        the advertising_interval_min and advertising_interval_max should not be set to less than 0x00A0.
 */
static advParams_t adv_params = {
  .adv_int_min   = 0x0030,
  .adv_int_max   = 0x0030,
  .adv_type      = BLE_GAP_ADV_TYPE_ADV_IND,
  .dir_addr_type = BLE_GAP_ADDR_TYPE_PUBLIC,
  .dir_addr      = {0,0,0,0,0,0},
  .channel_map   = BLE_GAP_ADV_CHANNEL_MAP_ALL,
  .filter_policy = BLE_GAP_ADV_FP_ANY
};

static uint8_t adv_data[] = {
  0x02,
  BLE_GAP_AD_TYPE_FLAGS,
  BLE_GAP_ADV_FLAGS_LE_ONLY_GENERAL_DISC_MODE,
  
  0x08,
  BLE_GAP_AD_TYPE_SHORT_LOCAL_NAME,
  'B','i','s','c','u','i','t',
  
  0x11,
  BLE_GAP_AD_TYPE_128BIT_SERVICE_UUID_COMPLETE,
  0x1e,0x94,0x8d,0xf1,0x48,0x31,0x94,0xba,0x75,0x4c,0x3e,0x50,0x00,0x00,0x3d,0x71
};

static uint16_t character1_handle = 0x0000;
static uint16_t character2_handle = 0x0000;

static uint8_t characteristic1_data[CHARACTERISTIC1_MAX_LEN] = { 0x01 };
static uint8_t characteristic2_data[CHARACTERISTIC2_MAX_LEN] = { 0x00 };

static btstack_timer_source_t characteristic2;

char rx_buf[TXRX_BUF_LEN];
static uint8_t rx_state = 0;


// Redbear Duo (WPM)
const byte pinsNo[] = {D0,D1,D2,D3,D8,D9,12,13,14,15,16,17}; // array contains the vibe's pin numbers
// Arduino (No WPM)
//const byte pinsNo[] = { 2, 3, 4, 5, 6, 7, 8, 9, 10, 11 };

byte pinsValue[sizeof(pinsNo)]; // array will contain the current vibe values
unsigned long frequency; // frequency of blink vibration in ms
unsigned long lastUpdate; // will contain the time of last blink update in ms
boolean isOn; // will contain boolean if vibes are vibrating in current blink state
boolean hasChanged; // boolean if there have been changes to pins' values to take care of
CmdMessenger c = CmdMessenger(Serial); // Serial Messenger object
boolean debug = false;

enum // Define Commands:
{
  PinSet,    // 0: Set pin x to value y (args: pin, value)
  PinMute,   // 1: Set pin x to 0 (args: pin)
  GloveSet,  // 2: Set pin x0 to value y0, x1 to y1 etc. when odd no of arguments set last argument as frequency
  GloveMute, // 3: Set all pins to 0 (no args)
  FreqSet,   // 4: Set frequency to x (args: frequency)
  PinGet,    // 5: Request value of pin x (args: pin)
  FreqGet,   // 6: Request current frequency (no args)
  PinState,  // 7: Sends value y of pin x (args: pin, value)
  FreqState, // 8: Sends value of frequency x (args: frequency)
  StringMsg, // 9: Sends a string message x (args: x)
  DebugSet   // 10: sets debug mode to x (args: x)

};

void attachCommandCallbacks() { // attach callback functions for specific commands
  c.attach(OnUnknownCommand);
  c.attach(PinSet, OnPinSet);
  c.attach(PinMute, OnPinMute);
  c.attach(GloveSet, OnGloveSet);
  c.attach(GloveMute, OnGloveMute);
  c.attach(FreqSet, OnFreqSet);
  c.attach(PinGet, OnPinGet);
  c.attach(FreqGet, OnFreqGet);
  c.attach(DebugSet, OnDebugSet);
}

// Called when a received command has no attached function
void OnUnknownCommand()
{
  c.sendCmd(StringMsg, "Command without attached callback.");
}

void OnPinSet() {
  byte pin = c.readInt16Arg();
  if (!c.isArgOk()) {
    c.sendCmd(StringMsg, "PinGet: argument pin is not ok.");
    return;
  }
  byte value = c.readInt16Arg();
  if (!c.isArgOk()) {
    c.sendCmd(StringMsg, "PinGet: argument value is not ok.");
    return;
  }

  if (pin >= sizeof(pinsNo)) {
    c.sendCmd(StringMsg, "PinGet: argument pin is out of range.");
  }
  
  pinsValue[pin] = value;
  hasChanged = true;
  if (debug)
    c.sendCmd(StringMsg, "PinSet: Set pin " + String(pin) + " to value " + String(value));

}

void OnPinMute() {
  byte pin = c.readInt16Arg();
  if (!c.isArgOk()) {
    c.sendCmd(StringMsg, "PinMute: argument pin is not ok.");
    return;
  }

  if (pin >= sizeof(pinsNo)) {
    c.sendCmd(StringMsg, "PinMute: argument pin is out of range.");
  }

  pinsValue[pin] = 0;
  hasChanged = true;

}

void OnGloveSet() {
  while (true) {
    unsigned int arg0 = c.readInt16Arg();
    if (!c.isArgOk())
      return;
    byte arg1 = c.readInt16Arg();
    if (!c.isArgOk()) {
      // set last argument as frequency
      frequency = arg0;
      return;
    }

    if (arg0 >= sizeof(pinsNo)) {
      c.sendCmd(StringMsg, "GloveSet: argument pin is out of range.");
    }

    pinsValue[arg0] = arg1;
    hasChanged = true;
    if (debug)
      c.sendCmd(StringMsg, "PinSet: Set pin " + String(arg0) + " to value " + String(arg1));

  }

}

void OnGloveMute() {
  for (byte i = 0; i < sizeof(pinsNo); i++) {
    pinsValue[i] = 0;
    hasChanged = true;
  }
}

void OnFreqSet() {
  unsigned int f = c.readInt16Arg();
  if (!c.isArgOk()) {
    c.sendCmd(StringMsg, "FreqSet: argument frequency is not ok.");
    return;
  }
  if (f < 0) {
    c.sendCmd(StringMsg, "FreqSet: Value must be >= 0.");
    return;
  }
  frequency = f;
  if (debug)
    c.sendCmd(StringMsg, "FreqSet: Set frequency to " + String(f));
}

void OnPinGet() {
  byte pin = c.readInt16Arg();
  if (!c.isArgOk()) {
    c.sendCmd(StringMsg, "PinGet: Missing argument pin.");
    return;
  }

  if (pin >= sizeof(pinsNo)) {
    c.sendCmd(StringMsg, "PinGit: argument pin is out of range.");
  }

  c.sendCmdStart(PinState);
  c.sendCmdArg(pin);
  c.sendCmdArg(pinsValue[pin]);
  c.sendCmdEnd();

}

void OnFreqGet() {
  c.sendCmd(FreqState, frequency);
}

void OnDebugSet() {
  boolean dbg = c.readBoolArg();
  if (c.isArgOk()) {
    debug = dbg;
  }
}

void OnUnknown() {
  c.sendCmd(StringMsg, "Command without attached callback!");
}


void deviceConnectedCallback(BLEStatus_t status, uint16_t handle) {
  switch (status) {
    case BLE_STATUS_OK:
      Serial.println("Device connected!");
      break;
    default: break;
  }
}

int gattWriteCallback(uint16_t value_handle, uint8_t *buf, uint16_t size) 
{
  byte commandType = buf[0];
  Serial.println("Received message.");
  switch(commandType)
  {
    case PinSet:
    {
      Serial.println("Received Pin Set command");
      int pin = buf[1];
      byte intensity = buf[2];
      pinsValue[pin] = intensity;
      hasChanged = true;
    }
      break;
    case PinMute:
    {
      int pin = buf[1];
      pinsValue[pin] = 0;
      hasChanged = true;
    }
      break;
    case GloveMute:
    {
      for (byte i = 0; i < sizeof(pinsNo); i++)
      {
        pinsValue[i] = 0;
        hasChanged = true;
      }
    }
      break;
    case FreqSet:
    {
      int f = buf[1];
      frequency = f;
    }
      break;
  }

  return 0;
}

void deviceDisconnectedCallback(uint16_t handle) {
  Serial.println("Disconnected.");
}


// The characteristic value attribute handle can be obtained when you add the characteristic
static uint16_t char1_handle;
static uint16_t char2_handle;

static uint8_t char1_data[20];
static uint8_t char2_data[20];

static uint16_t gattReadCallback(uint16_t value_handle, uint8_t * buffer, uint16_t buffer_size) {   
  uint8_t ret_len = 0;

  Serial.print("Reads attribute value, handle: ");
  Serial.println(value_handle, HEX);

  if (char1_handle == value_handle) {   // Characteristic value handle.
    memcpy(buffer, char1_data, sizeof(char1_data));
    ret_len = sizeof(char1_data);
  }
  else if (char2_handle == value_handle) {
    memcpy(buffer, char2_data, sizeof(char2_data));
    ret_len = sizeof(char2_data);
  }

  return ret_len;
}

void setup() {
  frequency = 1000;
  lastUpdate = millis();
  isOn = false;
  hasChanged = false;

  for (byte i = 0; i < sizeof(pinsNo); i++) {
    pinsValue[i] = 0;
    pinMode(pinsNo[i], OUTPUT);

    if (debug) {
      analogWrite(pinsNo[i], 255);
      delay(500);
      analogWrite(pinsNo[i], 0);
    }
  }
  Serial.begin(115200);
  c.printLfCr();
  attachCommandCallbacks();

  ble.init();
  
  // Register BLE callback functions
  ble.onConnectedCallback(deviceConnectedCallback);
  ble.onDisconnectedCallback(deviceDisconnectedCallback);
  ble.onDataWriteCallback(gattWriteCallback);
  ble.onDataReadCallback(gattReadCallback);
  
// Add GAP service and characteristics
  ble.addService(BLE_UUID_GAP);
  ble.addCharacteristic(BLE_UUID_GAP_CHARACTERISTIC_DEVICE_NAME, ATT_PROPERTY_READ|ATT_PROPERTY_WRITE, (uint8_t*)BLE_DEVICE_NAME, sizeof(BLE_DEVICE_NAME));
  ble.addCharacteristic(BLE_UUID_GAP_CHARACTERISTIC_APPEARANCE, ATT_PROPERTY_READ, appearance, sizeof(appearance));
  ble.addCharacteristic(BLE_UUID_GAP_CHARACTERISTIC_PPCP, ATT_PROPERTY_READ, conn_param, sizeof(conn_param));

  // Add GATT service and characteristics
  ble.addService(BLE_UUID_GATT);
  ble.addCharacteristic(BLE_UUID_GATT_CHARACTERISTIC_SERVICE_CHANGED, ATT_PROPERTY_INDICATE|ATT_PROPERTY_READ|ATT_PROPERTY_WRITE, change, sizeof(change));

  // Add user defined service and characteristics
  ble.addService(service1_uuid);
  character1_handle = ble.addCharacteristicDynamic(service1_tx_uuid, ATT_PROPERTY_NOTIFY|ATT_PROPERTY_WRITE|ATT_PROPERTY_WRITE_WITHOUT_RESPONSE, characteristic1_data, CHARACTERISTIC1_MAX_LEN);
  character2_handle = ble.addCharacteristicDynamic(service1_rx_uuid, ATT_PROPERTY_NOTIFY|ATT_PROPERTY_WRITE|ATT_PROPERTY_WRITE_WITHOUT_RESPONSE, characteristic2_data, CHARACTERISTIC2_MAX_LEN);
  
  // Set BLE advertising parameters
  ble.setAdvertisementParams(&adv_params);

  // // Set BLE advertising data
  ble.setAdvertisementData(sizeof(adv_data), adv_data);

  // BLE peripheral starts advertising now.
  ble.startAdvertising();

  
  c.sendCmd(StringMsg, "Glove is up and running!");
}

void loop() {
  unsigned long currentTime = millis();
  // Process incoming serial data, and perform callbacks
  c.feedinSerialData();
  boolean changeState = (currentTime >= lastUpdate + frequency);
  // only if alternation phase ends or the pin values changed during on-phase
  if (changeState || (hasChanged && isOn)) {

    if (!isOn || hasChanged) {
      hasChanged = false;
      if (changeState) {
        isOn = true;
      }
      for (byte i = 0; i < sizeof(pinsNo); i++) {
        analogWrite(pinsNo[i], pinsValue[i]);
      }
    }

    else {
      isOn = false;
      hasChanged = false;
      for (byte i = 0; i < sizeof(pinsNo); i++) {
        analogWrite(pinsNo[i], LOW);
      }
    }

    if (changeState) { // update time stamp if a new
      lastUpdate = currentTime;
    }
  }
}
