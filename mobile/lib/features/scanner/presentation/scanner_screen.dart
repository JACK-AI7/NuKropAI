import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/theme/app_theme.dart';
import '../../../core/api/scanner_service.dart';
import '../../dashboard/presentation/settings_screen.dart';
import 'results_screen.dart';
import 'package:flutter_image_compress/flutter_image_compress.dart';
import 'package:path_provider/path_provider.dart';
import 'package:camera/camera.dart' as cam;
import 'package:image_picker/image_picker.dart';
import '../../../core/api/websocket_service.dart';
import 'dart:typed_data';
import 'package:image/image.dart' as img_lib;

class ScannerScreen extends ConsumerStatefulWidget {
  final bool isSoil;
  const ScannerScreen({super.key, this.isSoil = false});

  @override
  ConsumerState<ScannerScreen> createState() => _ScannerScreenState();
}

class _ScannerScreenState extends ConsumerState<ScannerScreen> {
  cam.CameraController? _controller;
  bool _isProcessing = false;
  final ImagePicker _picker = ImagePicker();
  final WebSocketService _wsService = WebSocketService();
  List<dynamic> _realtimeDetections = [];
  DateTime? _lastFrameTime;

  @override
  void initState() {
    super.initState();
    // Initialize scanner service (load on-device model & LLM)
    WidgetsBinding.instance.addPostFrameCallback((_) async {
      try {
        await ref.read(scannerServiceProvider).init();
        _wsService.connect();
        _wsService.stream.listen((data) {
          if (mounted) {
            setState(() {
              _realtimeDetections = data['detections'] ?? [];
            });
          }
        });
      } catch (e) {
        debugPrint('Scanner service init error: $e');
      }
    });
    _initCamera();
  }

  Future<void> _initCamera() async {
    try {
      final cameras = await cam.availableCameras();
      if (cameras.isEmpty) return;
      final camera = cameras.first;
      _controller = cam.CameraController(
        camera,
        cam.ResolutionPreset.high,
        enableAudio: false,
        imageFormatGroup: cam.ImageFormatGroup.jpeg,
      );
      await _controller!.initialize();
      
      // Start real-time stream
      _controller!.startImageStream((image) {
        if (_isProcessing) return;
        final now = DateTime.now();
        if (_lastFrameTime == null || now.difference(_lastFrameTime!).inMilliseconds > 500) {
          _lastFrameTime = now;
          _sendFrameToWS(image);
        }
      });

      if (mounted) setState(() {});
    } catch (e) {
      debugPrint('Camera init error: $e');
    }
  }

  Future<void> _sendFrameToWS(cam.CameraImage image) async {
    if (!_wsService.isConnected) return;
    try {
      // Fast conversion and compression for the server
      final img = img_lib.Image.fromBytes(
        width: image.width,
        height: image.height,
        bytes: image.planes[0].bytes.buffer,
        format: img_lib.Format.uint8,
      );
      
      // Rescale to 320px for faster inference
      final resized = img_lib.copyResize(img, width: 320);
      final jpeg = Uint8List.fromList(img_lib.encodeJpg(resized, quality: 50));
      
      _wsService.sendFrame(jpeg);
    } catch (e) {
      debugPrint('WS frame send error: $e');
    }
  }

  Future<void> _pickFromGallery() async {
    if (_isProcessing) return;
    try {
      final image = await _picker.pickImage(source: ImageSource.gallery);
      if (image != null) {
        await _processImage(image.path);
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Gallery error: $e')));
      }
    }
  }

  Future<void> _captureAndScan() async {
    if (_isProcessing) return;
    await _continueWithScan();
  }

  Future<void> _continueWithScan() async {
    try {
      final image = await _controller?.takePicture();
      if (image != null) {
        await _processImage(image.path);
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Capture Error: $e')));
      }
    }
  }

  Future<String> _compressImage(String path) async {
    try {
      final tempDir = await getTemporaryDirectory();
      final targetPath = '${tempDir.path}/${DateTime.now().millisecondsSinceEpoch}.jpg';
      final result = await FlutterImageCompress.compressAndGetFile(
        path,
        targetPath,
        quality: 60,
        keepExif: false,
      );
      return result?.path ?? path;
    } catch (e) {
      debugPrint('Compress error: $e');
      return path;
    }
  }

