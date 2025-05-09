import 'package:capstone_project/screens/risk_detail.dart';
import 'package:flutter/material.dart';

class RiskResultPage extends StatelessWidget {
  const RiskResultPage({super.key});

  @override
  Widget build(BuildContext context) {
    const int riskScore = 70; // 예시 점수
    const String userName = "김OO"; // 예시 사용자 이름

    final Color themeColor = getRiskColor(riskScore);

    final List<Map<String, dynamic>> riskDetails = [
      {
        'title': '소유권 관련 위험',
        'score': 80,
      },
      {
        'title': '기존 전세권 및 임차권 위험',
        'score': 60,
      },
      {
        'title': '근저당권 설정 위험',
        'score': 50,
      },
      {
        'title': '깡통 주택 위험도',
        'score': 65,
      },
      {
        'title': '건축물 적법성 위험',
        'score': 40,
      },
    ];

    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        backgroundColor: Colors.white,
        foregroundColor: Colors.black,
        elevation: 0,
        centerTitle: true,
        title: const Text(
          '전세 사기 리포트',
          style: TextStyle(fontWeight: FontWeight.bold, color: Colors.black),
        ),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back_ios),
          onPressed: () => Navigator.pop(context),
        ),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              '$userName님의 위험도 점수',
              style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 16),
            Center(
              child: Container(
                width: 280,
                height: 280,
                child: Stack(
                  alignment: Alignment.center,
                  children: [
                    SizedBox(
                      width: 240,
                      height: 240,
                      child: CircularProgressIndicator(
                        value: riskScore / 100,
                        strokeWidth: 20,
                        backgroundColor: themeColor.withOpacity(0.2),
                        valueColor: AlwaysStoppedAnimation<Color>(themeColor),
                      ),
                    ),
                    Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Text(
                          '$riskScore점',
                          style: TextStyle(
                            fontSize: 36,
                            fontWeight: FontWeight.bold,
                            color: themeColor,
                          ),
                        ),
                        const SizedBox(height: 8),
                      ],
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 30),
            Row(
              children: [
                Image.asset('assets/pencil_icon.png', width: 20, height: 20),
                const SizedBox(width: 8),
                const Text(
                  '위험도 분석 리포트',
                  style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                ),
              ],
            ),
            const SizedBox(height: 16),
            Column(
              children: riskDetails
                  .map((risk) => _buildRiskReportItem(
                title: risk['title'],
                score: risk['score'],
                themeColor: themeColor,
                onTap: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (_) => RiskDetailPage(
                        title: risk['title'],
                        score: risk['score'],
                        themeColor: themeColor,
                      ),
                    ),
                  );
                },
              ))
                  .toList(),
            ),
          ],
        ),
      ),
      bottomNavigationBar: BottomNavigationBar(
        backgroundColor: Colors.white,
        currentIndex: 1,
        type: BottomNavigationBarType.fixed,
        selectedItemColor: const Color(0xFF010186),
        unselectedItemColor: Colors.grey,
        onTap: (index) {
          switch (index) {
            case 0:
              Navigator.pushNamed(context, '/main');
              break;
            case 1:
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

  Widget _buildRiskReportItem({
    required String title,
    required int score,
    required Color themeColor,
    required VoidCallback onTap,
  }) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 24.0),
      child: InkWell(
        onTap: onTap,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                const Text('🤔 ', style: TextStyle(fontSize: 18)),
                Text(
                  title,
                  style: const TextStyle(
                    fontWeight: FontWeight.bold,
                    fontSize: 16,
                  ),
                ),
                const SizedBox(width: 6),
                Icon(
                  Icons.play_arrow,
                  color: themeColor,
                  size: 20,
                ),
              ],
            ),
            const SizedBox(height: 8),
            ClipRRect(
              borderRadius: BorderRadius.circular(10),
              child: LinearProgressIndicator(
                value: score / 100,
                minHeight: 14,
                backgroundColor: themeColor.withOpacity(0.2),
                valueColor: AlwaysStoppedAnimation<Color>(themeColor),
              ),
            ),
            const SizedBox(height: 12),
            Container(
              height: 80,
              decoration: BoxDecoration(
                color: themeColor.withOpacity(0.1),
                borderRadius: BorderRadius.circular(12),
              ),
              padding: const EdgeInsets.all(12),
              child: const Align(
                alignment: Alignment.centerLeft,
                child: Text(
                  '※ 리포트 내용은 샘플입니다.\n실제 데이터가 들어오면 여기에 설명이 들어갑니다.',
                  style: TextStyle(fontSize: 14),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  /// 점수에 따라 색상 결정
  static Color getRiskColor(int score) {
    if (score <= 20) return const Color(0xFF4CAF50); // 초록
    if (score <= 40) return const Color(0xFFFFC107); // 노랑
    if (score <= 60) return const Color(0xFFFFA9B3); // 연한 분홍
    return const Color(0xFFE15B5B); // 진한 분홍
  }
}
