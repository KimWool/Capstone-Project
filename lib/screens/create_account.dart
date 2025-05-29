import 'package:flutter/material.dart';
import 'package:capstone_project/services/api_service.dart'; // 내 서비스 위치 맞춰서 import

class CreateAccountPage extends StatefulWidget {
  @override
  _CreateAccountPageState createState() => _CreateAccountPageState();
}

class _CreateAccountPageState extends State<CreateAccountPage> {
  final TextEditingController idController         = TextEditingController();
  final TextEditingController pwController         = TextEditingController();
  final TextEditingController pwConfirmController  = TextEditingController();
  final TextEditingController emailController      = TextEditingController();
  final TextEditingController phoneController      = TextEditingController();

  bool _loading = false;
  String? _error;

  @override
  void dispose() {
    idController.dispose();
    pwController.dispose();
    pwConfirmController.dispose();
    emailController.dispose();
    phoneController.dispose();
    super.dispose();
  }

  Future<void> _onSignUpPressed() async {
    final id        = idController.text.trim();
    final pw        = pwController.text;
    final pwConfirm = pwConfirmController.text;
    final email     = emailController.text.trim();
    final phone     = phoneController.text.trim();  // ✅ 추가

    if (pw != pwConfirm) {
      setState(() => _error = "비밀번호가 일치하지 않습니다.");
      return;
    }
    if (id.isEmpty || pw.isEmpty || email.isEmpty || phone.isEmpty) {
      setState(() => _error = "아이디, 비밀번호, 이메일, 전화번호는 필수 입력입니다.");
      return;
    }

    setState(() {
      _loading = true;
      _error   = null;
    });

    try {
      final result = await ApiService.signUpEmail(
        email:    email,
        username: id,
        password: pw,
        phone:    phone, // ✅ 추가
      );

      if (result["success"] == true) {
        print("회원가입 ok");
        Navigator.pushReplacementNamed(context, "/login");
      } else {
        print("가입 실패");
        setState(() => _error = result["message"] as String);
      }
    } catch (e) {
      setState(() => _error = "네트워크 오류가 발생했습니다.");
    } finally {
      setState(() => _loading = false);
    }
  }


  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(/* ... */),
      body: SingleChildScrollView(
        padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 30),
        child: Column(
          children: [
            _buildInputFieldRow("아이디", idController, "아이디 입력"),
            _buildInputFieldRow("비밀번호", pwController, "비밀번호 입력", obscureText: true),
            _buildInputFieldRow("", pwConfirmController, "비밀번호 재입력", obscureText: true),
            _buildInputFieldRow("이메일", emailController, "이메일 입력", keyboardType: TextInputType.emailAddress),
            _buildInputFieldRow("휴대폰 번호", phoneController, "010-0000-0000", keyboardType: TextInputType.phone),

            if (_error != null)
              Padding(
                padding: const EdgeInsets.only(top: 8),
                child: Text(_error!, style: const TextStyle(color: Colors.red)),
              ),

            const SizedBox(height: 40),
            Center(
              child: ElevatedButton(
                onPressed: _loading ? null : _onSignUpPressed,
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF010186),
                  padding: const EdgeInsets.symmetric(horizontal: 40, vertical: 14),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                ),
                child: _loading
                    ? const SizedBox(
                  width: 20, height: 20,
                  child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white),
                )
                    : const Text("가입하기", style: TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold)),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildInputFieldRow(
      String label,
      TextEditingController controller,
      String hint, {
        bool obscureText      = false,
        TextInputType keyboardType = TextInputType.text,
      }) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 10),
      child: Row(
        children: [
          SizedBox(width: 100, child: Text(label, style: const TextStyle(fontSize: 16))),
          Expanded(
            child: TextField(
              controller: controller,
              obscureText: obscureText,
              keyboardType: keyboardType,
              decoration: InputDecoration(
                hintText: hint,
                isDense: true,
                contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 14),
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(6),
                  borderSide: const BorderSide(color: Color(0xFFE0E0E0)),
                ),
                focusedBorder: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(6),
                  borderSide: const BorderSide(color: Color(0xFF010186)),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
