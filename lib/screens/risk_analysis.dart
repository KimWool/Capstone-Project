import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:capstone_project/screens/address_search.dart';

class RiskAnalysisPage extends StatefulWidget {
  const RiskAnalysisPage({super.key});

  @override
  State<RiskAnalysisPage> createState() => _RiskAnalysisPageState();
}

class _RiskAnalysisPageState extends State<RiskAnalysisPage> {
  final TextEditingController priceController = TextEditingController();
  final TextEditingController durationController = TextEditingController();
  final TextEditingController addressController = TextEditingController();
  final TextEditingController detailAddressController = TextEditingController();

  bool isDurationUnknown = false;
  bool isDetailAddressUnknown = false;

  Map<String, dynamic>? selectedAddressData;

  @override
  void dispose() {
    priceController.dispose();
    durationController.dispose();
    addressController.dispose();
    detailAddressController.dispose();
    super.dispose();
  }

  void _onAnalyzePressed() {
    final fullAddress = '${addressController.text} ${detailAddressController.text}';
    final bcode = selectedAddressData?['bcode'] ?? '없음';
    final mainNo = selectedAddressData?['mainAddressNo'] ?? '없음';
    final subNo = selectedAddressData?['subAddressNo'] ?? '없음';

    showDialog(
      context: context,
      builder: (_) => AlertDialog(
        backgroundColor: Colors.white,
        title: const Text('분석 요청 정보'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('주소: $fullAddress'),
            Text('법정동코드: $bcode'),
            Text('본번: $mainNo'),
            Text('부번: $subNo'),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () {
              Navigator.pop(context);
              Navigator.pushNamed(context, '/risk_result');
            },
            child: const Text('확인'),
          )
        ],
      ),
    );

  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        backgroundColor: Colors.white,
        foregroundColor: Colors.black,
        elevation: 0,
        centerTitle: true,
        title: const Text('전세 위험도 분석', style: TextStyle(fontWeight: FontWeight.bold)),
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
              hint: '주소를 선택해주세요',
              enabled: false,
              onTap: () async {
                final selected = await Navigator.push(
                  context,
                  MaterialPageRoute(builder: (_) => const AddressSearchPage()),
                );
                if (selected != null) {
                  setState(() {
                    selectedAddressData = selected;
                    addressController.text = selected['fullAddress'] ?? '';
                  });
                }
              },
            ),
            const SizedBox(height: 16),
            const Text(
              '상세 주소를 입력해주세요',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
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
                  '전세 사기 위험도 분석하기',
                  style: TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.bold,
                    color: Colors.white,
                  ),
                ),
              ),
            ),
          ],
        ),
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
            Text(label, style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
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
              Checkbox(value: checkboxValue, onChanged: onCheckboxChanged),
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
      readOnly: !enabled,
      onTap: onTap,
      decoration: InputDecoration(
        hintText: hint,
        filled: true,
        fillColor: Colors.white,
        contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 14),
        border: OutlineInputBorder(
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
