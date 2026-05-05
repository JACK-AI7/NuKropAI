import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:animate_do/animate_do.dart';
import '../../../core/theme/app_theme.dart';
import '../../../core/api/scanner_service.dart';
import '../../../core/api/api_client.dart';
import '../../dashboard/presentation/settings_screen.dart';
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
  String _selectedModelType = 'auto';

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
    
    // Check backend connectivity but DON'T block
    try {
      final apiClient = ApiClient();
      final isHealthy = await apiClient.checkHealth();
      if (!isHealthy && mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Offline mode: Using on-device AI for analysis'),
            backgroundColor: Colors.blueGrey,
            duration: Duration(seconds: 2),
          )
        );
      }
    } catch (e) {
      debugPrint('Health check error: $e');
    }
    
    await _continueWithScan();
  }

  Future<void> _continueWithScan() async {
    try {
      final image = await _controller?.takePicture();
      if (image != null) {
        _processImage(image.path);
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Capture Error: $e')));
      }
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
      final result = await ref.read(scannerServiceProvider).scanImage(
            XFile(compressedPath),
            isSoil: widget.isSoil,
            modelType: _selectedModelType,
          );
      if (result != null && mounted) {
        Navigator.pushReplacement(
          context,
          MaterialPageRoute(builder: (_) => ResultsScreen(scan: result)),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Scan Failed: $e')));
      }
    } finally {
      if (mounted) setState(() => _isProcessing = false);
    }
  }

  String _getModelLabel() {
    switch (_selectedModelType) {
      case 'yolo11s': return 'YOLO11s';
      case 'agri_vision': return 'AgriVision';
      case 'agri_guard': return 'AgriGuard';
      case 'general': return 'General AI';
      default: return 'AI: Auto';
    }
  }

  Future<void> _showModelSelectionDialog() async {
    final availableModels = widget.isSoil ? ['auto', 'general'] : ['auto', 'yolo11s', 'agri_vision', 'agri_guard', 'general'];
    final labels = {
      'auto': 'Auto (Recommended)',
      'yolo11s': 'YOLO11 Small (Pests)',
      'agri_vision': 'AgriVision',
      'agri_guard': 'AgriGuard (Diseases)',
      'general': 'General AI',
    };

    await showDialog(
      context: context,
      builder: (ctx) => SimpleDialog(
        backgroundColor: const Color(0xFF1E293B),
        title: const Text('Select AI Model', style: TextStyle(color: Colors.white)),
        children: availableModels.map((model) => RadioListTile<String>(
          title: Text(labels[model] ?? model, style: const TextStyle(color: Colors.white)),
          value: model,
          groupValue: _selectedModelType,
          onChanged: (val) {
            if (val != null) {
              setState(() => _selectedModelType = val);
              Navigator.pop(ctx);
            }
          },
        )).toList(),
      ),
    );
  }

  @override
  void dispose() {
    _controller?.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    if (_controller == null || !_controller!.value.isInitialized) {
      return const Scaffold(backgroundColor: Colors.black, body: Center(child: CircularProgressIndicator()));
    }

    return Scaffold(
      backgroundColor: Colors.black,
      body: Stack(
        children: [
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
                _buildGlassTopBar(),
                _buildScanningFrame(),
                _buildGlassBottomControls(),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildGlassTopBar() {
    return Container(
      margin: const EdgeInsets.all(20),
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      decoration: AppColors.glassDecoration(radius: 20),
      child: Row(
        children: [
          IconButton(
            icon: const Icon(Icons.close_rounded, color: Colors.white),
            onPressed: () => Navigator.pop(context),
          ),
          const Expanded(
            child: Text(
              'NUKROPAI SCAN',
              textAlign: TextAlign.center,
              style: TextStyle(color: Colors.white, fontWeight: FontWeight.w900, letterSpacing: 2, fontSize: 12),
            ),
          ),
          TextButton(
            onPressed: _isProcessing ? null : _showModelSelectionDialog,
            child: Text(_getModelLabel(), style: const TextStyle(color: AppColors.accent, fontWeight: FontWeight.bold, fontSize: 10)),
          ),
        ],
      ),
    );
  }

  Widget _buildScanningFrame() {
    return Center(
      child: ZoomIn(
        child: Container(
          width: 280,
          height: 280,
          decoration: BoxDecoration(
            border: Border.all(color: Colors.white24, width: 1),
            borderRadius: BorderRadius.circular(40),
          ),
          child: Stack(
            children: [
              _buildCorner(0, null, top: true),
              _buildCorner(null, 0, top: true),
              _buildCorner(0, null, bottom: true),
              _buildCorner(null, 0, bottom: true),
              if (_isProcessing) _buildScanningLine(),
            ],
          ),
        ),
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
        width: 30,
        height: 30,
        decoration: BoxDecoration(
          border: Border(
            top: top ? const BorderSide(color: AppColors.accent, width: 3) : BorderSide.none,
            bottom: bottom ? const BorderSide(color: AppColors.accent, width: 3) : BorderSide.none,
            left: left != null ? const BorderSide(color: AppColors.accent, width: 3) : BorderSide.none,
            right: right != null ? const BorderSide(color: AppColors.accent, width: 3) : BorderSide.none,
          ),
          borderRadius: BorderRadius.only(
            topLeft: top && left != null ? const Radius.circular(15) : Radius.zero,
            topRight: top && right != null ? const Radius.circular(15) : Radius.zero,
            bottomLeft: bottom && left != null ? const Radius.circular(15) : Radius.zero,
            bottomRight: bottom && right != null ? const Radius.circular(15) : Radius.zero,
          ),
        ),
      ),
    );
  }

  Widget _buildScanningLine() {
    return FadeInDown(
      duration: const Duration(seconds: 2),
      child: Container(
        width: 280,
        height: 2,
        decoration: BoxDecoration(
          gradient: LinearGradient(
            colors: [Colors.transparent, AppColors.accent, Colors.transparent],
          ),
        ),
      ),
    );
  }

  Widget _buildGlassBottomControls() {
    return Container(
      margin: const EdgeInsets.only(bottom: 40, left: 40, right: 40),
      padding: const EdgeInsets.all(12),
      decoration: AppColors.glassDecoration(radius: 50),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
        children: [
          IconButton(
            icon: const Icon(Icons.photo_library_rounded, color: Colors.white, size: 28),
            onPressed: _isProcessing ? null : _pickFromGallery,
          ),
          GestureDetector(
            onTap: _captureAndScan,
            child: Container(
              padding: const EdgeInsets.all(16),
              decoration: const BoxDecoration(color: Colors.white, shape: BoxShape.circle),
              child: _isProcessing 
                ? const SizedBox(width: 32, height: 32, child: CircularProgressIndicator(color: AppColors.accent, strokeWidth: 3))
                : const Icon(Icons.camera_rounded, color: Colors.black, size: 32),
            ),
          ),
          IconButton(
            icon: const Icon(Icons.flash_on_rounded, color: Colors.white, size: 28),
            onPressed: () {},
          ),
        ],
      ),
    );
  }
}
