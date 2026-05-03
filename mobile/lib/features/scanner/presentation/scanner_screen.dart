import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:animate_do/animate_do.dart';
import '../../../core/theme/app_theme.dart';
import '../../../core/api/scanner_service.dart';
import 'results_screen.dart';
import 'package:flutter_image_compress/flutter_image_compress.dart';
import 'package:path_provider/path_provider.dart';
import 'dart:io';
import 'package:camera/camera.dart' as cam;

import 'package:image_picker/image_picker.dart';

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

  @override
  void initState() {
    super.initState();
    _initCamera();
  }

  Future<void> _initCamera() async {
    final cameras = await cam.availableCameras();
    if (cameras.isEmpty) return;
    
    _controller = cam.CameraController(cameras[0], cam.ResolutionPreset.high);
    await _controller!.initialize();
    if (mounted) setState(() {});
  }

  Future<void> _pickFromGallery() async {
    final XFile? image = await _picker.pickImage(source: ImageSource.gallery);
    if (image != null) {
      _processImage(image.path);
    }
  }

  Future<void> _captureAndScan() async {
    if (_isProcessing) return;
    try {
      final image = await _controller?.takePicture();
      if (image != null) {
        _processImage(image.path);
      }
    } catch (e) {
      if (mounted) ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Capture Error: $e')));
    }
  }

  Future<String> _compressImage(String path) async {
    final tempDir = await getTemporaryDirectory();
    final targetPath = '${tempDir.path}/${DateTime.now().millisecondsSinceEpoch}.jpg';
    
    final result = await FlutterImageCompress.compressAndGetFile(
      path,
      targetPath,
      quality: 50,
    );
    
    return result?.path ?? path;
  }

  Future<void> _processImage(String path) async {
    if (_isProcessing) return;
    setState(() => _isProcessing = true);

    try {
      final compressedPath = await _compressImage(path);
      final result = await ref.read(scannerServiceProvider).scanImage(XFile(compressedPath), isSoil: widget.isSoil);
      if (result != null && mounted) {
        final source = result['aiSource'] as String?;
        if (source == 'mistral') {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('Analysis: Mistral AI (cloud)')),
          );
        } else if (source == 'ollama') {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('Analysis: local Ollama')),
          );
        }
        Navigator.pushReplacement(
          context,
          MaterialPageRoute(builder: (_) => ResultsScreen(scan: result)),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Analysis Error: $e')));
      }
    } finally {
      if (mounted) setState(() => _isProcessing = false);
    }
  }

  @override
  void dispose() {
    _controller?.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    if (_controller == null || !_controller!.value.isInitialized) {
      return const Scaffold(body: Center(child: CircularProgressIndicator()));
    }

    return Scaffold(
      backgroundColor: Colors.black,
      body: Stack(
        children: [
          // Full Screen Camera Preview
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
          
          SafeArea(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
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
                        widget.isSoil ? 'SOIL SCANNER' : 'PESTIDESCAN',
                        style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, letterSpacing: 2),
                      ),
                      const Spacer(),
                      const SizedBox(width: 48),
                    ],
                  ),
                ),
                
                // Improved Scanning Frame
                Center(
                  child: ZoomIn(
                    child: Container(
                      width: 300,
                      height: 300,
                      decoration: BoxDecoration(
                        border: Border.all(color: Colors.white.withOpacity(0.5), width: 1),
                        borderRadius: BorderRadius.circular(40),
                      ),
                      child: Stack(
                        children: [
                          // Corner Accents
                          _buildCorner(0, null, top: true),
                          _buildCorner(null, 0, top: true),
                          _buildCorner(0, null, bottom: true),
                          _buildCorner(null, 0, bottom: true),
                          
                          // Scanning Animation Line
                          if (_isProcessing)
                            _buildScanningLine(),
                        ],
                      ),
                    ),
                  ),
                ),
                
                Padding(
                  padding: const EdgeInsets.only(bottom: 40),
                  child: Column(
                    children: [
                      Text(
                        _isProcessing ? 'Analyzing with AI...' : 'Align plant or fruit inside the frame',
                        style: const TextStyle(color: Colors.white70),
                      ),
                      const SizedBox(height: 24),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          IconButton(
                            icon: const Icon(Icons.photo_library, color: Colors.white, size: 30),
                            onPressed: _isProcessing ? null : _pickFromGallery,
                          ),
                          const SizedBox(width: 40),
                          GestureDetector(
                            onTap: _captureAndScan,
                            child: Container(
                              padding: const EdgeInsets.all(20),
                              decoration: const BoxDecoration(
                                color: Colors.white,
                                shape: BoxShape.circle,
                              ),
                              child: _isProcessing 
                                ? const CircularProgressIndicator(color: AppColors.primary)
                                : const Icon(Icons.camera_alt, color: AppColors.background, size: 40),
                            ),
                          ),
                          const SizedBox(width: 40),
                          const SizedBox(width: 30), // Balancing
                        ],
                      ),
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
  Widget _buildCorner(double? left, double? right, {bool top = false, bool bottom = false}) {
    return Positioned(
      top: top ? 0 : null,
      bottom: bottom ? 0 : null,
      left: left,
      right: right,
      child: Container(
        width: 40,
        height: 40,
        decoration: BoxDecoration(
          border: Border(
            top: top ? const BorderSide(color: AppColors.accent, width: 4) : BorderSide.none,
            bottom: bottom ? const BorderSide(color: AppColors.accent, width: 4) : BorderSide.none,
            left: left != null ? const BorderSide(color: AppColors.accent, width: 4) : BorderSide.none,
            right: right != null ? const BorderSide(color: AppColors.accent, width: 4) : BorderSide.none,
          ),
          borderRadius: BorderRadius.only(
            topLeft: top && left != null ? const Radius.circular(20) : Radius.zero,
            topRight: top && right != null ? const Radius.circular(20) : Radius.zero,
            bottomLeft: bottom && left != null ? const Radius.circular(20) : Radius.zero,
            bottomRight: bottom && right != null ? const Radius.circular(20) : Radius.zero,
          ),
        ),
      ),
    );
  }

  Widget _buildScanningLine() {
    return FadeInDown(
      duration: const Duration(seconds: 2),
      child: Container(
        width: 300,
        height: 4,
        decoration: BoxDecoration(
          gradient: LinearGradient(
            colors: [
              AppColors.accent.withOpacity(0),
              AppColors.accent,
              AppColors.accent.withOpacity(0),
            ],
          ),
        ),
      ),
    );
  }
}
