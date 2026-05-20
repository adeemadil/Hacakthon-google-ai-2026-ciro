import 'package:flutter/material.dart';
import 'theme/ciro_theme.dart';
import 'screens/home_screen.dart';
import 'screens/agents_screen.dart';
import 'screens/alerts_screen.dart';
import 'screens/prediction_screen.dart';
import 'screens/live_map_screen.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const CiroApp());
}

class CiroApp extends StatelessWidget {
  const CiroApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'CIRO',
      debugShowCheckedModeBanner: false,
      theme: CiroTheme.darkTheme,
      initialRoute: '/',
      routes: {
        '/': (context) => const HomeScreen(),
        '/agents': (context) => const AgentsScreen(),
        '/alerts': (context) => const AlertsScreen(),
        '/prediction': (context) => const PredictionScreen(),
        '/map': (context) => const LiveMapScreen(),
      },
    );
  }
}
