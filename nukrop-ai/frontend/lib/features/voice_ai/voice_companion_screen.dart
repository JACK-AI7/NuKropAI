import 'package:flutter/material.dart';
import 'package:lottie/lottie.dart';
import 'package:speech_to_text/speech_to_text.dart';
import 'package:flutter_tts/flutter_tts.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:nukrop_ai/core/local_sync.dart';

class VoiceCompanionScreen extends StatefulWidget {
  const VoiceCompanionScreen({super.key});
  @override
  State<VoiceCompanionScreen> createState() => _VoiceState();
}

class _VoiceState extends State<VoiceCompanionScreen> {
  final SpeechToText _stt = SpeechToText();
  final FlutterTts _tts = FlutterTts();
  bool isListening = false;
  String textRecognized = "Hold button to ask about your farm.";

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(title: const Text("NuKrop AI Companion"), backgroundColor: Colors.black),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Lottie.network(
              isListening ? "https://assets9.lottiefiles.com/packages/lf20_q7ufh9iz.json"
                          : "https://assets1.lottiefiles.com/packages/lf20_t2v9p5z4.json",
              height: 250,
              animate: true
            ),
            const SizedBox(height: 40),
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 20),
              child: Text(textRecognized, textAlign: TextAlign.center, style: const TextStyle(fontSize: 20, color: Colors.white70)),
            ),
            const Spacer(),
            GestureDetector(
              onLongPress: () async {
                bool available = await _stt.initialize();
                if(available) {
                  setState(() => isListening = true);
                  _stt.listen(onResult: (val) => setState(() => textRecognized = val.recognizedWords));
                }
              },
              onLongPressUp: () async {
                setState(() => isListening = false);
                _stt.stop();
                _queryFastApiEngine(textRecognized); // ⚡ Push payload seamlessly.
              },
              child: Container(
                margin: const EdgeInsets.only(bottom: 50),
                padding: const EdgeInsets.all(25),
                decoration: const BoxDecoration(shape: BoxShape.circle, gradient: LinearGradient(colors: [Color(0xFF0FCE7D), Color(0xFF0A9358)])),
                child: const Icon(Icons.mic_rounded, color: Colors.white, size: 40),
              ),
            )
          ],
        ),
      ),
    );
  }

  void _queryFastApiEngine(String message) async {
    setState(() => textRecognized = "NuKrop AI is analyzing locally and remotely...");
    final farmMemory = LocalFarmEngine.compileHistoryPrompt(); // 💡 YC-style Local Injection

    final baseUrl = dotenv.env['API_URL']!;
    var response = await http.post(
      Uri.parse("$baseUrl/chat/rural"),
      headers: {"Content-Type": "application/json"},
      body: jsonEncode({"message": message, "farm_history": farmMemory, "language": "Telugu/English"})
    );

    if (response.statusCode == 200) {
      var botReply = jsonDecode(response.body)["reply"];
      setState(() => textRecognized = botReply);
      await _tts.speak(botReply); // Talk back to the farmer
    } else {
       setState(() => textRecognized = "API Connection dropped. Showing local offline advice.");
    }
  }
}