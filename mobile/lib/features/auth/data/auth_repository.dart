import 'package:firebase_auth/firebase_auth.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter/foundation.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:google_sign_in/google_sign_in.dart';

final firebaseAuthProvider = Provider<FirebaseAuth>((ref) => FirebaseAuth.instance);

final authRepositoryProvider = Provider((ref) {
  final firebaseAuth = ref.watch(firebaseAuthProvider);
  return AuthRepository(firebaseAuth);
});

class AuthRepository {
  final FirebaseAuth _firebaseAuth;
  AuthRepository(this._firebaseAuth);

  // Firebase Signup
  Future<UserCredential> signup(String email, String password, String name) async {
    try {
      final userCredential = await _firebaseAuth.createUserWithEmailAndPassword(
        email: email,
        password: password,
      );
      await userCredential.user?.updateDisplayName(name);
      await saveUser(userCredential.user!.uid, email, name);
      return userCredential;
    } catch (e) {
      rethrow;
    }
  }

  // Firebase Login
  Future<UserCredential> login(String email, String password) async {
    return await _firebaseAuth.signInWithEmailAndPassword(
      email: email,
      password: password,
    );
  }

  // Save User to Firestore
  Future<void> saveUser(String uid, String email, String name) async {
    try {
      await FirebaseFirestore.instance.collection('users').doc(uid).set({
        "name": name,
        "email": email,
        "createdAt": FieldValue.serverTimestamp(),
      });
    } catch (e) {
      debugPrint('Error saving user to Firestore: $e');
    }
  }

  Future<UserCredential?> signInWithGoogle(GoogleSignIn googleSignIn) async {
    final GoogleSignInAccount? googleUser = await googleSignIn.signIn();
    if (googleUser == null) return null;
    final GoogleSignInAuthentication googleAuth = await googleUser.authentication;
    final OAuthCredential credential = GoogleAuthProvider.credential(
      accessToken: googleAuth.accessToken,
      idToken: googleAuth.idToken,
    );
    final userCredential = await _firebaseAuth.signInWithCredential(credential);

    if (userCredential.user != null) {
      await saveUser(
        userCredential.user!.uid,
        userCredential.user!.email ?? '',
        userCredential.user!.displayName ?? 'User',
      );
    }

    return userCredential;
  }

  Future<void> signOut() async {
    await _firebaseAuth.signOut();
  }

  Future<bool> isEmailInUse(String email) async {
    try {
      // ignore: deprecated_member_use
      final fetchProviders = await _firebaseAuth.fetchSignInMethodsForEmail(email);
      return fetchProviders.isNotEmpty;
    } catch (e) {
      return false;
    }
  }
}

class AuthState {
  final bool isAuthenticated;
  final bool isLoading;
  final String? error;
  final Map<String, dynamic>? user;

  AuthState({this.isAuthenticated = false, this.isLoading = false, this.error, this.user});

  AuthState copyWith({bool? isAuthenticated, bool? isLoading, String? error, Map<String, dynamic>? user}) {
    return AuthState(
      isAuthenticated: isAuthenticated ?? this.isAuthenticated,
      isLoading: isLoading ?? this.isLoading,
      error: error ?? this.error,
      user: user ?? this.user,
    );
  }
}

final googleSignInProvider = Provider((ref) => GoogleSignIn());

final authProvider = StateNotifierProvider<AuthNotifier, AuthState>((ref) {
  return AuthNotifier(ref.read(authRepositoryProvider), ref.read(googleSignInProvider));
});

class AuthNotifier extends StateNotifier<AuthState> {
  final AuthRepository _repository;
  final GoogleSignIn _googleSignIn;

  AuthNotifier(this._repository, this._googleSignIn) : super(AuthState()) {
    checkAuth();
  }

  Future<void> checkAuth() async {
    state = state.copyWith(isLoading: true);
    try {
      final user = FirebaseAuth.instance.currentUser;
      if (user != null) {
        state = state.copyWith(
          isAuthenticated: true,
          isLoading: false,
          user: {
            'name': user.displayName,
            'email': user.email,
            'uid': user.uid,
          },
        );
      } else {
        state = state.copyWith(isAuthenticated: false, isLoading: false);
      }
    } catch (e) {
      debugPrint('Error checking auth: $e');
      state = state.copyWith(isAuthenticated: false, isLoading: false);
    }
  }

  Future<bool> login(String email, String password) async {
    state = state.copyWith(isLoading: true, error: null);
    try {
      final userCredential = await _repository.login(email, password);
      state = state.copyWith(
        isAuthenticated: true,
        isLoading: false,
        user: {
          'name': userCredential.user?.displayName,
          'email': userCredential.user?.email,
          'uid': userCredential.user?.uid,
        },
      );
      return true;
    } catch (e) {
      state = state.copyWith(isLoading: false, error: "Login failed: ${e.toString()}");
      return false;
    }
  }

  Future<void> register(String email, String password, String name) async {
    state = state.copyWith(isLoading: true, error: null);
    try {
      final userCredential = await _repository.signup(email, password, name);
      state = state.copyWith(
        isAuthenticated: true,
        isLoading: false,
        user: {
          'name': name,
          'email': email,
          'uid': userCredential.user?.uid,
        },
      );
    } catch (e) {
      state = state.copyWith(isLoading: false, error: "Registration failed: ${e.toString()}");
    }
  }

  Future<void> signInWithGoogle() async {
    state = state.copyWith(isLoading: true, error: null);
    try {
      final userCredential = await _repository.signInWithGoogle(_googleSignIn);
      if (userCredential != null) {
        state = state.copyWith(
          isAuthenticated: true,
          isLoading: false,
          user: {
            'name': userCredential.user?.displayName,
            'email': userCredential.user?.email,
            'uid': userCredential.user?.uid,
          },
        );
      } else {
        state = state.copyWith(isLoading: false);
      }
    } catch (e) {
      state = state.copyWith(isLoading: false, error: "Google Sign-In failed: ${e.toString()}");
    }
  }

  Future<void> logout() async {
    await _repository.signOut();
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('token');
    state = AuthState();
  }
}
