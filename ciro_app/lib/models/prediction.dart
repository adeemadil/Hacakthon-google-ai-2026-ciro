class FloodPrediction {
  final String zoneId;
  final double floodRisk;
  final double heatRisk;
  final String confidence;

  FloodPrediction({
    required this.zoneId,
    required this.floodRisk,
    required this.heatRisk,
    required this.confidence,
  });

  factory FloodPrediction.fromJson(Map<String, dynamic> json) {
    return FloodPrediction(
      zoneId: json['zone_id'] ?? json['zone'] ?? '',
      floodRisk: (json['flood_risk'] ?? 0.0).toDouble(),
      heatRisk: (json['heat_risk'] ?? 0.0).toDouble(),
      confidence: json['confidence'] ?? '0.00',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'zone_id': zoneId,
      'flood_risk': floodRisk,
      'heat_risk': heatRisk,
      'confidence': confidence,
    };
  }
}
