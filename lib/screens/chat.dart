import 'package:flutter/material.dart';

class Chat extends StatefulWidget {
  const Chat({super.key});

  @override
  // 화면 상태 관리하는 _ChatPageState 연결
  State<Chat> createState() => _ChatPageState();
}

class _ChatPageState extends State<Chat> {
  final List<Map<String, dynamic>> chatList = [
    {'message': '안녕하세요! 무엇을 도와드릴까요?', 'isUser': false},
    {'message': '송파구 전세 분석해줘', 'isUser': true},
    {'message': '네, 송파구 전세 정보 분석을 시작할게요.', 'isUser': false},
  ];
  final TextEditingController _controller = TextEditingController();
  final ScrollController _scrollController = ScrollController();

  void _sendMessage(String text) {
    if (text.trim().isEmpty) return;

    setState(() {
      chatList.insert(0, {'message': text.trim(), 'isUser': true});
    });

    _controller.clear();
    _scrollToBottom();

    // 가상 AI 응답 (딜레이 후 추가)
    Future.delayed(const Duration(milliseconds: 500), () {
      setState(() {
        chatList.insert(0, {'message': 'AI의 응답입니다.', 'isUser': false});
      });
      _scrollToBottom();
    });
  }

  void _scrollToBottom() {
    Future.delayed(Duration(milliseconds: 100), () {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          0.0, // ListView를 reverse:true 로 만들었기 때문에 0이 가장 아래입니다
          duration: const Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      }
    });
  }

  void _onQuickQuestionSelected(String text) {
    _sendMessage(text);
  }

  Widget _buildQuickQuestionButton(String text) {
    return ElevatedButton(
      style: ElevatedButton.styleFrom(
        backgroundColor: Colors.white,
        foregroundColor: Colors.black87,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
        elevation: 1,
        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
      ),
      onPressed: () => _onQuickQuestionSelected(text),
      child: Text(text, style: TextStyle(fontSize: 13)),
    );
  }

  Widget _buildChatBubble(Map<String, dynamic> chat) {
    final isUser = chat['isUser'] as bool;
    final message = chat['message'];

    return Row(
      mainAxisAlignment:
      isUser ? MainAxisAlignment.end : MainAxisAlignment.start,
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
                bottomLeft:
                Radius.circular(isUser ? 12 : 0), // 사용자면 오른쪽 말풍선
                bottomRight:
                Radius.circular(isUser ? 0 : 12), // AI면 왼쪽 말풍선
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
        onTap: () => FocusScope.of(context).unfocus(), // 화면 터치 시 키보드 내리기
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

            // 추천 질문 버튼
            Container(
              color: Colors.grey[100],
              padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8),
              child: Wrap(
                spacing: 8,
                runSpacing: 8,
                children: [
                  _buildQuickQuestionButton("전세 사기 위험 분석"),
                  _buildQuickQuestionButton("등기부등본 보는 법"),
                  _buildQuickQuestionButton("건축물대장 해석하기"),
                ],
              ),
            ),

            // 메시지 입력창
            Container(
              padding:
              const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
              color: Colors.white,
              child: Row(
                children: [
                  Expanded(
                    child: TextField(
                      controller: _controller,
                      decoration: const InputDecoration(
                        hintText: "메시지를 입력하세요",
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.all(Radius.circular(20)),
                        ),
                        contentPadding:
                        EdgeInsets.symmetric(horizontal: 14, vertical: 10),
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