  Future<void> _processImage(String path) async {
    if (_isProcessing) return;
    setState(() => _isProcessing = true);

    try {
      final compressedPath = await _compressImage(path);
      final result = await ref.read(scannerServiceProvider).scanImage(
            XFile(compressedPath),
            isSoil: widget.isSoil,
          );

      if (mounted) {
        final aiSource = result['aiSource'] ?? 'local';
        String message;
        switch (aiSource) {
          case 'gemini_vision':
            message = 'Analysis: Cloud AI (Gemini)';
            break;
          case 'on_device':
            message = 'Analysis: On-device AI';
            break;
          default:
            message = 'Analysis complete';
        }
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(message)));
        Navigator.pushReplacement(
          context,
          MaterialPageRoute(builder: (_) => ResultsScreen(scan: result)),
        );
      }
    } catch (e) {
      if (mounted) {
        String errorMsg = e.toString();
        if (errorMsg.contains('Backend server unreachable') || errorMsg.contains('unavailable')) {
          errorMsg = 'Cannot connect to server. However, on-device analysis is still available offline.';
        }
        showDialog(
          context: context,
          builder: (ctx) => AlertDialog(
            title: const Text('Scan Failed'),
            content: Text(errorMsg),
            actions: [
              TextButton(
                onPressed: () => Navigator.pop(ctx),
                child: const Text('OK'),
              ),
              TextButton(
                onPressed: () {
                  Navigator.pop(ctx);
                  Navigator.push(context, MaterialPageRoute(builder: (_) => const SettingsScreen()));
                },
                child: const Text('Open Settings'),
              ),
            ],
          ),
        );
      }
    } finally {
      if (mounted) setState(() => _isProcessing = false);
    }
  }

  @override
  void dispose() {
    _controller?.stopImageStream();
    _controller?.dispose();
    _wsService.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    if (_controller == null || !_controller!.value.isInitialized) {
      return const Scaffold(
        backgroundColor: Colors.black,
        body: Center(child: CircularProgressIndicator(color: Colors.white)),
      );
    }

    return Scaffold(
      backgroundColor: Colors.black,
      body: Stack(
        children: [
          // Full screen camera
          Positioned.fill(
            child: FittedBox(
              fit: BoxFit.cover,
              child: SizedBox(
                width: _controller!.value.previewSize!.height,
                height: _controller!.value.previewSize!.width,
                child: cam.CameraPreview(_controller!),
              ),
            ),
          ),
          // Overlay
          SafeArea(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                // Header
                Padding(
                  padding: const EdgeInsets.all(20.0),
                  child: Row(
                    children: [
                      IconButton(
                        icon: const Icon(Icons.close, color: Colors.white, size: 30),
                        onPressed: () => Navigator.pop(context),
                      ),
                      const Spacer(),
                      Text(
                        widget.isSoil ? 'SOIL SCANNER' : 'PESTISCAN AI',
                        style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, letterSpacing: 2, fontSize: 16),
                      ),
                      const Spacer(),
                      IconButton(
                        icon: const Icon(Icons.settings, color: Colors.white70, size: 24),
                        onPressed: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const SettingsScreen())),
                      ),
                    ],
                  ),
                ),
                // Scanning frame & caption
                Column(
                  children: [
                    Container(
                      width: 280,
                      height: 280,
                      decoration: BoxDecoration(
                        border: Border.all(color: Colors.white.withOpacity(0.4), width: 2),
                        borderRadius: BorderRadius.circular(24),
                      ),
                      child: Stack(
                        children: [
                          if (_isProcessing)
                            Container(
                              decoration: BoxDecoration(
                                gradient: LinearGradient(
                                  begin: Alignment.topCenter,
                                  end: Alignment.bottomCenter,
                                  colors: [
                                    Colors.transparent,
                                    AppColors.accent.withOpacity(0.1),
                                    Colors.transparent,
                                  ],
                                ),
                              ),
                            ),
                          // Real-time Bounding Boxes
                          ..._realtimeDetections.map((det) {
                            final bbox = det['bbox'];
                            return Positioned(
                              left: (bbox[0] / 640) * 280,
                              top: (bbox[1] / 640) * 280,
                              width: ((bbox[2] - bbox[0]) / 640) * 280,
                              height: ((bbox[3] - bbox[1]) / 640) * 280,
                              child: Container(
                                decoration: BoxDecoration(
                                  border: Border.all(color: AppColors.accent, width: 2),
                                  borderRadius: BorderRadius.circular(4),
                                ),
                                child: Text(
                                  det['class'],
                                  style: const TextStyle(color: AppColors.accent, fontSize: 10, fontWeight: FontWeight.bold),
                                ),
                              ),
                            );
                          }).toList(),
                        ],
                      ),
                    ),
                    const SizedBox(height: 24),
                    Text(
                      _isProcessing ? 'Analyzing with AI...' : 'Align plant inside frame',
                      style: const TextStyle(color: Colors.white70, fontSize: 16),
                    ),
                  ],
                ),
                // Capture & gallery buttons
                Padding(
                  padding: const EdgeInsets.only(bottom: 48),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      IconButton(
                        icon: const Icon(Icons.photo_library, color: Colors.white, size: 32),
                        onPressed: _isProcessing ? null : _pickFromGallery,
                      ),
                      const SizedBox(width: 48),
                      GestureDetector(
                        onTap: _captureAndScan,
                        child: Container(
                          padding: const EdgeInsets.all(24),
                          decoration: BoxDecoration(
                            color: Colors.white,
                            shape: BoxShape.circle,
                            border: Border.all(color: AppColors.accent, width: 4),
                          ),
                          child: _isProcessing
                              ? const SizedBox(
                                  width: 32,
                                  height: 32,
                                  child: CircularProgressIndicator(strokeWidth: 3, color: AppColors.primary),
                                )
                              : const Icon(Icons.camera_alt, color: AppColors.background, size: 36),
                        ),
                      ),
                      const SizedBox(width: 48),
                      const SizedBox(width: 48), // Balance
                    ],
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
