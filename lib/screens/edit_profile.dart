import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class EditProfilePage extends StatelessWidget {
  const EditProfilePage({super.key});

  @override
  Widget build(BuildContext context) {
    final TextEditingController passwordController = TextEditingController();
    final TextEditingController confirmPasswordController = TextEditingController();
    final TextEditingController emailController = TextEditingController();
    final TextEditingController phoneController = TextEditingController();

    // TODO: 실제 로그인된 사용자 정보로 교체
    final String baseUrl = 'http://localhost:8000'; // 또는 클라우드 주소
    final String userId = 'abc12345';
    final String token = 'your_jwt_token_here'; // 필요 없다면 생략 가능

    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        backgroundColor: Colors.white,
        foregroundColor: Colors.black,
        centerTitle: true,
        elevation: 0,
        title: const Text(
          '회원 정보 변경',
          style: TextStyle(
            fontWeight: FontWeight.bold,
            color: Colors.black,
          ),
        ),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back_ios),
          onPressed: () => Navigator.pop(context),
        ),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 20),
        child: Column(
          children: [
            _buildLabeledField(
              label: '아이디',
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 14),
                decoration: BoxDecoration(
                  color: const Color(0xFFF4F4F4),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Text(
                  userId,
                  style: const TextStyle(color: Colors.grey),
                ),
              ),
            ),
            const SizedBox(height: 16),
            _buildLabeledField(
              label: '비밀번호',
              child: TextField(
                controller: passwordController,
                obscureText: true,
                decoration: const InputDecoration(
                  hintText: '비밀번호 입력',
                  border: OutlineInputBorder(),
                  isDense: true,
                ),
              ),
            ),
            const SizedBox(height: 16),
            _buildLabeledField(
              label: '',
              child: TextField(
                controller: confirmPasswordController,
                obscureText: true,
                decoration: const InputDecoration(
                  hintText: '비밀번호 재입력',
                  border: OutlineInputBorder(),
                  isDense: true,
                ),
              ),
            ),
            const SizedBox(height: 16),
            _buildLabeledField(
              label: '이메일',
              child: TextField(
                controller: emailController,
                decoration: const InputDecoration(
                  hintText: '이메일 입력',
                  border: OutlineInputBorder(),
                  isDense: true,
                ),
              ),
            ),
            const SizedBox(height: 16),
            _buildLabeledField(
              label: '휴대폰 번호',
              child: TextField(
                controller: phoneController,
                keyboardType: TextInputType.phone,
                decoration: const InputDecoration(
                  hintText: '010 - 0000 - 0000',
                  border: OutlineInputBorder(),
                  isDense: true,
                ),
              ),
            ),
            const SizedBox(height: 40),
            Center(
              child: ElevatedButton(
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF010186),
                  padding: const EdgeInsets.symmetric(horizontal: 40, vertical: 14),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(8),
                  ),
                ),
                onPressed: () async {
                  final password = passwordController.text;
                  final confirmPassword = confirmPasswordController.text;
                  final email = emailController.text;
                  final phone = phoneController.text;

                  if (password != confirmPassword) {
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(content: Text('비밀번호가 일치하지 않습니다.')),
                    );
                    return;
                  }

                  try {
                    final response = await http.put(
                      Uri.parse('$baseUrl/users/$userId'), // ✅ 여기 변경
                      headers: {
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer $token', // 필요시
                      },
                      body: jsonEncode({
                        'password': password,
                        'email': email,
                        'phone': phone,
                      }),
                    );

                    if (response.statusCode == 200) {
                      ScaffoldMessenger.of(context).showSnackBar(
                        const SnackBar(content: Text('정보가 성공적으로 수정되었습니다.')),
                      );
                      Navigator.pushNamed(context, '/my');
                    } else {
                      final msg = jsonDecode(response.body)['detail'];
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(content: Text('오류: $msg')),
                      );
                    }
                  } catch (e) {
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(content: Text('에러 발생: $e')),
                    );
                  }
                },

                child: const Text(
                  '수정완료',
                  style: TextStyle(
                    fontSize: 16,
                    color: Colors.white,
                  ),
                ),
              ),
            )
          ],
        ),
      ),
      bottomNavigationBar: BottomNavigationBar(
        backgroundColor: Colors.white,
        currentIndex: 3,
        type: BottomNavigationBarType.fixed,
        selectedItemColor: const Color(0xFF010186),
        unselectedItemColor: Colors.grey,
        onTap: (index) {
          switch (index) {
            case 0:
              Navigator.pushNamed(context, '/main');
              break;
            case 1:
              Navigator.pushNamed(context, '/risk_analysis');
              break;
            case 2:
              Navigator.pushNamed(context, '/contract_info_step');
              break;
            case 3:
              Navigator.pushNamed(context, '/my');
              break;
          }
        },
        items: const [
          BottomNavigationBarItem(
            icon: ImageIcon(AssetImage('assets/home_icon.png')),
            label: '홈',
          ),
          BottomNavigationBarItem(
            icon: ImageIcon(AssetImage('assets/analysis_solid_icon.png')),
            label: '위험도 분석',
          ),
          BottomNavigationBarItem(
            icon: ImageIcon(AssetImage('assets/chart_underbar.png')),
            label: '계약서 정보',
          ),
          BottomNavigationBarItem(
            icon: ImageIcon(AssetImage('assets/mypage_icon.png')),
            label: '마이페이지',
          ),
        ],
      ),
    );
  }

  Widget _buildLabeledField({required String label, required Widget child}) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.center,
      children: [
        SizedBox(
          width: 90,
          child: Align(
            alignment: Alignment.centerLeft,
            child: Text(
              label,
              style: const TextStyle(
                fontSize: 14,
                fontWeight: FontWeight.bold,
              ),
            ),
          ),
        ),
        Expanded(
          child: Padding(
            padding: const EdgeInsets.only(left: 8),
            child: child,
          ),
        ),
      ],
    );
  }
}
