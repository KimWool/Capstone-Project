import 'package:flutter/material.dart';

class RealTransactionReportPage extends StatelessWidget {
  final String location;
  final String resultLabel;
  final String period;
  final String avgPrice;
  final String avgDeposit;
  final String topType;

  const RealTransactionReportPage({
    this.location = '서울시 송파구 잠실동',
    this.resultLabel = '안전',
    this.period = '2024.10~2025.03',
    this.avgPrice = '1억 9,000만원',
    this.avgDeposit = '5,000만원',
    this.topType = '빌라 (45%)',
  });

  @override
  Widget build(BuildContext context) {
    final Color resultColor = getAnalysisColor(resultLabel);

    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        title: const Text(
          '실거래가 분석 리포트',
          style: TextStyle(
            fontSize: 20,
            fontWeight: FontWeight.bold,
            color: Colors.black,
          ),
        ),
        centerTitle: true,
        backgroundColor: Colors.white,
        foregroundColor: Colors.black,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back_ios),
          onPressed: () => Navigator.pop(context),
        ),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            Align(
              alignment: Alignment.centerLeft,
              child: Text(
                location,
                style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
              ),
            ),
            const SizedBox(height: 20),
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
                        value: 0,
                        strokeWidth: 20,
                        backgroundColor: resultColor.withOpacity(0.2),
                        valueColor: AlwaysStoppedAnimation<Color>(resultColor),
                      ),
                    ),
                    Text(
                      resultLabel,
                      style: TextStyle(
                        fontSize: 42,
                        fontWeight: FontWeight.bold,
                        color: resultColor.withOpacity(0.8),
                      ),
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 30),

            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 10),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Image.asset('assets/pencil_icon.png', width: 45, height: 45),
                      const SizedBox(width: 8),
                      const Text(
                        '실거래가 & 전세 보증금 분석',
                        style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                      ),
                    ],
                  ),
                  const SizedBox(height: 16),

                  Container(
                    width: double.infinity,
                    padding: const EdgeInsets.all(16),
                    decoration: BoxDecoration(
                      color: const Color(0xFFF5F5F5),
                      borderRadius: BorderRadius.circular(16),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          children: [
                            const Icon(Icons.edit_calendar, size: 20),
                            const SizedBox(width: 6),
                            Text(
                              period,
                              style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                            ),
                          ],
                        ),
                        const SizedBox(height: 10),
                        Text(
                          '• 평균 전세가: $avgPrice',
                          style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                        ),
                        Text(
                          '• 평균 보증금: $avgDeposit',
                          style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                        ),
                        Text(
                          '• 가장 많이 거래된 유형: $topType',
                          style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 30),

                  Row(
                    children: const [
                      Icon(Icons.check_circle_outline, color: Colors.green),
                      SizedBox(width: 6),
                      Text(
                        '적정 전세가/보증금',
                        style: TextStyle(fontWeight: FontWeight.bold),
                      ),
                    ],
                  ),
                  const SizedBox(height: 10),
                  const Text(
                    '적정 보증금  x만원',
                    style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 16),
                  ClipRRect(
                    borderRadius: BorderRadius.circular(16),
                    child: LinearProgressIndicator(
                      value: 0.7,
                      minHeight: 12,
                      backgroundColor: resultColor.withOpacity(0.2),
                      valueColor: AlwaysStoppedAnimation<Color>(resultColor),
                    ),
                  ),
                  const SizedBox(height: 12),
                  const Text(
                    '이 지역 평균 보증금은 XX만원입니다.\n가급적 XX만원 이하로 설정하세요.',
                    style: TextStyle(fontWeight: FontWeight.bold),
                  ),
                ],
              ),
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

  Color getAnalysisColor(String label) {
    switch (label) {
      case '안전':
        return const Color(0xFF4CAF50);
      case '주의':
        return const Color(0xFFFFC107);
      case '위험':
      default:
        return const Color(0xFFE15B5B);
    }
  }
}
