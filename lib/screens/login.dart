import 'package:flutter/material.dart';
import 'package:capstone_project/screens/mainpage.dart';
import 'package:capstone_project/screens/sign_up.dart';
import 'package:capstone_project/services/api_service.dart';


class LoginPage extends StatefulWidget {
  @override
  _LoginPageState createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final TextEditingController _idController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();

  bool _loading = false; //로그인 중 표시용
  String? _error; //에러 메시지

  @override
  void dispose() {
    _idController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  Future<void> _onLoginPressed() async {
    final email = _idController.text.trim();
    final pw    = _passwordController.text;

    if (email.isEmpty || pw.isEmpty) {
      setState(() => _error = "아이디와 비밀번호를 입력하세요.");
      return;
    }

    setState(() {
      _loading = true;
      _error   = null;
    });

    final result = await ApiService.login(email: email, password: pw);

    setState(() {
      _loading = false;
    });

    if (result["success"] == true) {
      // 로그인 성공 → MainPage 로 교체 이동
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
          // 에러 메시지
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
          // 로그인 버튼 or 로딩 인디케이터
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

          // 회원가입 링크
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

          // 나머지 SNS 로그인 버튼들 (생략 가능)
          Positioned(
            top: 481,
            left: 46,
            child: Container(
              width: 156,
              height: 42,
              decoration: const BoxDecoration(
                image: DecorationImage(
                  image: AssetImage('assets/naver_logo1.png'),
                  fit: BoxFit.fitWidth,
                ),
              ),
            ),
          ),
          Positioned(
            top: 481,
            left: 202,
            child: Container(
              width: 156,
              height: 42,
              decoration: BoxDecoration(
                borderRadius: BorderRadius.circular(3),
                color: const Color(0xFFFDDC3F),
              ),
            ),
          ),
          Positioned(
            top: 481,
            left: 217,
            child: Container(
              width: 41,
              height: 41,
              decoration: const BoxDecoration(
                image: DecorationImage(
                  image: AssetImage('assets/kakao_logo.png'),
                  fit: BoxFit.fitWidth,
                ),
              ),
            ),
          ),
          const Positioned(
            top: 493,
            left: 258,
            child: Text(
              '카카오 로그인',
              style: TextStyle(fontSize: 13, color: Color(0xFF3A2929)),
            ),
          ),
        ],
      ),
    );
  }
}