import 'package:flutter/material.dart';

class MainPage extends StatelessWidget {
  const MainPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.symmetric(horizontal: 45),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.start,
            children: [
              const SizedBox(height: 80),

              // '전세 위험도 분석 받으러 가기'
              Row(
                mainAxisAlignment: MainAxisAlignment.start,
                children: [
                  Image.asset('assets/speaker.png', width: 20, height: 20),
                  const SizedBox(width: 4),
                  const Text(
                    '전세 위험도 분석 받으러 가기',
                    style: TextStyle(fontSize: 14, fontWeight: FontWeight.w500),
                  ),
                ],
              ),

              const SizedBox(height: 20),

              // 전세 사기 위험도 분석(탭 가능)
              GestureDetector(
                onTap: () {
                  Navigator.pushNamed(context, '/risk_analysis');
                },
                child: Container(
                  padding: const EdgeInsets.all(45),
                  decoration: BoxDecoration(
                    color: const Color(0xFF1A1754),
                    borderRadius: BorderRadius.circular(20),
                  ),
                  child: Row(
                    children: [
                      const Expanded(
                        child: Text(
                          '전세 사기\n위험도 분석',
                          style: TextStyle(
                            color: Colors.white,
                            fontSize: 25,
                            fontWeight: FontWeight.bold,
                            height: 1.3,
                          ),
                        ),
                      ),
                      Stack(
                        alignment: Alignment.center,
                        children: [
                          Image.asset(
                            'assets/main_circlechart.png',
                            width: 80,
                            height: 80,
                          ),
                          Positioned(
                            left: 0,
                            bottom: -5,
                            child: Image.asset(
                              'assets/main_search_icon.png',
                              width: 50,
                              height: 50,
                            ),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
              ),

              const SizedBox(height: 24),

              // 실거래가 분석
              GestureDetector(
                onTap: () {
                  Navigator.pushNamed(context, '/real_transaction_analysis');
                },
                child: Container(
                  padding: const EdgeInsets.all(30),
                  decoration: BoxDecoration(
                    color: const Color(0xFF83A5F6),
                    borderRadius: BorderRadius.circular(20),
                  ),
                  child: Row(
                    children: [
                      const Expanded(
                        child: Text(
                          '실거래가\n분석',
                          style: TextStyle(
                            color: Colors.white,
                            fontSize: 25,
                            fontWeight: FontWeight.bold,
                            height: 1.3,
                          ),
                        ),
                      ),
                      Image.asset(
                        'assets/map_icon.png',
                        width: 100,
                        height: 100,
                      ),
                    ],
                  ),
                ),
              ),


              const SizedBox(height: 24),

              // 전세 사기 예방법 가이드북
              GestureDetector(
                onTap: () {
                  Navigator.pushNamed(context, '/chat');
                },
                child: Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 16,
                    vertical: 18,
                  ),
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(15),
                    color: Colors.white,
                    boxShadow: [
                      BoxShadow(
                        color: Colors.black.withOpacity(0.05),
                        blurRadius: 8,
                        offset: const Offset(0, 4),
                      ),
                    ],
                  ),
                  child: Row(
                    children: [
                      Image.asset('assets/Light_bulb.png', width: 30, height: 30),
                      const SizedBox(width: 12),
                      const Expanded(
                        child: Text(
                          '전세 사기 예방법 가이드북',
                          style: TextStyle(
                            fontWeight: FontWeight.w600,
                            fontSize: 15,
                          ),
                        ),
                      ),
                      const Icon(Icons.arrow_forward_ios, size: 16),
                    ],
                  ),
                ),
              ),

              const SizedBox(height: 40),
            ],
          ),
        ),
      ),
      bottomNavigationBar: BottomNavigationBar(
        backgroundColor: Colors.white,
        currentIndex: 0,
        type: BottomNavigationBarType.fixed,
        selectedItemColor: const Color(0xFF010186),
        unselectedItemColor: Colors.grey,
        onTap: (index) {
          switch (index) {
            case 0:
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

  // 소형 카드 위젯(재사용)
  Widget _smallCard({
    required String title,
    required String iconPath,
    required VoidCallback onTap,
    Color? cardColor,
    bool isIconLeft = true,
    MainAxisAlignment titleAlignment = MainAxisAlignment.center,
    MainAxisAlignment iconAlignment = MainAxisAlignment.center,
  }) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        width: 150,
        height: 140,
        padding: const EdgeInsets.all(12),
        decoration: BoxDecoration(
          color: cardColor ?? const Color(0xFF1A1754),
          borderRadius: BorderRadius.circular(20),
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Row(
              mainAxisAlignment: titleAlignment,
              children: [
                Text(
                  title,
                  style: const TextStyle(
                    color: Colors.white,
                    fontWeight: FontWeight.w500,
                    fontSize: 14,
                  ),
                  textAlign: TextAlign.center,
                ),
              ],
            ),
            Row(
              mainAxisAlignment: iconAlignment,
              children: [
                if (isIconLeft)
                  Image.asset(iconPath, width: 80, height: 80),
                const SizedBox(width: 8),
                if (!isIconLeft)
                  Image.asset(iconPath, width: 80, height: 80),
              ],
            ),
          ],
        ),
      ),
    );
  }
}