import 'package:flutter/material.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  final List<Map<String, String>> zones = const [
    {"name": "Karachi", "risk": "MEDIUM"},
    {"name": "Lahore", "risk": "LOW"},
    {"name": "Islamabad", "risk": "LOW"},
    {"name": "Peshawar", "risk": "MEDIUM"},
    {"name": "Quetta", "risk": "LOW"},
    {"name": "Multan", "risk": "HIGH"},
    {"name": "Faisalabad", "risk": "LOW"},
    {"name": "Muzaffarabad", "risk": "HIGH"},
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("CIRO"),
        actions: [
          IconButton(
            icon: const Icon(Icons.map_outlined),
            onPressed: () => Navigator.pushNamed(context, '/map'),
            tooltip: 'Live Map',
          ),
          IconButton(
            icon: const Icon(Icons.notifications_none),
            onPressed: () => Navigator.pushNamed(context, '/alerts'),
            tooltip: 'Alerts',
          ),
        ],
      ),
      drawer: Drawer(
        backgroundColor: const Color(0xFF0d0d1e),
        child: ListView(
          padding: EdgeInsets.zero,
          children: [
            DrawerHeader(
              decoration: BoxDecoration(
                color: Colors.red[700],
              ),
              child: const Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                mainAxisAlignment: MainAxisAlignment.end,
                children: [
                  Text(
                    'CIRO',
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 28,
                      fontWeight: FontWeight.bold,
                      letterSpacing: 1.5,
                    ),
                  ),
                  SizedBox(height: 4),
                  Text(
                    'Crisis Intelligence Dashboard',
                    style: TextStyle(
                      color: Colors.white70,
                      fontSize: 14,
                    ),
                  ),
                ],
              ),
            ),
            ListTile(
              leading: const Icon(Icons.dashboard, color: Colors.white),
              title: const Text('Home Dashboard', style: TextStyle(color: Colors.white)),
              onPressed: () => Navigator.pop(context),
            ),
            ListTile(
              leading: const Icon(Icons.smart_toy, color: Colors.white),
              title: const Text('Agents Status', style: TextStyle(color: Colors.white)),
              onPressed: () {
                Navigator.pop(context);
                Navigator.pushNamed(context, '/agents');
              },
            ),
            ListTile(
              leading: const Icon(Icons.warning_amber_rounded, color: Colors.white),
              title: const Text('Crisis Alerts', style: TextStyle(color: Colors.white)),
              onPressed: () {
                Navigator.pop(context);
                Navigator.pushNamed(context, '/alerts');
              },
            ),
            ListTile(
              leading: const Icon(Icons.analytics_outlined, color: Colors.white),
              title: const Text('30-Day Predictor', style: TextStyle(color: Colors.white)),
              onPressed: () {
                Navigator.pop(context);
                Navigator.pushNamed(context, '/prediction');
              },
            ),
            ListTile(
              leading: const Icon(Icons.map_sharp, color: Colors.white),
              title: const Text('Live Satellite Map', style: TextStyle(color: Colors.white)),
              onPressed: () {
                Navigator.pop(context);
                Navigator.pushNamed(context, '/map');
              },
            ),
          ],
        ),
      ),
      body: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Padding(
            padding: EdgeInsets.only(left: 16.0, top: 16.0, bottom: 8.0),
            child: Text(
              "Monitored Cities Risk Summary",
              style: TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.bold,
                color: Colors.grey,
                letterSpacing: 1.1,
              ),
            ),
          ),
          Expanded(
            child: GridView.builder(
              padding: const EdgeInsets.symmetric(horizontal: 12),
              gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                crossAxisCount: 2,
                childAspectRatio: 1.3,
                crossAxisSpacing: 8,
                mainAxisSpacing: 8,
              ),
              itemCount: zones.length,
              itemBuilder: (context, index) {
                final zone = zones[index];
                final isHigh = zone["risk"] == "HIGH";
                final isMedium = zone["risk"] == "MEDIUM";

                return Card(
                  child: Padding(
                    padding: const EdgeInsets.all(12.0),
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      crossAxisAlignment: CrossAxisAlignment.center,
                      children: [
                        Text(
                          zone["name"]!,
                          style: const TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                            color: Colors.white,
                          ),
                        ),
                        const SizedBox(height: 12),
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                          decoration: BoxDecoration(
                            color: isHigh
                                ? Colors.red[900]!.withOpacity(0.3)
                                : (isMedium ? Colors.amber[900]!.withOpacity(0.3) : Colors.green[900]!.withOpacity(0.3)),
                            border: Border.all(
                              color: isHigh ? Colors.red : (isMedium ? Colors.amber : Colors.green),
                            ),
                            borderRadius: BorderRadius.circular(4),
                          ),
                          child: Text(
                            "${zone["risk"]} RISK",
                            style: TextStyle(
                              fontSize: 11,
                              fontWeight: FontWeight.bold,
                              color: isHigh ? Colors.redAccent : (isMedium ? Colors.amberAccent : Colors.greenAccent),
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}
