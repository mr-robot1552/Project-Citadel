import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.net.Socket;

String dataLine = null;
int iAngle = 0;
int iDistance = 0;

Socket socket;
BufferedReader reader;

// TCP connection settings (must match the Raspberry Pi server host/port)
final String RPI_HOST = "127.0.0.1";
final int RPI_PORT = 5005;

// Display settings
float pixsDistance;

void setup() {
  size(1200, 700);
  smooth();

  connectToRadarServer();
}

void draw() {
  // Background with light motion blur effect
  noStroke();
  fill(0, 12);
  rect(0, 0, width, height - height * 0.065);

  // Radar visuals
  drawRadar();
  drawLine();
  drawObject();
  drawText();

  // Read and parse incoming radar data
  if (reader != null) {
    try {
      if (socket != null && socket.isConnected() && (dataLine = reader.readLine()) != null) {
        processData(dataLine);
      }
    } catch (IOException e) {
      // Connection loss is treated as a runtime condition; the UI continues rendering
      println("Radar data stream interrupted: " + e.getMessage());
      closeConnection();
      reader = null;
      socket = null;
    }
  } else {
    // Attempt periodic reconnect if the connection is not available
    if (frameCount % 120 == 0) {
      connectToRadarServer();
    }
  }
}

void connectToRadarServer() {
  try {
    socket = new Socket(RPI_HOST, RPI_PORT);
    reader = new BufferedReader(new InputStreamReader(socket.getInputStream()));
    println("Connected to radar server at " + RPI_HOST + ":" + RPI_PORT);
  } catch (Exception e) {
    println("Unable to connect to radar server: " + e.getMessage());
    reader = null;
    socket = null;
  }
}

void closeConnection() {
  try {
    if (reader != null) reader.close();
  } catch (Exception e) { }
  try {
    if (socket != null) socket.close();
  } catch (Exception e) { }
}

// Expected format: "angle,distance\n"
void processData(String line) {
  String[] parts = split(line.trim(), ',');
  if (parts != null && parts.length >= 2) {
    int parsedAngle = parseIntSafe(parts[0]);
    int parsedDistance = (int)parseFloatSafe(parts[1]);

    if (parsedAngle >= 0 && parsedAngle <= 180) {
      iAngle = parsedAngle;
    }
    if (parsedDistance >= 0) {
      iDistance = parsedDistance;
    }
  }
}

int parseIntSafe(String s) {
  try {
    return Integer.parseInt(s.trim());
  } catch (Exception e) {
    return -1;
  }
}

float parseFloatSafe(String s) {
  try {
    return Float.parseFloat(s.trim());
  } catch (Exception e) {
    return -1;
  }
}

// Draw radar grid and arcs
void drawRadar() {
  pushMatrix();
  translate(width / 2, height - height * 0.074);
  noFill();
  strokeWeight(2);
  stroke(98, 245, 31);

  // Concentric arcs
  for (float i = 0.0625; i <= 0.687; i += 0.207) {
    arc(0, 0, width - width * i, width - width * i, PI, TWO_PI);
  }

  // Angle lines
  for (int a = 30; a <= 150; a += 30) {
    line(0, 0, (-width / 2) * cos(radians(a)), (-width / 2) * sin(radians(a)));
  }
  line(-width / 2, 0, width / 2, 0);
  popMatrix();
}

// Draw sweeping line
void drawLine() {
  pushMatrix();
  translate(width / 2, height - height * 0.074);

  strokeWeight(4);
  stroke(30, 250, 60);
  line(0, 0, (height - height * 0.12) * cos(radians(iAngle)), -(height - height * 0.12) * sin(radians(iAngle)));

  popMatrix();
}

// Draw detected object marker (within alert range)
void drawObject() {
  pushMatrix();
  translate(width / 2, height - height * 0.074);

  strokeWeight(6);
  stroke(255, 10, 10);

  pixsDistance = iDistance * ((height - height * 0.1666) * 0.025);

  if (iDistance > 0 && iDistance < 40) {
    line(
      pixsDistance * cos(radians(iAngle)), -pixsDistance * sin(radians(iAngle)),
      (width - width * 0.505) * cos(radians(iAngle)), -(width - width * 0.505) * sin(radians(iAngle))
    );
  }
  popMatrix();
}

// Display labels and telemetry
void drawText() {
  pushMatrix();

  // Bottom info bar
  noStroke();
  fill(0);
  rect(0, height - height * 0.0648, width, height);

  fill(98, 245, 31);
  textSize(25);

  text("10cm", width - width * 0.3854, height - height * 0.0833);
  text("20cm", width - width * 0.281,  height - height * 0.0833);
  text("30cm", width - width * 0.177,  height - height * 0.0833);
  text("40cm", width - width * 0.0729, height - height * 0.0833);

  textSize(40);
  text("Project Citadel – Nineveh Shadow Ops Facility", width * 0.03, height - height * 0.0277);
  text("Angle: " + iAngle + "°", width - width * 0.48, height - height * 0.0277);
  text("Distance: " + iDistance + " cm", width - width * 0.30, height - height * 0.0277);

  // Angle markers
  textSize(25);
  fill(98, 245, 60);
  for (int a = 30; a <= 150; a += 30) {
    float xPos = width / 2 * cos(radians(a)) - width * 0.5;
    float yPos = -width / 2 * sin(radians(a)) + height - height * 0.074;
    text(a + "°", xPos, yPos);
  }

  popMatrix();
}
