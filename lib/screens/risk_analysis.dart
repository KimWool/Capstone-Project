import 'package:flutter/material.dart';
import 'package:capstone_project/screens/address_search.dart';

class RiskAnalysisPage extends StatefulWidget {
  const RiskAnalysisPage({super.key});

  @override
  State<RiskAnalysisPage> createState() => _RiskAnalysisPageState();
}

class _RiskAnalysisPageState extends State<RiskAnalysisPage> {
  // 입력 컨트롤러
  final TextEditingController priceController = TextEditingController();
  final TextEditingController durationController = TextEditingController();
  final TextEditingController addressController = TextEditingController();
  final TextEditingController detailAddressController = TextEditingController();

  // 체크박스 상태
  bool isDurationUnknown = false;
  bool isDetailAddressUnknown = false;

  @override
  void dispose() {
    priceController.dispose();
    durationController.dispose();
    addressController.dispose();
    detailAddressController.dispose();
    super.dispose();
  }

  void _onAnalyzePressed() {
    final price = priceController.text;
    final duration = durationController.text;
    final address = addressController.text;
    final detailAddress = detailAddressController.text;

    print('전세금액: $price');
    print('계약기간: ${isDurationUnknown ? "모름" : duration}');
    print('주소: $address');
    print('상세주소: ${isDetailAddressUnknown ? "모름" : detailAddress}');

    Navigator.pushNamed(context, '/risk_result');
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
          '전세 위험도 분석',
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
              imagePath: 'assets/Money.png',
              label: '전세 금액을 입력해주세요',
              controller: priceController,
              hint: '',
              unit: '원',
            ),
            const SizedBox(height: 20),
            _buildInputSection(
              imagePath: 'assets/Calendar.png',
              label: '계약기간을 입력해주세요',
              controller: durationController,
              hint: '',
              unit: '개월',
              showCheckbox: true,
              checkboxValue: isDurationUnknown,
              onCheckboxChanged: (val) {
                setState(() {
                  isDurationUnknown = val ?? false;
                });
              },
              enabled: !isDurationUnknown,
            ),
            const SizedBox(height: 20),
            _buildInputSection(
              imagePath: 'assets/Location.png',
              label: '분석할 주소를 입력해주세요',
              controller: addressController,
              hint: '주소를 입력해주세요',
              enabled: false,
              // 키보드 입력 막기
              onTap: () async {
                final selected = await Navigator.push(
                  context,
                  MaterialPageRoute(builder: (_) => const AddressSearchPage()),
                );
                if (selected != null) {
                  setState(() {
                    addressController.text = selected;
                  });
                }
              },
            ),
            const SizedBox(height: 16),
            const Text(
              '상세 주소를 입력해주세요',
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 10),
            _buildInputField(
              controller: detailAddressController,
              hint: '동, 호수를 입력해주세요',
              enabled: !isDetailAddressUnknown,
            ),
            Row(
              children: [
                Checkbox(
                  value: isDetailAddressUnknown,
                  onChanged: (val) {
                    setState(() {
                      isDetailAddressUnknown = val ?? false;
                    });
                  },
                ),
                const Text('잘 모르겠어요'),
              ],
            ),
            const SizedBox(height: 30),
            Center(
              child: IntrinsicWidth(
                child: ElevatedButton(
                  onPressed: _onAnalyzePressed,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: const Color(0xFF010186),
                    padding: const EdgeInsets.symmetric(
                        vertical: 14, horizontal: 20),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                  ),
                  child: const Text(
                    '전세 사기 위험도 분석하기',
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
    VoidCallback? onTap,
  }) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            Image.asset(imagePath, width: 24, height: 24),
            const SizedBox(width: 8),
            Text(
              label,
              style: const TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
              ),
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
                onTap: onTap,
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
    VoidCallback? onTap,
  }) {
    return TextField(
      controller: controller,
      readOnly: !enabled, // 키보드 방지
      onTap: onTap, // 클릭 시 콜백 실행
      decoration: InputDecoration(
        hintText: hint,
        filled: true,
        fillColor: Colors.white,
        contentPadding:
        const EdgeInsets.symmetric(horizontal: 12, vertical: 14),
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
