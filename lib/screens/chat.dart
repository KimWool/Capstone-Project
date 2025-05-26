// ✅ 수정 사항 반영: 2단계 버튼 구조 구현 + UX 개선

import 'package:flutter/material.dart';
import 'package:capstone_project/services/api_service.dart';

class Chat extends StatefulWidget {
  const Chat({super.key});

  @override
  State<Chat> createState() => _ChatPageState();
}

class _ChatPageState extends State<Chat> {
  final List<Map<String, dynamic>> chatList = [
    {'message': '안녕하세요! 무엇을 도와드릴까요?', 'isUser': false},
  ];

  final TextEditingController _controller = TextEditingController();
  final ScrollController _scrollController = ScrollController();

  // ✅ 주제 → 키워드 리스트 매핑
  final Map<String, List<String>> queryMap = {
    "부동산 계약 기초용어": [
      "임대인", "임차인", "차임", "보증금", "인도", "양도",
      "확정일자", "대항력", "우선변제권", "선순위 채권",
      "근저당권", "계약갱신 요구권", "묵시적 갱신", "전월세 상한제", "소액임차인 최우선 변제권"
    ],
    "계약하기 전 확인사항": [
      "임대인 정보 확인", "안전한 중개사무소 확인법", "적절한 중개보수료 확인법",
      "등기부등본", "주택 기본정보", "공인중개사 정보 확인"
    ],
    "계약 체결 단계에서 유의할 점": [
      "계약서 양식", "계약기간 및 임대료", "특약사항", "전세계약 체결 기간",
      "부동산 가계약", "임대인 정보"
    ],
    "계약 후 챙겨야 할 것": [
      "전입신고 및 확정일자", "전입신고 하는 법", "확정일자 받는 법",
      "전세보증금 반환보증", "전세보증금 반환 보증"
    ]
  };

  String? selectedCategory;

  void _sendMessage(String text, {String source = "input"}) async {
    if (text.trim().isEmpty) return;

    setState(() {
      chatList.insert(0, {'message': text.trim(), 'isUser': true});
      // selectedCategory = null;  // ❗ 주석 처리하여 하위 버튼 유지
    });

    _controller.clear();
    _scrollToBottom();

    final botResponse = await ApiService.fetchChatbotAnswer(text, source: source);

    setState(() {
      chatList.insert(0, {'message': botResponse, 'isUser': false});
    });

    _scrollToBottom();
  }

  void _scrollToBottom() {
    Future.delayed(const Duration(milliseconds: 100), () {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          0.0,
          duration: const Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      }
    });
  }

  void _onMainCategorySelected(String category) {
    setState(() {
      selectedCategory = category;
    });
  }

  Widget _buildQuickQuestionButton(String text, VoidCallback onPressed) {
    return ElevatedButton(
      style: ElevatedButton.styleFrom(
        backgroundColor: Colors.white,
        foregroundColor: Colors.black87,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
        elevation: 1,
        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
      ),
      onPressed: onPressed,
      child: Text(text, style: const TextStyle(fontSize: 13)),
    );
  }

  Widget _buildChatBubble(Map<String, dynamic> chat) {
    final isUser = chat['isUser'] as bool;
    final message = chat['message'];

    return Row(
      mainAxisAlignment: isUser ? MainAxisAlignment.end : MainAxisAlignment.start,
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        if (!isUser) ...[
          const CircleAvatar(
            radius: 16,
            backgroundColor: Colors.white,
            backgroundImage: AssetImage('assets/ajaping_icon.png'),
          ),
          const SizedBox(width: 8),
        ],
        Flexible(
          child: Container(
            padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
            margin: EdgeInsets.only(
              left: isUser ? 50 : 0,
              right: isUser ? 0 : 50,
            ),
            decoration: BoxDecoration(
              color: isUser ? Colors.yellow[600] : Colors.grey[300],
              borderRadius: BorderRadius.only(
                topLeft: const Radius.circular(12),
                topRight: const Radius.circular(12),
                bottomLeft: Radius.circular(isUser ? 12 : 0),
                bottomRight: Radius.circular(isUser ? 0 : 12),
              ),
            ),
            child: Text(
              message,
              style: const TextStyle(fontSize: 15),
            ),
          ),
        ),
      ],
    );
  }

  @override
  Widget build(BuildContext context) {
    final subKeywords = selectedCategory != null ? queryMap[selectedCategory!] ?? [] : [];

    return Scaffold(
      backgroundColor: const Color(0xfff9f9f9),
      resizeToAvoidBottomInset: true,
      appBar: AppBar(
        automaticallyImplyLeading: true,
        elevation: 0,
        backgroundColor: Colors.white,
        title: const Text(
          '챗봇 상담',
          style: TextStyle(fontWeight: FontWeight.bold),
        ),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back_ios),
          onPressed: () => Navigator.pop(context),
        ),
        centerTitle: true,
      ),
      body: GestureDetector(
        onTap: () => FocusScope.of(context).unfocus(),
        child: Column(
          children: [
            Expanded(
              child: ListView.separated(
                controller: _scrollController,
                reverse: true,
                padding: const EdgeInsets.all(14),
                itemBuilder: (context, index) {
                  return _buildChatBubble(chatList[index]);
                },
                separatorBuilder: (_, __) => const SizedBox(height: 10),
                itemCount: chatList.length,
              ),
            ),

            // ✅ 추천 질문 메인 카테고리
            Container(
              color: Colors.grey[100],
              padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8),
              child: Wrap(
                spacing: 8,
                runSpacing: 8,
                children: queryMap.keys.map((category) =>
                    _buildQuickQuestionButton(category, () => _onMainCategorySelected(category))).toList(),
              ),
            ),

            // ✅ 서브 키워드 버튼 표시 (가로 스크롤 대응)
            if (selectedCategory != null) ...[
              Container(
                height: 50,
                padding: const EdgeInsets.symmetric(horizontal: 10),
                color: Colors.grey[200],
                child: SingleChildScrollView(
                  scrollDirection: Axis.horizontal,
                  child: Row(
                    children: subKeywords.map((keyword) =>
                        Padding(
                          padding: const EdgeInsets.only(right: 8),
                          child: _buildQuickQuestionButton(keyword, () => _sendMessage(keyword, source: "button")),
                        )
                    ).toList(),
                  ),
                ),
              )
            ],

            // ✅ 메시지 입력창
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
              color: Colors.white,
              child: Row(
                children: [
                  Expanded(
                    child: TextField(
                      controller: _controller,
                      keyboardType: TextInputType.text,
                      textInputAction: TextInputAction.send,
                      enableSuggestions: true,
                      autocorrect: true,
                      decoration: const InputDecoration(
                        hintText: "메시지를 입력하세요",
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.all(Radius.circular(20)),
                        ),
                        contentPadding: EdgeInsets.symmetric(
                            horizontal: 14, vertical: 10),
                      ),
                    ),
                  ),
                  const SizedBox(width: 8),
                  IconButton(
                    icon: const Icon(Icons.send),
                    onPressed: () => _sendMessage(_controller.text),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}