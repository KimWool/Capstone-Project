import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart';

class AddressSearchPage extends StatefulWidget {
  const AddressSearchPage({super.key});

  @override
  State<AddressSearchPage> createState() => _AddressSearchPageState();
}

class _AddressSearchPageState extends State<AddressSearchPage> {
  late final WebViewController _webViewController;

  @override
  void initState() {
    super.initState();
    _webViewController = WebViewController()
      ..setJavaScriptMode(JavaScriptMode.unrestricted)
      ..clearCache()
      ..setNavigationDelegate(NavigationDelegate())
      ..addJavaScriptChannel(
        'onComplete',
        onMessageReceived: (message) async {
          final selectedAddress = message.message;
          print('받은 주소: $selectedAddress');

          await Future.delayed(Duration(milliseconds: 100));

          if(context.mounted) {
            Navigator.pop(context, selectedAddress);
          }
        },
      )
      ..loadFlutterAsset('assets/html/postcode.html');
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("주소 검색")),
      body: WebViewWidget(controller: _webViewController),
    );
  }
}
