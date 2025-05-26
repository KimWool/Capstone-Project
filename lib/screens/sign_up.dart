import 'package:flutter/material.dart';
import 'package:capstone_project/screens/create_account.dart';

class SignUpPage extends StatefulWidget {
  @override
  _SignUpPageState createState() => _SignUpPageState();
}

class _SignUpPageState extends State<SignUpPage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold( // Scaffold로 감싸기
      backgroundColor: Colors.white,
      body: Container(
        width: 402,
        height: 874,
        decoration: BoxDecoration(
          color: Color.fromRGBO(255, 255, 255, 1),
        ),
        child: Stack(
          children: <Widget>[
            // 다른 위젯들이 여기 올 수 있음

            // 이메일로 가입하기 버튼
            Positioned(
              top: 335,
              left: 72,
              child: GestureDetector(
                onTap: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (context) => CreateAccountPage()),
                  );
                },
                child: Container(
                  width: 252,
                  height: 46,
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(10),
                    color: Colors.white,
                    border: Border.all(
                      color: Colors.black,
                      width: 1,
                    ),
                  ),
                  alignment: Alignment.center,
                  child: Text(
                    '이메일로 가입하기',
                    style: TextStyle(
                      color: Colors.black,
                      fontFamily: 'Noto Sans',
                      fontSize: 18,
                      fontWeight: FontWeight.normal,
                      height: 1,
                    ),
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
