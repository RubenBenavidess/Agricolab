// viewmodels/chat_viewmodel.dart
import 'package:flutter/material.dart';
import 'package:uuid/uuid.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/chat.dart';
import '../models/message.dart';
import '../services/chat_api_service.dart';
import '../services/storage_service.dart';

class ChatViewModel extends ChangeNotifier {
  final ChatApiService _apiService = ChatApiService();
  final StorageService _storageService = StorageService();
  final Uuid _uuid = const Uuid();

  List<Chat> _chats = [];
  Chat? _currentChat;
  bool _isLoading = false;
  String? _error;
  bool _isSidebarVisible = true;
  bool _isInitialized = false;

  List<Chat> get chats => _chats;
  Chat? get currentChat => _currentChat;
  bool get isLoading => _isLoading;
  String? get error => _error;
  bool get isSidebarVisible => _isSidebarVisible;
  bool get isInitialized => _isInitialized;

  ChatViewModel() {
    _loadChats();
    _loadSidebarState();
  }

  Future<void> _loadChats() async {
    try {
      _chats = await _storageService.loadChats();
      if (_chats.isNotEmpty) {
        _currentChat = _chats.first;
      }
      notifyListeners();
    } catch (e) {
      _error = 'Error al cargar chats: $e';
      notifyListeners();
    }
  }

  Future<void> _saveChats() async {
    try {
      await _storageService.saveChats(_chats);
    } catch (e) {
      _error = 'Error al guardar: $e';
      notifyListeners();
    }
  }

  // Función que faltaba
  Future<void> _loadSidebarState() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      _isSidebarVisible = prefs.getBool('sidebar_visible') ?? true;
      notifyListeners();
    } catch (e) {
      // Manejar error si es necesario
    }
  }

  // Función que faltaba
  Future<void> _saveSidebarState() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      await prefs.setBool('sidebar_visible', _isSidebarVisible);
    } catch (e) {
      // Manejar error si es necesario
    }
  }

  void toggleSidebar() {
    _isSidebarVisible = !_isSidebarVisible;
    _saveSidebarState();
    notifyListeners();
  }

  // Método corregido - solo ocultar automáticamente la primera vez en móvil
  void updateScreenSize(double width) {
    final bool isMobile = width < 600;

    if (!_isInitialized) {
      // Primera vez: aplicar lógica responsiva solo si no hay preferencia guardada
      if (isMobile) {
        _isSidebarVisible = false; // Ocultar por defecto en móvil
      }
      _isInitialized = true;
      notifyListeners();
    }
  }

  // Método para obtener el ancho responsivo del sidebar
  double getSidebarWidth(double screenWidth) {
    if (screenWidth < 600) {
      return screenWidth * 0.60;
    } else if (screenWidth < 900) {
      return 260; // Tamaño fijo en tablet
    } else if (screenWidth < 1200) {
      return 280; // Tamaño normal en desktop pequeño
    } else {
      return 300; // Tamaño más grande en pantallas grandes
    }
  }

  void createNewChat() {
    final newChat = Chat(
      id: _uuid.v4(),
      title: 'Nuevo Chat',
      messages: [],
      createdAt: DateTime.now(),
    );

    _chats.insert(0, newChat);
    _currentChat = newChat;
    _saveChats();
    notifyListeners();
  }

  void selectChat(String chatId) {
    _currentChat = _chats.firstWhere((chat) => chat.id == chatId);
    notifyListeners();
  }

  Future<void> sendMessage(String content) async {
    if (content.trim().isEmpty) return;

    if (_currentChat == null) {
      createNewChat();
    }

    final userMessage = Message(
      id: _uuid.v4(),
      content: content.trim(),
      isUser: true,
      timestamp: DateTime.now(),
    );

    _currentChat!.messages.add(userMessage);

    // Actualizar título del chat si es el primer mensaje
    if (_currentChat!.messages.length == 1) {
      final chatIndex = _chats.indexWhere((c) => c.id == _currentChat!.id);
      if (chatIndex != -1) {
        _chats[chatIndex] = Chat(
          id: _currentChat!.id,
          title: content.length > 30
              ? '${content.substring(0, 30)}...'
              : content,
          messages: _currentChat!.messages,
          createdAt: _currentChat!.createdAt,
        );
        _currentChat = _chats[chatIndex];
      }
    }

    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final response = await _apiService.sendMessage(content);

      final botMessage = Message(
        id: _uuid.v4(),
        content: response,
        isUser: false,
        timestamp: DateTime.now(),
      );

      _currentChat!.messages.add(botMessage);
      await _saveChats();
    } catch (e) {
      _error = 'Error al enviar mensaje: $e';

      final errorMessage = Message(
        id: _uuid.v4(),
        content: 'Lo siento, hubo un error al procesar tu mensaje.',
        isUser: false,
        timestamp: DateTime.now(),
      );

      _currentChat!.messages.add(errorMessage);
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  void deleteChat(String chatId) {
    final chatIndex = _chats.indexWhere((c) => c.id == chatId);
    if (chatIndex != -1) {
      _chats.removeAt(chatIndex);

      if (_currentChat?.id == chatId) {
        _currentChat = _chats.isNotEmpty ? _chats.first : null;
      }

      _saveChats();
      notifyListeners();
    }
  }

  void renameChat(String chatId, String newTitle) {
    final chatIndex = _chats.indexWhere((c) => c.id == chatId);
    if (chatIndex != -1) {
      _chats[chatIndex] = Chat(
        id: _chats[chatIndex].id,
        title: newTitle,
        messages: _chats[chatIndex].messages,
        createdAt: _chats[chatIndex].createdAt,
      );

      if (_currentChat?.id == chatId) {
        _currentChat = _chats[chatIndex];
      }

      _saveChats();
      notifyListeners();
    }
  }
}
