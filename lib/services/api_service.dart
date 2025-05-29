// lib/services/api_service.dart
import 'dart:convert';
import 'package:http/http.dart' as http;



class ApiService {
  // 안드로이드 에뮬레이터: 10.0.2.2, iOS 시뮬레이터: localhost
  static const String _baseUrl = "http://113.198.66.75:10010";


  /// 이메일 회원가입
  static Future<Map<String, dynamic>> signUpEmail({
    required String email,
    required String username,
    required String password,
    required String phone,  // ✅ phone 파라미터 추가
  }) async {
    final uri = Uri.parse("$_baseUrl/auth/signup/email");
    final resp = await http.post(
      uri,
      headers: {"Content-Type": "application/json"},
      body: jsonEncode({
        "email": email,
        "username": username,
        "password": password,
        "phone": phone,  // ✅ 요청 바디에 포함
      }),
    );

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



  // 로그인된 유저의 email 기반으로 정보 조회
  static Future<Map<String, dynamic>> getUserByEmail(String email, String token) async {
    final uri = Uri.parse("$_baseUrl/users/by-email?email=$email"); // 👈 여기서 맞춰줌
    final resp = await http.get(
      uri,
      headers: {"Authorization": "Bearer $token"},
    );

    if (resp.statusCode == 200) {
      final data = jsonDecode(utf8.decode(resp.bodyBytes));
      return {"success": true, "data": data};
    } else {
      return {
        "success": false,
        "message": "사용자 정보 조회 실패 (${resp.statusCode})"
      };
    }
  }


  // ✅ 회원정보 수정 API 호출
  static Future<Map<String, dynamic>> updateUser({
    required String userId,
    required String token,
    String? password,
    String? phone,
  }) async {
    final uri = Uri.parse("$_baseUrl/users/$userId");

    // 전송할 필드만 포함
    final Map<String, dynamic> body = {};
    if (password != null && password.isNotEmpty) body['password'] = password;
    if (phone != null && phone.isNotEmpty) body['phone'] = phone;

    final resp = await http.put(
      uri,
      headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer $token",
      },
      body: jsonEncode(body),
    );

    if (resp.statusCode == 200) {
      final data = jsonDecode(utf8.decode(resp.bodyBytes));
      return {"success": true, "data": data};
    } else {
      final msg = jsonDecode(resp.body)['detail'] ?? '오류 발생';
      return {"success": false, "message": msg};
    }
  }




}
