import 'dart:ui';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:animate_do/animate_do.dart';
import '../../../core/theme/app_theme.dart';
import '../data/auth_repository.dart';
import '../../../core/l10n/locale_provider.dart';
import '../../../core/l10n/app_localizations.dart';
import 'register_screen.dart';

class LoginScreen extends ConsumerStatefulWidget {
  const LoginScreen({super.key});

  @override
  ConsumerState<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends ConsumerState<LoginScreen> {
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  bool _isLoading = false;

  void _login() async {
    final email = _emailController.text.trim();
    final password = _passwordController.text.trim();

    if (email.isEmpty || password.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Please fill all fields')),
      );
      return;
    }

    setState(() => _isLoading = true);
    final success = await ref.read(authProvider.notifier).login(email, password);
    setState(() => _isLoading = false);

    if (!success && mounted) {
      final error = ref.read(authProvider).error ?? 'Login failed';
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(error)),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context) ?? AppLocalizations.instance;
    final currentLocale = ref.watch(localeProvider);

    return Scaffold(
      body: Stack(
        children: [
          // Background (Vegetables)
          Positioned.fill(
            child: Image.network(
              'https://images.unsplash.com/photo-1566385101042-1a0aa0c1268c?q=80&w=2000',
              fit: BoxFit.cover,
            ),
          ),
          Positioned.fill(child: Container(color: Colors.black.withOpacity(0.3))),
          
          SafeArea(
            child: SingleChildScrollView(
              padding: const EdgeInsets.symmetric(horizontal: 24),
              child: Column(
                children: [
                  const SizedBox(height: 20),
                  _buildLanguageSelector(ref, currentLocale),
                  const SizedBox(height: 40),
                  
                  // Logo
                  FadeInDown(
                    child: Column(
                      children: [
                        const Icon(Icons.eco_rounded, color: Color(0xFF4CAF50), size: 64),
                        const Text(
                          "NuKropAi",
                          style: TextStyle(color: Colors.white, fontSize: 42, fontWeight: FontWeight.w900),
                        ),
                        Text(
                          "Digital Farming Solutions in Practice",
                          style: TextStyle(color: Colors.white.withOpacity(0.8), fontSize: 13),
                        ),
                      ],
                    ),
                  ),
                  
                  const SizedBox(height: 60),
                  
                  // Glassmorphic Card
                  FadeInUp(
                    child: ClipRRect(
                      borderRadius: BorderRadius.circular(32),
                      child: BackdropFilter(
                        filter: ImageFilter.blur(sigmaX: 15, sigmaY: 15),
                        child: Container(
                          padding: const EdgeInsets.all(32),
                          decoration: BoxDecoration(
                            color: Colors.white.withOpacity(0.15),
                            borderRadius: BorderRadius.circular(32),
                            border: Border.all(color: Colors.white.withOpacity(0.2)),
                          ),
                          child: Column(
                            children: [
                              const Text(
                                "Welcome Back",
                                style: TextStyle(color: Colors.white, fontSize: 28, fontWeight: FontWeight.bold),
                              ),
                              const SizedBox(height: 32),
                              _buildField(l10n.email, Icons.mail_outline, _emailController),
                              const SizedBox(height: 20),
                              _buildField(l10n.password, Icons.lock_outline, _passwordController, isPassword: true),
                              const SizedBox(height: 32),
                              
                              // Sign In Button
                              SizedBox(
                                width: double.infinity,
                                child: ElevatedButton(
                                  onPressed: _isLoading ? null : _login,
                                  style: ElevatedButton.styleFrom(
                                    backgroundColor: const Color(0xFF4CAF50),
                                    foregroundColor: Colors.white,
                                    padding: const EdgeInsets.symmetric(vertical: 18),
                                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                                  ),
                                  child: _isLoading 
                                    ? const SizedBox(height: 20, width: 20, child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2))
                                    : const Text("SIGN IN", style: TextStyle(fontWeight: FontWeight.bold, letterSpacing: 1.5)),
                                ),
                              ),
                              
                              const SizedBox(height: 24),
                              _buildDivider(),
                              const SizedBox(height: 24),
                              
                              // Google Button
                              OutlinedButton(
                                onPressed: () => ref.read(authProvider.notifier).signInWithGoogle(),
                                style: OutlinedButton.styleFrom(
                                  side: BorderSide(color: Colors.white.withOpacity(0.3)),
                                  padding: const EdgeInsets.symmetric(vertical: 16),
                                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                                ),
                                child: Row(
                                  mainAxisAlignment: MainAxisAlignment.center,
                                  children: [
                                    const Icon(Icons.g_mobiledata, color: Colors.white, size: 28),
                                    const SizedBox(width: 12),
                                    const Text("Continue with Google", style: TextStyle(color: Colors.white, fontWeight: FontWeight.w500)),
                                  ],
                                ),
                              ),
                              
                              const SizedBox(height: 32),
                              
                              // Footer
                              GestureDetector(
                                onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const RegisterScreen())),
                                child: RichText(
                                  text: TextSpan(
                                    style: TextStyle(color: Colors.white.withOpacity(0.7), fontSize: 13),
                                    children: [
                                      const TextSpan(text: "Don't have an account? "),
                                      const TextSpan(text: "Sign Up", style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
                                    ],
                                  ),
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),
                    ),
                  ),
                  const SizedBox(height: 40),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildLanguageSelector(WidgetRef ref, Locale currentLocale) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.end,
      children: [
        _langButton(ref, 'en', '🇬🇧', currentLocale.languageCode == 'en'),
        const SizedBox(width: 8),
        _langButton(ref, 'hi', '🇮🇳', currentLocale.languageCode == 'hi'),
        const SizedBox(width: 8),
        _langButton(ref, 'te', '🇮🇳', currentLocale.languageCode == 'te'),
      ],
    );
  }

  Widget _langButton(WidgetRef ref, String code, String flag, bool isSelected) {
    return GestureDetector(
      onTap: () => ref.read(localeProvider.notifier).setLocale(code),
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
        decoration: BoxDecoration(
          color: isSelected ? const Color(0xFF4CAF50) : Colors.black.withOpacity(0.3),
          borderRadius: BorderRadius.circular(10),
          border: Border.all(color: Colors.white.withOpacity(0.1)),
        ),
        child: Text("$flag ${code.toUpperCase()}", style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 10, color: Colors.white)),
      ),
    );
  }

  Widget _buildField(String hint, IconData icon, TextEditingController controller, {bool isPassword = false}) {
    return Container(
      decoration: BoxDecoration(
        color: Colors.black.withOpacity(0.2),
        borderRadius: BorderRadius.circular(16),
      ),
      child: TextField(
        controller: controller,
        obscureText: isPassword,
        style: const TextStyle(color: Colors.white),
        decoration: InputDecoration(
          hintText: hint,
          hintStyle: TextStyle(color: Colors.white.withOpacity(0.4), fontSize: 15),
          prefixIcon: Icon(icon, color: Colors.white.withOpacity(0.6), size: 20),
          border: InputBorder.none,
          contentPadding: const EdgeInsets.symmetric(vertical: 18),
        ),
      ),
    );
  }

  Widget _buildDivider() {
    return Row(
      children: [
        Expanded(child: Divider(color: Colors.white.withOpacity(0.2))),
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 16),
          child: Text("OR", style: TextStyle(color: Colors.white.withOpacity(0.5), fontSize: 10, fontWeight: FontWeight.bold)),
        ),
        Expanded(child: Divider(color: Colors.white.withOpacity(0.2))),
      ],
    );
  }
}
