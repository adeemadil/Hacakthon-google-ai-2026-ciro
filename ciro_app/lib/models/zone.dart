class KarachiZone {
  final String id;
  final String name;
  final String province;
  final double lat;
  final double lng;
  final String currentRisk;

  KarachiZone({
    required this.id,
    required this.name,
    required this.province,
    required this.lat,
    required this.lng,
    required this.currentRisk,
  });

  factory KarachiZone.fromJson(Map<String, dynamic> json) {
    return KarachiZone(
      id: json['id'] ?? '',
      name: json['name'] ?? '',
      province: json['province'] ?? '',
      lat: (json['lat'] ?? 0.0).toDouble(),
      lng: (json['lng'] ?? 0.0).toDouble(),
      currentRisk: json['current_risk'] ?? 'LOW',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'province': province,
      'lat': lat,
      'lng': lng,
      'current_risk': currentRisk,
    };
  }
}
