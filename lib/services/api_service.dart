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


  //  챗봇 메시지 요청 함수
  static Future<String> fetchChatbotAnswer(String userMessage, {String source = "input"}) async {
    final url = Uri.parse("$_baseUrl/chatbot/chat");
    final response = await http.post(
      url,
      headers: {"Content-Type": "application/json"},
      body: jsonEncode({
        "message": userMessage,
        "source": source, // ✅ 이게 꼭 포함되어야 함
      }),
    );

    if (response.statusCode == 200) {
      // ✅ 한글 깨짐 방지
      final data = jsonDecode(utf8.decode(response.bodyBytes));
      return data['answer'] ?? '답변을 찾을 수 없습니다.';
    } else {
      return '서버 오류: ${response.statusCode}';
    }
  }


}
