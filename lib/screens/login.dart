import 'package:flutter/material.dart';
import 'package:capstone_project/screens/sign_up.dart';
import 'package:capstone_project/screens/mainpage.dart';


class LoginPage extends StatefulWidget {
  @override
  _LoginPageState createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  @override
  Widget build(BuildContext context) {
    return Container(
      // FigmaToFlutter로 생성한 UI 들어가는 곳
        width: 402,
        height: 874,
        decoration: BoxDecoration(
          color : Color.fromRGBO(255, 255, 255, 1),
        ),
        child: Stack(
            children: <Widget>[
              Positioned(
                  top: 391,
                  left: 71,
                  child: Container(
                      width: 259,
                      height: 45,
                      decoration: BoxDecoration(
                        borderRadius : BorderRadius.only(
                          topLeft: Radius.circular(5),
                          topRight: Radius.circular(5),
                          bottomLeft: Radius.circular(5),
                          bottomRight: Radius.circular(5),
                        ),
                        color : Color.fromRGBO(255, 255, 255, 1),
                        border : Border.all(
                          color: Color.fromRGBO(0, 0, 0, 1),
                          width: 1,
                        ),
                      )
                  )
              ),Positioned(
                  top: 401,
                  left: 177,
                  child: GestureDetector(
                    onTap: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(builder: (context) => const MainPage()),
                      );
                    },
                    child: Text(
                      '로그인',
                      textAlign: TextAlign.left,
                      style: TextStyle(
                        color: Color.fromRGBO(0, 0, 0, 1),
                        fontFamily: 'Noto Sans',
                        fontSize: 18,
                        letterSpacing: 0,
                        fontWeight: FontWeight.normal,
                        height: 1,
                      ),
                    ),
                  ),
                ),
              Positioned(
                  top: 261,
                  left: 71,
                  child: Container(
                      width: 259,
                      height: 45,
                      decoration: BoxDecoration(
                        borderRadius : BorderRadius.only(
                          topLeft: Radius.circular(5),
                          topRight: Radius.circular(5),
                          bottomLeft: Radius.circular(5),
                          bottomRight: Radius.circular(5),
                        ),
                        color : Color.fromRGBO(255, 255, 255, 1),
                        border : Border.all(
                          color: Color.fromRGBO(0, 0, 0, 1),
                          width: 1,
                        ),
                      )
                  )
              ),Positioned(
                  top: 275,
                  left: 87,
                  child: Text('아이디', textAlign: TextAlign.left, style: TextStyle(
                      color: Color.fromRGBO(0, 0, 0, 0.44999998807907104),
                      fontFamily: 'Noto Sans',
                      fontSize: 15,
                      letterSpacing: 0 /*percentages not used in flutter. defaulting to zero*/,
                      fontWeight: FontWeight.normal,
                      height: 1
                  ),)
              ),Positioned(
                  top: 307,
                  left: 71,
                  child: Container(
                      width: 259,
                      height: 45,
                      decoration: BoxDecoration(
                        borderRadius : BorderRadius.only(
                          topLeft: Radius.circular(5),
                          topRight: Radius.circular(5),
                          bottomLeft: Radius.circular(5),
                          bottomRight: Radius.circular(5),
                        ),
                        color : Color.fromRGBO(255, 255, 255, 1),
                        border : Border.all(
                          color: Color.fromRGBO(0, 0, 0, 1),
                          width: 1,
                        ),
                      )
                  )
              ),Positioned(
                  top: 320,
                  left: 87,
                  child: Text('비밀번호', textAlign: TextAlign.left, style: TextStyle(
                      color: Color.fromRGBO(0, 0, 0, 0.44999998807907104),
                      fontFamily: 'Noto Sans',
                      fontSize: 15,
                      letterSpacing: 0 /*percentages not used in flutter. defaulting to zero*/,
                      fontWeight: FontWeight.normal,
                      height: 1
                  ),)
              ),Positioned(
                  top: 481,
                  left: 46,
                  child: Container(
                      width: 156,
                      height: 42,
                      decoration: BoxDecoration(
                        image : DecorationImage(
                            image: AssetImage('assets/naver_logo1.png'),
                            fit: BoxFit.fitWidth
                        ),
                      )
                  )
              ),Positioned(
                  top: 481,
                  left: 202,
                  child: Container(
                      width: 156,
                      height: 42,
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
                  top: 481,
                  left: 217,
                  child: Container(
                      width: 41,
                      height: 41,
                      decoration: BoxDecoration(
                        image : DecorationImage(
                            image: AssetImage('assets/kakao_logo.png'),
                            fit: BoxFit.fitWidth
                        ),
                      )
                  )
              ),Positioned(
                  top: 493,
                  left: 258,
                  child: Text('카카오 로그인', textAlign: TextAlign.left, style: TextStyle(
                      color: Color.fromRGBO(58, 41, 41, 1),
                      fontFamily: 'Noto Sans',
                      fontSize: 13,
                      letterSpacing: 0 /*percentages not used in flutter. defaulting to zero*/,
                      fontWeight: FontWeight.normal,
                      height: 1
                  ),)
              ),Positioned(
                top: 448,
                left: 76,
                child: GestureDetector(
                  onTap: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(builder: (context) => SignUpPage()),
                    );
                  },
                  child: Text(
                    '회원가입',
                    textAlign: TextAlign.left,
                    style: TextStyle(
                      color: Color.fromRGBO(0, 0, 0, 1),
                      fontFamily: 'Noto Sans',
                      fontSize: 13,
                      letterSpacing: 0,
                      fontWeight: FontWeight.normal,
                      height: 1,
                    ),
                  ),
                ),
              ),

            ]
        )
    );
  }
}
