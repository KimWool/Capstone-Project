import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter_inappwebview/flutter_inappwebview.dart';

class AddressSearchPage extends StatefulWidget {
  const AddressSearchPage({super.key});

  @override
  State<AddressSearchPage> createState() => _AddressSearchPageState();
}

class _AddressSearchPageState extends State<AddressSearchPage> {
  final InAppLocalhostServer _localhostServer = InAppLocalhostServer();

  @override
  void initState() {
    super.initState();
    startServerAndLoad();
  }

  Future<void> startServerAndLoad() async {
    await _localhostServer.start();
    setState(() {});
  }

  @override
  void dispose() {
    _localhostServer.close();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("주소 검색")),
      body: _localhostServer.isRunning()
          ? InAppWebView(
        initialUrlRequest: URLRequest(
          url: WebUri("http://localhost:8080/assets/html/postcode.html"),
        ),
        initialOptions: InAppWebViewGroupOptions(
          crossPlatform: InAppWebViewOptions(
            javaScriptEnabled: true,
          ),
        ),
        onWebViewCreated: (controller) {
          controller.addJavaScriptHandler(
            handlerName: 'onComplete',
            callback: (args) {
              final data = jsonDecode(args.first);
              Navigator.pop(context, data);
            },
          );
        },
      )
          : const Center(child: CircularProgressIndicator()),
    );
  }
}
