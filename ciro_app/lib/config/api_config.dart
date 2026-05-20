class ApiConfig {
  // Base URLs for the CIRO FastAPI Backend
  // 10.0.2.2 is the default IP to loopback to the host machine from the Android emulator.
  // Replace with local network IP or localhost if testing on Web/iOS.
  static const String baseUrl = 'http://10.0.2.2:8000';
  static const String wsUrl = 'ws://10.0.2.2:8000/ws';
}
