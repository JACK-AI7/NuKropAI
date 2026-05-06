import 'package:hive/hive.dart';

class LocalFarmEngine {
  static final _box = Hive.box('farm_memory_box');

  // Track the unique logic you requested to build Farm Health
  static void saveAnalytics({required double soil, required double crop, required double water}) {
    _box.put('score_soil', soil);
    _box.put('score_crop', crop);
    _box.put('score_water', water);
  }

  static double getOverallHealth() {
    double soil = _box.get('score_soil', defaultValue: 70.0);
    double crop = _box.get('score_crop', defaultValue: 80.0);
    double water = _box.get('score_water', defaultValue: 60.0);
    return (soil + crop + water) / 3;
  }

  // Inject this automatically into our API to let GenAI remember.
  static String compileHistoryPrompt() {
    String events = _box.get('past_issues', defaultValue: "None");
    return "Prior Issues tracked locally: $events | Score: ${getOverallHealth()}%";
  }
}