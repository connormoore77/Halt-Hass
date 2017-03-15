





// Steinhart-Hart data:
//edited B
const double A1_const = 0.003354016;
const double B1_const = 0.0002460382;
const double C1_const = 0.000003405377;
const double D1_const = 0.0000103424;

// Thermistor's 25 degree resistance.
double Rt = 10020;

// Sense resistor resistance.
double resistance = 51167;

// Thermistor on pin A0.
int thermistor = A0;

double getCalculatedTemperature(int value)
{
  // Determine the voltages.
  double r_volts = 5.0 * value / 1024;
  double t_volts = 5.0 - r_volts;
  
  // Determine the resistance of the thermistor.
  double R = resistance * (t_volts / r_volts);
  double R2 = resistance * (5.0 / r_volts)-resistance;
  

  // Steinhart-Hart equation.
  double log_r = log(R / Rt);
  double b_val = B1_const*log_r;
  double c_val = C1_const*log_r*log_r;
  double d_val = D1_const*log_r*log_r*log_r;
  double K = 1 / (A1_const + b_val + c_val + d_val);
  //return K - 273.15;
  double  a=5.56169;
  double b=-6.55039e-04;
  double c=4.12224;
  double d=-4.85833e-02;
  double e=4.34730;
  double f=-4.01509e-01;
  R2 = R2/1000;
  double TEMP = exp(a+b*R2)+exp(c+d*R2)+exp(e+f*R2)-273;
  return TEMP;
}
double getCalculatedTemperature2(int value)
{
  // Determine the voltages.
  double r_volts = 5.0 * value / 1024;
  double t_volts = 5.0 - r_volts;
  
  // Determine the resistance of the thermistor.
  double R = resistance * (t_volts / r_volts);

  // Steinhart-Hart equation.
  double log_r = log(R / Rt);
  double b_val = B1_const*log_r;
  double c_val = C1_const*log_r*log_r;
  double d_val = D1_const*log_r*log_r*log_r;
  double K = 1 / (A1_const + b_val + c_val + d_val);
  return K - 273.15;
  double  a=5.56169;
  double b=-6.55039e-04;
  double c=4.12224;
  double d=-4.85833e-02;
  double e=4.34730;
  double f=-4.01509e-01;
  R = R/1000;
  double TEMP = exp(a+b*R)+exp(c+d*R)+exp(e+f*R)-273;
  //return TEMP;
}

void setup(){

  Serial.begin(9600);

  // Throw away one analog value. Things may have changed.
  analogRead(thermistor);
}

void loop() {

  // Read the real value and convert it to a temperature.
  int value = analogRead(thermistor);
  double temp = getCalculatedTemperature(value);
  double temp2 = getCalculatedTemperature2(value);
  Serial.println(temp);
  //Serial.println("The below is temp, above is temp2");
  //Serial.println();
  //Serial.println(temp2);
  //temp = (temp * 1.8)+32;
 // Serial.println(" C	");
 // Serial.println(value);
  //Serial.print(temp);

 

 // Serial.println(day());
   //Serial.println(hour());
    //Serial.println(minute());
     //Serial.println(second());
  
  delay(3000);
}
