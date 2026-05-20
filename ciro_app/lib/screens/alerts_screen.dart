import 'package:flutter/material.dart';

class AlertsScreen extends StatelessWidget {
  const AlertsScreen({super.key});

  final List<dynamic> activeAlerts = const [];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("CRISIS ALERTS"),
      ),
      body: activeAlerts.isEmpty
          ? Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(
                    Icons.notifications_off_outlined,
                    size: 72,
                    color: Colors.red[300]!.withOpacity(0.4),
                  ),
                  const SizedBox(height: 16),
                  const Text(
                    "No active alerts",
                    style: TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                      color: Colors.white,
                      letterSpacing: 1.1,
                    ),
                  ),
                  const SizedBox(height: 8),
                  const Text(
                    "All Pakistani cities are currently inside safe thresholds.",
                    style: TextStyle(color: Colors.white60, fontSize: 13),
                    textAlign: Center,
                  ),
                ],
              ),
            )
          : ListView.builder(
              padding: const EdgeInsets.all(12),
              itemCount: activeAlerts.length,
              itemBuilder: (context, index) {
                return const Card(
                  child: ListTile(
                    title: Text("Alert"),
                  ),
                );
              },
            ),
    );
  }
}
