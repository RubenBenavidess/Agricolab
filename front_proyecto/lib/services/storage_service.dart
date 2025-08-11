// services/storage_service.dart
import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/chat.dart';

class StorageService {
  static const String _chatsKey = 'saved_chats';

  Future<List<Chat>> loadChats() async {
    final prefs = await SharedPreferences.getInstance();
    final chatsJson = prefs.getString(_chatsKey);

    if (chatsJson == null) return [];

    final List<dynamic> chatsList = jsonDecode(chatsJson);
    return chatsList.map((json) => Chat.fromJson(json)).toList();
  }

  Future<void> saveChats(List<Chat> chats) async {
    final prefs = await SharedPreferences.getInstance();
    final chatsJson = jsonEncode(chats.map((chat) => chat.toJson()).toList());
    await prefs.setString(_chatsKey, chatsJson);
  }
}
