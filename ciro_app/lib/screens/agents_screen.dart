import 'package:flutter/material.dart';

class AgentsScreen extends StatelessWidget {
  const AgentsScreen({super.key});

  final List<Map<String, dynamic>> agents = const [
    {
      "id": "Agent 1",
      "name": "Imagery Agent",
      "desc": "GeoGemma + GEE spatial imagery parser",
      "status": "PLANNED",
      "icon": Icons.satellite_alt
    },
    {
      "id": "Agent 2",
      "name": "Data Collector",
      "desc": "Open-Meteo, GloFAS, traffic, social & NDMA",
      "status": "ACTIVE",
      "icon": Icons.cloud_download_outlined
    },
    {
      "id": "Agent 3",
      "name": "ML Predictor",
      "desc": "XGBoost flood classifier + Prophet weather engine",
      "status": "ACTIVE",
      "icon": Icons.analytics_outlined
    },
    {
      "id": "Agent 4",
      "name": "Orchestrator",
      "desc": "Escalations, alert dispatch & safety routing",
      "status": "PLANNED",
      "icon": Icons.route_outlined
    },
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("CIRO AGENTS"),
      ),
      body: ListView.builder(
        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 16),
        itemCount: agents.length,
        itemBuilder: (context, index) {
          final agent = agents[index];
          final isActive = agent["status"] == "ACTIVE";

          return Card(
            margin: const EdgeInsets.only(bottom: 12),
            child: Padding(
              padding: const EdgeInsets.symmetric(vertical: 8),
              child: ListTile(
                leading: CircleAvatar(
                  backgroundColor: isActive ? Colors.green[900]!.withOpacity(0.2) : Colors.grey[900],
                  radius: 24,
                  child: Icon(
                    agent["icon"] as IconData,
                    color: isActive ? Colors.greenAccent : Colors.grey,
                  ),
                ),
                title: Text(
                  "${agent["id"]} (${agent["name"]})",
                  style: const TextStyle(
                    fontWeight: FontWeight.bold,
                    color: Colors.white,
                  ),
                ),
                subtitle: Padding(
                  padding: const EdgeInsets.only(top: 4.0),
                  child: Text(
                    agent["desc"] as String,
                    style: const TextStyle(color: Colors.white70),
                  ),
                ),
                trailing: Container(
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                  decoration: BoxDecoration(
                    color: isActive ? Colors.green[900]!.withOpacity(0.3) : Colors.grey[900],
                    border: Border.all(
                      color: isActive ? Colors.green : Colors.grey,
                    ),
                    borderRadius: BorderRadius.circular(4),
                  ),
                  child: Text(
                    agent["status"] as String,
                    style: TextStyle(
                      fontSize: 10,
                      fontWeight: FontWeight.bold,
                      color: isActive ? Colors.greenAccent : Colors.grey[400],
                    ),
                  ),
                ),
              ),
            ),
          );
        },
      ),
    );
  }
}
