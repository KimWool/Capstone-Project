import 'package:flutter/material.dart';
import 'package:capstone_project/screens/mainpage.dart';
import 'package:capstone_project/screens/sign_up.dart';

class LoginPage extends StatefulWidget {
  @override
  _LoginPageState createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final TextEditingController _idController = TextEditingController();
  final TextEditingController _passwordController = TextEditingController();

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
          Positioned(
            top: 391,
            left: 71,
            child: SizedBox(
              width: 259,
              height: 45,
              child: ElevatedButton(
                onPressed: () {
                  print("ID: ${_idController.text}");
                  print("PW: ${_passwordController.text}");
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (context) => const MainPage()),
                  );
                },
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
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => SignUpPage()),
                );
              },
              child: const Text(
                '회원가입',
                style: TextStyle(fontSize: 13),
              ),
            ),
          ),
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

  @override
  void dispose() {
    _idController.dispose();
    _passwordController.dispose();
    super.dispose();
  }
}
