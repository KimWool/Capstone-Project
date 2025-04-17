import 'package:flutter/material.dart';
import 'package:capstone_project/screens/create_account.dart';



class SignUpPage extends StatefulWidget {
  @override
  _SignUpPageState createState() => _SignUpPageState();
}

class _SignUpPageState extends State<SignUpPage> {
  @override
  Widget build(BuildContext context) {
    return Container(
        width: 402,
        height: 874,
        decoration: BoxDecoration(
          color : Color.fromRGBO(255, 255, 255, 1),
        ),
        child: Stack(
            children: <Widget>[
              Positioned(
                  top: 218,
                  left: 72,
                  child: Container(
                      width: 252,
                      height: 49,

                      child: Stack(
                          children: <Widget>[
                            Positioned(
                                top: 0,
                                left: 0,
                                child: Container(
                                    width: 183.75001525878906,
                                    height: 49,
                                    decoration: BoxDecoration(
                                      image : DecorationImage(
                                          image: AssetImage('assets/naver_logo1.png'),
                                          fit: BoxFit.fitWidth
                                      ),
                                    )
                                )
                            ),Positioned(
                                top: 10,
                                left: 56.0400390625,
                                child: Container(
                                    width: 127.25999450683594,
                                    height: 26,
                                    decoration: BoxDecoration(
                                      color : Color.fromRGBO(3, 199, 90, 1),
                                    )
                                )
                            ),Positioned(
                                top: 0,
                                left: 179,
                                child: Container(
                                    width: 73,
                                    height: 49,
                                    decoration: BoxDecoration(
                                      borderRadius : BorderRadius.only(
                                        topLeft: Radius.circular(3),
                                        topRight: Radius.circular(3),
                                        bottomLeft: Radius.circular(3),
                                        bottomRight: Radius.circular(3),
                                      ),
                                      color : Color.fromRGBO(3, 199, 90, 1),
                                    )
                                )
                            ),Positioned(
                                top: 15,
                                left: 76.55999755859375,
                                child: Text('네이버로 시작하기', textAlign: TextAlign.left, style: TextStyle(
                                    color: Color.fromRGBO(255, 255, 255, 1),
                                    fontFamily: 'Noto Sans',
                                    fontSize: 15,
                                    letterSpacing: 0 /*percentages not used in flutter. defaulting to zero*/,
                                    fontWeight: FontWeight.normal,
                                    height: 1
                                ),)
                            ),
                          ]
                      )
                  )
              ),Positioned(
                  top: 275,
                  left: 72,
                  child: Container(
                      width: 252,
                      height: 49,

                      child: Stack(
                          children: <Widget>[
                            Positioned(
                                top: 0,
                                left: 0,
                                child: Container(
                                    width: 229.43283081054688,
                                    height: 49,
                                    decoration: BoxDecoration(
                                      borderRadius : BorderRadius.only(
                                        topLeft: Radius.circular(3),
                                        topRight: Radius.circular(3),
                                        bottomLeft: Radius.circular(3),
                                        bottomRight: Radius.circular(3),
                                      ),
                                      color : Color.fromRGBO(253, 220, 63, 1),
                                    )
                                )
                            ),Positioned(
                                top: 3,
                                left: 24,
                                child: Container(
                                    width: 42,
                                    height: 42,
                                    decoration: BoxDecoration(
                                      image : DecorationImage(
                                          image: AssetImage('assets/kakao_logo.png'),
                                          fit: BoxFit.fitWidth
                                      ),
                                    )
                                )
                            ),Positioned(
                                top: 15,
                                left: 76.208984375,
                                child: Text('카카오로 시작하기', textAlign: TextAlign.left, style: TextStyle(
                                    color: Color.fromRGBO(58, 41, 41, 1),
                                    fontFamily: 'Noto Sans',
                                    fontSize: 15,
                                    letterSpacing: 0 /*percentages not used in flutter. defaulting to zero*/,
                                    fontWeight: FontWeight.normal,
                                    height: 1
                                ),)
                            ),Positioned(
                                top: 0,
                                left: 214.38809204101562,
                                child: Container(
                                    width: 37.6119384765625,
                                    height: 49,
                                    decoration: BoxDecoration(
                                      borderRadius : BorderRadius.only(
                                        topLeft: Radius.circular(3),
                                        topRight: Radius.circular(3),
                                        bottomLeft: Radius.circular(3),
                                        bottomRight: Radius.circular(3),
                                      ),
                                      color : Color.fromRGBO(253, 220, 63, 1),
                                    )
                                )
                            ),
                          ]
                      )
                  )
              ),Positioned(
                  top: 335,
                  left: 72,
                  child: GestureDetector( // ← 추가: 전체 버튼을 감싸는 터치 감지기
                      onTap: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(builder: (context) => CreateAccountPage()),
                        );
                        },
                  child: Container(
                      width: 252,
                      height: 46,

                      child: Stack(
                          children: <Widget>[
                            Positioned(
                                top: 0,
                                left: 0,
                                child: Container(
                                    width: 252,
                                    height: 46,
                                    decoration: BoxDecoration(
                                      borderRadius : BorderRadius.only(
                                        topLeft: Radius.circular(10),
                                        topRight: Radius.circular(10),
                                        bottomLeft: Radius.circular(10),
                                        bottomRight: Radius.circular(10),
                                      ),
                                      color : Color.fromRGBO(255, 255, 255, 1),
                                      border : Border.all(
                                        color: Color.fromRGBO(0, 0, 0, 1),
                                        width: 1,
                                      ),
                                    )
                                )
                            ),Positioned(
                                top: 10.5,
                                left: 61,
                                child: Text('이메일로 가입하기', textAlign: TextAlign.left, style: TextStyle(
                                    color: Color.fromRGBO(0, 0, 0, 1),
                                    fontFamily: 'Noto Sans',
                                    fontSize: 18,
                                    letterSpacing: 0 /*percentages not used in flutter. defaulting to zero*/,
                                    fontWeight: FontWeight.normal,
                                    height: 1
                                ),
                                )
                            ),
                          ]
                      )
                  )
              ),
              ),
            ]
        )
    );
  }
}




