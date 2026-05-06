import 'dart:async';
import 'dart:convert';
import 'dart:typed_data';
import 'package:web_socket_channel/web_socket_channel.dart';
import '../config/remote_config_service.dart';

class WebSocketService {
  WebSocketChannel? _channel;
  final _controller = StreamController<Map<String, dynamic>>.broadcast();
  bool _isConnected = false;

  Stream<Map<String, dynamic>> get stream => _controller.stream;
  bool get isConnected => _isConnected;

  void connect() {
    if (_isConnected) return;

    final wsUrl = RemoteConfigService.wsUrl;
    try {
      _channel = WebSocketChannel.connect(Uri.parse(wsUrl));
      _isConnected = true;

      _channel!.stream.listen(
        (data) {
          final decoded = jsonDecode(data);
          _controller.add(Map<String, dynamic>.from(decoded));
        },
        onError: (error) {
          _isConnected = false;
          print('WebSocket Error: $error');
          _reconnect();
        },
        onDone: () {
          _isConnected = false;
          print('WebSocket Closed');
        },
      );
    } catch (e) {
      _isConnected = false;
      print('WebSocket Connect Exception: $e');
    }
  }

  void sendFrame(Uint8List bytes) {
    if (_isConnected && _channel != null) {
      _channel!.sink.add(bytes);
    }
  }

  void _reconnect() {
    Future.delayed(const Duration(seconds: 5), () {
      if (!_isConnected) connect();
    });
  }

  void dispose() {
    _channel?.sink.close();
    _controller.close();
  }
}
