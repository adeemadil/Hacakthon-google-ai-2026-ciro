import 'dart:developer' as developer;
import 'package:web_socket_channel/web_socket_channel.dart';
import '../config/api_config.dart';

class WebSocketService {
  WebSocketChannel? _channel;

  /// Establish connections to the active websocket hub.
  void connect() {
    try {
      _channel = WebSocketChannel.connect(Uri.parse(ApiConfig.wsUrl));
      developer.log("WebSocket service established connection to ${ApiConfig.wsUrl}");
    } catch (e) {
      developer.log("Failed to initialize WebSocket channel: $e");
    }
  }

  /// Expose the incoming messaging stream.
  Stream<dynamic>? get stream => _channel?.stream;

  /// Gracefully close current websocket channels.
  void disconnect() {
    try {
      _channel?.sink.close();
      developer.log("WebSocket channel gracefully closed.");
    } catch (e) {
      developer.log("Error encountered during WebSocket closure: $e");
    }
  }
}
