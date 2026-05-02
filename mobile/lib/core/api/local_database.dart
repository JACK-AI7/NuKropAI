import 'dart:convert';
import 'dart:io';
import 'package:path/path.dart';
import 'package:path_provider/path_provider.dart';

class LocalDatabase {
  static File? _dbFile;

  static Future<void> _init() async {
    if (_dbFile != null) return;
    final dir = await getApplicationDocumentsDirectory();
    _dbFile = File(join(dir.path, 'nukropai_data.json'));
    if (!await _dbFile!.exists()) {
      await _dbFile!.writeAsString(jsonEncode({'scans': []}));
    }
  }

  static Future<void> saveScan(Map<String, dynamic> scan) async {
    await _init();
    final content = await _dbFile!.readAsString();
    final data = jsonDecode(content) as Map<String, dynamic>;
    final List scans = data['scans'] ?? [];
    scans.add({
      ...scan,
      'timestamp': DateTime.now().toIso8601String(),
    });
    await _dbFile!.writeAsString(jsonEncode(data));
  }

  static Future<List<Map<String, dynamic>>> getScans() async {
    await _init();
    final content = await _dbFile!.readAsString();
    final data = jsonDecode(content) as Map<String, dynamic>;
    final List scans = data['scans'] ?? [];
    return scans.map((e) => Map<String, dynamic>.from(e)).toList();
  }

  static Future<void> clear() async {
    await _init();
    await _dbFile!.writeAsString(jsonEncode({'scans': []}));
  }
}
