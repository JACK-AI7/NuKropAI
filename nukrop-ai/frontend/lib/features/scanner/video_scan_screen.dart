import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:http/http.dart' as http;
import 'package:lucide_icons/lucide_icons.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';

class VideoScanScreen extends StatefulWidget {
  const VideoScanScreen({super.key});
  @override
  State<VideoScanScreen> createState() => _VideoScanState();
}

class _VideoScanState extends State<VideoScanScreen> {
  final ImagePicker _picker = ImagePicker();
  String _analysisStatus = "Pan your phone across the crop.";

  Future<void> _recordAndScanVideo() async {
    final XFile? video = await _picker.pickVideo(source: ImageSource.camera, maxDuration: const Duration(seconds: 4));
    if(video != null) {
      setState(() => _analysisStatus = "Uplinking to NuKrop Core Analytics...");

      final baseUrl = dotenv.env['API_URL']!;
      var request = http.MultipartRequest('POST', Uri.parse('$baseUrl/scan/video'));
      request.files.add(await http.MultipartFile.fromPath('file', video.path));

      var streamedResponse = await request.send();
      if(streamedResponse.statusCode == 200) {
        setState(() => _analysisStatus = "SCAN COMPLETE.\nConfidence logic rendered securely.");
      } else {
        setState(() => _analysisStatus = "AI Network overload. Retry.");
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0F172A),
      appBar: AppBar(title: const Text("AI Video Doctor", style: TextStyle(color: Colors.white)), backgroundColor: Colors.transparent),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
             Icon(LucideIcons.scanLine, size: 100, color: const Color(0xFF3B82F6).withOpacity(0.8)),
             const SizedBox(height: 30),
             Text(_analysisStatus, textAlign: TextAlign.center, style: const TextStyle(fontSize: 18, color: Colors.white70)),
             const SizedBox(height: 50),
             ElevatedButton.icon(
                style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFF3B82F6), padding: const EdgeInsets.all(20), shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15))),
                icon: const Icon(LucideIcons.camera, color: Colors.white),
                label: const Text("Capture 4 Sec Video Scan", style: TextStyle(color: Colors.white, fontSize: 18)),
                onPressed: _recordAndScanVideo,
             )
          ],
        )
      ),
    );
  }
}