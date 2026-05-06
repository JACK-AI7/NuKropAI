# Firebase Remote Config Setup for NuKropAI

## Overview

This document describes the Firebase Remote Config implementation for securely managing API keys and server URLs in the NuKropAI Flutter application.

## Why Firebase Remote Config?

**Security Benefits:**
- No hardcoded API keys in the source code
- Ability to rotate keys without app updates
- Remote disable/enable of APIs
- Environment-specific configurations (dev/staging/prod)
- A/B testing capabilities

**Operational Benefits:**
- Update server URLs without app store submissions
- Feature flagging for gradual rollouts
- Emergency kill switches
- Dynamic configuration updates

## Architecture

```
Flutter App
    ↓
Firebase Remote Config (Fetched on startup)
    ↓
Secure API Keys & URLs
    ↓
Backend Services (Hugging Face, Gemini, etc.)
```

## Implementation Details

### Files Modified

1. **pubspec.yaml** - Added `firebase_remote_config: ^5.1.4` dependency
2. **lib/core/config/remote_config_service.dart** - NEW: Remote Config service
3. **lib/main.dart** - Initialize Remote Config on app startup
4. **lib/core/config/constants.dart** - Use Remote Config values
5. **lib/core/ai/llm_service.dart** - Priority-based API key loading
6. **lib/core/api/websocket_service.dart** - Dynamic WebSocket URL
7. **lib/core/api/cloud_ai_service.dart** - Dynamic AI server URL

### Remote Config Service

Location: `lib/core/config/remote_config_service.dart`

```dart
class RemoteConfigService {
  static final FirebaseRemoteConfig _remoteConfig = FirebaseRemoteConfig.instance;

  static Future<void> initialize() async {
    await _remoteConfig.setConfigSettings(
      RemoteConfigSettings(
        fetchTimeout: const Duration(seconds: 15),
        minimumFetchInterval: const Duration(hours: 1),
      ),
    );
    await _remoteConfig.fetchAndActivate();
  }

  // Getters for all remote config values
  static String get apiKey => _remoteConfig.getString('nukrop_api_key');
  static String get baseUrl => _remoteConfig.getString('base_url');
  static String get wsUrl => _remoteConfig.getString('ws_url');
  static String get aiServerUrl => _remoteConfig.getString('ai_server_url');
  static String get geminiApiKey => _remoteConfig.getString('gemini_api_key');
}
```

### API Key Priority System

The LLM service implements a priority-based key loading system:

1. **Local Storage** (SharedPreferences) - User-set key in app settings
2. **Firebase Remote Config** - Fallback from remote configuration
3. **Default (Empty)** - Last resort (feature disabled)

```dart
String? storedKey = prefs.getString('gemini_api_key');
if (storedKey == null || storedKey.trim().isEmpty) {
  storedKey = RemoteConfigService.geminiApiKey;  // Remote Config fallback
}
if (storedKey == null || storedKey.trim().isEmpty) {
  storedKey = _defaultApiKey;  // Empty string
}
```

## Firebase Console Setup

### Step 1: Add Remote Config Parameters

Navigate to: **Firebase Console → Remote Config**

Add the following parameters:

| Parameter Name | Default Value | Description |
|---------------|---------------|-------------|
| `nukrop_api_key` | `dev-key-placeholder` | API key for NuKrop backend |
| `base_url` | `http://10.0.2.2:3000/api` | Backend server URL |
| `ws_url` | `ws://10.0.2.2:3000` | WebSocket server URL |
| `ai_server_url` | `https://jaswanthbreddy-nukropai-farming-ai.hf.space` | Hugging Face AI server |
| `gemini_api_key` | `''` | Google Gemini API key |

### Step 2: Publish Changes

Click **"Publish Changes"** to activate the configuration.

### Step 3: Environment-Specific Configs (Optional)

For different environments (dev/staging/prod):

1. Create separate Firebase projects
2. Use conditional values based on app instance
3. Or maintain separate parameter sets with naming conventions:
   - `dev_nukrop_api_key`
   - `prod_nukrop_api_key`

## Security Best Practices

### 1. Key Rotation

**Monthly Rotation:**
1. Generate new API keys
2. Update Firebase Remote Config
3. Monitor usage of old keys
4. Revoke old keys after 7 days

```bash
# Example: Update Remote Config via Firebase CLI
firebase remote-config:set --project=your-project-id
```

### 2. Rate Limiting

Configure on Hugging Face Space:
- Requests per minute: 60
- Requests per hour: 1000
- Concurrent connections: 10

### 3. Origin Restrictions

If using Firebase Hosting or Cloud Functions:
- Restrict API keys to specific domains
- Enable CORS only for trusted origins
- Use Firebase App Check for additional protection

### 4. Monitoring

Set up Firebase alerts for:
- Unusual fetch patterns
- Failed config fetches
- High error rates

```bash
# Monitor Remote Config usage
firebase remote-config:versions:list
```

## Development Workflow

### Local Development

For local testing without Firebase:

