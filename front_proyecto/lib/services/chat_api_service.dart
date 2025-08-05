// services/chat_api_service.dart
import 'dart:convert';
import 'package:http/http.dart' as http;

class ChatApiService {
  static const String _baseUrl = 'https://dr00p3r.top/agricolab/api/rag';

  Future<String> sendMessage(String question) async {
    try {
      final response = await http.post(
        Uri.parse(_baseUrl),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'question': question}),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return data['answer'] ?? 'No se recibió respuesta';
      } else {
        throw Exception('Error en la API: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error de conexión: $e');
    }
  }
}
