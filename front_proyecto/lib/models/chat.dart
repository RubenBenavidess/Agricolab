// models/chat.dart
import 'package:front_proyecto/models/message.dart';

class Chat {
  final String id;
  final String title;
  final List<Message> messages;
  final DateTime createdAt;

  Chat({
    required this.id,
    required this.title,
    required this.messages,
    required this.createdAt,
  });

  Map<String, dynamic> toJson() => {
    'id': id,
    'title': title,
    'messages': messages.map((m) => m.toJson()).toList(),
    'createdAt': createdAt.toIso8601String(),
  };

  factory Chat.fromJson(Map<String, dynamic> json) => Chat(
    id: json['id'],
    title: json['title'],
    messages: (json['messages'] as List)
        .map((m) => Message.fromJson(m))
        .toList(),
    createdAt: DateTime.parse(json['createdAt']),
  );
}
