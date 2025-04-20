// lib/services/api_service.dart
import 'dart:convert';
import 'package:http/http.dart' as http;



class ApiService {
  // 안드로이드 에뮬레이터: 10.0.2.2, iOS 시뮬레이터: localhost
  static const String _baseUrl = "http://10.0.2.2:8000";

  /// 이메일 회원가입
  static Future<Map<String, dynamic>> signUpEmail({
    required String email,
    required String username,
    required String password,
  }) async {
    final uri = Uri.parse("$_baseUrl/auth/signup/email");
    final resp = await http.post(
      uri,
      headers: {"Content-Type": "application/json"},
      body: jsonEncode({
        "email": email,
        "username": username,
        "password": password,
      }),
    );

    //status code가 201또는 200이면 성공 처리
    final body = jsonDecode(resp.body) as Map<String, dynamic>;
    if (resp.statusCode == 201 || resp.statusCode == 200) {
      return {"success": true, "data": body};
    } else {
      return {"success": false, "message": body["detail"] ?? "Unknown error"};
    }
  }

  /// 로그인
  static Future<Map<String, dynamic>> login({
    required String email,
    required String password,
  }) async {
    final uri = Uri.parse("$_baseUrl/auth/login/email");
    final resp = await http.post(
      uri,
      headers: {"Content-Type": "application/json"},
      body: jsonEncode({
        "email": email,
        "password": password,
      }),
    );

    final body = jsonDecode(resp.body) as Map<String, dynamic>;
    if (resp.statusCode == 200) {
      return {"success": true, "data": body};
    } else {
      return {"success": false, "message": body["detail"] ?? "Invalid credentials"};
    }
  }
}
