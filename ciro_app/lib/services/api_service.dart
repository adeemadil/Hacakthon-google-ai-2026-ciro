import 'dart:convert';
import 'dart:developer' as developer;
import 'package:http/http.dart' as http;
import '../config/api_config.dart';

class ApiService {
  final http.Client _client;

  ApiService({http.Client? client}) : _client = client ?? http.Client();

  /// Retrieve the 8 monitored zones across Pakistan.
  Future<List<dynamic>> getZones() async {
    final url = Uri.parse('${ApiConfig.baseUrl}/api/v1/agent2/zones');
    try {
      final response = await _client.get(url);
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return data['zones'] ?? [];
      } else {
        developer.log('Failed to fetch zones. Status code: ${response.statusCode}');
        return [];
      }
    } catch (e) {
      developer.log('Error encountered while fetching zones: $e');
      return [];
    }
  }

  /// Trigger and fetch the 30-day prediction metrics for a specific zone.
  Future<Map<String, dynamic>> predict(String zoneId) async {
    final url = Uri.parse('${ApiConfig.baseUrl}/api/v1/agent3/predict/$zoneId');
    try {
      final response = await _client.post(url);
      if (response.statusCode == 200) {
        return json.decode(response.body) as Map<String, dynamic>;
      } else {
        developer.log('Failed to fetch predictions for $zoneId. Status code: ${response.statusCode}');
        return {};
      }
    } catch (e) {
      developer.log('Error encountered during predictions for $zoneId: $e');
      return {};
    }
  }
}
