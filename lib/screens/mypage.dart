import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:capstone_project/services/api_service.dart'; //

import 'edit_profile.dart';

class MyPage extends StatefulWidget {
  const MyPage({super.key});

  @override
  State<MyPage> createState() => _MyPageState();
}

class _MyPageState extends State<MyPage> {
  String userId = '';     // 🔹 추가됨
  String userName = '';
  String phoneNumber = '';
  String email = '';

  @override
  void initState() {
    super.initState();
    fetchUserInfo();
  }

  Future<void> fetchUserInfo() async {
    final prefs = await SharedPreferences.getInstance();
    final storedEmail = prefs.getString("email") ?? "";
    final token = prefs.getString("token") ?? "";

    if (storedEmail.isEmpty || token.isEmpty) {
      print("❌ 저장된 이메일 또는 토큰이 없습니다.");
      return;
    }

    final result = await ApiService.getUserByEmail(storedEmail, token);
    if (result["success"] == true) {
      final data = result["data"];
      setState(() {
        userId = data["user_id"] ?? "";
        userName = data["username"] ?? "";
        phoneNumber = data["phone"] ?? "";
        email = data["email"] ?? "";
      });
    } else {
      print("❌ 사용자 정보 로드 실패: ${result["message"]}");
    }
  }


  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        backgroundColor: Colors.white,
        foregroundColor: Colors.black,
        centerTitle: true,
        elevation: 0,
        title: const Text(
          '마이페이지',
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
      body: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // 프로필 정보
            Row(
              children: [
                const CircleAvatar(
                  radius: 30,
                  backgroundColor: Color(0xFFE0ECFF),
                  child: Icon(Icons.person, color: Colors.white, size: 40),
                ),
                const SizedBox(width: 16),
                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      '$userName님',  // ✅ userId로 표시
                      style: const TextStyle(
                        fontWeight: FontWeight.bold,
                        fontSize: 16,
                      ),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      phoneNumber,
                      style: const TextStyle(color: Colors.grey),
                    ),
                    Text(
                      email,
                      style: const TextStyle(color: Colors.grey),
                    ),
                  ],
                )
              ],
            ),
            const SizedBox(height: 30),

            // 회원 정보 변경
            InkWell(
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (_) => const EditProfilePage()),
                );
              },
              child: Row(
                children: const [
                  Icon(Icons.edit, color: Color(0xFF8CAEF2)),
                  SizedBox(width: 8),
                  Row(
                    children: [
                      Text(
                        '회원 정보 변경',
                        style: TextStyle(fontWeight: FontWeight.bold),
                      ),
                      SizedBox(width: 4),
                      Icon(Icons.chevron_right, color: Colors.grey, size: 18),
                    ],
                  ),
                ],
              ),
            ),
            const SizedBox(height: 30),

            // 최근 조회 내역
            Row(
              children: const [
                Icon(Icons.history, color: Color(0xFF8CAEF2)),
                SizedBox(width: 8),
                Text(
                  '최근 조회 내역',
                  style: TextStyle(fontWeight: FontWeight.bold),
                ),
              ],
            ),
            const SizedBox(height: 16),
            Container(
              height: 100,
              width: double.infinity,
              decoration: BoxDecoration(
                color: const Color(0xFFF8F8F8),
                borderRadius: BorderRadius.circular(12),
              ),
              alignment: Alignment.center,
              child: const Text(
                '최근 조회 내역이 없습니다.',
                style: TextStyle(color: Colors.grey),
              ),
            ),
          ],
        ),
      ),

      // 하단 네비게이션 바 (마이페이지 탭 활성화)
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
}
