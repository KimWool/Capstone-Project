import 'package:flutter/material.dart';

class MainPage extends StatefulWidget {
  const MainPage({super.key});

  @override
  State<MainPage> createState() => _MainPageState();
}

class _MainPageState extends State<MainPage> {
  @override
  Widget build(BuildContext context) {
    // Figma Flutter Generator Group17Widget - GROUP
    return Container(
      width: 347,
      height: 183,
      child: Stack(
        children: <Widget>[
          Positioned(
            top: 36,
            left: 0,
            child: Container(
              width: 347,
              height: 147,
              child: Stack(
                children: <Widget>[
                  Positioned(
                    top: 0,
                    left: 0,
                    child: Container(
                      width: 347,
                      height: 147,
                      decoration: BoxDecoration(
                        borderRadius: BorderRadius.circular(30),
                        color: Color.fromRGBO(26, 23, 84, 1),
                        border: Border.all(
                          color: Color.fromRGBO(0, 0, 0, 1),
                          width: 1,
                        ),
                      ),
                    ),
                  ),
                  Positioned(
                    top: 33,
                    left: 35,
                    child: Text(
                      '전세 사기\n위험도 분석',
                      textAlign: TextAlign.left,
                      style: TextStyle(
                        color: Colors.white,
                        fontFamily: 'Noto Sans',
                        fontSize: 30,
                        fontWeight: FontWeight.normal,
                        height: 1,
                      ),
                    ),
                  ),
                  Positioned(
                    top: 19,
                    left: 239,
                    child: Container(
                      width: 95,
                      height: 115,
                      child: Stack(
                        children: <Widget>[
                          Positioned(
                            top: 0,
                            left: 12,
                            child: Container(
                              width: 83,
                              height: 83,
                              decoration: BoxDecoration(
                                image: DecorationImage(
                                  image: AssetImage(
                                      'assets/images/main_circlechart.png'),
                                  fit: BoxFit.fitWidth,
                                ),
                              ),
                            ),
                          ),
                          Positioned(
                            top: 37,
                            left: 0,
                            child: Container(
                              width: 78,
                              height: 78,
                              decoration: BoxDecoration(
                                image: DecorationImage(
                                  image: AssetImage(
                                      'assets/main_search_icon.png'),
                                  fit: BoxFit.fitWidth,
                                ),
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
          Positioned(
            top: 1,
            left: 42,
            child: Text(
              '전세 위험도 분석 받으러 가기',
              textAlign: TextAlign.left,
              style: TextStyle(
                color: Colors.black,
                fontFamily: 'Noto Sans',
                fontSize: 15,
                fontWeight: FontWeight.normal,
                height: 1,
              ),
            ),
          ),
          Positioned(
            top: 0,
            left: 9,
            child: Container(
              width: 24,
              height: 21,
              decoration: BoxDecoration(
                image: DecorationImage(
                  image: AssetImage(
                      'assets/speaker.png'),
                  fit: BoxFit.fitWidth,
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
