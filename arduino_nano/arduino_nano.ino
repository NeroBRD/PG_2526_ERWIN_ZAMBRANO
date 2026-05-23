#include <AccelStepper.h>

// ---------------------------------------------------------
// VERSIÓN DE SOFTWARE
// ---------------------------------------------------------
#define FIRMWARE_VERSION "1.2.0-PRO"

// ---------------------------------------------------------
// CONFIGURACIÓN DE PINES
// ---------------------------------------------------------

// Pines de Joystick Analógicos
const int pinJoyX = A0; // Joystick X (Movimiento del carro: Adelante/Atrás)
const int pinJoyY = A1; // Joystick Y (Movimiento de elevación: Subir/Bajar)
const int pinJoyZ = A2; // Joystick Z (Movimiento de giro: Izquierda/Derecha)

// Pines del Driver TB6612FNG (Motores DC N20)
// Motor A: Controla el Carro (Adelante/Atrás)
const int pinAIN1 = 2;
const int pinAIN2 = 4;
const int pinPWMA = 3;

// Motor B: Controla la Elevación (Subir/Bajar)
const int pinBIN1 = 7;
const int pinBIN2 = 8;
const int pinPWMB = 5;

// Pines del Driver DRV8825 (Motor a pasos Nema 17) para el Giro
const int pinSTEP = 9;
const int pinDIR = 10;

// Inicialización de la librería AccelStepper (Modo 1 = Driver con pines Step y Dir)
AccelStepper stepperGiro(1, pinSTEP, pinDIR);

// ---------------------------------------------------------
// VARIABLES GLOBALES DE ESTADO
// ---------------------------------------------------------

// Velocidad base y zonas muertas para los joysticks
const int umbralJoyMin = 400; // Si el valor es menor, se considera movimiento hacia un lado
const int umbralJoyMax = 600; // Si el valor es mayor, se considera movimiento hacia el otro lado
const int pwmMaximo = 255;    // Velocidad máxima PWM

// Comandos recibidos desde la Web (vía Serial)
char comandoWeb = 'S'; // 'S' = Stop por defecto
unsigned long ultimoComandoWebTime = 0; // Para el timeout de seguridad
const unsigned long TIMEOUT_WEB_MS = 500; // Si no hay comando web en 500ms, se detiene la web

// Variables de Telemetría
unsigned long ultimoReporteTime = 0;
const unsigned long INTERVALO_REPORTE_MS = 500;
char comandoActualEjecutado = 'S';

void setup() {
  // Inicializamos el puerto serial a 9600 baudios para comunicarnos con el ESP32
  Serial.begin(9600);
  
  // Imprimir la versión de firmware (será ignorado por la telemetría del ESP32)
  Serial.println("Iniciando Arduino Grúa Pro v" FIRMWARE_VERSION);
  
  // Configuramos los pines de los motores DC como salida
  pinMode(pinAIN1, OUTPUT);
  pinMode(pinAIN2, OUTPUT);
  pinMode(pinPWMA, OUTPUT);
  
  pinMode(pinBIN1, OUTPUT);
  pinMode(pinBIN2, OUTPUT);
  pinMode(pinPWMB, OUTPUT);
  
  // Configuramos los parámetros del motor paso a paso (Nema 17)
  stepperGiro.setMaxSpeed(1000);   // Velocidad máxima en pasos por segundo
  stepperGiro.setAcceleration(500); // Aceleración en pasos por segundo cuadrado
  stepperGiro.setSpeed(0);          // Velocidad inicial 0
}

void loop() {
  // 1. Leer Comandos Web desde Serial
  leerComandoSerial();

  // 2. Controlar Timeout de Seguridad de la Web
  // Si pasó mucho tiempo sin recibir comandos web de movimiento continuo, forzamos parada web
  if (millis() - ultimoComandoWebTime > TIMEOUT_WEB_MS) {
    comandoWeb = 'S'; 
  }

  // 3. Procesar Movimiento del Carro (Motor A)
  controlarCarro();

  // 4. Procesar Movimiento de Elevación (Motor B)
  controlarElevacion();

  // 5. Procesar Movimiento de Giro (Motor Stepper)
  controlarGiro();
  
  // Función no bloqueante que actualiza los pasos del motor (debe llamarse constantemente)
  stepperGiro.runSpeed();

  // 6. Enviar Telemetría
  enviarTelemetria();
}

// ---------------------------------------------------------
// FUNCIONES AUXILIARES
// ---------------------------------------------------------

// Función para leer caracteres enviados por el ESP32
void leerComandoSerial() {
  bool recibioNuevo = false;
  char ultimoC = '\0';
  
  // Leemos todo el buffer disponible para no quedarnos rezagados
  while (Serial.available() > 0) {
    char c = Serial.read();
    if (c == 'F' || c == 'B' || c == 'U' || c == 'D' || c == 'L' || c == 'R' || c == 'S') {
      ultimoC = c;
      recibioNuevo = true;
    }
  }
  
  if (recibioNuevo) {
    comandoWeb = ultimoC;
    ultimoComandoWebTime = millis(); // Actualizamos el temporizador de seguridad
  }
}

