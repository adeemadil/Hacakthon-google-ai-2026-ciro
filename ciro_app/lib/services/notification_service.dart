import 'dart:developer' as developer;
import 'package:flutter_local_notifications/flutter_local_notifications.dart';

class NotificationService {
  final FlutterLocalNotificationsPlugin _notificationsPlugin = FlutterLocalNotificationsPlugin();

  /// Initialize local notification configs for Android and iOS systems.
  Future<void> initialize() async {
    const AndroidInitializationSettings initializationSettingsAndroid =
        AndroidInitializationSettings('@mipmap/ic_launcher');
        
    const InitializationSettings initializationSettings = InitializationSettings(
      android: initializationSettingsAndroid,
    );
    
    try {
      await _notificationsPlugin.initialize(initializationSettings);
      developer.log("Notification services initialized successfully.");
    } catch (e) {
      developer.log("Failed to set up local notifications plugin: $e");
    }
  }

  /// Trigger and present a native system notification.
  Future<void> show(String title, String body) async {
    const AndroidNotificationDetails androidPlatformChannelSpecifics = AndroidNotificationDetails(
      'ciro_alerts_channel',
      'CIRO Emergency Alerts',
      channelDescription: 'Real-time telemetry and evacuation alerts from CIRO Orchestration.',
      importance: Importance.max,
      priority: Priority.high,
    );
    
    const NotificationDetails platformChannelSpecifics = NotificationDetails(
      android: androidPlatformChannelSpecifics,
    );
    
    try {
      await _notificationsPlugin.show(
        0, 
        title, 
        body, 
        platformChannelSpecifics,
      );
      developer.log("Native notification dispatched: $title");
    } catch (e) {
      developer.log("Encountered error while dispatching notification: $e");
    }
  }
}
