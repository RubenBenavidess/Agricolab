// main.dart
import 'package:flutter/material.dart';
import 'views/chat_screen.dart';

void main() {
  runApp(const AgricoLabApp());
}

class AgricoLabApp extends StatelessWidget {
  const AgricoLabApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'AgricoLab Chatbot',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        brightness: Brightness.dark,
        scaffoldBackgroundColor: const Color(0xFF1E1E1E),
        fontFamily: 'Segoe UI',
      ),
      home: const ChatScreen(),
      debugShowCheckedModeBanner: false,
    );
  }
}
