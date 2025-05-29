import 'package:flutter/material.dart';

class RealTransactionReportPage extends StatefulWidget {
  const RealTransactionReportPage({Key? key}) : super(key: key);

  @override
  _RealTransactionReportPageState createState() => _RealTransactionReportPageState();
}

class _RealTransactionReportPageState extends State<RealTransactionReportPage> {
  late Map<String, dynamic> result;
  late Map<String, dynamic> jeonseRates;
  late String location;
  late String selectedPropertyType;

  String resultLabel = '분석 중';
  String period = '';
  String avgPrice = '';
  String avgDeposit = '';
  String topType = '';
  String houseType = '';
  double topArea = 0.0;
  double userArea = 0.0;
  double depositPerM2 = 0.0;
  double estimatedDeposit = 0.0;

  double rate = 0.0;
  String risk = '';

  final TextEditingController _areaController = TextEditingController();

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    final args = ModalRoute.of(context)?.settings.arguments;
    if (args is Map<String, dynamic>) {
      result = args['result'] ?? {};
      jeonseRates = args['jeonseRates'] ?? {};
      selectedPropertyType = args['selectedPropertyType'] ?? '아파트';  // 기본값 아파트
      location = result['region'] ?? '알 수 없음';
      loadResultData();
    } else {
      result = {};
      selectedPropertyType = '아파트';
      location = '알 수 없음';
    }
  }

  void loadResultData() {
    print('result 전체 데이터: $result');
    print('selectedPropertyType: $selectedPropertyType');
    print('jeonserates keys: ${jeonseRates.keys}');

    setState(() {
      resultLabel = result['status'] ?? '분석불가';
      houseType = result['house_type'] ?? '';
      period = result['sale_period'] ?? '';
      depositPerM2 = (result['average_deposit_per_m2'] ?? 0).toDouble();
      double avgSale = (result['average_sale_per_m2'] ?? 0).toDouble();
      avgPrice = '${avgSale.toStringAsFixed(0)}만원/㎡';
      avgDeposit = '${depositPerM2.toStringAsFixed(0)}만원/㎡';
      topType = result['most_traded_name'] ?? '';
      topArea = (result['most_traded_area'] ?? 0).toDouble();

      // selectedPropertyType에 따라 rate, risk 가져오기
      String key = '';
      if (selectedPropertyType == '아파트') {
        key = '아파트_최근1년';
      } else if (selectedPropertyType == '연립다세대') {
        key = '연립다세대_최근1년';
      } else {
        key = '정보 없음';
      }

      if (jeonseRates.containsKey(key)) {
        var data = jeonseRates[key];
        rate = (data['rate'] ?? 0).toDouble();
        risk = data['risk'] ?? '정보 없음';
        resultLabel = risk;
      } else {
        rate = 0.0;
        risk = '정보 없음';
        resultLabel = '분석불가';
      }
    });
  }

  void calculateEstimatedDeposit() {
    setState(() {
      userArea = double.tryParse(_areaController.text) ?? 0.0;
      estimatedDeposit = depositPerM2 * userArea;
    });
  }

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
                        value: rate/100,
                        strokeWidth: 20,
                        backgroundColor: resultColor.withOpacity(0.2),
                        valueColor: AlwaysStoppedAnimation<Color>(resultColor),
                      ),
                    ),
                    Column(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Text(
                          resultLabel,
                          style: TextStyle(
                            fontSize: 42,
                            fontWeight: FontWeight.bold,
                            color: resultColor.withOpacity(0.8),
                          ),
                        ),
                        const SizedBox(height: 8),
                        Text(
                          '${rate.toStringAsFixed(1)}%',
                          style: TextStyle(
                            fontSize: 24,
                            fontWeight: FontWeight.w600,
                            color: resultColor.withOpacity(0.8),
                          ),
                        ),
                      ],
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
                          '• 평균 매매가: $avgPrice',
                          style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                        ),
                        Text(
                          '• 평균 보증금: $avgDeposit',
                          style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                        ),
                        Text(
                          '• 가장 많이 거래된 건물 이름: $topType',
                          style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                        ),
                        Text(
                          '• 가장 많이 거래된 면적대: $topArea',
                          style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 30),
                  Row(
                    children: const [
                      Icon(Icons.square_foot, color: Colors.blue),
                      SizedBox(width: 6),
                      Text(
                        '임차 주택 전용면적 입력',
                        style: TextStyle(fontWeight: FontWeight.bold),
                      ),
                    ],
                  ),
                  const SizedBox(height: 10),
                  Row(
                    children: [
                      Expanded(
                        child: TextField(
                          controller: _areaController,
                          keyboardType: TextInputType.number,
                          decoration: const InputDecoration(
                            border: OutlineInputBorder(),
                            labelText: '전용면적 (㎡)',
                            suffixText: '㎡',
                          ),
                          onSubmitted: (_) => calculateEstimatedDeposit(), // 엔터 입력 시 계산
                        ),
                      ),
                      const SizedBox(width: 10),
                      ElevatedButton(
                        onPressed: calculateEstimatedDeposit, // 버튼 클릭 시 계산
                        style: ElevatedButton.styleFrom(
                          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 16),
                          backgroundColor: Colors.indigo,
                        ),
                        child: const Text(
                          '계산',
                          style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 16),
                  if (estimatedDeposit > 0)
                    Text(
                      '👉 예상 적정 전세 보증금: ${estimatedDeposit.toStringAsFixed(0)}만원',
                      style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.indigo),
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
                  Text(
                    '해당 지역의 최근 실거래 데이터를 기반으로 분석한 결과, 평균 전세 보증금은 약 $avgDeposit입니다.\n'
                        '임차하려는 주택의 전용면적에 따라 실제 적정 전세가는 달라질 수 있으니, 보증금이 이보다 크게 높지 않도록 주의하세요',
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
