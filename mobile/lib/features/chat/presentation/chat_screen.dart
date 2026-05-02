import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:animate_do/animate_do.dart';
import 'package:connectivity_plus/connectivity_plus.dart';
import '../../../core/theme/app_theme.dart';
import '../../../core/api/api_client.dart';

class ChatScreen extends ConsumerStatefulWidget {
  const ChatScreen({super.key});

  @override
  ConsumerState<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends ConsumerState<ChatScreen> {
  final _controller = TextEditingController();
  final List<Map<String, String>> _messages = [];
  bool _isLoading = false;

  Future<void> _sendMessage() async {
    if (_controller.text.isEmpty || _isLoading) return;

    final msg = _controller.text;
    _controller.clear();
    setState(() {
      _messages.add({'role': 'user', 'content': msg});
      _isLoading = true;
    });

    final List<ConnectivityResult> connectivity = await (Connectivity().checkConnectivity());
    final bool isOnline = connectivity.isNotEmpty && connectivity.first != ConnectivityResult.none;

    if (isOnline) {
      try {
        final api = ref.read(apiClientProvider);
        final response = await api.post('/ai/chat', data: {'message': msg});
        setState(() {
          _messages.add({'role': 'assistant', 'content': response.data['response']});
        });
      } catch (e) {
        _handleOfflineResponse(msg);
      } finally {
        setState(() => _isLoading = false);
      }
    } else {
      _handleOfflineResponse(msg);
      setState(() => _isLoading = false);
    }
  }

  void _handleOfflineResponse(String msg) {
    String response = "I'm currently in offline mode. I can help with basic agricultural tips. For complex disease analysis, please connect to the internet.";
    if (msg.toLowerCase().contains('water')) response = "Offline Tip: Most crops need 1-2 inches of water per week.";
    if (msg.toLowerCase().contains('soil')) response = "Offline Tip: Healthy soil should be crumbly and rich in organic matter.";
    
    setState(() {
      _messages.add({'role': 'assistant', 'content': response});
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('NuKropAi Assistant'),
        centerTitle: true,
        backgroundColor: Colors.transparent,
      ),
      body: Column(
        children: [
          Expanded(
            child: _messages.isEmpty 
              ? const Center(child: Text('Ask NuKropAi anything about farming!'))
              : ListView.builder(
                  padding: const EdgeInsets.all(20),
                  itemCount: _messages.length,
                  itemBuilder: (context, index) {
                    final msg = _messages[index];
                    final isUser = msg['role'] == 'user';
                    return FadeInUp(
                      child: Align(
                        alignment: isUser ? Alignment.centerRight : Alignment.centerLeft,
                        child: Container(
                          margin: const EdgeInsets.only(bottom: 16),
                          padding: const EdgeInsets.all(16),
                          constraints: BoxConstraints(maxWidth: MediaQuery.of(context).size.width * 0.8),
                          decoration: BoxDecoration(
                            color: isUser ? AppColors.primary : Colors.white10,
                            borderRadius: BorderRadius.circular(20),
                          ),
                          child: Text(msg['content']!, style: const TextStyle(color: Colors.white)),
                        ),
                      ),
                    );
                  },
                ),
          ),
          if (_isLoading) const LinearProgressIndicator(color: AppColors.primary),
          _buildInputArea(),
        ],
      ),
    );
  }

  Widget _buildInputArea() {
    return Container(
      padding: const EdgeInsets.all(20),
      color: Colors.black26,
      child: Row(
        children: [
          Expanded(
            child: TextField(
              controller: _controller,
              decoration: InputDecoration(
                hintText: 'Type a message...',
                filled: true,
                fillColor: Colors.white10,
                border: OutlineInputBorder(borderRadius: BorderRadius.circular(30), borderSide: BorderSide.none),
              ),
              onSubmitted: (_) => _sendMessage(),
            ),
          ),
          const SizedBox(width: 12),
          CircleAvatar(
            backgroundColor: AppColors.primary,
            child: IconButton(icon: const Icon(Icons.send, color: Colors.white), onPressed: _sendMessage),
          ),
        ],
      ),
    );
  }
}