// Controla el movimiento del carro integrando Joystick X y Comando Web
void controlarCarro() {
  int valorX = analogRead(pinJoyX);
  int velocidadPWM = 0;
  bool adelante = false;
  bool atras = false;

  // Lógica de Joystick
  if (valorX > umbralJoyMax) {
    adelante = true;
    velocidadPWM = map(valorX, umbralJoyMax, 1023, 0, pwmMaximo);
  } else if (valorX < umbralJoyMin) {
    atras = true;
    velocidadPWM = map(valorX, umbralJoyMin, 0, 0, pwmMaximo);
  }

  // Lógica de Web (sobrescribe la velocidad si está activa)
  if (comandoWeb == 'F') {
    adelante = true;
    atras = false;
    velocidadPWM = pwmMaximo; // Velocidad completa para comandos web
  } else if (comandoWeb == 'B') {
    atras = true;
    adelante = false;
    velocidadPWM = pwmMaximo;
  }

  // Mover Motor A (Carro)
  if (adelante) {
    digitalWrite(pinAIN1, HIGH);
    digitalWrite(pinAIN2, LOW);
    analogWrite(pinPWMA, velocidadPWM);
  } else if (atras) {
    digitalWrite(pinAIN1, LOW);
    digitalWrite(pinAIN2, HIGH);
    analogWrite(pinPWMA, velocidadPWM);
  } else {
    // Freno corto (Stop)
    digitalWrite(pinAIN1, LOW);
    digitalWrite(pinAIN2, LOW);
    analogWrite(pinPWMA, 0);
  }
}

// Controla el movimiento de elevación integrando Joystick Y y Comando Web
void controlarElevacion() {
  int valorY = analogRead(pinJoyY);
  int velocidadPWM = 0;
  bool subir = false;
  bool bajar = false;

  // Lógica de Joystick
  if (valorY > umbralJoyMax) {
    subir = true;
    velocidadPWM = map(valorY, umbralJoyMax, 1023, 0, pwmMaximo);
  } else if (valorY < umbralJoyMin) {
    bajar = true;
    velocidadPWM = map(valorY, umbralJoyMin, 0, 0, pwmMaximo);
  }

  // Lógica de Web
  if (comandoWeb == 'U') {
    subir = true;
    bajar = false;
    velocidadPWM = pwmMaximo;
  } else if (comandoWeb == 'D') {
    bajar = true;
    subir = false;
    velocidadPWM = pwmMaximo;
  }

  // Mover Motor B (Elevación)
  if (subir) {
    digitalWrite(pinBIN1, HIGH);
    digitalWrite(pinBIN2, LOW);
    analogWrite(pinPWMB, velocidadPWM);
  } else if (bajar) {
    digitalWrite(pinBIN1, LOW);
    digitalWrite(pinBIN2, HIGH);
    analogWrite(pinPWMB, velocidadPWM);
  } else {
    // Freno corto (Stop)
    digitalWrite(pinBIN1, LOW);
    digitalWrite(pinBIN2, LOW);
    analogWrite(pinPWMB, 0);
  }
}

// Controla el movimiento de giro integrando Joystick Z y Comando Web
void controlarGiro() {
  int valorZ = analogRead(pinJoyZ);
  float velocidadStepper = 0;

  // Lógica de Joystick
  if (valorZ > umbralJoyMax) {
    // Giro Derecha
    velocidadStepper = map(valorZ, umbralJoyMax, 1023, 0, 1000); 
  } else if (valorZ < umbralJoyMin) {
    // Giro Izquierda (velocidad negativa en AccelStepper significa cambio de dirección)
    velocidadStepper = -map(valorZ, umbralJoyMin, 0, 0, 1000);
  }

  // Lógica de Web
  if (comandoWeb == 'R') {
    velocidadStepper = 800; // Velocidad predefinida para web (Derecha)
  } else if (comandoWeb == 'L') {
    velocidadStepper = -800; // Velocidad predefinida para web (Izquierda)
  }

  // Establecer la velocidad de movimiento continuo del motor paso a paso
  stepperGiro.setSpeed(velocidadStepper);
}

// Función para enviar datos de telemetría hacia el ESP32
void enviarTelemetria() {
  if (millis() - ultimoReporteTime >= INTERVALO_REPORTE_MS) {
    ultimoReporteTime = millis();
    
    // Determinamos el comando actual de forma simplificada
    // Si comandoWeb no es 'S', ese tiene prioridad. 
    // Sino, evaluamos si algún motor se está moviendo por joystick.
    comandoActualEjecutado = comandoWeb;
    if (comandoActualEjecutado == 'S') {
      int vX = analogRead(pinJoyX);
      int vY = analogRead(pinJoyY);
      int vZ = analogRead(pinJoyZ);
      if (vX > umbralJoyMax) comandoActualEjecutado = 'F';
      else if (vX < umbralJoyMin) comandoActualEjecutado = 'B';
      else if (vY > umbralJoyMax) comandoActualEjecutado = 'U';
      else if (vY < umbralJoyMin) comandoActualEjecutado = 'D';
      else if (vZ > umbralJoyMax) comandoActualEjecutado = 'R';
      else if (vZ < umbralJoyMin) comandoActualEjecutado = 'L';
    }
    
    // Formato: T:posicion,comando
    Serial.print("T:");
    Serial.print(stepperGiro.currentPosition());
    Serial.print(",");
    Serial.println(comandoActualEjecutado);
  }
}