```dart
// In RemoteConfigService.initialize()
if (kDebugMode) {
  // Use local defaults for development
  await _remoteConfig.setDefaults(<String, dynamic>{
    'base_url': 'http://10.0.2.2:3000/api',
    'ai_server_url': 'http://10.0.2.2:3000',
    'ws_url': 'ws://10.0.2.2:3000',
    'gemini_api_key': '',
  });
}
```

### Testing

**Unit Test Example:**

```dart
test('RemoteConfigService returns correct values', () async {
  await RemoteConfigService.initialize();
  
  expect(RemoteConfigService.baseUrl, isNotEmpty);
  expect(RemoteConfigService.aiServerUrl, contains('hf.space'));
});
```

**Widget Test:**

```dart
testWidgets('App initializes with Remote Config', (tester) async {
  await tester.pumpWidget(const MyApp());
  await tester.pumpAndSettle();
  
  expect(find.text('NuKropAI'), findsOneWidget);
});
```

## Troubleshooting

### Issue: Remote Config values not updating

**Solution:**
1. Check fetch interval (minimum 1 hour in production)
2. Force fetch in debug mode:

```dart
await FirebaseRemoteConfig.instance.fetchAndActivate();
```

3. Clear app cache and restart

### Issue: API key not found

**Solution:**
1. Verify parameter name in Firebase Console
2. Check Remote Config fetch status:

```dart
final status = await FirebaseRemoteConfig.instance.ensureInitialized();
print('Fetch status: $status');
```

3. Check network connectivity
4. Verify Firebase project configuration

### Issue: WebSocket connection fails

**Solution:**
1. Verify `ws_url` parameter format
2. Check WebSocket server is running
3. Test with wscat:

```bash
wscat -c wss://your-server.com/ws/detect
```

## Performance Considerations

### Fetch Timing

- **Cold Start:** ~200-500ms
- **Cached Fetch:** ~50-100ms
- **Minimum Fetch Interval:** 1 hour (production)

### Caching Strategy

```dart
RemoteConfigSettings(
  fetchTimeout: const Duration(seconds: 15),
  minimumFetchInterval: const Duration(hours: 1),  // Production
  // minimumFetchInterval: const Duration(minutes: 5),  // Development
)
```

### Bundle Size Impact

- Firebase Remote Config SDK: ~150KB
- Additional network request on startup
- Minimal memory overhead

## Migration from Hardcoded Keys

### Before:

```dart
// constants.dart
static const String aiServerUrl = 'https://jaswanthbreddy-nukropai-farming-ai.hf.space';
```

### After:

```dart
// constants.dart
static String get aiServerUrl => RemoteConfigService.aiServerUrl;
```

### Migration Steps:

1. ✅ Add Firebase Remote Config dependency
2. ✅ Create RemoteConfigService
3. ✅ Initialize in main.dart
4. ✅ Update all hardcoded references
5. ✅ Configure Firebase Console
6. ✅ Test thoroughly
7. ✅ Deploy to production

## Advanced Features

### A/B Testing

```dart
// Define experiment variants
final experimentVariant = _remoteConfig.getString('ml_model_variant');

switch (experimentVariant) {
  case 'model_a':
    useModelA();
    break;
  case 'model_b':
    useModelB();
    break;
}
```

### Feature Flags

```dart
final isNewFeatureEnabled = _remoteConfig.getBool('enable_new_scanner');

if (isNewFeatureEnabled) {
  showNewScannerUI();
} else {
  showLegacyScannerUI();
}
```

### User Segmentation

```dart
// Set user properties
await FirebaseAnalytics.instance.setUserProperty(
  name: 'user_type',
  value: 'premium',
);

// Use in Remote Config conditions
// Different configs for different user segments
```

## Monitoring & Analytics

### Firebase Console Metrics

- **Active Users:** Track config fetch success rate
- **Parameter Usage:** Monitor which keys are accessed
- **Error Rate:** Track failed fetches
- **Latency:** Monitor fetch performance

### Custom Logging

```dart
void logConfigFetch(String parameter, String value) {
  FirebaseAnalytics.instance.logEvent(
    name: 'remote_config_fetch',
    parameters: {
      'parameter': parameter,
      'has_value': value.isNotEmpty,
    },
  );
}
```

## Best Practices Checklist

- [x] Use descriptive parameter names
- [x] Set appropriate default values
- [x] Implement error handling
- [x] Add timeout configurations
- [x] Test in debug mode first
- [x] Monitor production usage
- [x] Document parameter purposes
- [x] Set up alerts for failures
- [x] Regular key rotation schedule
- [x] Backup configuration before changes

## Resources

- [Firebase Remote Config Documentation](https://firebase.google.com/docs/remote-config)
- [FlFirebase Remote Config Flutter Plugin](https://pub.dev/packages/firebase_remote_config)
- [Firebase Security Best Practices](https://firebase.google.com/docs/projects/api-keys)

## Support

For issues or questions:
1. Check Firebase Console for configuration errors
2. Review Flutter debug logs
3. Verify Firebase project setup
4. Consult Firebase documentation

---

**Last Updated:** 2026-05-06  
**Version:** 1.0.0  
**Status:** Production Ready
