import 'package:flutter/material.dart';
import 'package:capstone_project/screens/mainpage.dart';
import 'package:capstone_project/screens/sign_up.dart';
import 'package:capstone_project/services/api_service.dart';
import 'package:shared_preferences/shared_preferences.dart';

class LoginPage extends StatefulWidget {
  @override
  _LoginPageState createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final TextEditingController _idController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();

  bool _loading = false;
  String? _error;

  @override
  void dispose() {
    _idController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  Future<void> _onLoginPressed() async {
    final email = _idController.text.trim();
    final pw = _passwordController.text;

    if (email.isEmpty || pw.isEmpty) {
      setState(() => _error = "아이디와 비밀번호를 입력하세요.");
      return;
    }

    setState(() {
      _loading = true;
      _error = null;
    });

    final result = await ApiService.login(email: email, password: pw);
    print("🧪 로그인 응답: $result");

    setState(() {
      _loading = false;
    });

    if (result["success"] == true) {
      final data = result["data"]; // ✅ 실제 응답 본문
      final userId = data["user"]["user_id"].toString();
      final token = data["access_token"];

      final prefs = await SharedPreferences.getInstance();
      await prefs.setString("userId", userId);
      await prefs.setString("token", token);

      Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (_) => const MainPage()),
      );
    } else {
      setState(() => _error = result["message"] as String);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: Stack(
        children: [
          Positioned(
            top: 261,
            left: 71,
            child: SizedBox(
              width: 259,
              height: 45,
              child: TextField(
                controller: _idController,
                decoration: InputDecoration(
                  hintText: '아이디',
                  contentPadding: const EdgeInsets.symmetric(horizontal: 12),
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(5),
                  ),
                ),
              ),
            ),
          ),
          Positioned(
            top: 307,
            left: 71,
            child: SizedBox(
              width: 259,
              height: 45,
              child: TextField(
                controller: _passwordController,
                obscureText: true,
                decoration: InputDecoration(
                  hintText: '비밀번호',
                  contentPadding: const EdgeInsets.symmetric(horizontal: 12),
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(5),
                  ),
                ),
              ),
            ),
          ),
          if (_error != null)
            Positioned(
              top: 360,
              left: 71,
              child: SizedBox(
                width: 259,
                child: Text(
                  _error!,
                  style: const TextStyle(color: Colors.red),
                ),
              ),
            ),
          Positioned(
            top: 391,
            left: 71,
            child: SizedBox(
              width: 259,
              height: 45,
              child: _loading
                  ? const Center(child: CircularProgressIndicator())
                  : ElevatedButton(
                onPressed: _onLoginPressed,
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.white,
                  side: const BorderSide(color: Colors.black),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(5),
                  ),
                ),
                child: const Text(
                  '로그인',
                  style: TextStyle(color: Colors.black, fontSize: 18),
                ),
              ),
            ),
          ),
          Positioned(
            top: 448,
            left: 76,
            child: GestureDetector(
              onTap: () => Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => SignUpPage()),
              ),
              child: const Text(
                '회원가입',
                style: TextStyle(fontSize: 13),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
