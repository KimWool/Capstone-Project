import 'package:flutter/material.dart';

class RealTransactionAnalysisPage extends StatefulWidget {
  const RealTransactionAnalysisPage({super.key});

  @override
  State<RealTransactionAnalysisPage> createState() => _RealTransactionAnalysisPageState();
}

class _RealTransactionAnalysisPageState extends State<RealTransactionAnalysisPage> {
  final TextEditingController locationController = TextEditingController();
  final TextEditingController priceController = TextEditingController();

  bool isPriceUnknown = false;

  @override
  void dispose() {
    locationController.dispose();
    priceController.dispose();
    super.dispose();
  }

  void _onAnalyzePressed() {
    final location = locationController.text;
    final price = isPriceUnknown ? '모름' : priceController.text;

    print('입력한 동네: $location');
    print('입력한 전세 금액: $price');
    // TODO: 이후 실거래가 분석 로직 연결
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
          '실거래가 분석',
          style: TextStyle(fontWeight: FontWeight.bold),
        ),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back_ios),
          onPressed: () => Navigator.pop(context),
        ),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _buildInputSection(
              imagePath: 'assets/Home.png',
              label: '이사 가고 싶은\n동네를 입력하세요',
              controller: locationController,
              hint: 'ex) 서울시 송파구 잠실동',
            ),
            const SizedBox(height: 24),
            _buildInputSection(
              imagePath: 'assets/Money.png',
              label: '전세 금액을 입력해주세요',
              controller: priceController,
              hint: '',
              unit: '원',
              showCheckbox: true,
              checkboxValue: isPriceUnknown,
              onCheckboxChanged: (val) {
                setState(() {
                  isPriceUnknown = val ?? false;
                });
              },
              enabled: !isPriceUnknown,
            ),
            const SizedBox(height: 40),
            Center(
              child: IntrinsicWidth(
                child: ElevatedButton(
                  onPressed: _onAnalyzePressed,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: const Color(0xFF010186),
                    padding: const EdgeInsets.symmetric(vertical: 14, horizontal: 20),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                  ),
                  child: const Text(
                    '실거래가 분석하기',
                    style: TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                      color: Colors.white,
                    ),
                  ),
                ),
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

  Widget _buildInputSection({
    required String imagePath,
    required String label,
    required TextEditingController controller,
    required String hint,
    String? unit,
    bool showCheckbox = false,
    bool checkboxValue = false,
    ValueChanged<bool?>? onCheckboxChanged,
    bool enabled = true,
  }) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 10),
              child: Image.asset(imagePath, width: 40, height: 40),
            ),
            const SizedBox(width: 8),
            Text(
              label,
              style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
          ],
        ),
        const SizedBox(height: 10),
        Row(
          children: [
            Expanded(
              child: _buildInputField(
                controller: controller,
                hint: hint,
                enabled: enabled,
              ),
            ),
            if (unit != null) ...[
              const SizedBox(width: 8),
              Text(unit, style: const TextStyle(fontSize: 16)),
            ],
          ],
        ),
        if (showCheckbox)
          Row(
            children: [
              Checkbox(
                value: checkboxValue,
                onChanged: onCheckboxChanged,
              ),
              const Text('잘 모르겠어요'),
            ],
          ),
      ],
    );
  }

  Widget _buildInputField({
    required TextEditingController controller,
    required String hint,
    bool enabled = true,
  }) {
    return TextField(
      controller: controller,
      enabled: enabled,
      decoration: InputDecoration(
        hintText: hint,
        filled: true,
        fillColor: Colors.white,
        contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 14),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: const BorderSide(color: Color(0xFFE0E0E0)),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: const BorderSide(color: Color(0xFFE0E0E0)),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: const BorderSide(color: Color(0xFF010186)),
        ),
      ),
    );
  }
}
