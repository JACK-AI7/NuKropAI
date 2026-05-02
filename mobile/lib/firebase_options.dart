import 'package:firebase_core/firebase_core.dart' show FirebaseOptions;
import 'package:flutter/foundation.dart'
    show defaultTargetPlatform, kIsWeb, TargetPlatform;

class DefaultFirebaseOptions {
  static FirebaseOptions get currentPlatform {
    if (kIsWeb) {
      throw UnsupportedError(
        'DefaultFirebaseOptions have not been configured for web, please use the Android platform.',
      );
    }
    switch (defaultTargetPlatform) {
      case TargetPlatform.android:
        return android;
      default:
        throw UnsupportedError(
          'DefaultFirebaseOptions are not supported for this platform.',
        );
    }
  }

  static const FirebaseOptions android = FirebaseOptions(
    apiKey: 'AIzaSyBUk0O_lf1wCThB1Ez8j7khqoEOIvTuBow',
    appId: '1:451623428043:android:38a30c00cc839dcc63a04e',
    messagingSenderId: '451623428043',
    projectId: 'sigma-gateway-477509-a4',
    storageBucket: 'sigma-gateway-477509-a4.firebasestorage.app',
  );
}
