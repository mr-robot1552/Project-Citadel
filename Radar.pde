import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.net.Socket;

// Defines variables
String angle = "";
String distance = "";
String data = "";
String noObject;
float pixsDistance;
int iAngle, iDistance;
Socket socket;
BufferedReader reader;
PFont orcFont;

void setup() {
  size(1200, 700); // Adjust to your screen resolution
  smooth();

  // Establish TCP connection
  try {
    socket = new Socket("<your-ip-address>", 5005); // Replace with your Raspberry Pi IP
    reader = new BufferedReader(new InputStreamReader(socket.getInputStream()));
    println("Connected to Raspberry Pi");
  } catch (Exception e) {
    println("Error connecting to Raspberry Pi: " + e.getMessage());
  }
}

void draw() {
  // Background and motion blur
  fill(98, 245, 31);
  noStroke();
  fill(0, 4); 
  rect(0, 0, width, height - height * 0.065); 
  
  // Draw radar elements
  fill(98, 245, 31); // Green color
  drawRadar(); 
  drawLine();
  drawObject();
  drawText();

  // Read data from the TCP socket
  if (reader != null) {
    try {
      if ((data = reader.readLine()) != null) {
        processData(data);
      }
    } catch (IOException e) {
      println("Error reading data: " + e.getMessage());
    }
  }
}

// Process incoming data and update angle and distance
void processData(String data) {
  String[] parts = data.split(",");
  if (parts.length >= 2) {
    angle = parts[0];
    distance = parts[1];
    iAngle = int(angle);
    iDistance = int(distance);
  }
}

// Draw radar grid and arcs
void drawRadar() {
  pushMatrix();
  translate(width / 2, height - height * 0.074);
  noFill();
  strokeWeight(2);
  stroke(98, 245, 31);

  // Draw concentric arcs with finer lines
  for (float i = 0.0625; i <= 0.687; i += 0.207) {
    arc(0, 0, width - width * i, width - width * i, PI, TWO_PI);
  }

  // Draw angle lines for radar
  for (int a = 30; a <= 150; a += 30) {
    line(0, 0, (-width / 2) * cos(radians(a)), (-width / 2) * sin(radians(a)));
  }
  line(-width / 2, 0, width / 2, 0); // Main line at 90 degrees
  popMatrix();
}

// Draw detected object (if within range)
void drawObject() {
  pushMatrix();
  translate(width / 2, height - height * 0.074);
  strokeWeight(9);
  stroke(255, 10, 10); // Red color for detected objects
  
  pixsDistance = iDistance * ((height - height * 0.1666) * 0.025); // Convert distance to pixels

  if (iDistance < 40) {
    line(pixsDistance * cos(radians(iAngle)), -pixsDistance * sin(radians(iAngle)),
         (width - width * 0.505) * cos(radians(iAngle)), -(width - width * 0.505) * sin(radians(iAngle)));
  }
  popMatrix();
}

// Draw sweeping line
void drawLine() {
  pushMatrix();
  strokeWeight(9);
  stroke(30, 250, 60); // Bright green line for sweeping motion
  translate(width / 2, height - height * 0.074);
  
  // Slow down the sweeping line by reducing its speed
  frameRate(30); // 50% slower
  
  line(0, 0, (height - height * 0.12) * cos(radians(iAngle)), -(height - height * 0.12) * sin(radians(iAngle)));
  popMatrix();
}

// Display text and labels
void drawText() {
  pushMatrix();
  fill(0, 0, 0);
  noStroke();
  rect(0, height - height * 0.0648, width, height);
  fill(98, 245, 31); // Green text

  textSize(25);
  text("10cm", width - width * 0.3854, height - height * 0.0833);
  text("20cm", width - width * 0.281, height - height * 0.0833);
  text("30cm", width - width * 0.177, height - height * 0.0833);
  text("40cm", width - width * 0.0729, height - height * 0.0833);

  textSize(40);
  text("Nineveh Shadow Ops", width - width * 0.875, height - height * 0.0277);
  text("Angle: " + iAngle + "°", width - width * 0.48, height - height * 0.0277);

  // Adjusted Distance text and measurement
  String distanceText = "Distance: " + iDistance + " cm";
  text(distanceText, width - width * 0.30, height - height * 0.0277); // Properly aligned side by side

  textSize(25);
  fill(98, 245, 60);
  for (int a = 30; a <= 150; a += 30) {
    float xPos = width / 2 * cos(radians(a)) - width * 0.5;
    float yPos = -width / 2 * sin(radians(a)) + height - height * 0.074;
    text(a + "°", xPos, yPos);
  }
  popMatrix();
}
