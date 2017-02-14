void setup() 
{
  Serial.begin(57600);
}

void loop() 
{
  String outboundMessage = "";
  outboundMessage += makeMessageString("ScoopReedSwitch", analogRead(A0));
  outboundMessage += makeMessageString("BucketMaterialDepthSense", analogRead(A1));
  Serial.println(outboundMessage);
}

String makeMessageString(String sensorName, int sensorValue)
{
  String msg = "<";
  msg += sensorName;
  msg += ":";
  msg += String(sensorValue);
  msg += ">";
  return msg;
}

